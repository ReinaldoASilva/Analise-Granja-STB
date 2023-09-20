import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.title('Análise de Temperatura no Aviário')

st.write("Manter a temperatura adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.")

# Carregar os dados de temperatura a partir do arquivo Excel
dados_temperatura = pd.read_excel("/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx")

# Cria um gráfico de linha para temperatura média vs temperatura desejada
#Criar figura e eixos
fig, ax = plt.subplots()
ax.bar(dados_temperatura.index, dados_temperatura['Umidade_Media'], color='blue', label='Umidade Média')
ax.bar(dados_temperatura.index, dados_temperatura['Umidade_Desejada'], color='red', label='Umidade Desejada')

# Configurar rótulos e título
ax.set_xlabel('Idade_Vida')
ax.set_ylabel('Umidade')
ax.set_title('Umidade Média vs Umidade Desejada')

# Adicionar legenda
ax.legend()

# Exibir o gráfico usando o Streamlit
st.pyplot(fig)