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