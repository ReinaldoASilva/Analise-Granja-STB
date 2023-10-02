import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd

# modo responsivo
st.set_page_config(layout="wide")


# Carrega o logotipo
logo_path = "/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/logo.png"  # Substitua pelo caminho correto do seu logotipo
logo = Image.open(logo_path)

# Define a largura fixa do logotipo
logo_width = 300

# Cria uma coluna para exibir o logotipo acima do menu
col_logo, col_menu = st.sidebar.columns([logo_width, 1])

# Exibe o logotipo na coluna do logotipo
with col_logo:
    st.image(logo, width=logo_width)

# Título
st.markdown("<h2 style='text-align: center;'>Avaliando a Performance em Ambientes Controlados!</h2>", unsafe_allow_html=True)
# Texto
st.markdown("Este projeto de análise de dados tem como objetivo investigar como as condições ambientais afetam o desempenho das aves. \
Analisaremos os momentos em que a temperatura e umidade atingem niveis extremos, buscando compreender como esses fatores influenciam na conversão alimentar..\
A ideia é buscar melhorias nas práticas de manejo e identificar os intervalos perfeitos de temperatura e umidade, com o objetivo de maximizar os lucros nas granjas analisadas.")


# Visualizando a imagem
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
data = current_dir / 'producao-avicola.jpg'
image = Image.open(data)
st.image(image)
