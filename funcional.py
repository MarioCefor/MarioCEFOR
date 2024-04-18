import streamlit as st
import pandas as pd
from datetime import datetime



# Função para validar o e-mail
def validar_email(email):
    return email.endswith('@camara.leg.br')

# Função para ler o arquivo Excel 'uasub.xlsx'
def ler_uasub():
    df = pd.read_excel('uasub.xlsx', header=0)
    return df

# Função para ler o arquivo Excel 'acoes.xlsx'
def ler_acoes():
    df = pd.read_excel('acoes.xlsx', header=None)
    return df

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

# Adicionando a barra lateral (sidebar) com as opções de menu
menu_option = st.sidebar.selectbox('Menu', ['Identificação', 'Capacitação Interna', 'Capacitação Externa', 'Licença Capacitação'])

# Definindo unidades administrativas
df_uasub = ler_uasub()
unidades_administrativas = df_uasub.groupby('Unidade')['Subunidade'].apply(list).to_dict()

# Função para adicionar títulos grandes
def add_section_title(title):
    st.markdown(f"<h2 style='text-align: left;'>{title}</h2>", unsafe_allow_html=True)

if menu_option == 'Identificação':

    add_section_title("Identificação")
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


elif menu_option == 'Capacitação Interna':

    add_section_title("Capacitação Interna")
    acoes_educacionais = ler_acoes()[1].tolist()  # Carrega as ações educacionais da segunda coluna
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

elif menu_option == 'Capacitação Externa':
    add_section_title("Capacitação Externa")
    
    areas_tematicas = list(set(ler_acoes()[0].tolist()))
    select_acoes = []

    selected_area_tematica_01 = st.selectbox('Área Temática 01:', [''] + areas_tematicas, index=0 if st.session_state.selected_area_tematica_01 == '' else areas_tematicas.index(st.session_state.selected_area_tematica_01) + 1)
    if selected_area_tematica_01 != st.session_state.selected_area_tematica_01:
        st.session_state.selected_area_tematica_01 = selected_area_tematica_01
    
    curso_01 = st.text_input('Curso 01 de Capacitação Externa:', value=st.session_state.curso_01, max_chars=255)
    ha_valor_estimado_01 = st.checkbox("Deseja fornecer Valor Estimado para o Curso 01?")

    if ha_valor_estimado_01:
        valor_estimado_01 = st.number_input('Valor Estimado Curso 01:', value=st.session_state.valor_estimado_01, format="%.2f", step=0.01)
        if valor_estimado_01:
            st.session_state.valor_estimado_01 = valor_estimado_01
    else:
        st.session_state.valor_estimado_01 = 0.0
    st.session_state.ha_valor_estimado_01 = "SIM" if ha_valor_estimado_01 else "NÃO"

    selected_area_tematica_02 = st.selectbox('Área Temática 02:', [''] + areas_tematicas, index=0 if st.session_state.selected_area_tematica_02 == '' else areas_tematicas.index(st.session_state.selected_area_tematica_02) + 1)
    if selected_area_tematica_02 != st.session_state.selected_area_tematica_02:
       st.session_state.selected_area_tematica_02 = selected_area_tematica_02
    
    curso_02 = st.text_input('Curso 02 de Capacitação Externa:', value=st.session_state.curso_02, max_chars=255)
    ha_valor_estimado_02 = st.checkbox("Deseja fornecer Valor Estimado para o Curso 02?")

    if ha_valor_estimado_02:
        valor_estimado_02 = st.number_input('Valor Estimado Curso 02:', value=st.session_state.valor_estimado_02, format="%.2f", step=0.01)
        if valor_estimado_02:
            st.session_state.valor_estimado_02 = valor_estimado_02
    else:
        st.session_state.valor_estimado_02 = 0.0
    st.session_state.ha_valor_estimado_02 = "SIM" if ha_valor_estimado_02 else "NÃO"

    st.session_state.curso_01 = curso_01
    st.session_state.curso_02 = curso_02




elif menu_option == 'Licença Capacitação':
    add_section_title("Licença Capacitação")
    intencao_lc = st.checkbox("Intenção de Licença Capacitação:")
    periodo_lc = st.selectbox("Período da Intenção:", options=["", "1º trimestre", "2º trimestre", "3º trimeste", "4º trimestre"], index=["", "1º trimestre", "2º trimestre", "3º trimeste", "4º trimestre"].index(st.session_state.periodo_lc), disabled=not intencao_lc)
    curso_lc = st.text_input("Nome do Curso para Licença Capacitação:", value=st.session_state.curso_lc, max_chars=255, disabled=not intencao_lc)

    # Atualizar o estado da sessão
    st.session_state.intencao_lc = "SIM" if intencao_lc else "NÃO"
    st.session_state.periodo_lc = periodo_lc
    st.session_state.curso_lc = curso_lc



# Adicionando espaçamento na barra lateral para posicionar os botões na parte inferior
st.sidebar.markdown('<br>', unsafe_allow_html=True)

# Adicionando botões na barra lateral
submit_button = st.sidebar.button("Verificar Preenchimento")

# Verificar se os campos de identificação estão preenchidos
identificacao_preenchida = (
    st.session_state.input_name != ''
    and st.session_state.input_ponto != ''
    and st.session_state.input_email != ''
    and st.session_state.input_ua != ''
    and st.session_state.input_sub != ''
)

# Habilitar o botão de confirmação apenas se os campos de identificação estiverem preenchidos
confirm_button = st.sidebar.button("Confirmar Envio", disabled=not identificacao_preenchida)

if confirm_button:
    # Criar DataFrame com os dados do formulário
    data = {
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
    }
    df = pd.DataFrame(data)

    # Ler os dados existentes do arquivo 'dados.xlsx' (se existirem)
    try:
        df_dados = pd.read_excel('dados.xlsx')
    except FileNotFoundError:
        df_dados = pd.DataFrame()

    # Adicionar os novos dados ao DataFrame existente usando concat
    df_dados = pd.concat([df_dados, df], ignore_index=True)

    # Salvar o DataFrame atualizado no arquivo 'dados.xlsx'
    df_dados.to_excel('dados.xlsx', index=False)
    st.success("Dados confirmados e inseridos na planilha!")



if submit_button:
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
