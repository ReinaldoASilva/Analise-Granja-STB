import streamlit as st
from pathlib import Path
from PIL import Image


# Carrega a logo
logo_path = "/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/logo.png"  # Substitua pelo caminho correto da sua logo
logo = Image.open(logo_path)

# Exibe a logo acima da página inicial
st.image(logo, use_column_width=True)

# Conteúdo da página inicial
with st.beta_container():
    st.title("Página Inicial")
    st.write("Bem-vindo à página inicial!")

# Conteúdo da página principal (Home)
st.title("Home")
st.write("Bem-vindo à página principal!")
# Conteúdo da página inicial
with st.beta_container():
    st.title("Página Inicial")
    st.write("Bem-vindo à página inicial!")

# Conteúdo da página principal (Home)
st.title("Home")
st.write("Bem-vindo à página principal!")