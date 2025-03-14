import streamlit as st
from components.interactive_table import tabela_interativa_nx3
from data.sample_data import *
def main():
    st.set_page_config(layout="wide")
    st.title("Tabela Interativa nx3")
    
    # Exemplo de dados (lista de tuplas com string e dois floats)
    # Em um aplicativo real, isso poderia ser carregado de um arquivo ou entrada do usuário

    domain = st.sidebar.selectbox(
    "Selecione qual coisinho vc quer",
    ["Enare", "Aremg"]
    )
    # Cria a tabela interativa e obtém os inteiros atuais
    if domain == "Enare":
        df_editado, inteiros_atuais = tabela_interativa_nx3(dados_enare)
    else:
        df_editado, inteiros_atuais = tabela_interativa_nx3(dados_aremg)
    


if __name__ == "__main__":
    main()
