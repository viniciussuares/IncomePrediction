"""This file contains functions used for exploration, model selection, validation, etc"""
import pandas as pd

# EDA
def read_compressed_data(data_path: str, compression='gzip'):
    return pd.read_csv(data_path, compression=compression)

def nulls_percentage(df: pd.DataFrame):
    print("Null Percentage by Column: ")
    return df.isnull().mean().round(2) * 100