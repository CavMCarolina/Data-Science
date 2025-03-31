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

    st.sidebar.write("🔍 **Análise**")
    st.sidebar.page_link("pages/medidas_centrais.py", label="Medidas Centrais")
    st.sidebar.page_link("pages/medidas_dispersao.py", label="Medidas de Dispersão")
    st.sidebar.page_link("pages/distribuicoes.py", label="Distribuições")
    st.sidebar.page_link("pages/confianca.py", label="Intervalo de Confiança")

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
