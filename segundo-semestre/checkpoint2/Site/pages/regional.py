import streamlit as st
import plotly.express as px
import pandas as pd
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

colunas_selecionadas = ['x', 'y', 'id', 'cdalt', 'nm', 'respon', 'operad', 'dini', 'dfim', 'anoini', 'anofim']

# Adiciona colunas com os padrões especificados
padroes = ['anual', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'djf', 'mam', 'jja', 'son', 'cwd', 'cdd', 'sdii']
for col in df.columns:
  for padrao in padroes:
    if padrao in col.lower():
      if col not in colunas_selecionadas:
        colunas_selecionadas.append(col)

# Filtra o DataFrame com as colunas selecionadas
df_filtrado = df[colunas_selecionadas]

top_10_chuvosos = df_filtrado.nlargest(11, 'med_anual').sort_values('med_anual')
df_10 = top_10_chuvosos.sort_values(by='med_anual', ascending=False)

df_10.set_index('nm', inplace=True)
df_10 = df_10.drop('FRANCA  P11-140')

st.header("Análise Regional da Precipitação")

st.markdown("""
    A análise regional da precipitação é fundamental para entender como as chuvas variam em diferentes áreas e como essas variações podem impactar a vida das pessoas e o meio ambiente. Os gráficos regionais construídos mostram a distribuição espacial das estações pluviométricas analisadas, com destaque para a média anual de precipitação de cada uma.
    Ao utilizar a média anual como critério de cor, conseguimos perceber que determinadas regiões do país se destacam por seus elevados índices pluviométricos, o que pode estar relacionado a fatores climáticos locais, como umidade, altitude e presença de massas de ar úmidas. Essa análise espacial é essencial para entender a dinâmica da chuva no território analisado e pode auxiliar na gestão de recursos hídricos e prevenção de desastres naturais.
    
    O primeiro gráfico apresenta todas as estações do dataset, permitindo uma visão geral da precipitação em diferentes áreas geográficas. Já o segundo gráfico foca nas 10 estações mais chuvosas, destacando regiões com alta concentração de chuva. Essa abordagem facilita a identificação de padrões regionais, como áreas propensas a alagamentos, e também permite comparar a intensidade da precipitação entre diferentes locais.
""")

# Criando o gráfico com Plotly Express
fig = px.scatter_mapbox(df_filtrado, lat="y", lon="x", color="med_anual", size="med_anual",
                        color_continuous_scale=px.colors.sequential.Viridis, size_max=15, zoom=5,
                        mapbox_style="carto-positron", hover_name="nm", hover_data=["med_anual"])

fig.update_layout(
    title="Precipitação Anual por Região",
    margin={"r":0,"t":50,"l":0,"b":0},
    geo = dict(
        projection_scale=1
    )
)

st.plotly_chart(fig, use_container_width=True)

# Criando o gráfico com Plotly Express para as 10 regiões mais chuvosas
fig = px.scatter_mapbox(df_10, lat="y", lon="x", color="med_anual", size="med_anual",
                        color_continuous_scale=px.colors.sequential.Viridis, size_max=15, zoom=5,
                        mapbox_style="carto-positron", hover_name=df_10.index, hover_data=["med_anual"])

fig.update_layout(
    title="10 Regiões Mais Chuvosas",
    margin={"r":0,"t":50,"l":0,"b":0},
    geo = dict(
        projection_scale=1
    )
)

st.plotly_chart(fig, use_container_width=True)

show_sidebar()