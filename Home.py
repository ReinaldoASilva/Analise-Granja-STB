import streamlit as st
from pathlib import Path
import pandas as pd
from PIL import Image
st.markdown("<h2 style='text-align: center;'>Avaliando a Performance em Ambientes Controlados!</h2>", unsafe_allow_html=True)
    
st.markdown("Este projeto de análise de dados tem como objetivo investigar como as condições ambientais afetam o desempenho das aves. \
Analisaremos os momentos em que a temperatura e umidade atingem niveis extremos, buscando compreender como esses fatores influenciam na conversão alimentar..\
A ideia é buscar melhorias nas práticas de manejo e identificar os intervalos perfeitos de temperatura e umidade, com o objetivo de maximizar os lucros nas granjas analisadas.")


current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
data = current_dir /'producao-avicola.jpg'

profile_pic = Image.open(data)
st.image(profile_pic, caption='Produção Avícola')