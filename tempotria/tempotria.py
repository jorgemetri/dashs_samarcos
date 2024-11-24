import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

@st.cache_data
def load_data():
    tria = pd.read_excel("tempo_triagem_notas.xlsx")
    return tria


@st.cache_data
def get_data():
    # Criar colunas baseadas no alfabeto
    columns = ["Produto " + column for column in string.ascii_uppercase[:10]]  # Limitar para 10 produtos
    valores = np.random.normal(1000, 600, len(columns))
    dicionario = dict(zip(columns, valores))

    # Criar datas para o intervalo desejado
    data_vendas = pd.date_range(start=date(2023, 1, 1), end=date(2023, 12, 31), freq="D")

    # Criar DataFrame com os dados simulados
    data = pd.DataFrame(index=data_vendas)

    for column, valor in dicionario.items():
        data[column] = np.random.normal(valor, 500, len(data_vendas))

    return data


def Grafico_Rotulado_Data(data, axisx, axisy, rotuloY, titulo):
    """
    Exibe um gráfico de área interativo com hover, pontos, tooltips e rótulos.

    Parâmetros:
    - data: DataFrame com os dados a serem plotados.
    - axisx: Nome da coluna para o eixo X.
    - axisy: Nome da coluna para o eixo Y.
    - rotuloY: Título do eixo Y.
    - titulo: Título do gráfico.
    """
    hover = alt.selection_single(
        fields=[axisx],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Criar o gráfico de área
    area = (
        alt.Chart(data.reset_index(), title=alt.TitleParams(text=titulo, anchor="middle"))
        .mark_area(opacity=0.6, line={"color": "#005FB8"})  # Adiciona transparência e linha no contorno
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy, title=rotuloY),
            color=alt.value("#005FB8"),  # Define a cor da área
            tooltip=[
                alt.Tooltip(axisx, title="Data"),
                alt.Tooltip(axisy, title=rotuloY),
            ],
        )
    )

    # Pontos para o hover
    points = area.transform_filter(hover).mark_circle(size=65)

    # Rótulos nos pontos
    labels = (
        alt.Chart(data.reset_index())
        .mark_text(align='left', dx=5, dy=-5, fontSize=12,  color="black")
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy, title=rotuloY),
            text=alt.Text(axisy, format=".0f"),  # Formato dos valores exibidos
        )
    )

    # Regra de tooltips
    tooltips = (
        alt.Chart(data.reset_index())
        .mark_rule()
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy, title=rotuloY),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisx, title="Data"),
                alt.Tooltip(axisy, title=rotuloY),
            ],
        )
        .add_selection(hover)
    )

    # Combinação de camadas
    data_layer = area + points + labels + tooltips
    st.altair_chart(data_layer, use_container_width=True)




def Graficos_Tabelas(data):

    # Configurações iniciais
    #Grafico MSPN x Data-------------------------------------------------------------
    data1 = data[['Status','MSPN']]
    data1 =data1[data1['Status'] == 'MSPN']
    data1['Mes_Ano'] = data['MSPN'].dt.to_period("M")
    data1=data1.groupby("Mes_Ano")['Status'].count().reset_index()
    data1['Mes_Ano'] = data1['Mes_Ano'].dt.to_timestamp()
    data1

    data2 = data[[]]
    data3 = data[["Produto C"]]

    # Gráfico personalizado com Altair
    Grafico_Rotulado_Data(
        data=data1.reset_index(),
        axisx="index",
        axisy="Produto A",
        rotuloY="Qtd Produto A",
        titulo="Entrada de Nota Produto A",
    )

    Grafico_Rotulado_Data(
        data=data2.reset_index(),
        axisx="index",
        axisy="Produto B",
        rotuloY="Qtd Produto B",
        titulo="Entrada de Nota Produto B",
    )
    Grafico_Rotulado_Data(
        data=data3.reset_index(),
        axisx="index",
        axisy="Produto C",
        rotuloY="Qtd Produto C",
        titulo="Entrada de Nota Produto C",
    )

    st.dataframe(data,hide_index=True)

def Cartoes(data):
    mediaA = round(np.average(data[['Produto A']]), 2)
    mediaB = round(np.average(data[['Produto B']]), 2)
    mediaC = round(np.average(data[['Produto C']]), 2)

    with st.container(height=300):
        st.metric(label="Média Produto A", value=mediaA)
    with st.container(height=300):
        st.metric(label="Média Produto B", value=mediaB)
    with st.container(height=300):
        st.metric(label="Média Produto C", value=mediaC)


def Filtros(data):
    # Inicializando os filtros no st.session_state com valores padrão
    if "filtro1" not in st.session_state:
        st.session_state["filtro1"] = "Selecione uma empresa"
    if "filtro2" not in st.session_state:
        st.session_state["filtro2"] = "Selecione uma disciplina"
    if "filtro3" not in st.session_state:
        st.session_state["filtro3"] = "Selecione um CT"

    # Criando os filtros na barra lateral com valor padrão selecionado
    st.sidebar.selectbox(
        "Empresa:",
        options=["Selecione uma empresa"] + list(data['Empresa'].unique()),
        index=0,  # Define "Selecione uma empresa" como padrão
        key="filtro1",
    )
    st.sidebar.selectbox(
        "Disciplina:",
        options=["Selecione uma disciplina"] + list(data["Disciplina"].unique()),
        index=0,  # Define "Selecione uma disciplina" como padrão
        key="filtro2",
    )
    st.sidebar.selectbox(
        "Centro de Trabalho:",
        options=["Selecione um CT"] + list(data["Centro_de_Trabalho"].unique()),
        index=0,  # Define "Selecione um CT" como padrão
        key="filtro3",
    )



def Secao1(data):
    # Mantém uma cópia dos dados originais
    original_data = data.copy()

    # Selecionando colunas relevantes
    data = data[['Status', 'MSPN', 'Empresa', 'Disciplina', 'Centro_de_Trabalho']].copy()

    # Verificar se todos os filtros estão no estado padrão ou nenhum foi selecionado
    if (
        (not st.session_state["filtro1"] or st.session_state["filtro1"] == "Selecione uma empresa") and
        (not st.session_state["filtro2"] or st.session_state["filtro2"] == "Selecione uma disciplina") and
        (not st.session_state["filtro3"] or st.session_state["filtro3"] == "Selecione um CT")
    ):
        # Aplicar filtro padrão
        data = data[data["Status"] == "MSPN"]
    else:
        # Aplicar filtros específicos
        if st.session_state["filtro1"] and st.session_state["filtro1"] != "Selecione uma empresa":
            data = data[(data['Status'] == 'MSPN') & (data['Empresa'] == st.session_state["filtro1"])]
        if st.session_state["filtro2"] and st.session_state["filtro2"] != "Selecione uma disciplina":
            data = data[(data['Status'] == 'MSPN') & (data['Disciplina'] == st.session_state["filtro2"])]
        if st.session_state["filtro3"] and st.session_state["filtro3"] != "Selecione um CT":
            data = data[(data['Status'] == 'MSPN') & (data['Centro_de_Trabalho'] == st.session_state["filtro3"])]

    # Garantindo que 'MSPN' é datetime
    if not np.issubdtype(data['MSPN'].dtype, np.datetime64):
        data['MSPN'] = pd.to_datetime(data['MSPN'], errors='coerce')

    # Criando a coluna de mês/ano e agrupando
    data['Mes_Ano'] = data['MSPN'].dt.to_period("M")
    data = data.groupby("Mes_Ano")['Status'].count().reset_index()

    # Convertendo Mes_Ano para timestamp
    data['Mes_Ano'] = data['Mes_Ano'].dt.to_timestamp()

    # Configurando índice para Mes_Ano
    data.set_index('Mes_Ano', inplace=True)

    # Criando o gráfico
    with st.container(height=350):
        Grafico_Rotulado_Data(
            data=data.reset_index(),  # Reseta o índice para o gráfico
            axisx="Mes_Ano",
            axisy="Status",
            rotuloY="",
            titulo="Entrada de Notas MPSN",
        )

    
def Secao2(data):
    # Mantém uma cópia dos dados originais
    original_data = data.copy()
    # Selecionando colunas e filtrando por 'Status' == 'MSPN'
    data = data[['Status', 'MSPR']].copy()
    data = data[data['Status'] == 'MSPR']

    # Garantindo que 'MSPN' é datetime
    if not np.issubdtype(data['MSPR'].dtype, np.datetime64):
        data['MSPR'] = pd.to_datetime(data['MSPR'], errors='coerce')

    # Criando a coluna de mês/ano e agrupando
    data['Mes_Ano'] = data['MSPR'].dt.to_period("M")
    data = data.groupby("Mes_Ano")['Status'].count().reset_index()

    # Convertendo Mes_Ano para timestamp
    data['Mes_Ano'] = data['Mes_Ano'].dt.to_timestamp()

    # Configurando índice para Mes_Ano
    data.set_index('Mes_Ano', inplace=True)

    # Criando um container para as colunas
    with st.container(height=350):
        Grafico_Rotulado_Data(
                data=data.reset_index(),  # Reseta o índice para o gráfico
                axisx="Mes_Ano",
                axisy="Status",
                rotuloY="",
                titulo="Entrada de Notas MSPN x MSPR",
            )
def Secao3(data):
    # Mantém uma cópia dos dados originais
    original_data = data.copy()

    # Verificando os filtros aplicados no st.session_state
    if (
        (not st.session_state["filtro1"] or st.session_state["filtro1"] == "Selecione uma empresa") and
        (not st.session_state["filtro2"] or st.session_state["filtro2"] == "Selecione uma disciplina") and
        (not st.session_state["filtro3"] or st.session_state["filtro3"] == "Selecione um CT")
    ):
        # Nenhum filtro selecionado: utiliza os dados sem filtro
        data = data[['ORDA']].copy()
        data = data.dropna()
    else:
        # Aplicar filtros específicos
        if st.session_state["filtro1"] and st.session_state["filtro1"] != "Selecione uma empresa":
            data = data[data['Empresa'] == st.session_state["filtro1"]]
        if st.session_state["filtro2"] and st.session_state["filtro2"] != "Selecione uma disciplina":
            data = data[data['Disciplina'] == st.session_state["filtro2"]]
        if st.session_state["filtro3"] and st.session_state["filtro3"] != "Selecione um CT":
            data = data[data['Centro_de_Trabalho'] == st.session_state["filtro3"]]

        # Filtrando apenas a coluna ORDA
        data = data[['ORDA']].copy()
        data = data.dropna()

    # Garantindo que 'ORDA' é datetime
    data['ORDA'] = pd.to_datetime(data['ORDA'], errors='coerce')

    # Criando a coluna de mês/ano e agrupando
    data["Mes_Ano"] = data["ORDA"].dt.to_period("M")
    data = data.groupby("Mes_Ano")["ORDA"].count().reset_index()
    data["Mes_Ano"] = data["Mes_Ano"].dt.to_timestamp()

    # Configurando o índice para Mes_Ano
    data.set_index("Mes_Ano", inplace=True)

    # Criando o gráfico
    with st.container(height=350):
        Grafico_Rotulado_Data(
            data=data.reset_index(),  # Reseta o índice para o gráfico
            axisx="Mes_Ano",
            axisy="ORDA",
            rotuloY="Contagem de Ordens",
            titulo="Contagem de notas em Ordens",
        )
def Metricas(data):

    col1,col2,col3 = st.columns(3)
    col1.metric(label="Idade Média",value=round(np.average(data["Idade_média"]),2),delta=-10)
    col2.metric(label="Conversão MSPN x MSPR",value=round(np.nanmean(data["MSPN_X_MSPR"]),2),delta=-210)
    col3.metric(label="Conversão NT x OM",value=round(np.nanmean(data["MSPR_x_ORDA"]),2),delta=-210)

    style_metric_cards(border_left_color="#005FB8")


def Filtro_Ano(data):
    # Criando uma coluna de ano
    data['Ano'] = data['Data_de_criação'].dt.year
    lista_anos = list(data['Ano'].unique())

    # CSS para aumentar o tamanho do texto "Ano"
    st.markdown(
        """
        <style>
        label[data-testid="stSelectboxLabel"] {
            font-size: 20px; /* Altere o tamanho da fonte aqui */
            font-weight: bold; /* Deixe o texto em negrito se desejar */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Criando o selectbox
    option = st.selectbox(
        "Ano",
        lista_anos,
        index=None,
        placeholder="Selecione um ano...",
    )

    return option
def Tabela(data):
    st.dataframe(data[["Nota","Texto","Status","Idade_média","MSPN_X_MSPR","Centro_de_Trabalho"]],hide_index=True)



# Criando as abas com ícones nos nomes
tab1, tab2 = st.tabs(["📊 DashBoard: Triagem", "📥 Baixar dados"])

with tab1:
    st.title("Tempo de triagem :chart_with_upwards_trend:")
    data = get_data()
    data1 = load_data()
    col2, col3 = st.columns([3, 1])

    Filtros(data1)
    st.divider()

    Filtro_Ano(data1)
    Metricas(data1)

    Secao1(data1)
    Secao2(data1)
    Secao3(data1)
    Tabela(data1)

with tab2:
    st.write("📥 Baixar Dados")








