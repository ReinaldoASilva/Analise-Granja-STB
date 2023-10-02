import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import plotly.express as px
from PIL import Image


# Coletando dados
current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
data = current_dir /'smaai.csv'
umidade = pd.read_csv(data)

# Modo responsivo
st.set_page_config(layout="wide")

# Definindo as opções do submenu de Temperatura
submenu_umidade = ['Análise de Umidade', 'Análise por Período', 'Pico de Umidade']
subpagina_selecionada = st.sidebar.radio('Umidade',submenu_umidade)

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


#################################################################### PÁGINA ANÁLISE DE UMIDADE ####################################################################

if subpagina_selecionada == 'Análise de Umidade':

    # Título
    st.markdown("<div style='text-align: center;'>"
            "<h1>Análise de Umidade no Aviário</h1>"
            "</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>"
            "<h5>Manter a Umidade adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.</h5>"
            "</div>", unsafe_allow_html=True) 

    # Converter a coluna Data/Hora em um objeto datetime
    umidade['Data/Hora'] = pd.to_datetime(umidade['Data/Hora'])

    # Excluir a hora da coluna data/hora
    umidade['Data'] = umidade['Data/Hora'].dt.date

    # Criar um slider para selecionar a data/hora
    data_hora_selecionada = st.slider('Selecione a Data', min_value=umidade['Data'].min(), max_value=umidade['Data'].max())

    umidade_desejada = umidade['Umidade_Desejada'].iloc[0]

    # Filtrar os dados com base na data/hora selecionada
    dados_selecionados = umidade[umidade['Data'] == data_hora_selecionada]

    # Obter os valores min, max, medio e desejada da umidade
    umidade_minima = dados_selecionados['Umidade_Media'].min()
    umidade_media = dados_selecionados['Umidade_Media'].mean()
    umidade_maxima = dados_selecionados['Umidade_Media'].max()
    umidade_ideal = dados_selecionados ['Umidade_Desejada'].iloc[0]

    # Calcular a diferença entre as umidades min, max, media e a ideal
    delta_minima =  umidade_minima
    delta_media = umidade_media 
    delta_maxima = umidade_maxima
    delta_ideal = umidade_ideal

    # Criar colunas
    umidade_ideal, umidade_minima, umidade_media, umidade_maxima = st.columns(4)

    with umidade_ideal:
        st.metric(label='Umidade Ideal', value=format(delta_ideal))

    with umidade_minima:
        st.metric(label='Umidade Mínima', value=format(delta_minima))

    with umidade_media:
        st.metric(label='Umidade Média', value=format(delta_media, '.2f'))

    with umidade_maxima:
        st.metric(label='Umidade Máxima', value=format(delta_maxima))

    # Título
    st.write('#')
    st.markdown("<p style='text-align: center;'>No gráfico abaixo 👇 veremos a flutuação da Umidade durante o dia. A linha vermelha é nossa Umidade ideal!</p>", unsafe_allow_html=True)# Gráfico com as temperaturas

    # Gráfico 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados_selecionados['Data/Hora'], y=dados_selecionados['Umidade_Media'], mode='lines', name='Temperatura'))
    fig.add_trace(go.Scatter(x=dados_selecionados['Data/Hora'], y=dados_selecionados['Umidade_Desejada'],mode='lines', name='Umidade Ideal'))
    fig.update_layout(
        title='',
        xaxis_title='Data/Hora',
        yaxis_title="Umidade",
        width=800,
        height=600,
        legend=dict(
            orientation='h',
            yanchor='top',
            y=1.1
        )
    )
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

    #################################################################### PÁGINA ANÁLISE POR PERÍODO ####################################################################

elif subpagina_selecionada == 'Análise por Período':

    # Título
    st.markdown("<div style='text-align: center;'>"
            "<h1>Análise por Período</h1>"
            "</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>"
            "<h5>Aqui você pode fazer a Análise da Umidade por Período.👇</h5>"
            "</div>", unsafe_allow_html=True)       
   
    # Converter a colunadata/hora para dtypes
    umidade['Data/Hora'] = pd.to_datetime(umidade['Data/Hora'])

    # Arredondar os horários para períodos de 3Hs
    umidade['Periodo_Horas'] = umidade['Data/Hora'].dt.floor('3H')

    # Obter lista de dados de data únicos
    datas = umidade['Data/Hora'].dt.date.unique()

    # Converter as datas para string no formato 'YYYY-MM-DD'
    datas_str = [str(data) for data in datas]

    # Selecionar a data
    selecionar_data_str = st.selectbox('Selecione a Data:', datas_str)

    # Converter a data selecionada para o fomrato de data
    selecione_data = pd.to_datetime(selecionar_data_str)

    # Filtrar os dados da data selecionada
    dados_data = umidade[umidade['Data/Hora'].dt.date == selecione_data.date()]

    # Obter o limite de umidade
    limite_umidade = dados_data['Umidade_Desejada'].iloc[0]

    # Filtrar os horários em que a temperatura ultrapassou o limite desejado 
    limite_ultrapassado =  dados_data[dados_data['Umidade_Media'] > limite_umidade]['Data/Hora']

    # Agrupar o limites ultrapassados por periodo de 3H
    limite_agrupado = limite_ultrapassado.dt.floor('3H').dt.time

    # Contar o número de picos de temperatura em cada periodo de 3Hs
    contagem_picos = limite_agrupado.value_counts()

    # Exibir o intervalo de horário com base no periodo de 3hs
    st.markdown("Contagem de Picos de Umidade por Parte do Dia:")
    for horario, count in contagem_picos.items():
        st.markdown(f"{horario} - {count} pico(s)")

    # Exibir parte do dia com nase no horario
    parte_dia = limite_agrupado.apply(lambda x: 'Madrugada' if 0 <= x.hour <6 else 'Manhã' if 6<= x.hour <12 else 'Tarde' if 12 <= x.hour < 18 else 'Noite')
    parte_dia_contagem = parte_dia.value_counts()

    # Exibir a contagem de picos por parte do dia
    st.markdown("Contagens Picos Por Parte Do Dia")
    for parte, count in parte_dia_contagem.items():
        st.markdown(f"{parte}: {count} picos(s)")

    # Título do Gráfico
    st.markdown("<div style='text-align: center;'>"
                "<h5>Aqui você pode ver o gráfico da análise dos períodos.👇</h5>"
                "</div>", unsafe_allow_html=True)   


    # Verificar se há dados disponíveis na parte do dia
    if not parte_dia_contagem.empty:

        # Criar um gráfico de barras interativo para contagem de picos por parte do dia
            fig = px.bar(parte_dia_contagem, x=parte_dia_contagem.index, y=parte_dia_contagem.values, labels={'x': 'Parte do Dia', 'y':'Contagem de Picos'}, title='')
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': ['Manhã', 'Tarde', 'Noite', 'Madrugada']})

        # Exibir o gráfico de barras interativo no Streamlit
            st.plotly_chart(fig, config={'displayModeBar': False})

    else:
        st.markdown("Não há dados disponíveis para a data selecionada.")

#################################################################### PÁGINA PICOS DE TEMPERATURA ####################################################################

# Subpágina
elif subpagina_selecionada == 'Pico de Umidade':
    
    # Título
    st.markdown("<div style='text-align: center;'>"
            "<h1>Picos de Umidade</h1>"
            "</div>", unsafe_allow_html=True)
    st.markdown("<div>"
            "Aqui podemos visualizar a quantidade de dias em que ocorreram picos de Umidade, "
            "bem como a duração dos períodos consecutivos e o total de dias afetados. Essas informações nos "
            "ajudam a compreender a importância de uma gestão mais eficiente do ambiente, visando proporcionar "
            "condições ideais.👇"
            "</div>", unsafe_allow_html=True)

    # Dar espaço
    st.write("#")

    # Filtrar os dados para obter as umidade desejadas e médias
    umidade_media = umidade['Umidade_Media']
    umidade_desejada = umidade['Umidade_Desejada']
    datas = umidade['Data/Hora']

    # Encontrar os horários de maiores picos na umidade
    horarios_maiores_picos = datas[umidade_media > umidade_desejada]

    # Obter as dataas únicas com picos de umidade
    horarios_maiores_picos = pd.to_datetime(horarios_maiores_picos)
    dias_picos_umidade = horarios_maiores_picos.dt.date.unique()

    # Calcular quantidades de dias com pico de umidade
    quantidade_dias_picos = len(dias_picos_umidade)

    # Calcular a quantidade de dias
    umidade['data'] = pd.to_datetime(umidade['Data/Hora'])
    quantidade_dias = umidade['data'].dt.date.nunique()
    quantidade_dias_inteiro = int(quantidade_dias)


    # Determinar quantos dias seguidos de pico de umidade ocorreram
    dias_seguidos_picos_umidade = 0
    for i in range(len(dias_picos_umidade) - 1):
        data_atual = dias_picos_umidade[i]
        data_seguinte = dias_picos_umidade[i + 1]
        if (data_seguinte - data_atual).days == 1:
            dias_seguidos_picos_umidade += 1

    # Criar colunas
    dias_de_pico, dias_seguidos_picos, total_dias_umidade = st.columns(3)
    
    # Adicionar valores nas colunas criadas acima
    with dias_de_pico:
        st.metric(label= 'Dias de pico', value= quantidade_dias_picos)

    with dias_seguidos_picos:
        st.metric(label= ' Dias Seguidos de Pico', value=dias_seguidos_picos_umidade)

    with total_dias_umidade:
        st.metric(label='Total de Dias', value=quantidade_dias_inteiro)


    # Filtrar os dados para obter as umidade médias e desejadas
    umidade_medias = umidade['Umidade_Media']
    umidade_desejada = umidade['Umidade_Desejada']
    datas = umidade['Data/Hora']

    # Encontrar os horários de maiores picos na umidade
    horarios_maiores_picos = datas[ umidade_medias > umidade_desejada]
    horarios_maiores_picos.value_counts()
    
    #Título do Gráfico
    st.write("#")
    st.write("<div style='text-align: center;'>Abaixo,👇, destacado em vermelho, podemos observar os picos de temperatura ao longo de todo o Período.</div>", unsafe_allow_html=True)  

    # Gráfico Interativo dos picos
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=datas, y= umidade_medias, mode='lines', name='Umidade Média'))
    fig.add_trace(go.Scatter(x=datas, y=umidade_desejada, mode='lines', name='Umidade Desejada'))
    fig.add_trace(go.Scatter(x=horarios_maiores_picos, y=umidade_medias[umidade_medias > umidade_desejada], mode='markers', marker=dict(color='red'), name='Picos de Umidade'))
    fig.update_layout(
        title='',
        xaxis_title='Data/Hora',
        yaxis_title='Umidade',
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
    fig.update_traces(hovertemplate='Data/Hora: %{x}<br>Umidade: %{y}')

    # Exibir o gráfico interativo no Streamlit e deixar a barra menu ausente
    st.plotly_chart(fig, config={'displayModeBar': False})
        
    # Converter a coluna "Data/hora" para o tipo datetime
    umidade['Data/Hora'] = pd.to_datetime(umidade['Data/Hora'])

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
    dados_manha = umidade[(umidade['Data/Hora'].dt.time >= inicio_manha.time()) & (umidade['Data/Hora'].dt.time <= fim_manha.time())]

    # Filtrar os dados dentro do período da Tarde
    dados_tarde =umidade[(umidade['Data/Hora'].dt.time >= inicio_tarde.time()) & (umidade['Data/Hora'].dt.time <= fim_tarde.time())]

    # Filtrar os dados dentro do período da Noite
    dados_noite = umidade[(umidade['Data/Hora'].dt.time >= inicio_noite.time()) & (umidade['Data/Hora'].dt.time <= fim_noite.time())]

    # Filtrar os dados dentro do período da madrugada
    dados_madrugada = umidade[(umidade['Data/Hora'].dt.time >= inicio_madrugada.time()) & (umidade['Data/Hora'].dt.time <= fim_madrugada.time())]


    # Calcular a quantidade de picos no período da Manhã
    quantidade_picos_manha = dados_manha['Umidade_Desejada'].count()
  
    # Calcular a quantidade de picos no período da Tarde
    quantidade_picos_tarde = dados_tarde['Umidade_Desejada'].count()
  
    # Calcular a quantidade de picos no período da Noite
    quantidade_picos_noite = dados_noite['Umidade_Desejada'].count()

    # Calcular a quantidade de picos no período da madrugada
    quantidade_picos_madrugada = dados_madrugada['Umidade_Desejada'].count()


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

    # Título do gráfico
    st.write("#")
    st.write("<div style='text-align: center;'>Abaixo,👇, Resultado dos picos filtrados por período.</div>", unsafe_allow_html=True)  
  
 # Criar o gráfico de barras interativo usando o Plotly
    fig_bar = px.bar(resultados, x='Período', y='Quantidade de Picos', labels={'Quantidade de Picos': 'Quantidade de Picos'}, hover_data=['Quantidade de Picos'])

    # Exibir o gráfico de barras e o gráfico de linha no Streamlit
    st.plotly_chart(fig_bar, config={'displayModeBar': False})

    # Converter a coluna 'Data/Hora' em um objeto datetime
    umidade['Data/Hora'] = pd.to_datetime(umidade['Data/Hora'])

    # Definir a data de início como 16 de agosto
    data_inicio = pd.to_datetime('2023-08-16').date()

    # Adicionar a coluna 'Semana' considerando a data de início
    umidade['Semana'] = ((umidade['Data/Hora'].dt.date - data_inicio).dt.days // 7)

    # Contar a quantidade de picos em cada semana
    picos_por_semana = umidade['Semana'].value_counts()

    # Criar o DataFrame de resultados
    resultados = pd.DataFrame({'Semana': picos_por_semana.index, 'Quantidade de Picos': picos_por_semana.values})

    # Ordenar os resultados por quantidade de picos em ordem decrescente
    picos_por_semana = picos_por_semana.sort_values(ascending=False)

    # Título do gráfico
    st.write("#")
    st.write("<div style='text-align: center;'>Abaixo,👇, Resultado dos picos filtrados por Semanas.</div>", unsafe_allow_html=True)  
  
    # Criar o gráfico de barras interativo com o Plotly
    fig_bar = px.bar(resultados, x='Semana', y='Quantidade de Picos', labels={'Quantidade de Picos': 'Quantidade de Picos'}, hover_data=['Quantidade de Picos'])

    # Atualizar o layout do gráfico
    fig_bar.update_layout(title='', xaxis_title='Semana', yaxis_title='Quantidade de Picos')

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig_bar, config={'displayModeBar': False})

















































