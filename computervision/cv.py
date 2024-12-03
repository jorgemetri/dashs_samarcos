import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import altair as alt
from streamlit_extras.metric_cards import style_metric_cards

@st.cache_data
def load_data():
    tria = pd.read_excel("./PrevisaoHH.xlsx")
    tria.columns= ["X","y_train","y_pred"]
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
    Exibe um gráfico de linha com área preenchida, interativo, com hover, pontos, tooltips e rótulos.

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

    # Criar o gráfico de linha com área preenchida
    area = (
        alt.Chart(data.reset_index(), title=alt.TitleParams(text=titulo, anchor="middle"))
        .mark_area(opacity=0.4, line={"color": "#005FB8", "width": 2})  # Linha com área preenchida
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy, title=rotuloY),
            tooltip=[
                alt.Tooltip(axisx, title="Data"),
                alt.Tooltip(axisy, title=rotuloY),
            ],
        )
    )

    # Pontos para o hover
    points = area.transform_filter(hover).mark_circle(size=75, color="#005FB8")

    # Rótulos nos pontos
    labels = (
        alt.Chart(data.reset_index())
        .mark_text(align='left', dx=5, dy=-5, fontSize=12, color="#005FB8")
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy, title=rotuloY),
            text=alt.Text(axisy, format=".0f"),
        )
        .transform_filter(hover)  # Mostra apenas o rótulo no ponto de hover
    )

    # Regra de tooltips
    tooltips = (
        alt.Chart(data.reset_index())
        .mark_rule(color="gray")
        .encode(
            x=alt.X(axisx, title=""),
            opacity=alt.condition(hover, alt.value(0.5), alt.value(0)),
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

def Grafico_Rotulado_Data_Dual(data, axisx, axisy1, axisy2, rotuloY1, rotuloY2, titulo, cor1="#005FB8", cor2="#FF0000"):
    """
    Exibe um gráfico de linha com área preenchida para dois conjuntos de dados no mesmo eixo X.
    Interativo, com hover, pontos, tooltips e rótulos.

    Parâmetros:
    - data: DataFrame com os dados a serem plotados.
    - axisx: Nome da coluna para o eixo X.
    - axisy1: Nome da primeira coluna para o eixo Y.
    - axisy2: Nome da segunda coluna para o eixo Y.
    - rotuloY1: Título do primeiro eixo Y.
    - rotuloY2: Título do segundo eixo Y.
    - titulo: Título do gráfico.
    - cor1: Cor para o primeiro gráfico (padrão azul).
    - cor2: Cor para o segundo gráfico (padrão vermelho).
    """
    hover = alt.selection_single(
        fields=[axisx],
        nearest=True,
        on="mouseover",
        empty="none",
    )

    # Gráfico para o primeiro conjunto de dados (Y1)
    area1 = (
        alt.Chart(data.reset_index(), title=alt.TitleParams(text=titulo, anchor="middle"))
        .mark_area(opacity=0.4, line={"color": cor1, "width": 2})
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy1, title=rotuloY1),
            tooltip=[
                alt.Tooltip(axisx, title="Data"),
                alt.Tooltip(axisy1, title=rotuloY1),
            ],
        )
    )

    points1 = area1.transform_filter(hover).mark_circle(size=75, color=cor1)

    labels1 = (
        alt.Chart(data.reset_index())
        .mark_text(align='left', dx=5, dy=-5, fontSize=12, color=cor1)
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy1, title=rotuloY1),
            text=alt.Text(axisy1, format=".0f"),
        )
        .transform_filter(hover)
    )

    # Gráfico para o segundo conjunto de dados (Y2)
    area2 = (
        alt.Chart(data.reset_index())
        .mark_area(opacity=0.4, line={"color": cor2, "width": 2})
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy2, title=rotuloY2),
            tooltip=[
                alt.Tooltip(axisx, title="Data"),
                alt.Tooltip(axisy2, title=rotuloY2),
            ],
        )
    )

    points2 = area2.transform_filter(hover).mark_circle(size=75, color=cor2)

    labels2 = (
        alt.Chart(data.reset_index())
        .mark_text(align='left', dx=5, dy=-5, fontSize=12, color=cor2)
        .encode(
            x=alt.X(axisx, title=""),
            y=alt.Y(axisy2, title=rotuloY2),
            text=alt.Text(axisy2, format=".0f"),
        )
        .transform_filter(hover)
    )

    # Regra de tooltips
    tooltips = (
        alt.Chart(data.reset_index())
        .mark_rule(color="gray")
        .encode(
            x=alt.X(axisx, title=""),
            opacity=alt.condition(hover, alt.value(0.5), alt.value(0)),
            tooltip=[
                alt.Tooltip(axisx, title="Data"),
                alt.Tooltip(axisy1, title=rotuloY1),
                alt.Tooltip(axisy2, title=rotuloY2),
            ],
        )
        .add_selection(hover)
    )

    # Combinação de camadas
    data_layer = area1 + points1 + labels1 + area2 + points2 + labels2 + tooltips
    st.altair_chart(data_layer, use_container_width=True)





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
    # Configuração das colunas
    col1, col2, col3 = st.columns(3)
     # metrics/mAP50-95(B),metrics/mAP50(B),metrics/precision(B)
    x = np.average(data["metrics/mAP50-95(B)"])*100
    in1 = f"{x}%"
    in2 =  np.average(data["metrics/mAP50(B)"])*100
    in3 = np.average(data["metrics/precision(B)"])*100
    col1.metric(label="metrics/mAP50-95(B", value=f"{x:.2f} %", delta=0.2)
    col2.metric(label="metrics/mAP50(B)", value=f"{in2:.2f} %", delta=0.3)
    col3.metric(label="metrics/precision(B)", value=f"{in3:.2f} %", delta=2)

    # Aplicação de estilo
    style_metric_cards(border_left_color="#005FB8",background_color="#262730",border_color="#005FB8")

   
    

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
@st.cache_data
def carregadados():
    tria = pd.read_csv("./results.csv")
    return tria

# Criando as abas com ícones nos nomes
tab1, tab2 = st.tabs(["📊 DashBoard: Computer-Vision PPCM", "📥 Baixar dados"])

with tab1:
    st.title("Computer Vision PPCM :material/camera:")
    df = load_data()
    dados= carregadados()
    Metricas(dados)
    

    df.set_index('X', inplace=True)  # Colocando a coluna X como index

    # Agrupar por mês para y_train
    df_y_train = df['y_train'].groupby(df.index.to_period('M')).sum().reset_index()
    df_y_train['X'] = df_y_train['X'].dt.to_timestamp()
    df_y_train.set_index('X', inplace=True)

    # Agrupar por mês para y_pred
    df_y_pred = df['y_pred'].groupby(df.index.to_period('M')).sum().reset_index()
    df_y_pred['X'] = df_y_pred['X'].dt.to_timestamp()
    df_y_pred.set_index('X', inplace=True)

    with st.container(height=350):
        # metrics/mAP50-95(B),metrics/mAP50(B),metrics/precision(B)
        Grafico_Rotulado_Data(
                data=dados.reset_index(),  # Reseta o índice para o gráfico
                axisx="epoch",
                axisy="metrics/precision(B)",
                rotuloY="",
                titulo="metrics/precision(B)",
            )
    with st.container(height=350):
        Grafico_Rotulado_Data(
                data=dados.reset_index(),  # Reseta o índice para o gráfico
                axisx="epoch",
                axisy="metrics/mAP50(B)",
                rotuloY="",
                titulo="metrics/mAP50(B)",
            )
        
    with st.container(height=350):
        Grafico_Rotulado_Data(
                data=dados.reset_index(),  # Reseta o índice para o gráfico
                axisx="epoch",
                axisy="metrics/mAP50-95(B)",
                rotuloY="",
                titulo="metrics/mAP50-95(B)",
            )
        

   

    video_file = open("./samarco.mp4", "rb")
    video_bytes = video_file.read()

    st.video(video_bytes)
    st.dataframe(carregadados(), use_container_width=True)


 

with tab2:
    st.write("📥 Baixar Dados")








