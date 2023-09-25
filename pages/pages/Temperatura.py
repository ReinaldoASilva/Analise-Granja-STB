import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime as dt
import matplotlib.dates as mdates
import mplcursors


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

st.markdown("<h2 style='text-align: center;'>Comparativo</h2>", unsafe_allow_html=True)

if not dados_selecionados.empty:
    # Obter as datas das data/hora
    datas = dados_selecionados['Data/Hora']

    # Obter os valores das temperaturas
    temperaturas_medias = dados_selecionados['Temperatura_Media']
    temperatura_desejada = dados_selecionados['Temperatura_Desejada']

    # Configurar o gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(datas, temperaturas_medias, label='Temperatura')
    plt.plot(datas, temperatura_desejada, label='Temperatura Desejada')
    plt.xlabel('Data/Hora')
    plt.ylabel('Temperatura')
    plt.title('')
    plt.legend()
    plt.xticks(rotation=45)

     # Adicionar interatividade para exibir os valores no mouse hover
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_ydata()[sel.target.index]))


    # Exibir o gráfico no Streamlit
    st.pyplot(plt)
else:
    st.write('Não há dados disponíveis para a data/hora selecionada.')

st.markdown("<h2 style='text-align: center;'>Picos de Temperatura</h2>", unsafe_allow_html=True)

# Filtrar os dados para obter as temperaturas médias e desejadas
temperaturas_medias = granja['Temperatura_Media']
temperatura_desejada = granja['Temperatura_Desejada']
datas = granja['Data/Hora']

# Encontrar os horários de maiores picos na temperatura
horarios_maiores_picos = datas[temperaturas_medias > temperatura_desejada]
horarios_maiores_picos.value_counts()
# Configurar o gráfico
plt.figure(figsize=(10, 6))
plt.plot(datas, temperaturas_medias, label='Temperatura Média')
plt.plot(datas, temperatura_desejada, label='Temperatura Desejada')
plt.scatter(horarios_maiores_picos, temperaturas_medias[temperaturas_medias > temperatura_desejada], color='red', label='Picos de Temperatura')
plt.xlabel('Data/Hora')
plt.ylabel('Temperatura')
plt.title('')
plt.legend()
# Exibir o gráfico no Streamlit
st.pyplot(plt)


st.markdown("<h2 style='text-align: center;'>Análise por Período</h2>", unsafe_allow_html=True)
# Arredondar os horários para períodos de 3 horas
granja['Periodo_Horas'] = granja['Data/Hora'].dt.floor('3H')

# Obter lista de datas
datas = granja['Data/Hora'].dt.date.unique()

# Converter as datas para string no formato "YYYY-MM-DD"
datas_str = [str(data) for data in datas]

# Selecionar a data
selected_data_str = st.selectbox('Selecione a data:', datas_str)

# Converter a data selecionada para o formato de data
selected_data = pd.to_datetime(selected_data_str)

# Filtrar os dados para a data selecionada
dados_data = granja[granja['Data/Hora'].dt.date == selected_data.date()]

# Obter o limite de temperatura desejado
limite_temperatura = dados_data['Temperatura_Desejada'].iloc[0]  # Substitua pelo limite desejado

# Filtrar os horários em que a temperatura ultrapassou o limite desejado
horarios_ultrapassagem = dados_data[dados_data['Temperatura_Media'] > limite_temperatura]['Data/Hora']

# Agrupar os horários por período de 3 horas
horarios_agrupados = horarios_ultrapassagem.dt.floor('3H').dt.time

# Contar o número de picos de temperatura em cada período de 3 horas
contagem_picos = horarios_agrupados.value_counts()

# Exibir o intervalo de horários com base no período de 3 horas
st.write("Intervalo de Horários com Ultrapassagem do Limite de Temperatura:")
for horario, count in contagem_picos.items():
    st.write(f"{horario} - {count} pico(s)")

# Exibir a parte do dia com base no horário
parte_dia = horarios_agrupados.apply(lambda x: "Madrugada" if 0 <= x.hour < 6 else "Manhã" if 6 <= x.hour < 12 else "Tarde" if 12 <= x.hour < 18 else "Noite")
parte_dia_contagem = parte_dia.value_counts()

# Exibir a contagem de picos por parte do dia
st.write("Contagem de Picos de Temperatura por Parte do Dia:")
for parte, count in parte_dia_contagem.items():
    st.write(f"{parte}: {count} pico(s)")




# Converter a coluna "Data/hora" para o tipo datetime
granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'])

# Definir o período da madrugada
inicio_madrugada = pd.Timestamp("00:00:00")
fim_madrugada = pd.Timestamp("05:59:59")

inicio_manha = pd.Timestamp("06:00:00")
fim_manha = pd.Timestamp("11:59:59")

inicio_tarde = pd.Timestamp("12:00:00")
fim_tarde = pd.Timestamp("17:59:59")

inicio_noite = pd.Timestamp("18:00:00")
fim_noite = pd.Timestamp("23:59:59")


# Filtrar os dados dentro do período da madrugada
dados_madrugada = granja[(granja['Data/Hora'].dt.time >= inicio_madrugada.time()) & (granja['Data/Hora'].dt.time <= fim_madrugada.time())]

dados_manha = granja[(granja['Data/Hora'].dt.time >= inicio_manha.time()) & (granja['Data/Hora'].dt.time <= fim_manha.time())]

dados_tarde = granja[(granja['Data/Hora'].dt.time >= inicio_tarde.time()) & (granja['Data/Hora'].dt.time <= fim_tarde.time())]

dados_noite = granja[(granja['Data/Hora'].dt.time >= inicio_noite.time()) & (granja['Data/Hora'].dt.time <= fim_noite.time())]

# Calcular a quantidade de picos no período da madrugada
quantidade_picos_madrugada = dados_madrugada['Temperatura_Desejada'].count()

quantidade_picos_manha = dados_manha['Temperatura_Desejada'].count()

quantidade_picos_tarde = dados_tarde['Temperatura_Desejada'].count()

quantidade_picos_noite = dados_noite['Temperatura_Desejada'].count()



# Exibir a quantidade de picos no período da madrugada
print(f"A quantidade de picos no período da madrugada é: {quantidade_picos_madrugada}")
print(f"A quantidade de picos no período da manhã é: {quantidade_picos_manha}")
print(f"A quantidade de picos no período da tarde é: {quantidade_picos_tarde}")
print(f"A quantidade de picos no período da noite é: {quantidade_picos_noite}")



# Criar um DataFrame com os resultados
resultados = pd.DataFrame({
    'Período': ['Madrugada', 'Manhã', 'Tarde', 'Noite'],
    'Quantidade de Picos': [quantidade_picos_madrugada, quantidade_picos_manha, quantidade_picos_tarde, quantidade_picos_noite]
})

# Ordenar a tabela em ordem decrescente pela coluna 'Quantidade de Picos'
resultados = resultados.sort_values(by='Quantidade de Picos', ascending=False)

# Exibir a tabela de resultados ordenada
print(resultados)
# Exibir a tabela de resultados ordenada
st.write(resultados)