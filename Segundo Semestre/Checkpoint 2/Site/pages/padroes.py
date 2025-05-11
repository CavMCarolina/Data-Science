import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sidebar import show_sidebar

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

# Função para formatar o df com 2 casas decimais e separador de milhar
def formatar_df(df):
    df_formatado = df.copy()
    
    for coluna in df_formatado.select_dtypes(include=['float64', 'int64']):
        if coluna in ['anoini', 'anofim']:  
            df_formatado[coluna] = df_formatado[coluna].astype(str)  # Mantém como string sem formatação
        else:
            df_formatado[coluna] = df_formatado[coluna].apply(
                lambda x: "{:,.2f}".format(x).replace(",", "X").replace(".", ",").replace("X", ".")
            )
    
    return df_formatado

# Filtrar o df antes de formatar
colunas_selecionadas = ['x', 'y', 'id', 'nm', 'respon', 'operad', 'dini', 'dfim', 'anoini', 'anofim']

# Adiciona colunas com os padrões especificos
padroes = ['anual', 'jan', 'fev', 'mar','abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'djf', 'mam', 'jja', 'son', 'cwd', 'cdd']
for col in df.columns:
  for padrao in padroes:
    if padrao in col.lower():
      if col not in colunas_selecionadas:
        colunas_selecionadas.append(col)

df_filtrado = df[colunas_selecionadas]
top_10_chuvosos = df_filtrado.nlargest(11, 'med_anual').sort_values('med_anual')
df_10 = top_10_chuvosos.sort_values(by='med_anual', ascending=False)

df_10.set_index('nm', inplace=True)
df_10 = df_10.drop('FRANCA  P11-140')

st.subheader("Padrões Sazonais")

fig = go.Figure()
for index, row in df_10.iterrows():
    meses = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
    medias_mensais = [row[f'med_{mes}'] for mes in meses]
    fig.add_trace(go.Scatter(
        x=meses,
        y=medias_mensais,
        mode='lines+markers',
        name=index
    ))

fig.update_layout(
    title="Médias Mensais de Precipitação para as 10 Regiões Mais Chuvosas",
    xaxis_title="Mês",
    yaxis_title="Média Mensal de Precipitação (mm)",
    hovermode="x unified"
)

st.plotly_chart(fig)

# Supondo que df_10 já esteja definido e contenha as colunas 'med_djf', 'med_mam', 'med_jja', 'med_son'

estacoes = ['djf', 'mam', 'jja', 'son']
fig = go.Figure()

for index, row in df_10.iterrows():
  medias_estacoes = [row[f'med_{estacao}'] for estacao in estacoes]
  fig.add_trace(go.Bar(
      x=estacoes,
      y=medias_estacoes,
      name=index
  ))

fig.update_layout(
    title="Médias Sazonais de Precipitação para as 10 Regiões Mais Chuvosas",
    xaxis_title="Estação do Ano",
    yaxis_title="Média Sazonal de Precipitação (mm)",
    barmode='group' # Agrupa as barras para melhor visualização
)

st.plotly_chart(fig)

show_sidebar()