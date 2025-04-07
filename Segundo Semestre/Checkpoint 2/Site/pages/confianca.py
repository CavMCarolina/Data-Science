import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

st.header("Intervalo de Confiança:")
st.write("""
    Um intervalo de confiança representa uma estimativa da incerteza associada a um valor médio obtido a partir de dados amostrais. No contexto do nosso gráfico, usamos o intervalo de confiança de 95% para indicar uma margem de erro em torno da média anual de precipitação de cada local.

    Esses intervalos ajudam a interpretar os dados com mais segurança, pois mostram o quanto podemos confiar naquela média. Quanto menor o intervalo, maior a precisão da estimativa.
""")

st.divider()

# filtro = st.selectbox("Escolha um filtro para o gráfico:", ["Todas as Regiões", "10 Regiões Mais Chuvosas"])

# if filtro == "Todas as Regiões":
#     st.header("Todas as Regioes")

#     # Criar listas para os dados do gráfico
#     regioes = df_filtrado['nm'].tolist()
#     medias = df_filtrado['med_anual'].tolist()
#     desvios = df_filtrado['dp_anual'].tolist()

#     # Calcular os limites inferior e superior do intervalo de confiança (95%)
#     limite_inferior = [media - 1.96 * desvio for media, desvio in zip(medias, desvios)]
#     limite_superior = [media + 1.96 * desvio for media, desvio in zip(medias, desvios)]

#     # Criar o gráfico
#     fig = go.Figure()

#     # Adicionar os intervalos de confiança como linhas verticais
#     for i, regiao in enumerate(regioes):
#         fig.add_trace(go.Scatter(
#             x=[limite_inferior[i], limite_superior[i]],
#             y=[regiao, regiao],
#             mode='lines',
#             line=dict(color='red', width=2),
#             name=f"Intervalo de Confiança ({regiao})",
#             showlegend=False  # Evitar repetição na legenda
#         ))

#     # Adicionar os pontos das médias com cores diferentes para cada região
#     for i, regiao in enumerate(regioes):
#         fig.add_trace(go.Scatter(
#             x=[medias[i]],
#             y=[regioes[i]],
#             mode='markers',
#             marker=dict(size=8, color=f"rgba({i*25 % 255}, {i*50 % 255}, {i*75 % 255}, 1)"),  # Cores únicas
#             name=f"Média ({regiao})"
#         ))

#     # Adicionar os pontos para o limite inferior
#     fig.add_trace(go.Scatter(
#         x=limite_inferior,
#         y=regioes,
#         mode='markers',
#         marker=dict(color='blue', size=6, symbol='circle'),
#         name='Limite Inferior'
#     ))

#     # Adicionar os pontos para o limite superior
#     fig.add_trace(go.Scatter(
#         x=limite_superior,
#         y=regioes,
#         mode='markers',
#         marker=dict(color='orange', size=6, symbol='circle'),
#         name='Limite Superior'
#     ))

#     # Configurar o layout do gráfico
#     fig.update_layout(
#         title="Intervalos de Confiança (95%) por Região",
#         xaxis_title="Precipitação (mm)",
#         yaxis_title="Regiões",
#         template="plotly_white",
#         height=800,  # Ajustar a altura para acomodar todas as regiões
#         yaxis=dict(tickmode='linear', automargin=True)  # Garantir que os nomes fiquem visíveis
#     )

#     # Exibir o gráfico no Streamlit
#     st.plotly_chart(fig)

# elif filtro == "10 Regiões Mais Chuvosas":  
st.header("10 Regiões Mais Chuvosas")

# Pegar apenas os top 10 lugares mais chuvosos do df (top 11 pq tem duas Francas)
top_10_chuvosos = df_filtrado.nlargest(11, 'med_anual').sort_values('med_anual')
df_10 = top_10_chuvosos.sort_values(by='med_anual', ascending=True)

df_10.set_index('nm', inplace=True)
# Retirar uma das Francas
df_10 = df_10.drop('FRANCA  P11-140')

# Criar listas para os dados do gráfico
regioes = df_10.index.tolist()
medias = df_10['med_anual'].tolist()
desvios = df_10['dp_anual'].tolist()

# Calcular os limites inferior e superior do intervalo de confiança (95%)
limite_inferior = [media - 1.96 * desvio for media, desvio in zip(medias, desvios)]
limite_superior = [media + 1.96 * desvio for media, desvio in zip(medias, desvios)]

# Criar o gráfico
fig = go.Figure()

# Adicionar os intervalos de confiança como linhas verticais
for i, regiao in enumerate(regioes):
    fig.add_trace(go.Scatter(
        x=[limite_inferior[i], limite_superior[i]],
        y=[regiao, regiao],
        mode='lines',
        line=dict(color='red', width=2),
        name=f"Intervalo de Confiança ({regiao})",
        showlegend=False  # Evitar repetição na legenda
    ))

# Adicionar os pontos das médias
fig.add_trace(go.Scatter(
    x=medias,
    y=regioes,
    mode='markers',
    marker=dict(color='green', size=8),
    name='Média'
))

# Adicionar os pontos para o limite inferior
fig.add_trace(go.Scatter(
    x=limite_inferior,
    y=regioes,
    mode='markers',
    marker=dict(color='blue', size=6, symbol='circle'),
    name='Limite Inferior'
))

# Adicionar os pontos para o limite superior
fig.add_trace(go.Scatter(
    x=limite_superior,
    y=regioes,
    mode='markers',
    marker=dict(color='orange', size=6, symbol='circle'),
    name='Limite Superior'
))

# Configurar o layout do gráfico
fig.update_layout(
    title="Intervalos de Confiança (95%) por Região",
    xaxis_title="Precipitação (mm)",
    yaxis_title="Regiões",
    template="plotly_white",
    xaxis=dict(tickangle=45)  # Rotacionar os nomes das regiões
)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)

# Create a new DataFrame for the table
tabela = pd.DataFrame({
    'Média Anual': df_10['med_anual'],
    'Limite Inferior': limite_inferior,
    'Limite Superior': limite_superior
})

tabela.index.name = "Regiões"

st.dataframe(formatar_df(tabela))

st.subheader("Análise do Gráfico:")
st.write("""
    Ao observar o gráfico, é possível perceber que Cristais Paulista possui o maior intervalo de confiança, o que indica uma maior variabilidade na precipitação e, consequentemente, menor previsibilidade. Esse comportamento está associado a um maior desvio padrão, sugerindo que os valores de precipitação tendem a se afastar mais da média.

    Por outro lado, São Joaquim da Barra apresenta o menor intervalo de confiança, o que reflete uma menor dispersão dos dados e, portanto, maior consistência e previsibilidade nas precipitações ao longo do tempo.

    Essa diferença entre as regiões pode estar relacionada a fatores climáticos locais, relevo ou variações sazonais mais acentuadas em algumas áreas. Uma análise complementar poderia investigar eventos extremos, tamanho da amostra ou mudanças climáticas ao longo dos anos para entender melhor as causas dessa variabilidade.

    No entanto, é importante destacar que, apesar das diferenças nos tamanhos dos intervalos, todos os intervalos de confiança se sobrepõem. Isso significa que não podemos afirmar, com segurança estatística, que as médias reais de precipitação das regiões sejam significativamente diferentes entre si. A sobreposição sugere que as variações observadas podem estar dentro de uma margem esperada de incerteza, sendo necessário um estudo mais aprofundado para confirmar diferenças reais entre as médias.
""")

show_sidebar()