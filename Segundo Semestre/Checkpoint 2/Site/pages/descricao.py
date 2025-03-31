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

# Função para formatar o df com 2 casas decimais e separador de milhar
def formatar_df(df):
    df_formatado = df.copy()
    
    for coluna in df_formatado.select_dtypes(include=['float64', 'int64']):
        if coluna in ['ANOINI', 'ANOFIM']:  
            df_formatado[coluna] = df_formatado[coluna].astype(str)  # Mantém como string sem formatação
        else:
            df_formatado[coluna] = df_formatado[coluna].apply(
                lambda x: "{:,.2f}".format(x).replace(",", "X").replace(".", ",").replace("X", ".")
            )
    
    return df_formatado

st.header("Descrição do Dataset:")
st.write("O dataset contém dados sobre estações de monitoramento hidrometeorológico na região de Bebedouro e proximidades, incluindo Ribeirão Preto. Ele armazena informações como localização (coordenadas X e Y), nome da estação, responsável pela operação, e diversas estatísticas relacionadas a precipitação.")

df_formatado = formatar_df(df)
st.dataframe(df_formatado)

st.header("Identificação das Variáveis:")
st.write("**X, Y** = Coordenadas geográficas (longitude e latitude).")
st.write("**OBJECTID, ID** = Identificadores internos dos registros.")
st.write("**CD, CDALT** = Códigos que podem estar relacionados a estações meteorológicas.")
st.write("**NM** = Nome da estação meteorológica.")
st.write("**RESPON** = Órgão responsável pela estação (exemplo: DAEE-SP, ANA).")
st.write("**OPERAD** = Operador da estação (quem faz a manutenção e coleta os dados).")
st.write("**MESMAX, MESMIN** = Mês com maior e menor precipitação.")
st.write("**BIMMAX, BIMMIN** = Bimestre com maior e menor precipitação. ")
st.write("**TRIMAX, TRIMIN** = Trimestre com maior e menor precipitação.")
st.write("**QUAMAX, QUAMIN** = Quadrimestre com maior e menor precipitação.")
st.write("**SEMMAX, SEMMIN** = Semestre com maior e menor precipitação.")
# RIO, DINI, DFIM, ANOINI, ANOFIM, EMOPER, ADKM2, PCBRUT, PCCONS, PCFALH, NANOSF, NSF10PF, N_ANUAL, MED_ANUAL, DP_ANUAL, CV_ANUAL, MIN_ANUAL, MAX_ANUAL, N_JAN, MED_JAN.
# VERIFICAR SE MED_ANUAL, MAX_ANUAL ou PCBRUT estão relacionadas à precipitação.
st.write("**X, Y** = ")
st.write("**X, Y** = ")


show_sidebar()