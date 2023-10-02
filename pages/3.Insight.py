import streamlit as st
from pathlib import Path
from PIL import Image
import pandas as pd

# Modo responsivo
st.set_page_config(layout="wide")

# Imagem
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
data = current_dir / 'insight.jpeg'
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



st.title("Insight")

st.write("A umidade no aviário foi um problema durante o tempo do lote, \
        houve 24 dias consecutivos com picos e um total de 27 dias com picos no geral. Já a temperatura também foi um desafio, \
        desafio também durante os 30 dias no período, sendo que em 20 deles ocorreram picos consecutivos e em 24 dias houve picos em algum momento. \
        Esses dados revelam que as aves têm sofrido com estresse térmico, sendo particularmente preocupante a ocorrência de 20 dias seguidos \
        com temperatura acima dos limites recomendados. Além disso, a umidade chegou a atingir picos de 99%, o que agrava ainda mais a situação. \
        Nesse contexto, é essencial tomar medidas para proporcionar um ambiente o mais confortável possível para as aves.")

st.write(" ➡️ : Algumas medias que podem ser tomadas para um controle mais eficiente da ambiência")
st.write(" - Ventilação adequada: Garanta uma boa circulação de ar no aviário para ajudar a reduzir a umidade, permitindo a saída do ar úmido e a entrada de ar fresco.")
st.write(" - Instalação de Janelas.")
st.write(" - Instalação de inlet")
st.write(" - Utilização de Ventiladores.")
st.write(" - Utilização de Exaustores.")
st.write(" - Isolamento Térmico")
st.write(" - Resfriamento Evaporativo")



















