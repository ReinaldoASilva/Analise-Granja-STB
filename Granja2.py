import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import dash_table
import dash
import dash_core_components as dcc
import dash_html_components as html



import plotly.graph_objects as go


# Leitura do arquivo
granja = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Setembro/Aviário-2/smaai_leituras.xlsx')
matriz = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Setembro/Aviário-2/Umidade x Temperatura_cobb.xlsx')

# Renomear a coluna data/hora
granja = granja.rename(columns={'Data/Hora':'Data'}) 

# Substituir valores nan por 0 
granja = granja.fillna(0)

# Excluir colunas que somente tem o valor = 0 / Atualemente com 108 colunas
colunas_zero = granja.columns[(granja == 0).all()]

# Excluir as colunas identificadas
granja = granja.drop(columns=colunas_zero)

# Excluir colunas que contenham somente valores = 
colunas_igual_1 = granja.columns[(granja == 1).any()]
granja = granja.drop(columns=colunas_igual_1)

# Converter a coluna data para o tipo datetime
granja['Data'] = pd.to_datetime(granja['Data'])

# Remover a hora da coluna
granja['Data'] = granja['Data'].dt.date

# Encontrar a data mínima
data_minima = granja['Data'].min()

# Calcular a idade de vida em dias
granja['Idade de Vida'] = (granja['Data'] - data_minima).dt.days

# Preencher a coluna 'semana' com base nas datas
granja['Semana'] = (granja['Data'] - data_minima).apply(lambda x: divmod(x.days,7)[0])

########################################################################################################################################################################


# Calcular a temperatura média por semana
TP_Media_Semanal = granja.groupby('Semana')['Temperatura_Media'].mean().apply(lambda x: int(x))

# Add média semanal ao dataframe

granja = granja.merge(TP_Media_Semanal, left_on='Semana', right_index=True, suffixes=('','_Media_Semanal'))

# Calcular temperatura media diária

TP_Media_Diaria = granja.groupby('Idade de Vida')['Temperatura_Media'].mean().apply(lambda x: int(x))

# Add temperatura media no dataframe
granja['TP_Media_Diaria'] = granja['Idade de Vida'].map(TP_Media_Diaria)

# Renomear Coluna
granja.rename(columns={'Temperatura_Media_Media_Semanal':'Media_Semanal'}, inplace=True )

# Lista de Colunas que serão excluídas
colunas_excluir = ['T1','T3', 'T4', 'T5','TU1_Temperatura', 'TU1_Umidade', 'AD1', 'AD2']

# Excluir colunas
granja = granja.drop(colunas_excluir, axis=1)

# Transformar a coluna Temperatura desejada em inteiro
granja['Temperatura_Desejada'] = granja['Temperatura_Desejada'].astype(int)

granja['Umidade_Desejada'].value_counts()

########################################################################################################################################################################

# Calcular Umidade média semanal
granja_umidade_semanal = granja.groupby('Semana')['Umidade_Media'].mean().reset_index()

# Calcular a umidade média diária
granja_umidade_diaria = granja.groupby('Idade de Vida')['Umidade_Media'].mean().reset_index()

########################################################################################################################################################################

# Análise Gráfica dos dados Temperatura e Umidade

# Criar aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    # Título do dashboard
    html.H1('Dashboard de Temperatura e Umidade no Aviário'),
    
    # Gráfico de temperatura
    html.H2('Gráfico de Temperatura'),
    dcc.Graph(figure=go.Figure([
        go.Scatter(x=granja['Idade de Vida'], y=granja['Temperatura_Desejada'], name='Temperatura Desejada'),
        go.Scatter(x=granja['Idade de Vida'], y=granja['TP_Media_Diaria'], name='Temperatura Média Diária')
    ])),
    
    # Gráfico de umidade
    html.H2('Gráfico de Umidade'),
    dcc.Graph(figure=go.Figure([
        go.Scatter(x=granja['Idade de Vida'], y=granja['Umidade_Desejada'], name='Umidade Desejada'),
        go.Scatter(x=granja['Idade de Vida'], y=granja['Umidade_Media'], name='Umidade Média')
    ]))
])

# Executar o aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)





########################################################################################################################################################################


# Salvar o Arquivo

#granja.to_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Setembro/Aviário-2/smaai_leituras_atualizado.xlsx')
