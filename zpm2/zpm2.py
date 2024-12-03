import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards 


st.header("ZPM2")
@st.cache_data
def load_data():
    dados = pd.read_excel("./Ordens_zpm2zpm3.xlsx")
    return dados

def Grafico_Rotulado_Barras(data, axisx, axisy, rotuloX, titulo):
    """
    Exibe um gráfico de barras horizontais interativo com hover, tooltips e rótulos.

    Parâmetros:
    - data: DataFrame com os dados a serem plotados.
    - axisx: Nome da coluna para o eixo X.
    - axisy: Nome da coluna para o eixo Y.
    - rotuloX: Título do eixo X.
    - titulo: Título do gráfico.
    """
    hover = alt.selection_single(
        fields=[axisy],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Criar o gráfico de barras horizontais
    bars = (
        alt.Chart(data.reset_index(), title=alt.TitleParams(text=titulo, anchor="middle"))
        .mark_bar(opacity=0.8, color="#005FB8")
        .encode(
            x=alt.X(axisx, title=rotuloX),
            y=alt.Y(axisy, title="", sort="-x"),
            tooltip=[
                alt.Tooltip(axisy, title="Categoria"),
                alt.Tooltip(axisx, title=rotuloX),
            ],
        )
    )

    # Rótulos nas barras
    labels = (
        alt.Chart(data.reset_index())
        .mark_text(align='left', dx=5, fontSize=12, color="#FFFFFF")
        .encode(
            x=alt.X(axisx, title=rotuloX),
            y=alt.Y(axisy, title="", sort="-x"),
            text=alt.Text(axisx, format=".2f"),  # Formato dos valores exibidos
        )
    )

    # Regra de tooltips
    tooltips = (
        alt.Chart(data.reset_index())
        .mark_rule(color="gray")
        .encode(
            x=alt.X(axisx, title=rotuloX),
            y=alt.Y(axisy, title="", sort="-x"),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisy, title="Categoria"),
                alt.Tooltip(axisx, title=rotuloX),
            ],
        )
        .add_selection(hover)
    )

    # Combinação de camadas
    data_layer = bars + labels + tooltips
    st.altair_chart(data_layer, use_container_width=True)
def Grafico_Rotulado_Barras_Veticais(data, axisx, axisy, rotuloY, titulo):
    """
    Exibe um gráfico de barras verticais interativo com hover, tooltips e rótulos.

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

    # Criar o gráfico de barras verticais
    bars = (
        alt.Chart(data.reset_index(), title=alt.TitleParams(text=titulo, anchor="middle"))
        .mark_bar(opacity=0.8, color="#005FB8")
        .encode(
            x=alt.X(axisx, title="", sort="-y"),
            y=alt.Y(axisy, title=rotuloY),
            tooltip=[
                alt.Tooltip(axisx, title="Tipo"),
                alt.Tooltip(axisy, title=rotuloY),
            ],
        )
    )

    # Rótulos nas barras
    labels = (
        alt.Chart(data.reset_index())
        .mark_text(dy=-5, fontSize=12, color="#FFFFFF")  # Ajusta a posição vertical do texto
        .encode(
            x=alt.X(axisx, title="", sort="-y"),
            y=alt.Y(axisy, title=rotuloY),
            text=alt.Text(axisy, format=".2f"),  # Formato dos valores exibidos
        )
    )

    # Regra de tooltips
    tooltips = (
        alt.Chart(data.reset_index())
        .mark_rule(color="gray")
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy, title=rotuloY),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisx, title="Tipo"),
                alt.Tooltip(axisy, title=rotuloY),
            ],
        )
        .add_selection(hover)
    )

    # Combinação de camadas
    data_layer = bars + labels + tooltips
    st.altair_chart(data_layer, use_container_width=True)

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
        .mark_text(align='left', dx=5, dy=-5, fontSize=12,  color="#FFFFFF")
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
def Metricas(data):
    # Configuração das colunas
    col1, col2 = st.columns(2)

    col1.metric(
        label="%ZPM2", 
        value=f'{round(len(data[data["Tipo"] == "ZPM2"]) / len(data) * 100, 2)} %', 
        delta=-10
    )
    col2.metric(
        label="%ZPM3",  
        value=f'{round(len(data[data["Tipo"] == "ZPM3"]) / len(data) * 100, 2)} %', 
        delta=-210
    )

    # Aplicação de estilo
    style_metric_cards(border_left_color="#005FB8", background_color="#262730", border_color="#005FB8")
def Grafico_Rotulado_Barras_Horizontal(data, axisx, axisy, rotuloY, titulo):
    """
    Exibe um gráfico de barras horizontal interativo com hover, rótulos e tooltips.

    Parâmetros:
    - data: DataFrame com os dados a serem plotados.
    - axisx: Nome da coluna para o eixo X.
    - axisy: Nome da coluna para o eixo Y.
    - rotuloY: Título do eixo Y.
    - titulo: Título do gráfico.
    """
    hover = alt.selection_single(
        fields=[axisy],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Criar o gráfico de barras
    bars = (
        alt.Chart(data.reset_index(), title=alt.TitleParams(text=titulo, anchor="middle"))
        .mark_bar(opacity=0.8, color="#005FB8")  # Adiciona cor e opacidade às barras
        .encode(
            y=alt.Y(axisy, title=rotuloY, sort="-x"),  # Ordena por valores do eixo X
            x=alt.X(axisx, title=""),
            tooltip=[
                alt.Tooltip(axisy, title=rotuloY),
                alt.Tooltip(axisx, title="Contagem"),
            ],
        )
    )

    # Rótulos nas barras
    labels = (
        alt.Chart(data.reset_index())
        .mark_text(align='left', dx=5, dy=0, fontSize=12, color="#FFFFFF")
        .encode(
            y=alt.Y(axisy, title=rotuloY, sort="-x"),
            x=alt.X(axisx, title=""),
            text=alt.Text(axisx, format=".0f"),  # Formato dos valores exibidos
        )
    )

    # Regra de tooltips
    tooltips = (
        alt.Chart(data.reset_index())
        .mark_rule()
        .encode(
            y=alt.Y(axisy, title=rotuloY, sort="-x"),
            x=alt.X(axisx, title=""),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisy, title=rotuloY),
                alt.Tooltip(axisx, title="Contagem"),
            ],
        )
        .add_selection(hover)
    )

    # Combinação de camadas
    data_layer = bars + labels + tooltips
    st.altair_chart(data_layer, use_container_width=True)

def Secao1(data):
    # Mantém uma cópia dos dados originais
    original_data = data.copy()

    # Selecionando colunas relevantes
    data = original_data[['Ordem', 'Tipo', 'Data_de_Criacao', 'CT',"Disciplina"]].copy()

    # Verificar se todos os filtros estão no estado padrão ou nenhum foi selecionado
    if (
        (not st.session_state["filtro1"] or st.session_state["filtro1"] == "Selecione um tipo") and
        (not st.session_state["filtro2"] or st.session_state["filtro2"] == "Selecione uma disciplina") and
        (not st.session_state["filtro3"] or st.session_state["filtro3"] == "Selecione um CT")
    ):
        # Aplicar filtro padrão
        pass
    else:
        # Aplicar filtros específicos
        if st.session_state["filtro1"] and st.session_state["filtro1"] != "Selecione um tipo":
            data = data[data['Tipo'] == st.session_state["filtro1"]]
        if st.session_state["filtro2"] and st.session_state["filtro2"] != "Selecione uma disciplina":
            data = data[data['Disciplina'] == st.session_state["filtro2"]]
        if st.session_state["filtro3"] and st.session_state["filtro3"] != "Selecione um CT":
            data = data[data['CT'] == st.session_state["filtro3"]]

    # Garantindo que 'MSPN' é datetime
    if not np.issubdtype(data['Data_de_Criacao'].dtype, np.datetime64):
        data['Data_de_Criacao'] = pd.to_datetime(data['Data_de_Criacao'], errors='coerce')

    # Criando a coluna de mês/ano e agrupando
   
    data['Mes_Ano'] = data['Data_de_Criacao'].dt.to_period("M")
    data = data.groupby("Mes_Ano")['Ordem'].count().reset_index()
   
    # Convertendo Mes_Ano para timestamp
    data['Mes_Ano'] = data['Mes_Ano'].dt.to_timestamp()

    # Configurando índice para Mes_Ano
    data.set_index('Mes_Ano', inplace=True)

    # Criando o gráfico
    with st.container(height=350):
        Grafico_Rotulado_Data(
            data=data.reset_index(),  # Reseta o índice para o gráfico
            axisx="Mes_Ano",
            axisy="Ordem",
            rotuloY="",
            titulo="Contagem de orndes ZPM2/ZPM3",
        )
def Secao2(data):
    # Mantém uma cópia dos dados originais
    original_data = data.copy()

    # Selecionando colunas relevantes
    data = original_data[['Ordem', 'Tipo', 'Data_de_Criacao', 'CT',"Disciplina"]].copy()

    # Verificar se todos os filtros estão no estado padrão ou nenhum foi selecionado
    if (
        (not st.session_state["filtro1"] or st.session_state["filtro1"] == "Selecione um tipo") and
        (not st.session_state["filtro2"] or st.session_state["filtro2"] == "Selecione uma disciplina") and
        (not st.session_state["filtro3"] or st.session_state["filtro3"] == "Selecione um CT")
    ):
        # Aplicar filtro padrão
        pass
    else:
        # Aplicar filtros específicos
        if st.session_state["filtro1"] and st.session_state["filtro1"] != "Selecione um tipo":
            data = data[data['Tipo'] == st.session_state["filtro1"]]
        if st.session_state["filtro2"] and st.session_state["filtro2"] != "Selecione uma disciplina":
            data = data[data['Disciplina'] == st.session_state["filtro2"]]
        if st.session_state["filtro3"] and st.session_state["filtro3"] != "Selecione um CT":
            data = data[data['CT'] == st.session_state["filtro3"]]

    # Criando a coluna de CT e agrupando os dados por contagem de 'Ordem'
    data = data.groupby("CT")['Ordem'].count().reset_index()

    # Criar o gráfico de barras horizontais
    with st.container():
        Grafico_Rotulado_Barras_Horizontal(
            data=data,  # Passa o DataFrame agrupado
            axisx="Ordem",  # O eixo X agora contém a contagem
            axisy="CT",     # O eixo Y contém os valores categóricos de 'CT'
            rotuloY="CT",   # Título do eixo Y
            titulo="Contagem de ordens ZPM2/ZPM3 por CT",  # Título do gráfico
        )
def Secao3(data):
     # Mantém uma cópia dos dados originais
    original_data = data.copy()

    # Selecionando colunas relevantes
    data = original_data[['Ordem', 'Tipo', 'Data_de_Criacao', 'CT',"Disciplina"]].copy()

    # Verificar se todos os filtros estão no estado padrão ou nenhum foi selecionado
    if (
        (not st.session_state["filtro1"] or st.session_state["filtro1"] == "Selecione um tipo") and
        (not st.session_state["filtro2"] or st.session_state["filtro2"] == "Selecione uma disciplina") and
        (not st.session_state["filtro3"] or st.session_state["filtro3"] == "Selecione um CT")
    ):
        # Aplicar filtro padrão
        pass
    else:
        # Aplicar filtros específicos
        if st.session_state["filtro1"] and st.session_state["filtro1"] != "Selecione um tipo":
            data = data[data['Tipo'] == st.session_state["filtro1"]]
        if st.session_state["filtro2"] and st.session_state["filtro2"] != "Selecione uma disciplina":
            data = data[data['Disciplina'] == st.session_state["filtro2"]]
        if st.session_state["filtro3"] and st.session_state["filtro3"] != "Selecione um CT":
            data = data[data['CT'] == st.session_state["filtro3"]]

    

    # Criando a coluna de mês/ano e agrupando
    # Criando a coluna de mês/ano e agrupando
    data = data.groupby("Tipo")['Ordem'].count().reset_index()  # Agrupamento e contagem
    data["Ordem"] = pd.to_numeric(data["Ordem"], errors="coerce").fillna(0)  # Substituir NaN por 0
    data["Ordem"] = (data["Ordem"] / data["Ordem"].sum()) * 100  # Calcular porcentagem
    data["Ordem"] = data["Ordem"].round(2)  # Arredondar valores

    # Exibir o DataFrame
    with st.container():
        Grafico_Rotulado_Barras_Veticais(
            data=data,  # DataFrame preparado
            axisx="Tipo",  # Categorias no eixo X
            axisy="Ordem",  # Valores no eixo Y
            rotuloY="Porcentagem (%)",
            titulo="Contagem de ordens ZPM2/ZPM3 por CT",
        )
    
def Filtros(data):
    # Inicializando os filtros no st.session_state com valores padrão
    if "filtro1" not in st.session_state:
        st.session_state["filtro1"] = "Selecione um tipo"
    if "filtro2" not in st.session_state:
        st.session_state["filtro2"] = "Selecione uma disciplina"
    if "filtro3" not in st.session_state:
        st.session_state["filtro3"] = "Selecione um CT"

    # Criando os filtros na barra lateral com valor padrão selecionado
    st.sidebar.selectbox(
        "Tipo:",
        options=["Selecione um tipo"] + list(data['Tipo'].unique()),
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
        "CT:",
        options=["Selecione um CT"] + list(data["CT"].unique()),
        index=0,  # Define "Selecione uma disciplina" como padrão
        key="filtro3",
    )
  

def Filtro_Ano(data):
    # Criando uma coluna de ano
    data['Ano'] = data['Data_de_Criacao'].dt.year
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


data=load_data()


tab1, tab2 = st.tabs(["📊 DashBoard: Ordens ZPM2/ZPM3", "📥 Baixar dados"])

with tab1:
    st.title("Ordens ZPM2/ZPM3 :chart_with_upwards_trend:")
    Filtros(data)
    st.divider()
    Filtro_Ano(data)
    Metricas(data)
    Secao1(data)
    Secao2(data)
    Secao3(data)
    #st.write(data.columns)
    st.dataframe(data[["Ordem","Tipo","Texto_da_Ordem","Empresa","CT","Data_de_Encerramento","Disciplina"]],hide_index=True,use_container_width=True)
    #Tabela(data1)



with tab2:
    st.write("📥 Baixar Dados")

