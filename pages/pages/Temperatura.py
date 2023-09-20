import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

st.title('Análise de Temperatura no Aviário')

st.write("Manter a temperatura adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.")

# Carregar os dados de temperatura a partir do arquivo Excel
dados_temperatura = pd.read_excel("/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx")

# Criar figura
fig = go.Figure()

# Adicionar barras de umidade média
fig.add_trace(go.Bar(
    x=dados_temperatura['Idade de Vida'],
    y=dados_temperatura['Umidade_Media'],
    name='Umidade Média',
    marker_color='blue'
))

# Adicionar barras de umidade desejada
fig.add_trace(go.Bar(
    x=dados_temperatura['Idade de Vida'],
    y=dados_temperatura['Umidade_Desejada'],
    name='Umidade Desejada',
    marker_color='red'
))

# Configurar layout do gráfico
fig.update_layout(
    title='Umidade Média vs Umidade Desejada',
    xaxis_title='Idade_Vida',
    yaxis_title='Umidade'
)

# Exibir o gráfico usando o Streamlit
st.plotly_chart(fig)