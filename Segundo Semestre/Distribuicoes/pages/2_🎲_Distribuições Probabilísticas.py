import streamlit as st
import pandas as pd
import numpy as np
import scipy.stats as stats
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotnine import *

# Configuração da página
st.set_page_config(page_title="Dashboard de Distribuições Probabilísticas", layout="wide")

# Adicionando o logo
st.logo("logo.png")

# Adicionando o logo
st.image("logo.png", width=150)

# Criando as sub-abas (pages)
pages = st.sidebar.selectbox("Escolha a Distribuição:", [
    "Distribuição de Bernoulli",
    "Distribuição Binomial",
    "Distribuição de Poisson",
    "Distribuição Normal",
    "Analise seus Dados"
])

st.sidebar.markdown("Desenvolvido por Prof. Tiago Marum [THM Estatística](https://thmestatistica.com)")

# Função para exibir gráfico Plotly
def plot_distribution(x, y, title, xlabel, ylabel):
    fig = go.Figure(data=[go.Bar(x=x, y=y)])
    fig.update_layout(title=title, xaxis_title=xlabel, yaxis_title=ylabel)
    st.plotly_chart(fig)

if pages == "Distribuição de Bernoulli":
    st.header("Distribuição de Bernoulli")
    st.write("A distribuição de Bernoulli modela experimentos com duas possibilidades: sucesso (1) ou fracasso (0). Um exemplo clássico é o lançamento de uma moeda, onde podemos definir sucesso como 'cara' e fracasso como 'coroa'.")
    
    st.latex(r"P(X = x) = p^x (1 - p)^{1-x}, \quad x \in \{0,1\}")
    p = st.slider("Probabilidade de sucesso (p):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    valores = [0, 1]
    probabilidades = [1 - p, p]
    df_bernoulli = pd.DataFrame({"X": valores, "P(X)": probabilidades}).set_index("X")
    
    col1, col2 = st.columns([0.25,0.75])

    col1.write("Tabela de Probabilidades:")
    col1.write(df_bernoulli)
    col1.write("Uma tabela de probabilidades mostra todas as possibilidades de um evento acontecer e a chance de cada uma delas. Por exemplo, ao jogar um dado, a tabela pode mostrar que a chance de sair qualquer número de 1 a 6 é 1/6. É uma forma simples de visualizar as probabilidades de diferentes resultados.")

    col2.write("Distribuição de Probabilidades")
    fig = go.Figure(data=[go.Bar(x=valores, y=probabilidades)])
    fig.update_layout(title="Distribuição de Bernoulli", xaxis_title="Resultado", yaxis_title="Probabilidade")
    col2.plotly_chart(fig)

elif pages == "Distribuição Binomial":
    st.header("Distribuição Binomial")
    st.subheader("A distribuição binomial modela a probabilidade de sucessos em tentativas independentes. Útil para prever resultados e apoiar decisões estratégicas")
    st.write("A distribuição binomial tem suas raízes no estudo das probabilidades, um campo desenvolvido por matemáticos como Blaise Pascal e Pierre de Fermat no século XVII. Esses estudos iniciais formaram a base do que viria a ser a teoria das probabilidades moderna. Jacob Bernoulli, um matemático suíço, foi um dos pioneiros a descrever a distribuição binomial em sua obra Ars Conjectandi, publicada postumamente em 1713. Na figura abaixo vemos as representações de Blaise Pascal e Pierre de Fermat.")
    st.image("binomial.jpg")
    st.write("A distribuição Binomial modela o número de sucessos em n tentativas independentes. Um exemplo seria acertar um pênalti em 10 tentativas, dado que um jogador tem 80% de acerto.")
    st.subheader("Fórmula da Distribuição Binomial")
    st.latex(r"P(X = k) = \binom{n}{k} p^k (1 - p)^{n-k}")
    st.divider()

    col1, col2 = st.columns([0.5,0.5])
    n_max = col1.number_input("Número máximo de tentativas", value=50)
    n = col1.slider("Número de tentativas (n):", min_value=1, max_value=n_max, value=10, step=1)
    k = col2.slider("Número de sucessos (k):", min_value=0, max_value=n, value=5, step=1)
    p = col2.slider("Probabilidade de sucesso (p):", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
    
    x = np.arange(0, n + 1)
    y = stats.binom.pmf(x, n, p)
    df_binomial = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y)}).set_index("X")
    st.write("Tabela de probabilidades:")
    st.write(df_binomial)
    plot_distribution(x, y, "Distribuição Binomial", "Número de sucessos", "Probabilidade")
    
    st.markdown("Para saber mais leia a [matéria completa no blog](https://thmestatistica.com/blog/educacao/aulas-e-tutoriais/a-matematica-do-sucesso-entenda-como-utilizar-distribuicao-binomial)")

elif pages == "Distribuição de Poisson":
    st.header("Distribuição de Poisson")
    st.markdown('''A **distribuição de Poisson** é uma ferramenta estatística usada para modelar a **ocorrência de eventos raros** dentro de um intervalo fixo de tempo ou espaço. Imagine um caixa eletrônico e quantas pessoas chegam a ele a cada hora – essa variação pode ser prevista com a distribuição de Poisson. Ela é muito útil porque nos ajuda a entender a frequência esperada de eventos que acontecem aleatoriamente, como chamadas recebidas em um call center, número de acidentes de trânsito em uma rodovia ou até mesmo a quantidade de gols marcados em uma partida de futebol.''')    
    st.markdown('''Esse tipo de distribuição é amplamente aplicado em diversas áreas. No atendimento ao cliente, por exemplo, bancos e hospitais usam a distribuição de Poisson para prever o fluxo de pessoas e evitar longas filas. Na área da saúde, epidemiologistas utilizam essa abordagem para modelar a ocorrência de doenças raras em uma população, ajudando a detectar surtos incomuns. Já na engenharia de tráfego, ela é empregada para estimar quantos carros passam por um determinado ponto da cidade em um período de tempo. Esses exemplos mostram como a distribuição de Poisson ajuda a planejar recursos, otimizar serviços e entender melhor o comportamento de eventos aleatórios.''')
    st.video("https://youtu.be/OnbmtKSIILE?si=JQfvjskJAjPERVHJ")
    st.subheader("Fórmula da Distribuição de Poisson")
    st.latex(r"P(X = k) = \frac{e^{-\lambda} \lambda^k}{k!}")

    col1, col2 = st.columns([0.3,0.7])
    lambd = col1.number_input("Taxa média de ocorrência (λ):",min_value=0.001,step=0.01,value=2.0)
    x_max = col1.number_input("Número de eventos desejado",min_value=0, step=1,value=20)
    x = np.arange(0, x_max)  
    y = stats.poisson.pmf(x, lambd)
    df_poisson = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y),
                               "P(X > k) (Acumulado Cauda Direita)": 1-np.cumsum(y)}).set_index("X")
    col2.write("Tabela de probabilidades:")
    col2.write(df_poisson)
    plot_distribution(x, y, "Distribuição de Poisson", "Número de eventos", "Probabilidade")

elif pages == "Distribuição Normal":
    st.header("Distribuição Normal")

    st.markdown('''A distribuição normal, também conhecida como distribuição de Gauss, é uma das mais importantes na estatística e na ciência de dados. Ela descreve fenômenos naturais e sociais em que os valores se concentram ao redor de uma média, formando um gráfico em forma de sino. Esse comportamento é comum em diversas situações do dia a dia, como alturas de pessoas, notas em provas e erros de medição em experimentos.''')
    col1, col2 = st.columns([0.5,0.5])
    col1.image('gauss_normal.jpg',caption="Gauss e a Distribuição Normal",width=350)
    col2.markdown('''Uma característica fundamental da distribuição normal é que seus dados seguem um padrão previsível: aproximadamente 68% dos valores estão a um desvio padrão da média, 95% dentro de dois desvios e 99,7% dentro de três desvios. Essa propriedade permite calcular probabilidades e tomar decisões informadas em diversas áreas, como controle de qualidade, modelagem financeira, inteligência artificial e testes estatísticos. A normalidade dos dados é um conceito essencial na inferência estatística, servindo como base para métodos como testes de hipóteses e intervalos de confiança.''')
    col2.subheader('Não tão normal assim - Estatística Acústica THM [Spotify](https://open.spotify.com/intl-pt/track/0ITg7M5wJ4ptJOK871oMbW?si=d7261b1ce4534ebd)')
    
    # Exibir a fórmula da distribuição normal
    st.subheader("Fórmula da Distribuição Normal")
    st.latex(r"f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{(x - \mu)^2}{2\sigma^2}}")
 
    mu = st.number_input("Média (μ):", value=0.0)
    sigma = st.number_input("Desvio Padrão (σ):", value=1.0, min_value=0.1)
    x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
    y = stats.norm.pdf(x, mu, sigma)
    y_cdf = stats.norm.cdf(x, mu, sigma)
    
    curva2 = st.checkbox("Curva 2")
    if curva2:
        mu_2 = st.number_input("Média 2 (μ):", value=2.0)
        sigma_2 = st.number_input("Desvio Padrão 2 (σ):", value=1.0, min_value=0.1)
        x_2 = np.linspace(mu_2 - 4*sigma_2, mu_2 + 4*sigma_2, 100)
        y_2 = stats.norm.pdf(x_2, mu_2, sigma_2)
        y_2_cdf = stats.norm.cdf(x_2, mu_2, sigma_2)

    col3, col4 = st.columns(2)  
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='PDF'))
    fig.update_layout(title="Distribuição Normal", xaxis_title="Valores", yaxis_title="Densidade de Probabilidade")
    if curva2:
        fig.add_trace(go.Scatter(x=x_2, y=y_2, mode='lines', name='Curva2'))
    col3.plotly_chart(fig)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x, y=y_cdf, mode='lines', name='CDF'))
    fig2.update_layout(title="Distribuição Normal Acumulada", xaxis_title="Valores", yaxis_title="Probabilidade Acumulada")
    if curva2:
        fig2.add_trace(go.Scatter(x=x_2, y=y_2_cdf, mode='lines', name='Curva2'))
    col4.plotly_chart(fig2)

elif pages == "Analise seus Dados":
    st.header("Análise de Dados")
    st.write("Faça upload do seu arquivo Excel para analisar a distribuição de uma variável numérica.")
    uploaded_file = st.file_uploader("Carregue seu arquivo Excel", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("Amostra dos dados:")
        st.write(df.head())
        
        colunas_numericas = df.select_dtypes(include=[np.number]).columns.tolist()
        if colunas_numericas:
            coluna_escolhida = st.selectbox("Escolha uma coluna numérica:", colunas_numericas)
            
            if coluna_escolhida:
                st.write("Distribuição dos dados:")
                st.write(df[coluna_escolhida].describe())
                
                dist = st.selectbox("Escolha a distribuição para análise:", ["Poisson", "Normal", "Binomial"])
                
                if dist == "Poisson":
                    
                    col1, col2 = st.columns([0.3,0.7])
                    
                    lambda_est = df[coluna_escolhida].mean()

                    x_min = col1.number_input("Número mínimo de eventos",value=0)
                    x_max = col1.number_input("Número máximo de eventos desejado",value=2*lambda_est)
                    
                    x = np.arange(x_min, x_max)
                    y = stats.poisson.pmf(x, lambda_est)
                    y_cdf = stats.poisson.cdf(x,lambda_est)

                    df_poisson = pd.DataFrame({"X": x, "P(X)": y, "P(X ≤ k) (Acumulado)": np.cumsum(y),"P(X > k) (Acumulado Cauda Direita)": 1-np.cumsum(y)}).set_index("X")

                    col2.write("Tabela de probabilidades:")
                    col2.write(df_poisson)
                    
                    st.subheader(f"Estimativa de λ (Taxa média de Ocorrência): {lambda_est:.2f}")
                    prob_acum = st.toggle("Probabilidade Acumulada")
                    if prob_acum:
                        st.write("Probabilidades 'somadas' desde a origem!")
                        y_selec = y_cdf
                        fig = go.Figure(data=[go.Line(x=x, y=y_selec)])
                        fig.update_layout(title="Distribuição de Poisson Acumulada", xaxis_title="Número de eventos", yaxis_title="Probabilidade Acumulada")
                        st.plotly_chart(fig)
                    else:
                        y_selec = y
                        plot_distribution(x, y_selec, "Distribuição de Poisson", "Número de eventos", "Probabilidade")
                    


                    
                elif dist == "Normal":
                    
                    n = df[coluna_escolhida].count()
                    mu_est = df[coluna_escolhida].mean()
                    sigma_est = df[coluna_escolhida].std()
                    st.subheader(f"Estimativa de μ: {mu_est:.2f}, σ: {sigma_est:.2f}")


                    # Create distplot with custom bin_size
                    #colunas_categoricas = df.select_dtypes(include=[np.character]).#columns.tolist()
                    
                    #st.selectbox("Escolha uma variável qualitativa",colunas_categoricas)


                    hist_data = [df[coluna_escolhida].dropna().tolist()]
                    group_labels=['distplot']
                    b_size = st.number_input("Largura de Classe - Histograma",min_value=0.1,value=5.0)

                    fig = ff.create_distplot(
                        hist_data, group_labels, bin_size=b_size)
                    
                    teorica = st.checkbox("Curva teórica")
                    if teorica:

                        # Adicionando a curva da distribuição normal teórica com média e desvio padrão da amostra
                        x = np.linspace(mu_est - 4*sigma_est, mu_est + 4*sigma_est, 100)
                        y = stats.norm.pdf(x, mu_est, sigma_est)

                        # Criando um trace da curva normal
                        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Curva Normal', line=dict(color='red')))
                    
                    st.plotly_chart(fig)

                    p = ggplot(df, aes(sample=coluna_escolhida)) + geom_qq(size=3,colour='red',alpha=0.7) + geom_qq_line()+theme_bw()+labs(x="Quantis Teóricos",y = "Quantis Amostrais", title="Gráfico QQPlot")
                    st.pyplot(ggplot.draw(p))





                
                elif dist in ["Binomial"]:
                    threshold = st.number_input("Defina o limiar para True/False:")
                    p_est = (df[coluna_escolhida] > threshold).mean()
                    k = st.slider("Número de sucessos (k):", min_value=0, max_value=50, value=5, step=1)
                    st.write(f"Estimativa de p: {p_est:.2f}")
                    valores = np.arange(0, k + 1)
                    probabilidades = stats.binom.pmf(valores, k, p_est)
                    plot_distribution(valores, probabilidades, f"Distribuição {dist}", "Resultado", "Probabilidade")
                    df_binomial = pd.DataFrame({"X": valores, "P(X)": probabilidades})
                    st.write("Tabela de probabilidades:")
                    st.write(df_binomial)