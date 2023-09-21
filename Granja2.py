import pandas as pd
import matplotlib.pyplot as plt
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
granja = granja.drop(columns=colunas_zero)

# Excluir colunas que contenham somente valores = 
colunas_igual_1 = granja.columns[(granja == 1).any()]
granja = granja.drop(columns=colunas_igual_1)

# Excluir Colunas que não serão utilizadas
colunas_inuteis = ['T1','T3','T4','T5','TU1_Temperatura','TU1_Umidade','AD1','AD2']
granja = granja.drop(columns=colunas_inuteis)

# Converter a coluna data para o tipo datetime
granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'], format='%Y-%m-%d')


# Criar coluna chamada semana
primeira_data = granja['Data/Hora'].iloc[0]
granja['Semana'] = ((granja['Data/Hora'] - primeira_data).dt.days // 7).astype(int)


########################################################################################################################################################################

# Calcular a temperatura por Dia
TP_Media_Diaria = granja.groupby('Data/Hora')['Temperatura_Media'].mean().apply(lambda x: int(x))
TP_Maxima_Diaria = granja.groupby('Data/Hora')['Temperatura_Media'].max().apply(lambda x: int(x))
TP_Minima_Diaria = granja.groupby('Data/Hora')['Temperatura_Media'].min().apply(lambda x: int(x))

# Add média semanal ao dataframe

granja['TP_Media_Diaria'] = granja['Data/Hora'].map(TP_Media_Diaria)
granja['TP_Maxima_Diaria'] = granja['Data/Hora'].map(TP_Maxima_Diaria)
granja['TP_Minima_Diaria'] = granja['Data/Hora'].map(TP_Minima_Diaria)

# Calcular temperatura media Semanal
TP_Media_Semanal = granja.groupby('Semana').agg({'Temperatura_Media': ['max', 'mean', 'min']}).reset_index()

# Renomear as colunas
TP_Media_Semanal.columns = ['Semana', 'TP_Media_Semanal','TP_Maxima_Semanal', 'TP_Minima_Semanal']

# Mesclar as estatísticas com o DataFrame "granja"
granja = granja.merge(TP_Media_Semanal, on='Semana', how='left')

########################################################################################################################################################################

# Calcular Umidade média Diária
UMI_Media_Diaria = granja.groupby('Data/Hora').agg({'Umidade_Media': ['max', 'min', 'mean']}).reset_index()

# Renomear as colunas
UMI_Media_Diaria.columns = ['Data/Hora', 'UMI_Media_Diaria', 'UMI_Maxima_Diaria', 'UMI_Minima_Diaria']

# Mesclar as Estatisticas ao Dataframe

granja = granja.merge(UMI_Media_Diaria, on= 'Data/Hora', how='left')


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
