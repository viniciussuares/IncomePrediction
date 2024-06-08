"""This file contains functions used for exploration, model selection, validation, etc"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# EDA
def read_compressed_data(data_path: str, compression='gzip'):
    return pd.read_csv(data_path, compression=compression)

def nulls_percentage(df: pd.DataFrame):
    print("Null Percentage by Column: ")
    print("---"*20)
    print(df.isnull().mean().round(2) * 100)

def formatted_description(df: pd.DataFrame):
    return df.describe().iloc[1:, :].round(1)

def outlier_percentage(df: pd.DataFrame):
    """Uses the fence method to identify the percentage of outliers per column"""
    total_rows = df.shape[0]
    result = {}
    for col in df.columns:
        q1 = df[col].quantile(.25)
        q3 = df[col].quantile(.75)
        iqr = q3 - q1
        inner_fence = df.loc[(df[col] < q1 - 1.5*iqr) | (df[col] > q3 + 1.5*iqr)].shape[0]
        outer_fence = df.loc[(df[col] < q1 - 3*iqr) | (df[col] > q3 + 3*iqr)].shape[0]
        result[col] = [f'{inner_fence/total_rows * 100: .2f}%', f'{outer_fence/total_rows * 100: .2f}%']
    
    print('Percentage of Outliers per Column: ')
    return pd.DataFrame(result, index=['Inner Fence', 'Outer Fence']).T
