import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import time
#Definindo função para pegar dados

#Definindo as pages

st.set_page_config(layout="wide")
backlog = st.Page("backlog_ordens/backlog.py",title="BackLog de Ordens",icon=":material/dashboard:") 
tempotria = st.Page("tempotria/tempotria.py",title="Tempo de Triagem",icon=":material/dashboard:")
ci =  st.Page("ci/ci.py",title="Condições Inseguras",icon=":material/dashboard:")
jump =  st.Page("jump/jump.py",title="Jump",icon=":material/dashboard:")
zpm2 =  st.Page("zpm2/zpm2.py",title="ZPM2",icon=":material/dashboard:")
cv = st.Page("computervision/cv.py",title="Computer-Vision-PPCM",icon=":material/camera:")

def Logo(url):
    st.logo(
        url,
        link="https://streamlit.io/gallery",size="large"
    )

LOGO_URL_LARGE="images/samarco.png"
Logo(LOGO_URL_LARGE)


pg = st.navigation(
    {
        "DashBoards Analíticos":[tempotria,zpm2,jump],
        "DashBoards Preditivos":[backlog],
        "Computer-Vision":[cv]
    }
)
pg.run()