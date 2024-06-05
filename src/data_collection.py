# Importing libraries
import basedosdados as bd
import config

# Initial test
df = bd.read_sql(config.SQL_QUERY, billing_project_id=config.BILLING_PROJECT_ID)
print(df.columns)
print(df.info())

