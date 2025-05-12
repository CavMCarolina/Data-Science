import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Dados",
    page_icon="🏃🏼",
    layout="wide"
)

df = st.session_state["data"]

tipos='Todos'
tipos = np.append(tipos,df["Post type"].unique())
tipo = st.sidebar.selectbox("Tipo de Post", tipos)
st.sidebar.markdown("Desenvolvido por Prof. Tiago Marum [THM Estatística](https://thmestatistica.com)")

if tipo == 'Todos':
    df_filtered = df
else:
    df_filtered = df[(df["Post type"]==tipo)]

#df_filtered
st.dataframe(df_filtered,
             column_config={
                 "Likes": st.column_config.ProgressColumn(
                     "Likes", format="%f", min_value=0, max_value=int(df_filtered["Likes"].max()))
                 })