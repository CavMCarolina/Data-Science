import streamlit as st

def show_sidebar():
    # Oculta a navegação padrão do Streamlit com CSS
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    # Criando o sidebar personalizado
    st.sidebar.title("Navegação")
    st.sidebar.write("❓ **Introdução**")
    st.sidebar.page_link("introducao.py", label="Contextualização do Problema")
    st.sidebar.page_link("pages/descricao.py", label="Descrição do Dataset")

    st.sidebar.divider()

    st.sidebar.write("🔍 **Análise Exploratória**")
    st.sidebar.page_link("pages/normal.py", label="Distribuição Normal")
    st.sidebar.page_link("pages/confianca.py", label="Intervalo de Confiança")
    st.sidebar.page_link("pages/hipotese.py", label="Teste de Hipóteses")
    st.sidebar.page_link("pages/regional.py", label="Regional")

    st.sidebar.divider()

    st.sidebar.write("📊 **Discussão**")
    st.sidebar.page_link("pages/padroes.py", label="Padrões Sazonais")

    st.sidebar.divider()

    st.sidebar.write("👥 **Integrantes**")
    st.sidebar.markdown(f"""
        <ul>
            <li>
                <a href="https://www.linkedin.com/in/beatriz-sp-rocha">Beatriz Silva</a><br>
            </li>
            <li>
                <a href="https://www.linkedin.com/in/carolinacavallimachado">Carolina Machado</a><br>
            </li>
            <li>
                <a href="https://www.linkedin.com/in/edson-leonardo-4b500a289">Edson Leonardo</a><br>
            </li>
            <li>
                <a href="https://www.linkedin.com/in/eduardo-mazelli">Eduardo Mazelli</a><br>
            </li>
            <li>
                <a href="https://www.linkedin.com/in/nathanuflacker">Nathan Uflacker</a>
            </li>
        </ul>
    """, unsafe_allow_html=True)
