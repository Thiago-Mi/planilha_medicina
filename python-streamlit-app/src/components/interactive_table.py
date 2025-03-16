import streamlit as st
import pandas as pd
from components.operations import sum_weight
from components.operations import apply_exclusive_connections
from data.sample_data import exclusive_groups



def tabela_interativa_nx3(dados_tuplas):
    """
    Cria uma tabela interativa nx3 a partir de uma lista de tuplas,
    com botões para download e upload dos dados inteiros.
    
    Parâmetros:
    dados_tuplas (list): Lista de tuplas, cada uma contendo (string, float1, float2)
    
    Retorna:
    tuple: (DataFrame editado, lista de inteiros atuais)
    """
    # Inicialização do estado da sessão para inteiros
    if 'integers' not in st.session_state:
        st.session_state.integers = [0] * len(dados_tuplas)
    
    # Redimensionar se necessário
    if len(st.session_state.integers) != len(dados_tuplas):
        st.session_state.integers = [0] * len(dados_tuplas)
    
    # Preparação do DataFrame para exibição
    display_data = []
    for idx, ((string, float1, float2), integer) in enumerate(zip(dados_tuplas, st.session_state.integers)):
        display_data.append({
            "String": string,
            "Point": float1,
            "Limit": float2,
            "Inteiro": integer
        })
    display_df = pd.DataFrame(display_data)

    # Criar um formulário para conter o editor
    edited_df = st.data_editor(
            display_df,
            column_config={
                "String": st.column_config.TextColumn("String"),
                "Float|Float": st.column_config.TextColumn("Float|Float", disabled=True),
                "Inteiro": st.column_config.NumberColumn("Inteiro", min_value=0, max_value=100, step=1, format="%d")
            },
            hide_index=True,
            use_container_width=True,
            key="data_editor"
        )
    
    display_df = apply_exclusive_connections(display_df, exclusive_groups)
    # Calcular a soma usando a função sum_weight
    soma_inteiros = sum_weight(display_df["Point"].tolist(), 
                               display_df["Limit"].tolist(), 
                               edited_df["Inteiro"].tolist())
    
    st.write(f"Soma de todos os inteiros: {soma_inteiros}")
    
    # Atualizar o estado da sessão com os novos valores inteiros
    st.session_state.integers = edited_df["Inteiro"].tolist()
    
    # NOVO: Botão para download dos dados inteiros e da soma
    col1, col2 = st.columns(2)
    
    with col1:
        # Preparar o conteúdo do arquivo de texto para download
        txt_content = "Valores Inteiros\n"
        for idx, valor in enumerate(edited_df["Inteiro"].tolist()):
            string = edited_df["String"].iloc[idx]
            txt_content += f"{string}: {valor}\n"
        txt_content += f"\nSoma total: {soma_inteiros}"
        
        # Botão de download
        st.download_button(
            label="Baixar Dados Inteiros",
            data=txt_content,
            file_name="dados_inteiros.txt",
            mime="text/plain"
        )
    
    with col2:
        # NOVO: Botão para importar dados inteiros
        uploaded_file = st.file_uploader("Importar dados inteiros", type=["txt"])
        print(uploaded_file)
        if uploaded_file is not None:
            # Ler o conteúdo do arquivo
            content = uploaded_file.getvalue().decode("utf-8")
            lines = content.split("\n")
            
            # Extrair os valores inteiros
            imported_integers = []
            for line in lines:
                if ":" in line:  # Verifica se é uma linha com valor inteiro
                    try:
                        value = int(line.split(":")[1].strip())
                        imported_integers.append(value)
                        print(line, value, line.split(":"))
                    except (ValueError, IndexError):
                        print(ValueError, IndexError)
                        pass

            # Atualizar os inteiros se a quantidade for compatível
            print(imported_integers, st.session_state.integers)
            if len(imported_integers) == len(st.session_state.integers):
                st.session_state.integers = imported_integers
                st.success("Dados importados com sucesso!")
                st.rerun()  # Reexecutar para atualizar a tabela
            else:
                st.error(f"Número de valores incompatível. Esperado: {len(st.session_state.integers)}, Encontrado: {len(imported_integers)}")
    
    return edited_df, st.session_state.integers
