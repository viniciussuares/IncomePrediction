"""This file contains functions used for exploration, pre-processing, model selection, validation, etc"""
from typing import Union
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from scipy.stats.mstats import winsorize
from sklearn.feature_selection import mutual_info_regression

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
    print("Nulls Percentage by Column: ")
    return mapped_nulls

def winsorize_columns(df: pd.DataFrame, lower_percentil: float= 0.01, upper_percentil: float=0.01):
    """This function winsorizes all columns in a dataframe based on the specied percentils"""
    df_winsorized = df.copy()
    for col in df.columns:
        df_winsorized[col] = winsorize(df[col], limits=(lower_percentil, upper_percentil))
    return df_winsorized

def plot_histogram(col: pd.Series, title: str, y_label: str, x_label: str, bins='auto', stat='percent', cumulative=False, 
                   color='#088F8F', element='bars'):
    ax = sns.histplot(col, stat=stat, cumulative=cumulative, color=color, element=element, bins=bins)
    plt.title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if element == 'step':
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

def normality_plot(col: pd.Series):
    stats.probplot(col, plot=plt)
    plt.show()

def return_region(state):
    if state in ['RS', 'PR', 'SC']:
        return 1 #South
    elif state in ['SP', 'RJ', 'MG', 'ES']:
        return 2 #Southeast
    elif state in ['MT', 'MS', 'GO', 'DF']:
        return 3 #Center West
    elif state in ['AL', 'BA', 'CE', 'SE', 'MA', 'PB', 'PE', 'PI', 'RN']:
        return 4 #Northeast
    else:
        return 5 #North

def plot_regplot(df: pd.DataFrame, numeric_columns: list, target: str, x_label = '', y_label='Total Monthly Income (R$)', 
                 color='#088F8F', robust=True, ci=None):
    for num_col in numeric_columns:
        ax = sns.regplot(data=df, x=num_col, y=target, color=color, robust=robust, ci=ci)
        ax.set_ylabel(y_label)
        ax.set_xlabel(num_col)
        plt.title(f'Relationship between {num_col} and Income')
        plt.show()

def plot_stripplot(df: pd.DataFrame, cat_columns: list, target: str, color='#088F8F', y_label=''):
    for cat in cat_columns:
        ax = sns.stripplot(data=df, x=cat, y=target, color=color)
        ax.set_ylabel(y_label)
        ax.set_xlabel(cat)
        plt.title(f'Income Distribution between Groups in {cat}')
        plt.show()

def mutual_information(X, y, discrete_features):
    mi = mutual_info_regression(X, y, discrete_features=discrete_features)
    result = pd.Series(mi, index=X.columns)
    result.sort_values(ascending=False, inplace=True)
    return result

def show_barplot(cat: list, values: list, title: str, x_label = 'Total Monthly Income (R$)', y_label = '', color='#088F8F'):
    ax = sns.barplot(y=cat, x=values, color=color)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.title(title)
    plt.show()

def check_spearmanr(num_df: pd.DataFrame, target=Union[np.array, pd.Series], confidence_interval=0.05):
    """This function uses spearman correlation from scipy stats to calculate the association and a p-value for 2 array_like objects"""
    # Performing the test
    corr_matrix, pvalues = stats.spearmanr(num_df, target)

    # Creating labels
    x_labels = list(num_df.columns)
    y_labels = list(num_df.columns)
    x_labels.append(target.name)
    y_labels.append(target.name)

    # Returning results
    if (pvalues > confidence_interval).any():
        print('Cannot assume correlation between all columns')
        return
    else:
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', robust=True, xticklabels=x_labels, yticklabels=y_labels)
        plt.title('Spearman Correlation Between Numeric Columns')
        plt.show()

def test_differences_subgroups(df: pd.DataFrame, cols_to_test: list, target: str='all_work_income', confidence_interval=0.05):
    """This function uses non-parametric tests to assess if differences between 2 or more groups are statistically significant"""
    result = []
    for col in cols_to_test:
        unique_groups = df[col].unique()
        arrays = []
        for unique in unique_groups:
            array = np.array(df.loc[df[col] == unique, target])
            arrays.append(array)
        if len(arrays) == 2:
            _, pvalue = stats.mannwhitneyu(arrays[0], arrays[1])
        elif len(arrays) > 2:
            _, pvalue = stats.kruskal(*arrays)
        result.append(f'{pvalue >= confidence_interval}, p-value was {pvalue}, stats was {_}')
    print('Income means are no different between groups within new features?')
    return pd.Series(result, index=cols_to_test)

def show_pairplot(df: pd.DataFrame, selected_columns: list, diag_kind = 'kde', corner=True):
    # joins target to selected column
    if 'all_work_income' not in selected_columns:
        selected_columns.insert(0, 'all_work_income')
    
    plt.figure(figsize=(15,15))
    sns.pairplot(data=df[selected_columns], diag_kind=diag_kind, corner=corner)
    plt.show()

def show_scatterplot(df: pd.DataFrame, x: str, y: str='all_work_income', hue=None, ylabel='Total Monthly Income (R$)'):
    ax = sns.scatterplot(data=df, x=x, y=y, hue=hue)
    ax.set_ylabel(ylabel)
    plt.show()

def discretize_age(age: int):
    if age < 18: # minors
        return 1
    elif age < 25: # adults problem not achieved a stable career or graduation
        return 2
    elif age < 65: # mature professionals
        return 3
    else:
        return 4 # retired
    
def discretize_weekly_worked_hours_all_jobs(hours: int):
    if hours <= 20: # part-time
        return 1
    elif hours <= 40: # in between part and full time
        return 2
    elif hours <= 60: # full time and second part time job
        return 3
    elif hours <= 80: # up to 2 full time jobs
        return 4
    else:
        return 5 #

def discretize_years_studied(years: int):
    if years <= 9: # elemntary school
        return 1
    elif years <= 13: # high-school
        return 2
    else:
        return 3 # some college degree