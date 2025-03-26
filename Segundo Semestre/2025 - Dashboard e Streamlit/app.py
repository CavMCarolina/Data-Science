# pip install streamlit
# pip install pandas
# pip install openpyxl
# streamlit run app.py (terminal)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Dashboard do Instagram") # Marketing Analytics
st.text("Esse Dashboard resume os dados das campanhas de marketing para melhores tomadas de decisões")

uploaded_file = st.file_uploader("Carregue aqui seu arquivo")

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write(df.describe())

    st.header("Banco de Dados")
    st.write(df.head())

    fig, ax = plt.subplots(1, 1)
    ax. scatter(x = df['Reach'], y = df['Likes'])
    ax.set_xlabel('Alcancse')
    ax. set_ylabel('Curtidas')

    st.pyplot(fig)