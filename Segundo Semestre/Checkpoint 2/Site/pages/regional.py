import streamlit as st
import plotly.express as px
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