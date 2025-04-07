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
df_formatado = formatar_df(df_filtrado)

st.header("Descrição do Dataset:")
st.write("O dataset contém dados sobre estações de monitoramento hidrometeorológico na região de Bebedouro e proximidades. Ele foi filtrado de maneira que mostra as precipitações anuais, mensais e sazonais de cada estação meteorológica.")

st.dataframe(df_formatado)

st.header("Identificação das Variáveis:")
st.write("**X, Y** = Coordenadas geográficas (longitude e latitude).")
st.write("**ID** = Identificador interno dos registros.")
st.write("**NM** = Nome da estação meteorológica.")
st.write("**Respon** = Órgão responsável pela estação (exemplo: DAEE-SP, ANA).")
st.write("**Operad** = Operador da estação (quem faz a manutenção e coleta os dados).")
st.write("**Dini, Dfim, Anoini, Anofim** = Representa o intervalo em que os dados foram calculados.")
st.write("**DJF** = Indica o verão: Dezembro, Janeiro e Fevereiro.")
st.write("**MAM** = Indica a primavera: Março, Abril e Maio.")
st.write("**JJA** = Indica o inverno: Junho, Julho e Agosto.")
st.write("**SON** = Indica o outono: Setembro, Outubro e Novembro.")
st.write("**CWD** = Dias chuvosos consecutivos.")
st.write("**CDD** = Dias secos consecutivos.")
st.write("**N** = Número de dados válidos dentro daquela categoria. No dataset temos o n de todas as variáveis de precipitação (anual, mensal, sazonal e períodos chuvosos e secos.")
st.write("**Med** = Média daquela categoria. No dataset temos a média de todas as variáveis de precipitação (anual, mensal, sazonal e períodos chuvosos e secos).")
st.write("**DP** = Desvio padrão daquela categoria. No dataset temos o desvio padrão de todas as variáveis de precipitação (anual, mensal, sazonal e períodos chuvosos e secos).")
st.write("**CV** = Coeficiente de variação daquela categoria. No dataset temos o coeficiente de variação de todas as variáveis de precipitação (anual, mensal, sazonal e períodos chuvosos e secos).")
st.write("**Min** = Mínimo daquela categoria. No dataset temos o mínimo de todas as variáveis de precipitação (anual, mensal, sazonal e períodos chuvosos e secos).")
st.write("**Max** = Máximo daquela categoria. No dataset temos o máximo de todas as variáveis de precipitação (anual, mensal, sazonal e períodos chuvosos e secos).")
st.write("**Q25, Q75** = Primeiro e terceiro quartil daquela categoria. No dataset temos o q25 e o q75 das variáveis cwd e cdd (períodos chuvosos e secos).")

show_sidebar()