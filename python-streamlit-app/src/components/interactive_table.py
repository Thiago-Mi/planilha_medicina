import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from components.operations import sum_weight

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
    
    # Configuração das opções do grid
    gb = GridOptionsBuilder.from_dataframe(display_df)
    gb.configure_column('String', editable=False)
    gb.configure_column('Inteiro',
                       editable=True,
                       type=["numericColumn", "numberColumnFilter"],
                       valueFormatter="data.Inteiro.toFixed(0)")
    gb.configure_grid_options(enableRangeSelection=True)
    grid_options = gb.build()
    
    # Exibir o grid
    grid_response = AgGrid(
        display_df,
        gridOptions=grid_options,
        width='100%',
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        update_mode="MODEL_CHANGED"
    )
    
    # Obter o dataframe atualizado
    result_df = grid_response['data']
    
    # Calcular a soma usando a função sum_weight
    soma_inteiros = sum_weight(display_df["Point"].tolist(), 
                               display_df["Limit"].tolist(), 
                               result_df["Inteiro"].tolist())
    
    st.write(f"Soma de todos os inteiros: {soma_inteiros}")
    
    # Atualizar o estado da sessão com os novos valores inteiros
    st.session_state.integers = result_df["Inteiro"].tolist()
    
    # NOVO: Botão para download dos dados inteiros e da soma
    col1, col2 = st.columns(2)
    
    with col1:
        # Preparar o conteúdo do arquivo de texto para download
        txt_content = "Valores Inteiros:\n"
        for idx, valor in enumerate(result_df["Inteiro"].tolist()):
            string = result_df["String"].iloc[idx]
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
                    except (ValueError, IndexError):
                        pass
            
            # Atualizar os inteiros se a quantidade for compatível
            if len(imported_integers) == len(st.session_state.integers):
                st.session_state.integers = imported_integers
                st.success("Dados importados com sucesso!")
                st.rerun()  # Reexecutar para atualizar a tabela
            else:
                st.error(f"Número de valores incompatível. Esperado: {len(st.session_state.integers)}, Encontrado: {len(imported_integers)}")
    
    return result_df, st.session_state.integers
