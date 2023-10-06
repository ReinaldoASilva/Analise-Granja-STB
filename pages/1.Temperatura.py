import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import datetime as dt
import plotly.express as px
from pathlib import Path
from PIL import Image

# Coletando dados
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
data = current_dir /'smaai.csv'
granja = pd.read_csv(data)

# Modo responsivo
st.set_page_config(layout="wide")

# Definindo as opções do submenu de Temperatura
submenu_temperatura = ["Análise de Temperatura", "Análise por Período", "Pico de Temperatura"]
subpagina_selecionada = st.sidebar.radio("1.Temperatura", submenu_temperatura)

# Visualizar logo
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
logo_path = current_dir /'logo.png'

logo = Image.open(logo_path)

# Define a largura fixa do logotipo
logo_width = 300

# Cria uma coluna para exibir o logotipo acima do menu
col_logo, col_menu = st.sidebar.columns([logo_width, 1])

# Exibe o logotipo na coluna do logotipo

with col_logo:
    st.image(logo, width=logo_width)

# Remover o menu do streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#################################################################### PÁGINA Análise de Temperatura ####################################################################

# Verifica qual subpágina foi selecionada e exibe o conteúdo correspondente
if subpagina_selecionada == "Análise de Temperatura":
    
    
    st.markdown("<div style='text-align: center;'>"
            "<h1>Análise de Temperatura</h1>"
            "</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>"
            "<h5>Aqui você pode fazer a Análise da temperatura.👇</h5>"
            "</div>", unsafe_allow_html=True)       
  
    # Converter a coluna 'Data/Hora' em um objeto datetime
    granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'])

    # Excluir a hora da coluna data
    granja['Data'] = granja['Data/Hora'].dt.date

    # Extrair os valores da coluna 'Temperatura_Desejada'
    temperatura_desejada = granja['Temperatura_Desejada'].values

    # Criar o slider para selecionar a data/hora
    data_hora_selecionada = st.slider('Selecione a Data/Hora', min_value=granja['Data'].min(), max_value=granja['Data'].max())

    # Filtrar o DataFrame com base na data/hora selecionada
    dados_selecionados = granja[granja['Data'] == data_hora_selecionada]

    # Obter os valores das temperaturas mínima, máxima e média para a data/hora selecionada
    temperatura_minima = dados_selecionados['TP_Minima_Diaria'].min()
    temperatura_maxima = dados_selecionados['TP_Maxima_Diaria'].max()
    temperatura_media = dados_selecionados['TP_Media_Diaria'].mean()
    
    # Obter o valor da temperatura desejada do DataFrame
    temperatura_ideal = dados_selecionados['Temperatura_Desejada'].iloc[0]

    # Calcular a diferença entre a temperatura mínima e desejada
    delta_minima = temperatura_minima 
    delta_maxima = temperatura_maxima 
    delta_media =  temperatura_media
    delta_ideal = temperatura_ideal
    

    # Criar as colunas
    temperatura_ideal, temperatura_minima, temperatura_media, temperatura_maxima = st.columns(4)


    with temperatura_ideal:
        st.metric(label="Temperatura Ideal", value=format(delta_ideal))

    with temperatura_minima:
        st.metric(label="Temperatura Mínima", value=format(delta_minima))
        
    with temperatura_media:
        st.metric(label="Temperatura Média", value=format(delta_media, '.2f'))

    with temperatura_maxima:
       st.metric(label="Temperatura Máxima", value=format(delta_maxima))

    # Gráfico
    st.write('#')
    st.markdown("<p style='text-align: center;'>No gráfico abaixo 👇 veremos a flutuação da temperatura durante o dia.</p>", unsafe_allow_html=True)# Gráfico com as temperaturas
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_selecionados['Data/Hora'], y=dados_selecionados['Temperatura_Media'], mode='lines', name='Temperatura'))
    fig.add_trace(go.Scatter(x=dados_selecionados['Data/Hora'], y=dados_selecionados['Temperatura_Desejada'], mode='lines', name='Temperatura Ideal'))
    fig.update_layout(
        title=' ',
        xaxis_title='Data/Hora',
        yaxis_title='Temperatura',
        width=800,  # Definir a largura da janela do gráfico
        height=600,  # Definir a altura da janela do gráfico
        legend=dict(
            orientation="h",  # Orientação horizontal
            yanchor="top",  # Âncora superior
            y=1.1  # Posição vertical
        )
    )
    fig.update_xaxes(tickangle=45)

# Exibir o gráfico interativo no Streamlit
    st.plotly_chart(fig,config={'displayModeBar': False})

#################################################################### PÁGINA ANÁLISE POR PERÍODO ####################################################################

elif subpagina_selecionada == "Análise por Período":
   
   # Seleção de períodos para analisar os dados# Conteúdo da subpágina "Análise por Período"

    st.markdown("<div style='text-align: center;'>"
            "<h1>Análise por Período</h1>"
            "</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>"
            "<h5>Aqui você pode fazer a Análise da Temperatura por Período.👇</h5>"
            "</div>", unsafe_allow_html=True)       

    # Converter a colunadata/hora para dtypes
    granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'])

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
    st.markdown("Intervalo de Horários com Ultrapassagem do Limite de Temperatura:")
    for horario, count in contagem_picos.items():
        st.markdown(f"{horario} - {count} pico(s)")

    # Exibir a parte do dia com base no horário
    parte_dia = horarios_agrupados.apply(lambda x: "Madrugada" if 0 <= x.hour < 6 else "Manhã" if 6 <= x.hour < 12 else "Tarde" if 12 <= x.hour < 18 else "Noite")
    parte_dia_contagem = parte_dia.value_counts()

    # Exibir a contagem de picos por parte do dia
    st.markdown("Contagem de Picos de Temperatura por Parte do Dia:")
    for parte, count in parte_dia_contagem.items():
        st.markdown(f"{parte}: {count} pico(s)")

    # Título do Gráfico
    st.markdown("<div style='text-align: center;'>"
                "<h5>Aqui você pode ver o gráfico da análise dos períodos.👇</h5>"
                "</div>", unsafe_allow_html=True)   

        # Verificar se há dados disponíveis para a parte do dia
    if not parte_dia_contagem.empty:
            
            # Criar um gráfico de barras interativo para a contagem de picos por parte do dia
            fig = px.bar(parte_dia_contagem, x=parte_dia_contagem.index, y=parte_dia_contagem.values, labels={'x': 'Parte do Dia', 'y': 'Contagem de Picos'}, title='')
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': ['Madrugada', 'Manhã', 'Tarde', 'Noite']})  # Ordenar as categorias corretamente

            # Exibir o gráfico de barras interativo no Streamlit
            st.plotly_chart(fig, config={'displayModeBar': False})
       
    else:
        st.markdown("Não há dados disponíveis para a data selecionada.")

#################################################################### PÁGINA PICOS DE TEMPERATURA ####################################################################

elif subpagina_selecionada == "Pico de Temperatura":

    # Título
    st.markdown("<div style='text-align: center;'>"
            "<h1>Picos de Temperatura</h1>"
            "</div>", unsafe_allow_html=True)
    st.markdown("<div>"
            "Aqui podemos visualizar a quantidade de dias em que ocorreram picos de temperatura, "
            "bem como a duração dos períodos consecutivos e o total de dias afetados. Essas informações nos "
            "ajudam a compreender a importância de uma gestão mais eficiente do ambiente, visando proporcionar "
            "condições ideais.👇"
            "</div>", unsafe_allow_html=True)

    st.write("#")

    #Filtrar os dados para obter as temperaturas médias e desejadas
    temperaturas_medias = granja['Temperatura_Media']
    temperatura_desejada = granja['Temperatura_Desejada']
    datas = granja['Data/Hora']
    #datas = datas.to_frame().rename(columns={0: 'Data/Hora'})

     # Encontrar os horários de maiores picos na umidade
    horarios_maiores_picos = datas[temperaturas_medias > temperatura_desejada]

    # Obter as dataas únicas com picos de temperatura
    horarios_maiores_picos = pd.to_datetime(horarios_maiores_picos)
    dias_picos_temperatura = horarios_maiores_picos.dt.date.unique()

    # Calcular quantidades de dias com pico de temperatura
    quantidade_dias_picos = len(dias_picos_temperatura)

    # Calcular a quantidade de dias
    granja['data'] = pd.to_datetime(granja['Data/Hora'])
    quantidade_dias = granja['data'].dt.date.nunique()
    quantidade_dias_inteiro = int(quantidade_dias)

    # Determinar quantos dias seguidos de pico de temperatura ocorreram
    dias_seguidos_picos = 0
    for i in range(len(dias_picos_temperatura) - 1):
        data_atual = dias_picos_temperatura[i]
        data_seguinte = dias_picos_temperatura[i + 1]
        if (data_seguinte - data_atual).days == 1:
            dias_seguidos_picos += 1

    # Criar colunas
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        # Exibir a quantidade de dias com picos de temperatura
        st.metric(label="", value="")

    with col2:
        # Exibir a quantidade de dias com picos de temperatura
        st.metric(label="Dias com pico", value=quantidade_dias_picos)

    with col3:
        # Exibir a quantidade de dias seguidos de pico de temperatura
        st.metric(label="Dias seguidos", value=dias_seguidos_picos)

    with col4:
        # Exibir o valor total de dias
        st.metric(label="Total de dias", value=quantidade_dias_inteiro)
    
    with col5:
        # Exibir a quantidade de dias com picos de temperatura
        st.metric(label="", value="")


    # Filtrar os dados para obter as temperaturas médias e desejadas
    temperaturas_medias = granja['Temperatura_Media']
    temperatura_desejada = granja['Temperatura_Desejada']
    datas = granja['Data/Hora']

     # Encontrar os horários de maiores picos na temperatura
    horarios_maiores_picos = datas[temperaturas_medias > temperatura_desejada]
    horarios_maiores_picos.value_counts()
    
    # Título do Gráfico
    st.write("#")
    st.write("<div style='text-align: center;'>Abaixo,👇, destacado em vermelho, podemos observar os picos de temperatura ao longo de todo o Período.</div>", unsafe_allow_html=True)  
    
    # Gráfico Interativo dos picos
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=datas, y=temperaturas_medias, mode='lines', name='Temperatura Média'))
    fig.add_trace(go.Scatter(x=datas, y=temperatura_desejada, mode='lines', name='Temperatura Desejada'))
    fig.add_trace(go.Scatter(x=horarios_maiores_picos, y=temperaturas_medias[temperaturas_medias > temperatura_desejada], mode='markers', marker=dict(color='red'), name='Picos de Temperatura'))
    fig.update_layout(
        title='',
        xaxis_title='Data/Hora',
        yaxis_title='Temperatura',
        width=1200,  # Definir a largura da janela do gráfico
        height=1000,  # Definir a altura da janela do gráfico
        legend=dict(
            orientation="h",  # Orientação horizontal
            yanchor="top",  # Âncora superior
            y=1.1  # Posição vertical
        )
)
    fig.update_xaxes(tickangle=45)

    # Adicionar interatividade para exibir os valores no hover
    fig.update_traces(hovertemplate='Data/Hora: %{x}<br>Temperatura: %{y}')
   
    # Exibir o gráfico interativo no Streamlit sem o menu de interação
    st.plotly_chart(fig, config={'displayModeBar': False})
        
    # Converter a coluna "Data/hora" para o tipo datetime
    granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'])

    # Definir o período da manhã
    inicio_manha = pd.Timestamp("06:00:00")
    fim_manha = pd.Timestamp("11:59:59")

    # Definir o período da Tarde 
    inicio_tarde = pd.Timestamp("12:00:00")
    fim_tarde = pd.Timestamp("17:59:59")

    # Definir o período da Noite
    inicio_noite = pd.Timestamp("18:00:00")
    fim_noite = pd.Timestamp("23:59:59")

    # Definir o período da Madrugada
    inicio_madrugada = pd.Timestamp("00:00:00")
    fim_madrugada = pd.Timestamp("05:59:59")
    
    # Filtrar os dados dentro do período da Manhã
    dados_manha = granja[(granja['Data/Hora'].dt.time >= inicio_manha.time()) & (granja['Data/Hora'].dt.time <= fim_manha.time())]

    # Filtrar os dados dentro do período da Tarde
    dados_tarde = granja[(granja['Data/Hora'].dt.time >= inicio_tarde.time()) & (granja['Data/Hora'].dt.time <= fim_tarde.time())]

    # Filtrar os dados dentro do período da Noite
    dados_noite = granja[(granja['Data/Hora'].dt.time >= inicio_noite.time()) & (granja['Data/Hora'].dt.time <= fim_noite.time())]

    # Filtrar os dados dentro do período da madrugada
    dados_madrugada = granja[(granja['Data/Hora'].dt.time >= inicio_madrugada.time()) & (granja['Data/Hora'].dt.time <= fim_madrugada.time())]

    # Calcular a quantidade de picos no período da Manhã
    quantidade_picos_manha = dados_manha['Temperatura_Desejada'].count()
  
    # Calcular a quantidade de picos no período da Tarde
    quantidade_picos_tarde = dados_tarde['Temperatura_Desejada'].count()
  
    # Calcular a quantidade de picos no período da Noite
    quantidade_picos_noite = dados_noite['Temperatura_Desejada'].count()

    # Calcular a quantidade de picos no período da madrugada
    quantidade_picos_madrugada = dados_madrugada['Temperatura_Desejada'].count()


    # Exibir a quantidade de picos nos períodos
    
    print(f"A quantidade de picos no período da manhã é: {quantidade_picos_manha}")
    print(f"A quantidade de picos no período da tarde é: {quantidade_picos_tarde}")
    print(f"A quantidade de picos no período da noite é: {quantidade_picos_noite}")
    print(f"A quantidade de picos no período da madrugada é: {quantidade_picos_madrugada}")


    # Criar um DataFrame com os resultados
    resultados = pd.DataFrame({
        'Período': ['Madrugada', 'Manhã', 'Tarde', 'Noite'],
        'Quantidade de Picos': [quantidade_picos_madrugada, quantidade_picos_manha, quantidade_picos_tarde, quantidade_picos_noite]
    })

    # Ordenar a tabela em ordem decrescente pela coluna 'Quantidade de Picos'
    resultados = resultados.sort_values(by='Quantidade de Picos', ascending=False)

    # Título
    st.write("#")
    st.write("<div style='text-align: center;'>Abaixo,👇, Resultado dos picos filtrados por período.</div>", unsafe_allow_html=True)  
  
 # Criar o gráfico de barras interativo usando o Plotly
    fig_bar = px.bar(resultados, x='Período', y='Quantidade de Picos', labels={'Quantidade de Picos': 'Quantidade de Picos'}, hover_data=['Quantidade de Picos'])

    # Exibir o gráfico de barras e o gráfico de linha no Streamlit
    st.plotly_chart(fig_bar, config={'displayModeBar': False})

            
    # Converter a coluna 'Data/Hora' em um objeto datetime
    granja['Data/Hora'] = pd.to_datetime(granja['Data/Hora'])

    # Definir a data de início como 16 de agosto
    data_inicio = pd.to_datetime('2023-08-16').date()

    # Adicionar a coluna 'Semana' considerando a data de início
    granja['Semana'] = ((granja['Data/Hora'].dt.date - data_inicio).dt.days // 7)

    # Contar a quantidade de picos em cada semana
    picos_por_semana = granja['Semana'].value_counts()

    # Criar o DataFrame de resultados
    resultados = pd.DataFrame({'Semana': picos_por_semana.index, 'Quantidade de Picos': picos_por_semana.values})

    # Ordenar os resultados por quantidade de picos em ordem decrescente
    picos_por_semana = picos_por_semana.sort_values(ascending=False)

    # Texto
    st.write("#")
    st.write("<div style='text-align: center;'>Abaixo,👇, Resultado dos picos filtrados por Semanas.</div>", unsafe_allow_html=True)  
  
    # Criar o gráfico de barras interativo com o Plotly
    fig_bar = px.bar(resultados, x='Semana', y='Quantidade de Picos', labels={'Quantidade de Picos': 'Quantidade de Picos'}, hover_data=['Quantidade de Picos'])

    # Atualizar o layout do gráfico
    fig_bar.update_layout(title='', xaxis_title='Semana', yaxis_title='Quantidade de Picos')

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_bar, config={'displayModeBar': False})



