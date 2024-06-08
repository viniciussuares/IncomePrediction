"""This file contains functions used for exploration, model selection, validation, etc"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# EDA
def read_compressed_data(data_path: str, compression='gzip'):
    return pd.read_csv(data_path, compression=compression)

def make_percentage(float: float):
    """Transforms a float between 0 and 1 into a string percentage"""
    if 0 <= float <= 1:
        return f'{float * 100: .2f}%'
    else:
        return None

def nulls_percentage(df: pd.DataFrame):
    nulls_per_column = df.isnull().mean()
    mapped_nulls = nulls_per_column.sort_values(ascending=False).map(make_percentage)
    print("Null Percentage by Column: ")
    return mapped_nulls

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
        result[col] = [make_percentage(inner_fence/total_rows), make_percentage(outer_fence/total_rows)]
    
    print('Percentage of Outliers per Column: ')
    return pd.DataFrame(result, index=['Inner Fence', 'Outer Fence']).T

def winsorizing_outliers(c: pd.Series, fence='outer'):
    """Winsorizes a column or Series using the fence method to deal with outliers"""
    col = c.copy()
    
    q1 = col.quantile(.25)
    q3 = col.quantile(.75)
    iqr = q3 - q1

    if fence == 'outer':
        iqr *= 3
    elif fence == 'inner':
        iqr *= 1.5
    else:
        return "Unknown fence method"
    
    floor = q1 - iqr
    ceiling = q3 + iqr

    col.loc[col < floor] = floor 
    col.loc[col > ceiling] = ceiling

    return col
    