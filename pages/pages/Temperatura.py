import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime as dt


# Supondo que você tenha um DataFrame chamado 'granja' com as colunas 'Data/Hora' e 'Temperatura_Desejada'
granja = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx')


# Converter a coluna 'Data/Hora' em um objeto datetime
granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'])
#excluir a hora da coluna data

granja['Data'] = granja['Data/Hora'].dt.date

st.title('Análise de Temperatura no Aviário')

st.write("Manter a temperatura adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.")


# Extrair os valores da coluna 'Temperatura_Desejada'
temperatura_desejada = granja['Temperatura_Desejada'].values

# Criar o slider para selecionar a data/hora
data_hora_selecionada = st.slider('Selecione a Data/Hora', min_value=granja['Data'].min(), max_value=granja['Data'].max())

# Filtrar o DataFrame com base na data/hora selecionada
dados_selecionados = granja[granja['Data'] == data_hora_selecionada]

# Obter os valores das temperaturas mínima, máxima e média para a data/hora selecionada
temperatura_minima = dados_selecionados['TP_Minima_Diaria'].min()
temperatura_maxima = dados_selecionados['TP_Maxima_Diaria'].max()
temperatura_media = round(dados_selecionados['TP_Media_Diaria'].mean(), 2)

# Arredondar a temperatura média para 2 casas decimais
temperatura_media_formatada = format(temperatura_media, '.2f')

# Calcular a diferença entre a temperatura mínima e desejada
delta_minima = temperatura_minima - temperatura_desejada[0]

# Exckuir colunas
colunas_excluir = ['Unnamed: 0','Data']
granja = granja.drop(columns=colunas_excluir)


# Criar as colunas
col1, col2, col3 = st.columns(3)

# Aplicando o formato aos modelos de temperatura
##st.metric(label="Temperatura Mínima", value=temperatura_minima, delta=delta_minima, delta_color="inverse")

with col1:
    st.metric(label="Temperatura Mínima", value=format(temperatura_minima, '.2f'), delta=format(delta_minima, '.2f'), delta_color="inverse")

with col2:
    st.metric(label="Temperatura Máxima", value=format(temperatura_maxima, '.2f'),delta=format(temperatura_maxima - temperatura_desejada[0], '.2f'), delta_color="inverse")

with col3:
    st.metric(label="Temperatura Média", value=format(temperatura_media, '.2f'), delta=format(temperatura_media - temperatura_desejada[0], '.2f'), delta_color="inverse")
# Exibir a temperatura média em um texto simples formatado manualmente
# Criar o slider para selecionar a data/hora

# Verificar se há dados selecionados
if not dados_selecionados.empty:
    # Obter os valores das temperaturas
    temperaturas = dados_selecionados['Temperatura_Media']

    # Configurar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(dados_selecionados['Data/Hora'], temperaturas)
    plt.xlabel('Data/Hora')
    plt.ylabel('Temperatura Média')
    plt.title('Gráfico de Linha - Temperatura Média')
    plt.xticks(rotation=45)

    # Exibir o gráfico no Streamlit
    st.pyplot(plt)
else:
    st.write('Não há dados disponíveis para a data/hora selecionada.')