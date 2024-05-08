import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime


# Função para validar o e-mail
def validar_email(email):
    return email.endswith('@camara.leg.br')

# Estabelecendo Conexão com o GoogleSheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Função para ler dados da aba 'servidor'
def ler_servidor():
    df_servidor = conn.read(worksheet="servidor", usecols=list(range(18)), ttl=5)
    df_servidor = df_servidor.dropna(how="all")
    return df_servidor

# Função para ler dados da aba 'acoes'
def ler_acoes():
    df_acoes = conn.read(worksheet="acoes", usecols=list(range(2)), ttl=5)
    df_acoes = df_acoes.dropna(how="all")
    return df_acoes

# Função para ler dados da aba 'uasub'
def ler_uasub():
    df_uasub = conn.read(worksheet="uasub", usecols=list(range(2)), ttl=5)
    df_uasub = df_uasub.dropna(how="all")
    return df_uasub

# Definindo unidades administrativas
df_uasub = ler_uasub()
unidades_administrativas = df_uasub.groupby('Unidade')['Subunidade'].apply(list).to_dict()

# Função para inicializar o estado da sessão
def initialize_session_state():
    if 'input_name' not in st.session_state:
        st.session_state.input_name = ''
    if 'input_ponto' not in st.session_state:
        st.session_state.input_ponto = ''
    if 'input_email' not in st.session_state:
        st.session_state.input_email = ''
    if 'input_ua' not in st.session_state:
        st.session_state.input_ua = ''
    if 'input_sub' not in st.session_state:
        st.session_state.input_sub = ''
    if 'selected_acoes' not in st.session_state:
        st.session_state.selected_acoes = []
    if 'selected_area_tematica_01' not in st.session_state:
        st.session_state.selected_area_tematica_01 = ''
    if 'curso_01' not in st.session_state:
        st.session_state.curso_01 = ''
    if 'ha_valor_estimado_01' not in st.session_state:
        st.session_state.ha_valor_estimado_01 = 'NÃO'
    if 'valor_estimado_01' not in st.session_state:
        st.session_state.valor_estimado_01 = 0.0
    if 'selected_area_tematica_02' not in st.session_state:
        st.session_state.selected_area_tematica_02 = ''
    if 'curso_02' not in st.session_state:
        st.session_state.curso_02 = ''
    if 'ha_valor_estimado_02' not in st.session_state:
        st.session_state.ha_valor_estimado_02 = 'NÃO'
    if 'valor_estimado_02' not in st.session_state:
        st.session_state.valor_estimado_02 = 0.0
    if 'intencao_lc' not in st.session_state:
        st.session_state.intencao_lc = 'NÃO'
    if 'periodo_lc' not in st.session_state:
        st.session_state.periodo_lc = ''
    if 'curso_lc' not in st.session_state:
        st.session_state.curso_lc = ''
    if 'input_data' not in st.session_state:
        st.session_state['input_data'] = datetime.now().strftime('%d-%m-%Y, %H:%M:%S')

# Leitura inicial dos dados
initialize_session_state()

# Adicionando o logo e o Título

st.image("logo.jpeg", use_column_width=True, width=300)

# Adicionando a barra lateral (sidebar) com as opções de menu
menu_option = st.sidebar.radio('Selecione para preencher os campos de cada área', ['Identificação', 'Capacitação Interna', 'Capacitação Externa', 'Licença Capacitação', 'Verificar Preenchimento'])

# Função para adicionar títulos grandes
def add_section_title(title):
    st.markdown(f"<h2 style='text-align: left;'>{title}</h2>", unsafe_allow_html=True)

if menu_option == 'Identificação':

    add_section_title("Identificação:")
    st.markdown("""
    <style>
        .red-bold {
            color: red;
            font-weight: bold;
        }
    </style>
    <div class="red-bold">Todos os campos de identificação são obrigatórios</div>
    <div class="red-bold">isso é condição para que o botão "Enviar" na barra lateral seja ativado quando for sinalizada a verificação de preenchimento</div>
    """, unsafe_allow_html=True)
    
    input_name = st.text_input('Qual o seu nome?', value=st.session_state.input_name)
    input_ponto = st.text_input('Qual o seu Ponto?', value=st.session_state.input_ponto, max_chars=4)
    input_email = st.text_input('Qual o seu e-mail Câmara?', value=st.session_state.input_email)
    
    # Validação do e-mail
    if not validar_email(input_email):
        st.error('Utilize seu email @camara.leg.br')
        st.session_state.input_email = ''  # Reset do valor do e-mail se não for válido
    else:
        st.session_state.input_email = input_email  # Atualização do estado da sessão se o e-mail for válido
    
    input_ponto = input_ponto if input_ponto.isdigit() and len(input_ponto) == 4 else ''
    input_ua = st.selectbox('Qual a sua Unidade Administrativa?', [''] + list(unidades_administrativas.keys()), index=0 if st.session_state.input_ua == '' else [i+1 for i, ua in enumerate(unidades_administrativas.keys()) if ua == st.session_state.input_ua][0])

    if input_ua != st.session_state.input_ua:
        st.session_state.input_ua = input_ua
        subunidades = unidades_administrativas.get(input_ua, [])
        st.session_state.input_sub = subunidades[0] if subunidades else ''

    input_sub = st.selectbox('Qual a sua Subunidade?', [''] + unidades_administrativas.get(st.session_state.input_ua, []), index=0 if st.session_state.input_sub == '' else [i+1 for i, sub in enumerate(unidades_administrativas.get(st.session_state.input_ua, [])) if sub == st.session_state.input_sub][0])

    # Atualizar o estado da sessão
    st.session_state.input_name = input_name
    st.session_state.input_ponto = input_ponto
    st.session_state.input_ua = input_ua
    st.session_state.input_sub = input_sub


# Código da interface de 'Capacitação Interna'

elif menu_option == 'Capacitação Interna':

    add_section_title("Capacitação Interna")
    st.markdown("""
    <style>
        .red-bold {
            color: red;
            font-weight: bold;
        }
    </style>
    <div class="red-bold">Selecione no máximo 4 ações educacionais (excesso de marcações serão anuladas pelo sistema aleatoriamente)</div>
   
    """, unsafe_allow_html=True)

    
    # Carrega as ações educacionais da coluna desejada
    acoes_educacionais = ler_acoes()['acoes'].tolist()
    selected_acoes = []

    # Dividir a tela em duas colunas
    col1, col2 = st.columns(2)

    # Apresentar metade das ações em uma coluna e a outra metade na segunda coluna
    for i, acao in enumerate(acoes_educacionais):
        if i < len(acoes_educacionais) // 2:
            checkbox = col1.checkbox(acao, value=acao in st.session_state.selected_acoes, key=acao)
        else:
            checkbox = col2.checkbox(acao, value=acao in st.session_state.selected_acoes, key=acao)
        if checkbox:
            selected_acoes.append(acao)
    while len(selected_acoes) > 4:
        st.warning("Selecione no máximo 4 ações educacionais.")
        selected_acoes.pop()

    # Atualizar o estado da sessão
    st.session_state.selected_acoes = selected_acoes

# Função para carregar áreas temáticas da aba 'acoes'
def carregar_areas_tematicas():
    df_acoes = conn.read(worksheet="acoes", usecols=list(range(18)), ttl=5)
    areas_tematicas = list(set(df_acoes['area'].dropna().tolist()))
    return areas_tematicas

# Código da interface de 'Capacitação Externa'
if menu_option == 'Capacitação Externa':
    add_section_title("Capacitação Externa")
    
    # Carregar áreas temáticas
    areas_tematicas = carregar_areas_tematicas()
    
    selected_area_tematica_01 = st.selectbox('Área Temática 01: Escolha aqui a área temática do curso pretendido', [''] + areas_tematicas, index=0 if st.session_state.selected_area_tematica_01 == '' else areas_tematicas.index(st.session_state.selected_area_tematica_01) + 1)
    if selected_area_tematica_01 != st.session_state.selected_area_tematica_01:
        st.session_state.selected_area_tematica_01 = selected_area_tematica_01
    
    curso_01 = st.text_input('Curso 01 de Capacitação Externa: Escreva aqui o NOME do curso pretendido', value=st.session_state.curso_01, max_chars=255)
    ha_valor_estimado_01 = st.checkbox("Deseja fornecer Valor Estimado para o curso pretendido? Se SIM marque, se NÃO, deixe desmarcado")

    if ha_valor_estimado_01:
        valor_estimado_01 = st.number_input('Qual o valor estimado para o curso?', value=st.session_state.valor_estimado_01, format="%.2f", step=0.01)
        if valor_estimado_01:
            st.session_state.valor_estimado_01 = valor_estimado_01
    else:
        st.session_state.valor_estimado_01 = 0.0
    st.session_state.ha_valor_estimado_01 = "SIM" if ha_valor_estimado_01 else "NÃO"

    selected_area_tematica_02 = st.selectbox('Área Temática 02: Escolha aqui a área temática do curso pretendido', [''] + areas_tematicas, index=0 if st.session_state.selected_area_tematica_02 == '' else areas_tematicas.index(st.session_state.selected_area_tematica_02) + 1)
    if selected_area_tematica_02 != st.session_state.selected_area_tematica_02:
       st.session_state.selected_area_tematica_02 = selected_area_tematica_02
    
    curso_02 = st.text_input('Curso 02 de Capacitação Externa: Escreva aqui o NOME do curso pretendido', value=st.session_state.curso_01, max_chars=255)
    ha_valor_estimado_02 = st.checkbox("Deseja fornecer um valor estimado para o curso pretendido? Se SIM marque, se NÃO, deixe desmarcado")

    if ha_valor_estimado_02:
        valor_estimado_02 = st.number_input('Qual o valor estimado para o curso?', value=st.session_state.valor_estimado_02, format="%.2f", step=0.01)
        if valor_estimado_02:
            st.session_state.valor_estimado_02 = valor_estimado_02
    else:
        st.session_state.valor_estimado_02 = 0.0
    st.session_state.ha_valor_estimado_02 = "SIM" if ha_valor_estimado_02 else "NÃO"

    st.session_state.curso_01 = curso_01
    st.session_state.curso_02 = curso_02




elif menu_option == 'Licença Capacitação':
    add_section_title("Licença Capacitação")
    intencao_lc = st.checkbox("Intenção de Licença Capacitação: Marque para SIM ou deixe desmarcado para NÃO")
    periodo_lc = st.selectbox("Período da Intenção: Escolha o trimeste previsto", options=["", "1º trimestre", "2º trimestre", "3º trimeste", "4º trimestre"], index=["", "1º trimestre", "2º trimestre", "3º trimeste", "4º trimestre"].index(st.session_state.periodo_lc), disabled=not intencao_lc)
    curso_lc = st.text_input("QUal o nome do curso que pretende cursar em sua Licença Capacitação?", value=st.session_state.curso_lc, max_chars=255, disabled=not intencao_lc)

    # Atualizar o estado da sessão
    st.session_state.intencao_lc = "SIM" if intencao_lc else "NÃO"
    st.session_state.periodo_lc = periodo_lc
    st.session_state.curso_lc = curso_lc

    # Inicializar selected_acoes
if "selected_acoes" not in st.session_state:
    st.session_state.selected_acoes = []

# Verificar se os campos de identificação estão preenchidos e se o checkbox está marcado
# Verificar se os campos de identificação estão preenchidos
identificacao_preenchida = (
    st.session_state.input_name != ''
    and st.session_state.input_ponto != ''
    and st.session_state.input_email != ''
    and st.session_state.input_ua != ''
    and st.session_state.input_sub != ''
    and "checkbox_confirmado" in st.session_state
    and st.session_state.checkbox_confirmado
    and len(st.session_state.selected_acoes) <= 4
)

# Inicializar o checkbox "Dados Confirmados?"
if "checkbox_confirmado" not in st.session_state:
    st.session_state.checkbox_confirmado = False

if menu_option == 'Verificar Preenchimento':

    # Criar uma nova página em branco para exibir os dados preenchidos

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Dados Preenchidos</h2>", unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    
    # Dados de Identificação
    add_section_title("Identificação")
    st.write(f'Nome: {st.session_state.input_name}')
    st.write(f'Ponto: P_{st.session_state.input_ponto}')
    st.write(f'Email: {st.session_state.input_email}')
    st.write(f'Unidade Administrativa: {st.session_state.input_ua}')
    st.write(f'Subunidade: {st.session_state.input_sub}')
    
    # Dados de Capacitação Interna
    add_section_title("Capacitação Interna")
    st.write('Ações Educacionais selecionadas:')
    for acao in st.session_state.selected_acoes:
        st.write(f'- {acao}')
    
    # Dados de Capacitação Externa
    add_section_title("Capacitação Externa")
    st.write(f'Área temática 01: {st.session_state.selected_area_tematica_01}')
    st.write(f'Curso 01 de Capacitação Externa: {st.session_state.curso_01}')
    st.write(f'Há valor estimado 01: {st.session_state.ha_valor_estimado_01}')
    st.write(f'Valor Estimado Curso 01: {st.session_state.valor_estimado_01}')
    st.write(f'Área temática 02: {st.session_state.selected_area_tematica_02}')
    st.write(f'Curso 02 de Capacitação Externa: {st.session_state.curso_02}')
    st.write(f'Há valor estimado 02: {st.session_state.ha_valor_estimado_02}')
    st.write(f'Valor Estimado Curso 02: {st.session_state.valor_estimado_02}')
    
    # Dados de Licença Capacitação
    add_section_title("Licença Capacitação")
    st.write(f'Intenção de Licença Capacitação: {st.session_state.intencao_lc}')
    st.write(f'Período da Intenção: {st.session_state.periodo_lc}')
    st.write(f'Nome do Curso para Licença Capacitação: {st.session_state.curso_lc}')


    add_section_title("Confirmação de Dados")
# Criar o checkbox "Dados Confirmados?"
    st.checkbox("Dados Confirmados? Marque se SIM", key="checkbox_confirmado")


# Habilitar o botão de confirmação apenas se todos os campos estiverem preenchidos e houver no máximo 4 ações selecionadas

confirm_button = st.sidebar.button("Enviar", disabled=not identificacao_preenchida, key="confirmar_envio")

st.sidebar.markdown("""
    <style>
        .red-bold {
            color: red !important;
            font-weight: bold !important;
        }
    </style>

    <p class="red-bold">O Botão será ativado se os campos de identificação estiverem preenchidos corretamente, 
    houver no máximo 4 ações educacionais selecionadas para Capacitação Interna e o 
    Checkbox de verificação do preenchimento estiver marcado.</p>
    """, unsafe_allow_html=True
)


# Fetch existing servidor data
df_dados = conn.read(worksheet="servidor", usecols=list(range(18)), ttl=5)

df_dados = df_dados.dropna(how="all")

if confirm_button:

    df = pd.DataFrame({
        'Nome': [st.session_state.input_name],
        'Ponto': [st.session_state.input_ponto],
        'Email': [st.session_state.input_email],
        'Unidade': [st.session_state.input_ua],
        'Subunidade': [st.session_state.input_sub],
        'capinterna': ['|'.join(st.session_state.selected_acoes)],
        'cexterareatema01': [st.session_state.selected_area_tematica_01],
        'cextercurso01': [st.session_state.curso_01],
        'haestimado01': [st.session_state.ha_valor_estimado_01],
        'estimado01': [st.session_state.valor_estimado_01],
        'cexterareatema02': [st.session_state.selected_area_tematica_02],
        'cextercurso02': [st.session_state.curso_02],
        'haestimado02': [st.session_state.ha_valor_estimado_02],
        'estimado02': [st.session_state.valor_estimado_02],
        'intencaoLC': [st.session_state.intencao_lc],
        'periodo': [st.session_state.periodo_lc],
        'cursoLC': [st.session_state.curso_lc],
        'Data': [st.session_state.input_data]
    })

    # Adicionar novos dados à tabela dados do Sheets
    df_dados = pd.concat([df_dados, df], ignore_index=True)
    
    # Atualizar os dados no Google Sheets
    conn.update(worksheet="servidor", data=df_dados)
    

    st.success("Dados enviados com sucesso!")
