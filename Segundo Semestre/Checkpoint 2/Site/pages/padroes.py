import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
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

st.header("Padrões Sazonais:")
st.markdown("""
    Padrões sazonais são variações regulares que ocorrem em determinados períodos do ano, geralmente associadas a fatores climáticos, como estações do ano, ciclos de temperatura, vento, umidade e, principalmente, chuvas. Em séries temporais, esses padrões se repetem em intervalos previsíveis, o que os diferencia de tendências de longo prazo ou variações aleatórias.

    No contexto de dados de precipitação, identificar e compreender os padrões sazonais é essencial por diversas razões. Primeiramente, a distribuição de chuvas ao longo do ano tem impacto direto em áreas como agricultura, gestão de recursos hídricos, planejamento urbano e prevenção de desastres naturais, como enchentes e secas. Por exemplo, o plantio de determinadas culturas agrícolas depende do conhecimento das épocas mais e menos chuvosas para garantir produtividade e evitar perdas.

    Além disso, ao analisar séries temporais de precipitação, o reconhecimento de padrões sazonais permite separar flutuações esperadas (naturais do ciclo climático) de mudanças anômalas ou tendências de longo prazo. Isso é particularmente importante em estudos de mudanças climáticas, pois a detecção de uma tendência significativa (como aumento ou diminuição da precipitação ao longo dos anos) só pode ser confiável se a sazonalidade for devidamente compreendida e isolada da análise.

    Portanto, a análise da sazonalidade não apenas enriquece a interpretação dos dados de precipitação, como também contribui para uma tomada de decisão mais informada em diversas áreas dependentes do regime de chuvas. Os gráficos a seguir mostram os padrões sazonais de precipitação para as 10 regiões mais chuvosas do Brasil. As médias mensais e sazonais são apresentadas, permitindo uma análise detalhada das variações de precipitação ao longo do ano.
""")

analise = st.selectbox("Selecione uma Análise:", ["Por Estações", "Por Perídos", "Estações x Períodos"])

st.divider()

if analise == "Por Estações":
    st.subheader("Padrão Anual para as 10 Regiões Mais Chuvosas:")
    # Grafico de linhas para médias mensais
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

    st.markdown("""
        Ao analisar o gráfico acima, é possível perceber que todas apresentam um mesmo padrão sazonal ao longo do ano. Esse padrão se organiza de forma coerente com as estações do ano:

        - Verão (dezembro a fevereiro): é o período com maior volume de chuvas. Em todas as estações, os meses de verão apresentam picos de precipitação, caracterizando uma estação chuvosa. Essa concentração de chuvas é comum em muitas regiões do Brasil, principalmente nas áreas de clima tropical, devido à maior incidência solar e à intensificação de fenômenos como a Zona de Convergência do Atlântico Sul (ZCAS).

        - Outono (março a maio): observa-se uma tendência decrescente nas chuvas. Os valores mensais começam a cair gradualmente em todas as estações, indicando a transição do período chuvoso para o seco.

        - Inverno (junho a agosto): é a estação mais seca do ano. Os dados mostram que, de forma consistente, o volume de precipitação atinge seus valores mais baixos nesse período em todas as estações analisadas. Esse comportamento está associado à redução da umidade atmosférica e à presença de massas de ar mais seco.

        - Primavera (setembro a novembro): há uma tendência crescente nas chuvas, marcando o início do retorno do período úmido. Os registros mostram aumento gradual da precipitação, especialmente nos meses de outubro e novembro.

        A regularidade desse comportamento entre todas as estações permite dividir os dados em blocos sazonais — verão, outono, inverno e primavera — para análises estatísticas mais específicas, como o cálculo de médias sazonais e correlações dentro e entre as estações.
    """)

    st.divider()

    st.subheader("Médias Sazonais por Estação para as 10 Regiões Mais Chuvosas:")

    # Gráfico de barras para médias sazonais
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

    st.markdown("""
        Ao segmentar os dados de precipitação por estações do ano — verão, outono, inverno e primavera — e calcular as médias das 10 estações mais chuvosas em cada período, é possível identificar claramente um padrão sazonal.

        - Verão se destaca como a estação com maiores volumes médios de precipitação entre as regiões mais chuvosas. Isso reforça a característica já esperada do verão brasileiro, associado a temperaturas elevadas e maior ocorrência de chuvas intensas e frequentes, muitas vezes convectivas.

        - Inverno, por outro lado, apresenta as menores médias de precipitação entre as 10 estações mais chuvosas desse período, demonstrando que mesmo as regiões mais úmidas tendem a registrar baixos volumes de chuva nesse trimestre.

        - Primavera mostra uma média de chuva ligeiramente superior à do outono, o que pode estar relacionado às tendências opostas observadas nessas estações: enquanto o outono apresenta uma tendência decrescente de chuvas ao longo dos meses, a primavera apresenta uma tendência crescente, preparando o ambiente para o retorno das chuvas intensas do verão.
    """)

elif analise == "Por Perídos":
    st.subheader("Padrão Anual para as 10 Regiões Mais Chuvosas:")

   # Seleciona as colunas para o heatmap e adiciona a coluna de desvio padrão
    colunas_heatmap = ['dp_djf', 'dp_mam', 'dp_jja', 'dp_son', 'med_cwd', 'med_cdd', 'dp_anual']
    df_heatmap = df_filtrado[colunas_heatmap]

    # Calcula a matriz de correlação
    correlation_matrix = df_heatmap.corr()

    # Cria o heatmap com Plotly Figure Factory para exibir os valores de r
    fig = ff.create_annotated_heatmap(correlation_matrix.values.tolist(),
                                    x=colunas_heatmap,
                                    y=colunas_heatmap,
                                    annotation_text=np.around(correlation_matrix.values, decimals=2).tolist(),  # Arredonda para 2 casas decimais
                                    colorscale='RdBu')

    # Personalize a aparência do heatmap
    for i in range(len(fig.layout.annotations)):
        annotation = fig.layout.annotations[i]
        if float(annotation.text) != 1:
            annotation.font.color = 'black'

    fig.update_layout(
        title='Heatmap de Correlação entre as médias e o Desvio Padrão da Precipitação',
        width=800,
        height=600,
        xaxis_title="Variáveis",
        yaxis_title="Variáveis"
    )   
    
    st.plotly_chart(fig)

    st.markdown("""

    """)

    st.subheader("Correlação de CWD e CDD com o DP:")
    fig = go.Figure()

    for region in df_10.index:
        fig.add_trace(go.Bar(
            x=['Dias Consecutivos Chuvosos (CWD)', 'Dias Consecutivos Secos (CDD)'],
            y=[df_10.loc[region, 'med_cwd'], df_10.loc[region, 'med_cdd']],
            name=region
        ))

    fig.update_layout(
        title="Dias Consecutivos Chuvosos e Secos para as 10 Regiões Mais Chuvosas",
        xaxis_title="Tipo de Dia",
        yaxis_title="Média",
        barmode='group'
    )

    st.plotly_chart(fig)

else:
    # Heatmap de correlação
    colunas_heatmap = ['med_djf', 'med_mam', 'med_jja', 'med_son', 'med_cwd', 'med_cdd']
    df_heatmap = df_filtrado[colunas_heatmap]

    # Calcula a matriz de correlação
    correlation_matrix = df_heatmap.corr()

    # Cria o heatmap com Plotly Figure Factory para exibir os valores de r
    fig = ff.create_annotated_heatmap(correlation_matrix.values.tolist(),
                                    x=colunas_heatmap,
                                    y=colunas_heatmap,
                                    annotation_text=np.around(correlation_matrix.values, decimals=2).tolist(), # Arredonda para 2 casas decimais
                                    colorscale='Viridis')

    fig.update_layout(
        title='Heatmap de Correlação entre as médias',
        width=800,  # Ajuste a largura conforme necessário
        height=600, # Ajuste a altura conforme necessário
        xaxis_title="Variáveis",
        yaxis_title="Variáveis"
    )

    st.plotly_chart(fig)

show_sidebar()