import streamlit as st
import pandas as pd
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder



def sum_weight(unit, limit, value, weight=1):
    """
    Calcula a soma ponderada dos produtos de unidades e valores com limites aplicados.
    
    Suporta tanto valores únicos quanto listas:
    - Se as entradas forem valores únicos, os trata como listas de comprimento 1
    - Se as entradas forem listas, calcula os resultados para cada tripla, soma e aplica o peso
    
    Parâmetros:
    unit (número ou lista): Valor(es) de unidade
    limit (número ou lista): Valor(es) limite
    value (número ou lista): Valor(es) a serem multiplicados com as unidades
    weight (float): Peso para multiplicar a soma final (padrão: 1)
    
    Retorna:
    float: Soma ponderada dos resultados
    """
    # Converte valores únicos para listas de comprimento 1
    unit_list = unit if isinstance(unit, list) else [unit]
    limit_list = limit if isinstance(limit, list) else [limit]
    value_list = value if isinstance(value, list) else [value]
    # Verifica se as listas têm o mesmo comprimento
    if not (len(unit_list) == len(limit_list) == len(value_list)):
        raise ValueError("As listas de unidades, limites e valores devem ter o mesmo comprimento")
    
    # Calcula o resultado para cada conjunto de elementos correspondentes
    total = sum(min(u * v, l) for u, l, v in zip(unit_list, limit_list, value_list))
    
    # Multiplica a soma pelo peso
    return total * weight

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


dados_exemplo = [
        ("Item A", 1.23, 4.56),
        ("Item B", 7.89, 10.11),
        ("Item C", 12.34, 56.78),
        ("Item D", 15.4, 30)
    ]

dados_aremg = [
    ("Aproveitamento Curricular - ≥ 50% notas ≥ 85 (4 primeiros anos)", 1.5, 3.0),
    ("Aproveitamento Curricular - ≥ 50% notas ≥ 80 (4 primeiros anos)", 1.0, 3.0),
    ("Aproveitamento Curricular - ≥ 50% notas ≥ 75 (4 primeiros anos)", 0.5, 3.0),
    ("Aproveitamento Curricular - Notas dos 4 primeiros anos não atingem valores acima", 0.25, 3.0),
    ("Aproveitamento Curricular - Notas dos 4 primeiros anos apenas suficientes", 0.25, 3.0),
    ("Aproveitamento Curricular - Não possuo histórico escolar (4 primeiros anos)", 0.0, 3.0),
    ("Aproveitamento Curricular - ≥ 70% notas ≥ 85 ou Conceito A (2 últimos anos)", 1.0, 3.0),
    ("Aproveitamento Curricular - ≥ 70% notas ≥ 80 ou Conceito B (2 últimos anos)", 0.5, 3.0),
    ("Aproveitamento Curricular - Notas dos 2 últimos anos não atingem valores acima", 0.25, 3.0),
    ("Aproveitamento Curricular - Notas dos 2 últimos anos apenas conceituais", 0.25, 3.0),
    ("Aproveitamento Curricular - Apenas cópia de diploma ou CRM", 0.10, 3.0),
    ("Índice ENADE 4 ou 5", 1.0, 3.0),
    ("Índice ENADE 3", 0.5, 3.0),
    ("Índice ENADE 2 ou 1", 0.0, 3.0),
    ("Título avançado em inglês (Titulação Internacional)", 1.0, 1.0),
    ("Título intermediário em inglês (Titulação Internacional)", 0.5, 1.0),
    ("Título avançado em outra língua (Titulação Internacional)", 0.5, 1.0),
    ("Ter cursado 4 semestres de outra língua (Faculdade de Letras)", 0.3, 1.0),
    ("Ter cursado 4 semestres de outra língua (Histórico Escolar Medicina)", 0.3, 1.0),
    ("Estágio Extracurricular - 6 meses (mín. 180 horas)", 0.7, 2.0),
    ("Estágio Extracurricular - 2 estágios de 3 meses cada (mín. 90 horas cada)", 0.7, 2.0),
    ("Projeto ou Programa de Extensão na área médica (01 projeto)", 0.5, 0.5),
    ("Monitoria/Programa de Iniciação à Docência - 01 semestre (mín. 80 horas)", 0.7, 2.0),
    ("Bolsa de Iniciação Científica - BIC (mín. 6 meses)", 0.6, 1.30),
    ("Participação Voluntária em Iniciação Científica (mín. 6 meses)", 0.4, 1.30),
    ("Participação em Projeto de Pesquisa (c/ publicação ou apresentação)", 0.3, 1.30),
    ("Residência Médica/Multiprofissional/Área Profissional da Saúde", 0.5, 0.5),
    ("Mestrado em área da saúde (CAPES/MEC)", 0.5, 0.5),
    ("Doutorado em área da saúde (CAPES/MEC)", 0.5, 0.5),
    ("Especialização Médica (mín. 360 horas ou Título de Especialista CFM)", 0.5, 0.5),
    ("Organizador em evento científico (mín. 8 horas)", 0.4, 1.0),
    ("Palestrante em evento científico (mín. 8 horas)", 0.3, 1.0),
    ("Ouvinte em congresso estadual/nacional (Sociedade/Entidade Médica)", 0.2, 1.0),
    ("Participação em até 2 ligas acadêmicas (2 semestres não coincidentes)", 1.0, 1.0),
    ("Cargo titular Diretório Acadêmico/Representação discente (mín. 1 ano)", 0.30, 1.0),
    ("Curso Suporte Avançado à Vida (mín. 16 horas, válido)", 0.5, 0.5),
    ("Curso Suporte Básico à Vida (mín. 8 horas, válido)", 0.3, 0.3),
    ("Curso Ética Médica (últimos 5 anos)", 0.3, 0.5),
    ("Curso Medicina Baseada em Evidências (mín. 8 horas, últimos 5 anos)", 0.2, 0.5),
    ("Curso Mercado de Trabalho (mín. 8 horas, últimos 5 anos)", 0.2, 0.5),
    ("Participação Voluntária em Projeto Comunitário (mín. 2 projetos, 16 horas)", 0.30, 0.80),
    ("Estágio em Vigilância à Saúde (6 meses, mín. 180 horas)", 0.5, 0.80),
    ("Estágio em Vigilância à Saúde (3 meses, mín. 90 horas)", 0.3, 0.80),
    ("Apresentação de trabalho em evento científico", 0.3, 1.50),
    ("Apresentação c/ publicação em revista indexada", 0.5, 1.50),
    ("Publicação de artigo científico completo em revista indexada", 0.7, 1.50),
    ("Publicação de livro ou capítulo de livro técnico (máx. 1 autor e 3 coautores)", 0.5, 0.5)
]


dados_enare = [
    ("Histórico Escolar - ≥ 50% menção A ou nota 7-10/70-100", 40, 40),
    ("Histórico Escolar - ≥ 50% menção A e B ou SS e MS ou nota 7-10/70-100", 30, 40),
    ("Histórico Escolar - ≥ 50% menção A, B ou C ou SS, MS e MM ou nota 5-10/50-100", 20, 40),
    ("Programa ou projeto de Extensão (mín. 30 horas)", 4.0, 8),
    ("Vivências no SUS - ≥ 6 meses", 2.0, 4),
    ("Vivências no SUS - ≥ 1 ano", 4.0, 4),
    ("Vivências no SUS - ≥ 2 anos", 6.0, 4),
    ("Monitoria - por semestre letivo", 3.0, 9),
    ("Monitoria - por ano letivo", 6.0, 9),
    ("Atividade de Pesquisa - período ≥ 1 ano", 6.0, 12),
    ("Trabalhos científicos apresentados (Regional/Local)", 0.3, 1.5),
    ("Trabalhos Científicos apresentados (Nacional/Internacional)", 0.5, 1.5),
    ("Artigo científico publicado (não indexado/anais)", 1.0, 3),
    ("Artigo científico publicado (indexado, com DOI)", 1.5, 4.5),
    ("Participação em Congresso/Simpósio/Jornada (área profissional)", 0.1, 0.5),
    ("Representação estudantil em órgão colegiado - por ano", 1.0, 2),
    ("Participação em Ligas Acadêmicas - ≥ 12 meses", 0.5, 1),
    ("Língua estrangeira: proficiência ou curso (≥ 3 anos)", 1.0, 1)
]

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
