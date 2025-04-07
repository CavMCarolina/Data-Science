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

show_sidebar()

# Deixar o arquivo na memória
if "data" not in st.session_state:
    st.session_state["data"] = pd.read_csv("../precipitacao.csv")

df = st.session_state["data"]

st.header("Contextualização do Problema:")

col1, col2, col3 = st.columns([0.5, 0.1, 0.4])
col1.write("""A precipitação intensa é um dos principais fatores que contribuem para alagamentos em diversas cidades do interior paulista. Regiões como Ribeirão Preto, São José do Rio Preto, Franca, Barretos, Catanduva e Sertãozinho possuem áreas urbanizadas onde o escoamento da água da chuva é dificultado devido à impermeabilização do solo e à drenagem inadequada. Além disso, municípios menores, como Bebedouro, Monte Alto e Pontal, também podem sofrer com enchentes devido à proximidade com rios e córregos que transbordam durante períodos chuvosos.

Os impactos desses eventos vão desde prejuízos materiais para moradores e comerciantes até danos à infraestrutura urbana, como erosões, rompimento de vias e problemas na mobilidade. A análise da precipitação registrada nas estações meteorológicas dessas regiões pode fornecer informações valiosas sobre a correlação entre chuvas intensas e a ocorrência de alagamentos, permitindo prever riscos e auxiliar no planejamento urbano para mitigar danos futuros.""")

col3.image("https://ogimg.infoglobo.com.br/in/25332675-485-441/FT1086A/96791326_An-aerial-view-shows-a-neighbourhood-during-flooding-caused-by-the-overflowing-Cachoeira-ri.jpg")

st.markdown("#### Impactos dos Alagamentos")
st.write("Os impactos dos alagamentos são amplos e podem incluir:")
st.markdown("""
    - **Desalojamento de Famílias:** Centenas de famílias já foram obrigadas a deixar suas residências devido às inundações.
    - **Danos materiais:** Perdas em residências, comércios e indústrias devido à invasão da água.
    - **Problemas na infraestrutura urbana:** Ruas alagadas, erosão de vias, rompimento de pavimentação e problemas na rede elétrica.
    - **Impactos na mobilidade:** Interrupção de vias e dificuldades no transporte público e privado.
    - **Riscos à saúde pública:** Contaminação da água, proliferação de doenças transmitidas por enchentes (como leptospirose) e aumento da umidade, favorecendo doenças respiratórias.
    - **Prejuízos ao agronegócio:** Perdas de plantações e impactos na produção agrícola, especialmente em regiões com grandes áreas de cultivo.
""")

st.header("Correlação com o Dataset:")
st.write("O dataset contém registros de estações meteorológicas distribuídas por diversas regiões do estado de São Paulo, possibilitando uma análise detalhada da relação entre precipitação e alagamentos. Através dos dados históricos de chuva, é possível:")
st.markdown("""
    - **Previsão de Alagamentos:** Identificar padrões de chuva que precedem inundações permite a emissão de alertas antecipados à população.
    - **Planejamento Urbano:** Compreender a relação entre volume de chuva e áreas afetadas auxilia na implementação de melhorias na infraestrutura de drenagem.​
    - **Definição de Políticas Públicas:** Dados precisos embasam a criação de políticas de prevenção e resposta a desastres naturais.
    - **Identificar padrões climáticos:** Avaliar a frequência e intensidade das chuvas em diferentes períodos do ano.
    - **Auxiliar no planejamento urbano e agrícola:** Fornecer subsídios para políticas públicas e estratégias de mitigação, como melhorias na drenagem urbana e planejamento de plantios agrícolas.       
    - **Apoiar sistemas de alerta precoce:** Criar modelos preditivos para antecipar eventos de alagamento e minimizar danos.
""")

st.header("Perguntas Iniciais:")
st.write("**1-** Quais regiões do dataset apresentam maior ocorrência de precipitação?")
st.write("**2-** Como a instabilidade na precipitação (desvio padrão alto) impacta a frequência de eventos extremos (chuvas longas ou secas)?")
st.write("**3-** Existe um padrão sazonal na incidência de chuvas mais volumosas nas cidades analisadas?")
st.write("**4-** Quais regiões apresentam maior quantidade de dias consecutivos chuvosos e dias consecutivos secos?")
st.write("**5-** Há uma relação entre a estação do ano e a ocorrência de períodos consecutivos de dias chuvosos ou secos?")