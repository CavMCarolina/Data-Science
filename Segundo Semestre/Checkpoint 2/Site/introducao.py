import streamlit as st
import pandas as pd
from sidebar import show_sidebar

st.set_page_config(page_title="Checkpoint 2", layout="wide", page_icon="images/icon2.png")
st.logo("images/icon2.png")

show_sidebar()

# Deixar o arquivo na memória
if "data" not in st.session_state:
    st.session_state["data"] = pd.read_csv("../precipitacao.csv")

df = st.session_state["data"]

st.header("Contextualização do Problema:")

col1, col2, col3 = st.columns([0.5, 0.1, 0.4])
col1.write("Ribeirão Preto, município no interior de São Paulo, tem enfrentado desafios significativos relacionados a alagamentos urbanos decorrentes de chuvas intensas. A análise da relação entre precipitações e alagamentos na cidade é fundamental para compreender os impactos das chuvas e desenvolver estratégias eficazes de mitigação.")

col1.markdown("#### Histórico de Precipitações e Alagamentos")
col1.write("Eventos de chuvas intensas têm causado alagamentos significativos em Ribeirão Preto ao longo dos anos. Em novembro de 2024, por exemplo, a cidade registrou 100 mm de chuva em 24 horas, resultando em alagamentos em diversos pontos, como a Avenida Eduardo Andrea Matarazzo (Via Norte) e bairros como Campos Elíseos e Vila Virgínia . Outro evento marcante ocorreu em dezembro de 2009, quando 94 mm de chuva foram registrados em 12 horas, desalojando 33 pessoas e alagando ruas e casas.​")

col3.image("https://f.i.uol.com.br/fotografia/2023/12/23/17033455656586fd9d396b4_1703345565_3x2_md.jpg")

st.markdown("#### Impactos dos Alagamentos")
st.write("Os alagamentos em Ribeirão Preto resultam em diversos transtornos, incluindo:")
st.markdown("""
    - **Desalojamento de Famílias:** Centenas de famílias já foram obrigadas a deixar suas residências devido às inundações.
    - **Danos à Infraestrutura:** Pontes danificadas, ruas interditadas e prejuízos ao transporte público são consequências frequentes.
    - **Prejuízos Econômicos:** Comércios afetados, veículos danificados e custos elevados para reparos urbanos impactam negativamente a economia local
""")

st.markdown("Importância da Análise de Dados de Precipitação")
st.write("Analisar os dados de precipitação é essencial para:")
st.markdown("""
    - **Previsão de Alagamentos:** Identificar padrões de chuva que precedem inundações permite a emissão de alertas antecipados à população.
    - **Planejamento Urbano:** Compreender a relação entre volume de chuva e áreas afetadas auxilia na implementação de melhorias na infraestrutura de drenagem.​
    - **Definição de Políticas Públicas:**  Dados precisos embasam a criação de políticas de prevenção e resposta a desastres naturais.
""")

st.write("Diante dos desafios impostos pelos alagamentos em Ribeirão Preto, a análise detalhada dos dados de precipitação é uma ferramenta fundamental para a proteção da população e o desenvolvimento sustentável da cidade.")

st.header("Perguntas Iniciais:")
st.write("**1-** Existe uma correlação entre o volume de precipitação e a ocorrência de alagamentos?")
st.write("**2-** Quais são os períodos do ano com maior incidência de chuvas e como isso se relaciona com os alagamentos?")
st.write("**3-** Há uma tendência de aumento ou diminuição das precipitações ao longo dos anos?")
st.write("**4-** Existe um limite mínimo de precipitação a partir do qual os alagamentos começam a ocorrer?")
st.write("**5-** O tempo de duração da chuva influencia a severidade dos alagamentos?")