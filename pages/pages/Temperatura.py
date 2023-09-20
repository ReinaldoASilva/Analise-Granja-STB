import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title('Análise de Temperatura no Aviário')

st.write("Manter a temperatura adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.")

# Carregar os dados de temperatura a partir do arquivo Excel
dados_temperatura = pd.read_excel("/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx")

# Cria um gráfico de linha para temperatura média vs temperatura desejada
fig, ax = plt.subplots()
ax.plot(dados_temperatura['TP_Media_Diaria'], dados_temperatura['Temperatura_Desejada'], marker='o')
ax.set_xlabel('Temperatura Média Diária')
ax.set_ylabel('Temperatura Desejada')
ax.set_title('Temperatura Média Diária vs Temperatura Desejada')
st.pyplot(fig)

# Cria um gráfico de barras para umidade média vs umidade desejada
fig, ax = plt.subplots()
ax.bar(dados_temperatura['Umidade_Media'], dados_temperatura['Umidade_Desejada'])
ax.set_xlabel('Umidade Média')
ax.set_ylabel('Umidade Desejada')
ax.set_title('Umidade Média vs Umidade Desejada')
st.pyplot(fig)
