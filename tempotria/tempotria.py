import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import altair as alt

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
    Exibe um gráfico de área interativo com hover, pontos, e tooltips.

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
    #262739
    # Pontos para o hover
    points = area.transform_filter(hover).mark_circle(size=65)

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
    data_layer = area + points + tooltips
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
    st.sidebar.selectbox("Escolha o tipo de Produto:",data.columns,index =None,placeholder="Selecione um produto",key='side1')
    st.sidebar.selectbox("Escolha o tipo de Produto:",data.columns,index =None,placeholder="Selecione um produto",key='side2')
    st.sidebar.selectbox("Escolha o tipo de Produto:",data.columns,index =None,placeholder="Selecione um produto",key='side3')

st.header("Tempo de triagem")
data = get_data()
data1= load_data()
col2,col3 = st.columns([3,1])

Filtros(data)
# Selecionando colunas e filtrando os dados

def Secao1(data):
    # Mantém uma cópia dos dados originais
    original_data = data.copy()

    # Selecionando colunas e filtrando por 'Status' == 'MSPN'
    data = data[['Status', 'MSPN']].copy()
    data = data[data['Status'] == 'MSPN']

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

    # Criando um container para as colunas
    with st.container(height=350):
        col1, col2 = st.columns([3, 1])

        # Plotando o gráfico na primeira coluna
        with col1:
            Grafico_Rotulado_Data(
                data=data.reset_index(),  # Reseta o índice para o gráfico
                axisx="Mes_Ano",
                axisy="Status",
                rotuloY="",
                titulo="Entrada de Notas MPSN",
            )

        # Calculando e exibindo a métrica na segunda coluna
        with col2:
            if 'Idade_média' in original_data.columns:
                mediaA = np.average(original_data['Idade_média'])
                st.metric(label="Idade Média", value=round(mediaA, 2))
            else:
                st.warning("Coluna 'Idade média' não encontrada nos dados.")
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
    with st.container(height=310):
        col1, col2 = st.columns([3, 1])

        # Plotando o gráfico na primeira coluna
        with col1:
            Grafico_Rotulado_Data(
                data=data.reset_index(),  # Reseta o índice para o gráfico
                axisx="Mes_Ano",
                axisy="Status",
                rotuloY="",
                titulo="Entrada de Notas MSPN x MSPR",
            )

        # Calculando e exibindo a métrica na segunda coluna
        with col2:
            st.metric(label="Conversão MPSPN x MSPR",value=round(np.nanmean(original_data['MSPN_X_MSPR']),2))


Secao1(data1)
Secao2(data1)






