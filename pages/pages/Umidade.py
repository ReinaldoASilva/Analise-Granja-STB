import streamlit as st


st.title('Umidade!')

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title('Análise de Umidade no Aviário')

st.write("Manter a temperatura adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.")

# Carregar os dados de temperatura a partir do arquivo Excel
dados_temperatura = pd.read_excel("/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx")
matriz = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Setembro/Aviário-2/Umidade x Temperatura_cobb.xlsx')

# Cria um gráfico de linha comparativo com Umidade_Media e Umidade_Desejada
fig, ax = plt.subplots()
ax.plot(dados_temperatura['Umidade_Media'], label='Umidade Média')
ax.plot(dados_temperatura['Umidade_Desejada'], label='Umidade Desejada')
ax.set_xlabel('Data')
ax.set_ylabel('Umidade')
ax.set_title('Umidade Média vs Umidade Desejada')
ax.legend()
# Exibe o gráfico
st.pyplot(fig)

# Umidade maxima, minima e media da Matriz

fig, ax = plt.subplots()
ax.plot(matriz['Umidade Minima'], label='Umidade Mínmima')
ax.plot(matriz['Umidade Maxima'], label='Umidade Máxima')
ax.plot(matriz['Umidade Media'], label='Umidade Média')
ax.set_xlabel('Idade em Dias')
ax.set_ylabel('Umidade')
ax.set_title('Matriz Temporal - Umidade Mínima x Máxima x Média')
ax.legend()
st.pyplot(fig)