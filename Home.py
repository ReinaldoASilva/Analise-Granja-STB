import streamlit as st



st.markdown("<h2 style='text-align: center;'>Avaliando a Performance em Ambientes Controlados!</h2>", unsafe_allow_html=True)
    
st.write("Este projeto de análise de dados tem como objetivo investigar como as condições ambientais afetam o desempenho das aves. \
Analisaremos os momentos em que a temperatura e umidade atingem niveis extremos, buscando compreender como esses fatores influenciam na conversão alimentar..\
A ideia é buscar melhorias nas práticas de manejo e identificar os intervalos perfeitos de temperatura e umidade, com o objetivo de maximizar os lucros nas granjas analisadas.")


uploaded_file = st.file_uploader("/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/producao-avicola.jpg", type=["jpg", "png"])
if uploaded_file is not None:
    st.image(uploaded_file)


