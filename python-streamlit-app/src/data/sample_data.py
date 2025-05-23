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
    # Atualização: única entrada para os 4 semestres completos de língua estrangeira, conforme edital
    ("Ter cursado 4 semestres completos de outra língua (Titulação Internacional)", 0.5, 1.0),
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
    ("Língua estrangeira - proficiência ou curso (≥ 3 anos)", 1.0, 1)
]

exclusive_groups = [
    [
        "Aproveitamento Curricular - ≥ 50% notas ≥ 85 (4 primeiros anos)",
        "Aproveitamento Curricular - ≥ 50% notas ≥ 80 (4 primeiros anos)",
        "Aproveitamento Curricular - ≥ 50% notas ≥ 75 (4 primeiros anos)",
        "Aproveitamento Curricular - Notas dos 4 primeiros anos não atingem valores acima",
        "Aproveitamento Curricular - Notas dos 4 primeiros anos apenas suficientes"
    ],
    # Outras conexões podem ser adicionadas aqui...
]