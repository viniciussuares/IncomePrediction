# GENERAL LIBRARIES
import os 




# DATA COLLECTION

# Connection to Bigquery
BILLING_PROJECT_ID = "incomeprediction-425511"

SQL_QUERY = """
SELECT
    sigla_uf AS state
    , V2009 AS age
    , V2007 AS sex
    , V2010 AS race
    , V3001 AS literate
    , VD3004 AS highest_educational_level
    , VD3005 AS years_studied
    , VD4009 AS worker_type
    , VD4010 AS work_segment
    , VD4011 AS occupation_group
    , VD4012 AS tax_payer
    , VD4013 AS weekly_worked_hours
    , VD4016 AS main_work_income
    , VD4019 AS all_work_income
    , VD4031 AS weekly_worked_hours_all_jobs
FROM 
    basedosdados.br_ibge_pnadc.microdados
WHERE
    ano = 2023
    AND VD4015 <> '2' -- excludes people not payed in money for their work""" 

# Saving collected data
CURRENT_DIR = os.path.dirname(__file__)

DATA_FOLDER = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data"))

COLLECTED_DATA_PATH = os.path.join(DATA_FOLDER, "collected_data.gz")






# PRE-PROCESSING

FEATURES = ['state', 'age', 'sex', 'race', 'literate', 'highest_educational_level', 'years_studied', 'worker_type', 'work_segment', 
                'occupation_group', 'tax_payer', 'weekly_worked_hours', 'weekly_worked_hours_all_jobs']

TARGET = 'all_work_income'







# MODEL BUILDING
MODEL_FOLDER = os.path.abspath(os.path.join(CURRENT_DIR, "..", "model"))

TRAINED_MODEL_PATH = os.path.join(MODEL_FOLDER, "model.joblib")







# FLASK API
INPUT_VALIDATION = {
    'state': ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 
              'RO', 'RR', 'SC', 'SP', 'SE', 'TO'],
    'age': range(14, 121),
    'sex': [1, 2],
    'race': [1, 2, 3, 4, 5, 9],
    'literate': [1, 2],
    'educational_level': range(1, 8),
    'studied_years': range(0, 17),
    'worker_type': range(1, 10),
    'work_segment': range(1, 13),
    'occupation_group': range(1, 12),
    'tax_payer': [1, 2],
    'hours_range': range(1, 6),
    'hours_value': range(0, 121)
}

DEBUG_MODE = True	