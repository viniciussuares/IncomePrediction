"""This file contains functions used for exploration, model selection, validation, etc"""
import pandas as pd

def read_compressed_data(data_path: str, compression='gzip'):
    return pd.read_csv(data_path, compression=compression)
