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

def apply_exclusive_connections(df, exclusive_groups, value_col="Inteiro", max_col="Limit"):
    """
    Recebe um DataFrame e uma lista de grupos de strings mutuamente exclusivos.
    Para cada grupo, se um dos itens tiver o valor preenchido (maior que zero) na coluna value_col,
    os demais itens do grupo terão seu valor (value_col) zerado e o valor máximo (max_col) ajustado para zero, 
    para que não possam ser alterados.
    
    Parâmetros:
      df (pd.DataFrame): DataFrame que contém, entre outras, as colunas 'String', value_col e max_col.
      exclusive_groups (list of list): Lista de grupos; cada grupo é uma lista de termos (strings) que se 
                                       excluem mutuamente.
      value_col (str): Coluna que representa o valor atual (padrão "Inteiro")
      max_col (str): Coluna que representa o valor máximo permitido (padrão "Limit")
      
    Retorna:
      pd.DataFrame: DataFrame modificado.
    """
    # Para cada grupo de exclusão
    for group in exclusive_groups:
        # Seleciona as linhas que possuem a string em um dos termos do grupo
        group_mask = df["String"].isin(group)
        
        # Se não há itens suficientes, pula o grupo
        if group_mask.sum() < 2:
            continue
        
        # Verifica se algum item já foi preenchido (valor > 0)
        selected_indices = df[group_mask & (df[value_col] > 0)].index.tolist()
        if selected_indices:
            # Mantém apenas o primeiro selecionado e zera os demais
            chosen = selected_indices[0]
            for idx in df[group_mask].index:
                if idx != chosen:
                    df.at[idx, value_col] = 0
                    df.at[idx, max_col] = 0
                    # Se preferir remover o item para evitar confusão no formulário, pode descomentar a linha a seguir:
                    # df.drop(idx, inplace=True)
    return df