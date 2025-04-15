import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Configurações iniciais
sns.set(style="whitegrid")
st.set_page_config(
    page_title="Análise de Renda - Projeto 2",
    page_icon="https://pbs.twimg.com/media/GocDJWSXYAAe-Ya?format=jpg&name=900x900",
    layout="wide"
)

# Carregamento e pré-processamento
df = pd.read_csv(r'C:\Users\Lopes\Downloads\original\projeto 2\input\previsao_de_renda.csv')
df['data_ref'] = pd.to_datetime(df['data_ref'], format='%Y-%m-%d')
df['renda'] /= 1000  # Convertendo para milhares de reais

# Filtro por data
st.markdown("### Selecione o Período de Análise")

escolha_data = st.radio(
    "Método de seleção de tempo:",
    ["Selecionar Intervalo", "Escolher Datas"],
    horizontal=True
)

data_min = df['data_ref'].min()
data_max = df['data_ref'].max()

if escolha_data == "Selecionar Intervalo":
    inicio, fim = st.date_input(
        "Escolha um intervalo de datas:",
        value=(data_min, data_max),
        min_value=data_min,
        max_value=data_max
    )
    df = df[(df['data_ref'] >= pd.to_datetime(inicio)) & (df['data_ref'] <= pd.to_datetime(fim))]
else:
    datas_opcoes = sorted(df['data_ref'].dt.date.unique(), reverse=True)
    datas_escolhidas = st.multiselect("Escolha datas específicas:", datas_opcoes)
    if datas_escolhidas:
        df = df[df['data_ref'].dt.date.isin(datas_escolhidas)]

# PRIMEIRO CONTAINER COM QUATRO GRÁFICOS
with st.container():
    st.markdown("### Análises de Distribuição")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.caption("Distribuição por Gênero")
        graf1 = px.histogram(df, x='sexo', y='renda', color='sexo', title=None)
        graf1.update_layout(yaxis_tickprefix="R$", yaxis_tickformat=".2f", showlegend=False)
        st.plotly_chart(graf1, use_container_width=True)

    with c2:
        st.caption("Distribuição por Estado Civil")
        graf2 = px.histogram(df, x='estado_civil', y='renda', color='estado_civil', title=None)
        graf2.update_layout(yaxis_tickprefix="R$", yaxis_tickformat=".2f", showlegend=False)
        st.plotly_chart(graf2, use_container_width=True)

    with c3:
        st.caption("Quantidade de Pessoas na Residência")
        graf3 = px.violin(df, x='qt_pessoas_residencia', y='renda', color='qt_pessoas_residencia', box=True, title=None)
        graf3.update_layout(yaxis_tickprefix="R$", yaxis_tickformat=".2f", showlegend=False)
        st.plotly_chart(graf3, use_container_width=True)

    with c4:
        st.caption("Renda por Tipo de Renda")
        graf4 = px.bar(df, x='tipo_renda', y='renda', color='tipo_renda', title=None)
        graf4.update_layout(yaxis_tickprefix="R$", yaxis_tickformat=".2f", showlegend=False)
        st.plotly_chart(graf4, use_container_width=True)

# SEGUNDO CONTAINER - RENDA POR IDADE
with st.container():
    st.markdown("### Média de Renda por Idade")

    media_idade = df.groupby('idade')['renda'].mean().reset_index()

    fig_idade = go.Figure(go.Bar(
        x=media_idade['idade'],
        y=media_idade['renda'],
        marker=dict(color='rgba(135, 206, 235, 0.8)'),
        hoverinfo='x+y'
    ))

    fig_idade.update_layout(
        xaxis_title='Idade',
        yaxis_title='Renda Média (mil R$)',
        title="",
        template="simple_white",
        margin=dict(l=20, r=20, t=20, b=20),
        height=400
    )

    st.plotly_chart(fig_idade, use_container_width=True)
