import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *
from sidebar import show_sidebar
from scipy.stats import norm
import matplotlib.pyplot as plt

st.set_page_config(page_title="Checkpoint 2", layout="wide", page_icon="images/icon2.png")
st.logo("images/icon2.png")

# Função para aplicar o css :)
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

css_file = "scss/style.css"
load_css(css_file)

# Deixar o arquivo na memória
if "data" not in st.session_state:
    st.session_state["data"] = pd.read_csv("../precipitacao.csv")

df = st.session_state["data"]
df.columns = df.columns.str.lower()

# Filtrar o df
colunas_selecionadas = ['x', 'y', 'id', 'nm', 'respon', 'operad', 'dini', 'dfim', 'anoini', 'anofim']

# Adiciona colunas com os padrões especificos
padroes = ['anual', 'jan', 'fev', 'mar','abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'djf', 'mam', 'jja', 'son', 'cwd', 'cdd']
for col in df.columns:
  for padrao in padroes:
    if padrao in col.lower():
      if col not in colunas_selecionadas:
        colunas_selecionadas.append(col)

df_filtrado = df[colunas_selecionadas]

# Pegar apenas os top 10 lugares mais chuvosos do df (top 11 pq tem duas Francas)
top_10_chuvosos = df_filtrado.nlargest(11, 'med_anual').sort_values('med_anual')
df_10 = top_10_chuvosos.sort_values(by='med_anual', ascending=False)

df_10.set_index('nm', inplace=True)
# Retirar uma das Francas
df_10 = df_10.drop('FRANCA  P11-140')

# Formatar selectbox
regioes = {
  'Fazenda Ponta da Serra': 'FAZENDA PONTA DA SERRA',
  'Cristais Paulista': 'CRISTAIS PAULISTA',
  'Fazenda São Jorge': 'FAZENDA SÃO JORGE',
  'Fazenda Floresta': 'FAZENDA FLORESTA',
  'São Joaquim da Barra': 'SÃO JOAQUIM DA BARRA',
  'Nuporanga': 'NUPORANGA - FUMEST',
  'Franca': 'FRANCA',
  'Cruz das Posses': 'CRUZ DAS POSSES',
  'Ipuã': 'IPUÃ',
  'Fazenda Santa Cecília': 'FAZENDA SANTA CECÍLIA'
}

st.subheader("Distribuição Normal da Precipitação Anual:")

st.markdown("""
  A distribuição normal é uma das distribuições de probabilidade mais importantes na estatística. Ela é caracterizada por sua forma simétrica em torno da média, o que significa que a maioria dos dados se concentra em torno desse valor central, com menos dados se afastando dele. A distribuição normal é definida por dois parâmetros principais: a média (μ) e o desvio padrão (σ). <br>
  A média representa o valor central da distribuição, enquanto o desvio padrão indica a dispersão dos dados em relação à média. Em uma distribuição normal, aproximadamente **68%** dos dados estão dentro de um desvio padrão da média, cerca de **95%** estão dentro de dois desvios padrão e cerca de **99,7%** estão dentro de três desvios padrão. Essa propriedade é conhecida como a regra empírica ou regra dos 68-95-99,7.
  
  Utilizamos as variáveis **n_anual**, **med_anual** e **dp_anual** para criar o gráfico da distribuição normal referente a cada região. Com esses parâmetros, foi possível representar visualmente a curva de distribuição dos dados anuais.<br>
  A partir dessa distribuição, conseguimos calcular o limite inferior e o limite superior do intervalo de confiança, considerando um nível de confiança de 95%. Dessa forma, identificamos a faixa na qual esperamos que os valores reais se encontrem na maioria das vezes, com base nos dados disponíveis. Essa abordagem permite uma análise mais precisa e fundamentada sobre o comportamento dos dados em cada região.
""", unsafe_allow_html=True)

st.divider()
coluna_escolhida = st.selectbox("**Escolha uma Região:**", regioes)
regiao = regioes[coluna_escolhida]

# Criacao das variaveis para o gráfico
n = df_10.loc[regiao]['n_anual']
med = df_10.loc[regiao]['med_anual']
dp = df_10.loc[regiao]['dp_anual']
st.subheader(f"Estimativa de μ: {med:.2f}, σ: {dp:.2f}")

x = np.linspace(med - 4*dp, med + 4*dp, 1000)
y = norm.pdf(x, med, dp)

intervalo_68_inf = med - dp
intervalo_68_sup = med + dp

intervalo_997_inf = med - 3 * dp
intervalo_997_sup = med + 3 * dp

# 95% de confianca -> o que quero analisar
limite_inferior = med - 2 * dp
limite_superior = med + 2 * dp

# Criando o gráfico interativo com Plotly
fig = go.Figure()

# Adicionando a curva da distribuição normal
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Distribuição Normal', line=dict(color='red')))

# Adicionando a média
fig.add_trace(go.Scatter(x=[med], y=[norm.pdf(med, med, dp)], mode='markers+text',
                         name='Média (μ)', text=f"μ = {med:.2f}", textposition="top center",
                         marker=dict(color='green', size=10)))

# Adicionando o limite inferior (azul) e o limite superior (laranja)
fig.add_trace(go.Scatter(x=[limite_inferior], y=[norm.pdf(limite_inferior, med, dp)],
                         mode='markers+text', name='Limite Inferior (-2σ)',
                         text=f"-2σ = {limite_inferior:.2f}", textposition="top center",
                         marker=dict(color='blue', size=10)))

fig.add_trace(go.Scatter(x=[limite_superior], y=[norm.pdf(limite_superior, med, dp)],
                         mode='markers+text', name='Limite Superior (+2σ)',
                         text=f"+2σ = {limite_superior:.2f}", textposition="top center",
                         marker=dict(color='orange', size=10)))


# Área sombreada para o intervalo de confiança de 95%
x_conf = np.linspace(limite_inferior, limite_superior, 1000)
y_conf = norm.pdf(x_conf, med, dp)

fig.add_trace(go.Scatter(
    x=np.concatenate([[limite_inferior], x_conf, [limite_superior]]),
    y=np.concatenate([[0], y_conf, [0]]),
    fill='toself',
    fillcolor='rgba(0, 100, 255, 0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo='skip',
    name='Intervalo de Confiança (95%)'
))

# Configurando o layout do gráfico
fig.update_layout(
    title="Distribuição Normal da Precipitação",
    xaxis_title="Precipitação (mm)",
    yaxis_title="Densidade de Probabilidade",
    template="plotly_white"
)

st.plotly_chart(fig)

st.subheader("Análise da Distribuição Normal:")
st.markdown(f"""
Com base na distribuição normal ajustada para a região **{coluna_escolhida}**, podemos concluir que:

- Aproximadamente **68%** dos dados estão entre **{intervalo_68_inf:.2f} mm** e **{intervalo_68_sup:.2f} mm**.
- Aproximadamente **95%** dos dados estão entre **{limite_inferior:.2f} mm** e **{limite_superior:.2f} mm**.
- Aproximadamente **99,7%** dos dados estão entre **{intervalo_997_inf:.2f} mm** e **{intervalo_997_sup:.2f} mm**.

Esses intervalos representam faixas onde é mais provável que os valores reais de precipitação se concentrem, com base na média e na variabilidade dos dados observados.

A distribuição normal é fundamental para o cálculo do intervalo de confiança porque, com ela, sabemos que aproximadamente 95% dos dados estão dentro de dois desvios padrão em relação à média. Por isso, ao usarmos essa distribuição, conseguimos definir com segurança os limites superior e inferior que representam esse intervalo de confiança de 95%.
""")

show_sidebar()