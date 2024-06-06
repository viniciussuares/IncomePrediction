# Importing libraries
import basedosdados as bd
import pandas as pd
import config

def query_datalake(sql_query: str, billing_project_id: str):
    return bd.read_sql(sql_query, billing_project_id)

def save_data(df: pd.DataFrame, file_path: str, index=False):
    df.to_csv(file_path, index=index, compression='gzip')

def main():
    try:
        df = query_datalake(config.SQL_QUERY, config.BILLING_PROJECT_ID)
        save_data(df, config.COLLECTED_DATA_PATH)
        lines, columns = df.shape
        print(f"{lines} lines and {columns} columns collected and saved successfully!")
    except Exception as e:
        print(f"An error ocurred: {e}")

if __name__ == "__main__":
    main()