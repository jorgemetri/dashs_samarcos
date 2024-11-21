import streamlit as st
import pandas as pd
import numpy as np
from datetime import date, timedelta
import string
import time



#Definindo as pages

backlog = st.Page("backlog_ordens/backlog.py",title="BackLog de Ordens",icon=":material/dashboard:") 
tempotria = st.Page("tempotria/tempotria.py",title="Tempo de Triagem",icon=":material/dashboard:")
ci =  st.Page("ci/ci.py",title="Condições Inseguras",icon=":material/dashboard:")
jump =  st.Page("jump/jump.py",title="Jump",icon=":material/dashboard:")
zpm2 =  st.Page("zpm2/zpm2.py",title="ZPM2",icon=":material/dashboard:")



pg = st.navigation(
    {
        "DashBoards Analíticos":[tempotria,ci,jump,zpm2],
        "DashBoards Preditivos":[backlog]
    }
)
pg.run()