import streamlit as st


# Modo responsivo
st.set_page_config(layout="wide")

# Definindo as opções do submenu de Temperatura
submenu_umidade = ['Análise de Umidade', 'Análise por Período', 'Pico de Umidade']
subpagina_selecionada = st.sidebar.radio('3.Insight',submenu_umidade)



st.write("A umidade no aviário foi um problema durante o tempo do lote, \
        houve 24 dias consecutivos com picos e um total de 27 dias com picos no geral. Já a temperatura também foi um desafio, \
        desafio também durante os 30 dias no período, sendo que em 20 deles ocorreram picos consecutivos e em 24 dias houve picos em algum momento. \
        Esses dados revelam que as aves têm sofrido com estresse térmico, sendo particularmente preocupante a ocorrência de 20 dias seguidos \
        com temperatura acima dos limites recomendados. Além disso, a umidade chegou a atingir picos de 99%, o que agrava ainda mais a situação. \
        Nesse contexto, é essencial tomar medidas para proporcionar um ambiente o mais confortável possível para as aves.")

st.write("Algumas medias que podem ser tomadas para um controle mais eficiente da ambiência")
st.write("Medidas para baixar a umidade do aviário:")
st.write("- Ventilação adequada: Garanta uma boa circulação de ar no aviário para ajudar a reduzir a umidade, permitindo a saída do ar úmido e a entrada de ar fresco.")
st.write("- Instalação de janelas.")
st.write("- Utilização de ventiladores.")
st.write("- Utilização de exaustores.")


















