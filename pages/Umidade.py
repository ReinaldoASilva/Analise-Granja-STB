import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


umidade = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx')
smaai_leituras_atualizado.xlsx
try:
    st.write('Trying with back slashes')
    st.dataframe(pd.read_sxls(r'.\\files\\smaai_leituras_atualizado.xlsx'))
except:
    st.write('It didn\'t work with back slashes.')


submenu_umidade = ['Análise de Umidade', 'Análise por Período', 'Pico de Umidade']
subpagina_selecionada = st.sidebar.radio('Umidade',submenu_umidade)

#################################################################### PÁGINA ANÁLISE DE UMIDADE ####################################################################

if subpagina_selecionada == 'Análise de Umidade':


    st.title('Análise de Umidade no Aviário')

    st.write("Manter a temperatura adequada no aviário é essencial para promover o bem-estar, otimizar o desempenho, controlar a reprodução, prevenir doenças e obter melhores resultados econômicos na criação de aves.")

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

    # Gráfico com as temperaturas

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

    st.write = ' Nesse momento teremos uma visão mais ampla sobrea situação\
        do aviário, analisando a umidade por dia, o que nos da uma visão\
        mais completa.'

    # Se o gráfico não tiver dados na abertura é para reconhecer esse caminho
    if 'umidade' not in locals():
        umidade = pd.read_excel('/Users/reinaldoblack/Documents/documentos/Sitio-Balão/Analise-Granja-STB/smaai_leituras_atualizado.xlsx')

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

    # Verificar se há dados disponíveis na parte do dia
    if not parte_dia_contagem.empty:

        # Criar um gráfico de barras interativo para contagem de picos por parte do dia
            fig = px.bar(parte_dia_contagem, x=parte_dia_contagem.index, y=parte_dia_contagem.values, labels={'x': 'Parte do Dia', 'y':'Contagem de Picos'}, title='')
            fig.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': ['Manhã', 'Tarde', 'Noite', 'Madrugada']})

        # Exibir o gráfico de barras interativo no Streamlit
            st.plotly_chart(fig)

    else:
        st.markdown("Não há dados disponíveis para a data selecionada.")



















































