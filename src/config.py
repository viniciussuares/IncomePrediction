import os 

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
    , V4076 AS tempo_desempregado_procurando_trabalho
    , VD2002 AS condicao_domicilio
    , VD2003 AS numero_componente_domicilio
    , VD3005 AS anos_estudos
    , VD4001 AS condicao_forca_trabalho
    , VD4002 AS condicao_ocupacao
    , VD4003 AS forca_trabalho_potencial
    , VD4007 AS posicao_ocupacao_principal
    , VD4016 AS rendimento_mensal_habitual_trabalho_principal
    , VD4017 AS rendimento_mensal_efetivo_trabalho_principal
    , VD4019 AS rendimento_mensal_habitual_todos_trabalhos
    , VD4020 AS rendimento_mensal_habitual_todos_trabalhos
    , VD4031 AS horas_semana_todos_trabalhos
FROM basedosdados.br_ibge_pnadc.microdados
"""
COLLECTED_DATA_PATH = os.path.join(os.getcwd(), "..", "data", "collected_data.csv")