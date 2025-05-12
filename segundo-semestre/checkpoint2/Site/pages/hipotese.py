import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import ttest_ind
from sidebar import show_sidebar
from geopy import distance
import numpy as np
import plotly.graph_objects as go
from pymannkendall import original_test

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

# Filtrar o df antes de formatar
colunas_selecionadas = ['x', 'y', 'id', 'nm', 'respon', 'operad', 'dini', 'dfim', 'anoini', 'anofim']

padroes = ['anual', 'jan', 'fev', 'mar','abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez', 'djf', 'mam', 'jja', 'son', 'cwd', 'cdd']
for col in df.columns:
    for padrao in padroes:
        if padrao in col.lower():
            if col not in colunas_selecionadas:
                colunas_selecionadas.append(col)

df_filtrado = df[colunas_selecionadas]

st.header("Teste de Hipóteses:")
st.markdown("""
Um teste de hipótese é um procedimento estatístico usado para avaliar suposições sobre uma população com base em uma amostra de dados. Com ele, podemos verificar se duas ou mais amostras apresentam diferenças estatísticas reais, ou se essas diferenças podem ter ocorrido por acaso.

- A **hipótese nula (H0)** é a suposição de que não há diferença significativa.
- A **hipótese alternativa (H1)** propõe que existe uma diferença estatisticamente significativa.

A interpretação depende do **valor de p (p-valor)**, que indica a probabilidade de observarmos os dados obtidos assumindo que a hipótese nula é verdadeira:

- Se **p > 0.05**, não rejeitamos H0 (diferença pode ser por acaso).
- Se **p <= 0.05**, rejeitamos H0 (diferença é estatisticamente significativa).
""")

st.header("Nível de Significância:")
st.markdown("""
    O nível de significância (α) representa a probabilidade máxima de cometer um erro do tipo I, ou seja, rejeitar H₀ quando ela é verdadeira. O valor mais comum para α é 0,05, o que significa que aceitamos uma chance de 5% de cometer esse erro. Isso implica que, se o p-valor for menor ou igual a 0,05, rejeitamos a hipótese nula e consideramos que há evidências suficientes para apoiar a hipótese alternativa.
""")

st.divider()

teste = st.selectbox("Selecione um teste:", ["Teste T de Student", "Teste S de Mann-Kendall"])

# Função para calcular a distância
def calcular_distancia(df, referencia):
    return df.apply(lambda row: distance.distance((row["y"], row["x"]), referencia).km, axis=1)


if teste == "Teste T de Student":
    st.header("Teste T de Student:")
    st.markdown("""
    O Teste T de Student é uma técnica estatística utilizada para comparar as médias de dois grupos e verificar se há uma diferença significativa entre elas. Ele parte da hipótese de que não existe diferença real nas médias (hipótese nula) e calcula a probabilidade de observarmos uma diferença tão grande quanto a encontrada apenas por acaso. Essa probabilidade é representada pelo valor de p. Quando o p-valor é menor ou igual ao nível de significância adotado (geralmente 0,05), rejeita-se a hipótese nula e conclui-se que as médias dos grupos são significativamente diferentes. Esse teste é bastante útil quando se tem dados que seguem uma distribuição aproximadamente normal.
    """)
    
    st.divider()

    st.subheader("Hipóteses do Estudo:")
    st.markdown("""
    **Hipótese Nula (H0):** As estações mais próximas da estação mais chuvosa não apresentam diferença significativa na média de precipitação anual em comparação às estações mais distantes.
    <br>
    **Hipótese Alternativa (H1):** As estações mais próximas da estação mais chuvosa apresentam diferença significativa na média de precipitação anual em relação às estações mais distantes.
    """, unsafe_allow_html=True)

    # Variaveis para o teste
    mais_chuvosa = df_filtrado.sort_values("med_anual", ascending=False).iloc[0]
    estacao_mais_chuvosa = df_filtrado[df_filtrado["nm"] == mais_chuvosa["nm"]]
    outros = df_filtrado[df_filtrado["nm"] != mais_chuvosa["nm"]]

    # Calcular distâncias para a estação mais chuvosa
    outros = outros.copy()
    referencia_chuvosa = (mais_chuvosa["y"], mais_chuvosa["x"])
    outros["distancia"] = calcular_distancia(outros, referencia_chuvosa)

    # Dividir em dois grupos: mais próximos e mais distantes
    outros_ordenado = outros.sort_values("distancia")
    meio = len(outros_ordenado) // 2
    grupo_proximas, grupo_distantes = outros_ordenado.iloc[:meio], outros_ordenado.iloc[meio:]

    # Teste T de Student e p_valor
    t_stat, p_valor = ttest_ind(grupo_proximas["med_anual"], grupo_distantes["med_anual"], equal_var=False)

    # Adicionando grupo para visualização
    grupo_proximas["grupo"], grupo_distantes["grupo"] = "Mais próximas", "Mais distantes"
    df_visual = pd.concat([grupo_proximas, grupo_distantes])

    # Boxplot comparando os grupos
    fig = px.box(
        df_visual,
        x="grupo",
        y="med_anual",
        points="all",
        color="grupo",
        title="Comparação da Precipitação Anual entre Estações Mais Próximas e Mais Distantes",
        labels={"med_anual": "Precipitação Anual (mm)", "grupo": "Grupo de Estações"}
    )
    st.plotly_chart(fig, use_container_width=True)

    # Calcular distância para a estação mais próxima e mais distante
    outros["distancia_km"] = calcular_distancia(outros, referencia_chuvosa)

    # Selecionar a estação mais próxima e mais distante
    mais_proxima, mais_distante = outros.loc[outros["distancia_km"].idxmin()], outros.loc[outros["distancia_km"].idxmax()]

    # DataFrames individuais com rótulos para visualização
    mais_proxima_df = pd.DataFrame([mais_proxima]).assign(grupo="Mais próxima")
    mais_distante_df = pd.DataFrame([mais_distante]).assign(grupo="Mais distante")
    estacao_mais_chuvosa["grupo"] = "Mais chuvosa"

    # Juntar todos em um único DataFrame
    df_visual = pd.concat([estacao_mais_chuvosa, mais_proxima_df, mais_distante_df])

    # Gráfico de barras comparando as estações
    fig = px.bar(
        df_visual,
        x="grupo",
        y="med_anual",
        color="grupo",
        text="med_anual",
        title="Comparação de Precipitação Anual",
        labels={"med_anual": "Precipitação Anual (mm)", "grupo": "Estação"}
    )
    fig.update_traces(texttemplate='%{text:.2f} mm', textposition='outside')
    fig.update_layout(showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)

    # Resultados do teste
    st.subheader("Resultado do Teste:")
    st.markdown(f"""
    **Conclusão:**  
    {"Rejeitamos" if p_valor <= 0.05 else "Não rejeitamos"} a hipótese nula ao nível de significância de 5%.  
    As médias de precipitação anual das estações mais próximas e das mais distantes {"são significativamente diferentes." if p_valor <= 0.05 else "não apresentam diferença estatisticamente significativa."} Inclusive, pode-se dizer que as estações mais distantes têm médias de precipitação anual menores em comparação com as mais próximas.

    **Grupos Comparados:**
    - {len(grupo_proximas)} estações mais próximas
    - {len(grupo_distantes)} estações mais distantes

    **Resultado do Teste T:**
    - Estatística t: {t_stat:.2f}
    - Valor p: {p_valor:.4f}
    """)

else:
    st.header("Teste S de Mann-Kendall:")
    st.markdown("""
    O Teste de Mann-Kendall é um teste estatístico não paramétrico amplamente utilizado para identificar a presença de tendências em séries temporais, como dados climáticos ao longo dos anos. Ele verifica se há uma tendência monotônica (ou seja, que só aumenta ou só diminui) sem exigir que os dados sigam uma distribuição específica. Através da comparação entre pares de valores ao longo do tempo, o teste estima se há um padrão de crescimento ou declínio consistente. Se o p-valor do teste for inferior ao nível de significância (por exemplo, 0,05), considera-se que a tendência é estatisticamente significativa. É uma ferramenta valiosa em estudos ambientais, especialmente para detectar mudanças de longo prazo.
    """)

    st.divider()

    st.subheader("Hipóteses do Estudo:")
    st.markdown("""
    **Hipótese Nula (H0):** Não há variação significativa na precipitação entre os meses de junho e julho nas regiões: mais chuvosa, mais próxima e mais distante da primeira.
    <br>
    **Hipótese Alternativa (H1):** Há variação significativa na precipitação entre os meses de junho e julho nas regiões: mais chuvosa, mais próxima e mais distante da primeira.
    """, unsafe_allow_html=True)

    # Encontre a estação mais chuvosa
    estacao_mais_chuvosa = df_filtrado.loc[df_filtrado['med_anual'].idxmax()]

    # Calcule as distâncias entre a estação mais chuvosa e as demais
    distances = []
    for index, row in df_filtrado.iterrows():
        distance = np.sqrt((row['x'] - estacao_mais_chuvosa['x'])**2 + (row['y'] - estacao_mais_chuvosa['y'])**2)
        distances.append(distance)

    df_filtrado['distance'] = distances

    # Encontre a estação mais próxima
    segunda_mais_proxima = df_filtrado.sort_values(by='distance').iloc[1]

    # Encontre a estação mais distante
    mais_distante = df_filtrado.sort_values(by='distance').iloc[-1]

    st.write(f"Estação mais chuvosa: {estacao_mais_chuvosa['nm']}")
    st.write(f"Estação mais próxima da mais chuvosa: {segunda_mais_proxima['nm']}")
    st.write(f"Estação mais distante da mais chuvosa: {mais_distante['nm']}")

    # combinar as estações em um grupo
    stations = [estacao_mais_chuvosa['nm'], segunda_mais_proxima['nm'], mais_distante['nm']]
    station_data = df_filtrado[df_filtrado['nm'].isin(stations)]

    # Criando gráfico de barras para comparação
    fig = go.Figure()

    for station in stations:
        station_df = station_data[station_data['nm'] == station]
        fig.add_trace(go.Bar(
            x=['Junho', 'Julho'],
            y=[station_df['med_jun'].iloc[0], station_df['med_jul'].iloc[0]],
            name=station
        ))

    fig.update_layout(
        title="Comparação das médias de precipitação em Junho e Julho",
        xaxis_title="Mês",
        yaxis_title="Média de precipitação (mm)",
        barmode='group'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Criando Teste S de Mann-Kendall
    jun_data = []
    jul_data = []
    for station in stations:
        station_df = station_data[station_data['nm'] == station]
        jun_data.append(station_df['med_jun'].iloc[0])
        jul_data.append(station_df['med_jul'].iloc[0])

    # Combine os dados de junho e julho em uma única lista
    combined_data = []
    for i in range(len(stations)):
        combined_data.append(jun_data[i])
        combined_data.append(jul_data[i])

    # Resultado do teste com os dados combinados
    result = original_test(combined_data)

    st.subheader("Resultado do Teste:")
    st.markdown(f"""
        **Conclusão:**  
        {"Rejeitamos" if result.p <= 0.05 else "Não rejeitamos"} a hipótese nula ao nível de significância de 5%.  
        As estações mais chuvosa, mais próxima da chuvosa e mais distante da chuvosa possuem precipitação {"com variação significante de junho para julho." if result.p <= 0.05 else "sem variação significante de junho para julho."} Inclusive, mostrando tendência decrescente.

        **Resultado do Teste T:**
        - Trend: {result.trend}
        - Estatística s: {result.s}
        - Valor p: {result.p:.4f}
    """)


show_sidebar()