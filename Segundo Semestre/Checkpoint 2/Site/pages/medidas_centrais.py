import streamlit as st
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


show_sidebar()