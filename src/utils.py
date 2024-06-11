"""This file contains functions used for exploration, model selection, validation, etc"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
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

def central_measurements(numeric_series: pd.Series):
    mean = numeric_series.mean()
    median = numeric_series.median()
    mode = numeric_series.mode()[0]
    result = pd.Series([mean, median, mode], index=['mean', 'median', 'mode'])
    result.sort_values(ascending=True, inplace=True)
    return result

def plot_histogram(col: pd.Series, title: str, y_label: str, x_label: str, stat='percent', binwidth=500, cumulative=False, 
                   color='#088F8F', element='bars'):
    ax = sns.histplot(col, stat=stat, binwidth=binwidth, cumulative=cumulative, color=color, element=element)
    plt.title(title)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    if element == 'step':
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

def normality_plot(col: pd.Series):
    stats.probplot(col, plot=plt)
    plt.show()

def mean_per_group(df: pd.DataFrame, group_by: str, mean_column: str):
    return df.groupby(group_by)[mean_column].mean().sort_values(ascending=False)

def show_barplot(cat: list, values: list, title: str, x_label = 'Total Monthly Income (R$)', y_label = '', color='#088F8F'):
    ax = sns.barplot(y=cat, x=values, color=color)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.title(title)
    plt.show()

def normality_test(means_array: list, confidence_interval=0.05):
    return stats.shapiro(means_array).pvalue >= confidence_interval

def check_homogeneity(means_array: list, confidence_interval=0.05):
    return stats.levene(*means_array).pvalue >= confidence_interval

def test_multiple_means(means_array: list, confidence_interval=0.05):
    """Performs hypothesis testing on multiple means to understand if differences are significant"""
    # Choosing between parametric and non-parametric tests
    if normality_test(means_array) == True and check_homogeneity(means_array) == True:
        _, pvalue = stats.f_oneway(*means_array)
    else:
        _, pvalue = stats.kruskal(*means_array)
    
    # Printing results
    if pvalue < confidence_interval:
        print('Differences were statistically significant\n p-value was: ', pvalue)
        return True
    else:
        print("Can't reject the null\n p-value was: ", pvalue)
        return False

def return_region(state):
    if state in ['RS', 'PR', 'SC']:
        return 'South'
    elif state in ['SP', 'RJ', 'MG', 'ES']:
        return 'Southeast'
    elif state in ['MT', 'MS', 'GO', 'DF']:
        return 'Center West'
    elif state in ['AL', 'BA', 'CE', 'SE', 'MA', 'PB', 'PE', 'PI', 'RN']:
        return 'Northeast'
    else:
        return 'North'

def factorize_column(rank_series: pd.Series, num_col: pd.Series):
    """This column factorizes a column based upon a numeric rank associated"""
    ranks = {}
    for rank, value in enumerate(rank_series, start=1):
        ranks[value] = rank
    factorized_column = num_col.map(ranks)
    return factorized_column

def plot_regplot(df: pd.DataFrame, numeric_columns: list, target: str):
    for num_col in numeric_columns:
        sns.regplot(data=df, x=num_col, y=target)
        plt.title(f'Relationship between {num_col} and Total Monthly Income (R$)')
        plt.show()

def plot_stripplot(df: pd.DataFrame, cat_columns: list, target: str):
    for cat in cat_columns:
        sns.stripplot(data=df, x=cat, y=target)
        plt.title(f'Relationship between {cat} and Total Monthly Income (R$)')
        plt.show()

def mutual_information(X, y, discrete_features):
    mi = mutual_info_regression(X, y, discrete_features=discrete_features)
    result = pd.Series(mi, index=X.columns)
    result.sort_values(ascending=False, inplace=True)
    return result

def show_boxplot(df, x, y, x_label, y_label, title, color='#088F8F'):
    ax = sns.boxplot(data=df, x=x, y=y, color=color)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    plt.title(title)
    plt.show()