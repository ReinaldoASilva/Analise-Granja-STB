import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Análise de Temperatura no Aviário')

st.write("Manter a temperatura adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.")




# Dados de exemplo
dados_temperatura = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx')

df_temperatura = pd.DataFrame(dados_temperatura)

Temperatura_Desejada = len(df_temperatura['Temperatura_Desejada'])

col1, col2, col3 = st.columns(3)
col1.metric('Temperatura_Desejada', Temperatura_Desejada)

# Gráfico de barras comparativo
st.header('Comparação de Temperatura')
fig, ax = plt.subplots()
df_temperatura.plot(x='Idade de Vida', y=['Temperatura_Desejada', 'TP_Media_Diaria'], kind='bar', ax=ax)
ax.set_ylabel('Temperatura (°C)')
ax.set_xlabel('Idade de Vida')
plt.show()

st.pyplot(fig)