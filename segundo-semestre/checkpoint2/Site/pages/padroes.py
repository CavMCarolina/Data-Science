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

analise = st.selectbox("Selecione uma Análise:", ["Por Estações", "Por Períodos", "Estações x Períodos"])

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

elif analise == "Por Períodos":
    st.header("Análise de Desvio Padrão:")
    st.markdown("""
        Para investigar a instabilidade da precipitação ao longo do ano, foi analisado o desvio padrão sazonal (DP) das 10 regiões com maior média de chuva. O desvio padrão foi calculado separadamente para cada estação — verão (DJF), outono (MAM), inverno (JJA) e primavera (SON) — permitindo avaliar como a variabilidade da chuva se comporta sazonalmente nas áreas mais úmidas do país.
    """)
    st.subheader("Desvio Padrão Anual para as 10 Regiões Mais Chuvosas:")

    estacoes = ['djf', 'mam', 'jja', 'son']

    fig = go.Figure()

    for index, row in df_10.iterrows():
        medias_estacoes = [row[f'dp_{estacao}'] for estacao in estacoes]
        fig.add_trace(go.Bar(
            x=estacoes,
            y=medias_estacoes,
            name=index
        ))

    fig.update_layout(
        title="Desvios Padrão Sazonais de Precipitação para as 10 Regiões Mais Chuvosas",
        xaxis_title="Estação do Ano",
        yaxis_title="Desvio Padrão Sazonal de Precipitação (mm)",
        barmode='group'  # Agrupa as barras para melhor visualização
    )

    st.plotly_chart(fig)
    st.markdown("""
    A visualização dos DPs sazonais em um gráfico de barras mostra que, mesmo entre as regiões com maior índice pluviométrico, há diferenças importantes na instabilidade das chuvas entre as estações. De modo geral:
    - O verão (DJF) apresenta maior variabilidade, refletindo a natureza intensa e irregular das chuvas nesse período.
    - O inverno (JJA), por outro lado, tende a apresentar menor variabilidade, coerente com a baixa ocorrência de chuvas nessa estação.
    - Outono (MAM) e primavera (SON) ficam em um patamar intermediário, com a primavera mostrando leve aumento na instabilidade — possivelmente em função de sua tendência crescente de chuvas.
    """)

    st.subheader("Correlação entre CWD e CDD e o DP:")

   # Seleciona as colunas para o heatmap e adiciona a coluna de desvio padrão
    colunas_heatmap = ['dp_djf', 'dp_mam', 'dp_jja', 'dp_son', 'med_cwd', 'med_cdd']
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
    Com base na média dos DPs sazonais dessas 10 regiões, foi construído um heatmap de correlação entre os desvios padrão e as médias sazonais de CWD (dias consecutivos chuvosos) e CDD (dias consecutivos secos). A análise revelou:
    - Outono (dp_mam) com correlação moderada positiva (0.32) com CWD: maior instabilidade se associa a mais dias seguidos de chuva.
    - Inverno (dp_jja) com correlação negativa moderada (-0.32) com CDD: quanto menor a variabilidade, mais prolongados tendem a ser os períodos secos.
    - As demais estações apresentam correlações fracas ou quase nulas, indicando uma relação menos evidente entre a instabilidade da precipitação e os extremos nesses períodos.
    """)

    st.subheader("Resultado da Análise de DP:")
    st.markdown("""
    A análise dos desvios padrão sazonais nas regiões mais chuvosas reforça a ideia de que a variabilidade da precipitação varia com a estação do ano e está parcialmente relacionada à ocorrência de eventos extremos como chuvas contínuas ou longos períodos secos. Essa abordagem permite identificar estações críticas para planejamento e adaptação a extremos climáticos, especialmente em regiões com histórico elevado de chuva.
    """)

    st.divider() 

    st.header("Análise de Média:")
    st.markdown("""
    Ao analisar as 10 estações mais chuvosas do dataset, esperava-se encontrar um padrão claro de frequentes dias consecutivos de chuva, dado que essas regiões costumam registrar alagamentos e eventos extremos relacionados à alta precipitação. Para investigar isso, foi construído um gráfico de barras com as médias de dias consecutivos chuvosos (med_cwd) e secos (med_cdd) dessas estações.
    """)

    st.subheader("Média de Cwd e CDD para as 10 Regiões mais Chuvosas:")
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

    st.markdown("""
    Mesmo entre as estações com maior volume médio de precipitação, a média de dias consecutivos secos (med_cdd) foi significativamente maior do que a média de dias consecutivos chuvosos (med_cwd). Ou seja, mesmo em regiões que alagam com frequência, predominam os períodos mais longos de seca do que de chuva contínua.
                
    Esse comportamento, à primeira vista contraditório, pode ser explicado por dois fatores principais:
    - Chuvas intensas concentradas em poucos dias: Regiões com tendência a alagamentos frequentemente sofrem com eventos de chuva muito intensa em um curto período, em vez de chuvas constantes e duradouras. Assim, mesmo com um baixo número de dias consecutivos chuvosos, o volume total acumulado pode ser elevado o suficiente para causar impactos severos.
    - Distribuição irregular das chuvas: Essas áreas podem apresentar um padrão de distribuição de precipitação bastante instável, com alternância entre dias secos e eventos extremos de chuva. Isso é coerente com uma alta variabilidade climática, frequentemente observada em regiões tropicais ou com influência de fenômenos como a ZCIT ou El Niño.
    """)

    st.subheader("Resultado da Análise de Média:")
    st.markdown("""
    A análise evidencia que, mesmo em regiões muito chuvosas, os dias de chuva não necessariamente ocorrem de forma contínua. Pelo contrário, são intercalados com períodos secos mais longos, mas quando a chuva ocorre, ela é intensa o suficiente para gerar alagamentos e extremos climáticos. Essa informação é valiosa para o planejamento urbano e a gestão de riscos, pois mostra que não é apenas a frequência de chuva que importa, mas também sua intensidade e distribuição no tempo.
                
    - Estação com maior média de dias consecutivos chuvosos: **São Joaquim da Barra** (med_cwd = 2.5)
    - Estação com maior média de dias consecutivos secos: **Fazenda Floresta** (med_cdd = 17.25)
    
    - Estação com menor média de dias consecutivos chuvosos: **Fazenda Floresta** (med_cwd = 7.6)
    - Estação com menor média de dias consecutivos secos: **Franca** (med_cdd = 43.15)
    """)

else:
    st.header("Correlação das Médias de Estações e de Períodos:")

    st.markdown("""
    O heatmap de correlação entre as médias sazonais de precipitação (DJF, MAM, JJA, SON) e as médias de períodos consecutivos chuvosos (med_cwd) e secos (med_cdd) revela padrões importantes sobre o comportamento climático das regiões analisadas.

    Observamos que a med_cwd (média de dias consecutivos chuvosos) apresenta correlações positivas com todas as estações do ano, especialmente com o verão (DJF: R = 0,67) e a primavera (SON: R = 0,56), indicando que essas estações, por serem mais chuvosas, tendem a concentrar mais dias seguidos de chuva. Já no inverno (JJA: R = 0,05), essa relação é praticamente inexistente, o que é coerente com o fato de ser a estação menos chuvosa do ano.

    Por outro lado, a med_cdd (média de dias consecutivos secos) tem correlações negativas com todas as estações, sendo a mais forte com o inverno (JJA: R = -0,57), seguido do outono (MAM: R = -0,43) e primavera (SON: R = -0,37). Isso mostra que, quanto mais chuvosa a estação, menor a tendência de longos períodos secos, o que reforça a lógica esperada de que estações com maior volume de chuva têm menor ocorrência de secas prolongadas.

    A correlação entre med_cdd e med_cwd é levemente negativa (R = -0,12), indicando que, embora não fortemente, existe uma tendência de que regiões com mais dias chuvosos consecutivos tenham menos dias secos consecutivos — uma relação esperada, mas que varia conforme o regime climático local.

    Essas correlações ajudam a entender como a distribuição da precipitação ao longo do ano influencia a frequência e duração de eventos extremos, como secas ou chuvas prolongadas.
    """)

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