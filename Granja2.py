import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go


# Leitura do arquivo
granja = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Setembro/Aviário-2/smaai_leituras.xlsx')
matriz = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Setembro/Aviário-2/Umidade x Temperatura_cobb.xlsx')

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
granja = granja.drop(columns=colunas_inuteis )

# Converter a coluna data para o tipo datetime
granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'], format='%Y-%m-%d')

#Determinar a data inicial
data_inicial = granja['Data/Hora'].min()

# Criar a nova coluna com a contagem dos dias
granja['Idade_em_Dias'] = (granja['Data/Hora'] - data_inicial).dt.days
granja.columns

# Criar coluna chamada semana
primeira_data = granja['Data/Hora'].iloc[0]
granja['Semana'] = ((granja['Data/Hora'] - primeira_data).dt.days // 7).astype(int)


########################################################################################################################################################################

# Calcular a temperatura por Dia
TP_Media_Diaria = granja.groupby('Data/Hora').agg({'Temperatura_Media': ['max', 'mean', 'min']}).reset_index()

# Renomear as colunas
TP_Media_Diaria.columns = ['Data/Hora','TP_Media_Diaria','TP_Maxima_Diaria','TP_Minima_Diaria']

# Add média Diária ao dataframe
granja = granja.merge(TP_Media_Diaria, on='Data/Hora', how='left')

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

# Calcular a Umidade Semanal

UMI_Media_Semanal = granja.groupby('Semana').agg({'Umidade_Media':['mean','max', 'min']}).reset_index()

# Renomear as colunas

UMI_Media_Semanal.columns=['Semana', 'UMI_Media_Semanal', 'UMI_Maxima_Semanal', 'UMI_Minima_Semanal']

# Add as colunas métricas ao dataframe granja

granja = granja.merge(UMI_Media_Semanal, on='Semana', how='left')

# Formatar colunas e deixar com apenas duas casas decimais

granja['UMI_Media_Semanal'] = granja['UMI_Media_Semanal'].apply(lambda x: "{:.2f}".format(x))


# Organizar as colunas
nova_ordem=['Data/Hora', 'Semana', 'Idade em Dias', 'Temperatura_Desejada', 'Temperatura_Media', \
     'TP_Media_Diaria', 'TP_Maxima_Diaria', 'TP_Minima_Diaria', 'TP_Media_Semanal', \
     'TP_Maxima_Semanal', 'TP_Minima_Semanal','Umidade_Desejada', 'Umidade_Media', \
     'UMI_Media_Diaria', 'UMI_Maxima_Diaria', 'UMI_Minima_Diaria','UMI_Media_Semanal', \
     'UMI_Maxima_Semanal', 'UMI_Minima_Semanal','Pressao_Desejada']

granja = granja.reindex(columns=nova_ordem)

# Salvar o Arquivo

granja.to_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Setembro/Aviário-2/smaai_leituras_atualizado.xlsx')


########################################################################################################################################################################

# Análise Gráfica dos dados Temperatura e Umidade

# Criar aplicativo Dash
app = dash.Dash(__name__)

# Layout do aplicativo
app.layout = html.Div([
    # Título do dashboard
    html.H1('Comparativo de Temperatura  no Aviário'),
    
    # Gráfico de temperatura
    html.H2('Temperatura Desejada x Temperatura Média Diária'),
    dcc.Graph(figure=go.Figure([
        go.Bar(x=granja['Data/Hora'], y=granja['Temperatura_Desejada'], name='Temperatura Desejada', marker=dict(color='blue')),
        go.Bar(x=granja['Data/Hora'], y=granja['TP_Media_Diaria'], name='Temperatura Média Diária', marker=dict(color='red'))
    ])),
    # Gráfico de temperatura
    html.H2('Temperatura Desejada x Temperatura Maxima Diária'),
    dcc.Graph(figure=go.Figure([
        go.Scatter(x=granja['Data/Hora'], y=granja['Temperatura_Desejada'], name='Temperatura Desejada'),
        go.Scatter(x=granja['Data/Hora'], y=granja['TP_Maxima_Diaria'], name='Temperatura Maxima Diária')
    ])),
    # Gráfico de umidade
    html.H2('Temperatura Desejada x Temperatura Minima Diária'),
    dcc.Graph(figure=go.Figure([
        go.Scatter(x=granja['Data/Hora'], y=granja['Temperatura_Desejada'], name='Temperatura Desejada'),
        go.Scatter(x=granja['Data/Hora'], y=granja['TP_Minima_Diaria'], name='Temperatura Minima Diária')
    ])),
    # Comparativo matriz
    html.H2('Temperatura Desejada x Temperatura Minima Diária'),
    dcc.Graph(figure=go.Figure([
        go.Scatter(x=matriz['Idade em Dias'], y=matriz['Temperatura Media'], name='Temperatura Media-Matriz'),
        go.Scatter(x=granja['Idade em Dias'], y=granja['TP_Media_Diaria'], name='TP_Media_Diaria-Granja')
    ]))

])

# Executar o aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)





########################################################################################################################################################################


# Supondo que você tenha um DataFrame chamado 'granja' com as colunas 'Data/Hora' e 'Temperatura_Desejada'
granja = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx')

# Renomear coluna
granja = granja.rename(columns={'Idade em Dias': 'Idade_em_Dias'})

# Idade_em_Dias comecar em 0
data_inicial = granja['Data/Hora'].min()
granja['Idade_em_Dias'].replace((granja['Data/Hora'] - data_inicial).dt.days)
granja.columns

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