# Data Collection
BILLING_PROJECT_ID = "incomeprediction-425511"
SQL_QUERY = """
SELECT 
    ano
    , trimestre
    , sigla_uf
    , id_domicilio
    , V1022 AS situacao_domicilio
    , V1027 AS peso_sem_pos_estratificacao
    , V1028 AS peso_com_pos_estratificacao
    , V2001 AS pessoas_domicilio
    , V2005 AS condicao_domicilio
    , V2007 AS sexo
    , V2009 AS idade
    , V2010 AS cor
    , V3001 AS alfabetizado
    , V3009 AS curso_mais_elevado
    , V3009A AS curso_mais_elevado_2
FROM basedosdados.br_ibge_pnadc.microdados
LIMIT 10
"""

