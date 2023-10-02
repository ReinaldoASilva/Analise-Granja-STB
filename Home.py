import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd

# modo responsivo
st.set_page_config(layout="wide")

# Carrega o logotipo
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
logo_path = current_dir / 'logo.png'

logo = Image.open(logo_path)

# Define a largura fixa do logotipo
logo_width = 300

# Cria uma coluna para exibir o logotipo acima do menu
col_logo, col_menu = st.sidebar.columns([logo_width, 1])

# Exibe o logotipo na coluna do logotipo

with col_logo:
    st.image(logo, width=logo_width)

# Remover o menu do streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Título
st.markdown("<h2 style='text-align: center;'>Avaliando a Performance em Ambientes Controlados!</h2>", unsafe_allow_html=True)
# Texto
st.markdown("Este projeto de análise de dados tem como objetivo investigar como as condições ambientais afetam o desempenho das aves. \
Analisaremos os momentos em que a temperatura e umidade atingem niveis extremos, buscando compreender como esses fatores influenciam na conversão alimentar..\
A ideia é buscar melhorias nas práticas de manejo e identificar os intervalos perfeitos de temperatura e umidade, com o objetivo de maximizar os lucros nas granjas analisadas.")

# Imagem
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
data = current_dir / 'producao-avicola.jpg'
image = Image.open(data)

container = st.container()
container.markdown(
    f"""
    <style>
    .center {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

container.image(image, use_column_width=True, caption='')
