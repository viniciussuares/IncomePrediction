from typing import Callable
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from category_encoders import TargetEncoder
import utils

class AddFeature(BaseEstimator, TransformerMixin):
    """This class adds a new feature based on a function that maps a previous existing column"""

    def __init__(self, existing_column: str, new_feature_name: str, function: Callable):
        self.existing_column = existing_column 
        self.new_feature_name = new_feature_name 
        self.function = function
    
    def fit(self, X, y=None):
        # raises an error if column does not exist. Otherwise does nothing
        if self.existing_column not in X.columns:
            raise ValueError(f'{self.existing_column} not found in input columns')
        return self
    
    def transform(self, X):
        # performs mapping
        X_copy = X.copy()
        X_copy[self.new_feature_name] =X[self.existing_column].map(self.function)
        return X_copy
    
class CategoricalTargetEncoder(BaseEstimator, TransformerMixin):
    """This class builds a transformer to encode categorical columns based on the target mean for each value"""

    def __init__(self, smoothing=1):
        self.smoothing = smoothing  # term to smooth the average
        self._columns = []  
        self._target_means_ = {}  
        self._global_mean_ = None  
    
    def fit(self, X, y):
        # Defines important variables
        X = pd.DataFrame(X)
        y = pd.Series(y)
        concat = pd.concat([X, y], axis=1)

        # Updates self
        self._columns = list(X.columns)
        self._global_mean_ = y.mean()

        # For each column, obtain the grouped mean, smooth it, and populate the target means dictionary
        for col in self._columns:
            col_means = concat.groupby(col)[y.name].mean()
            counts = concat.groupby(col).size()
            smoothed_means = (counts * col_means + self.smoothing * self._global_mean_) / (counts + self.smoothing)
            self._target_means_[col] = smoothed_means
        
        return self
    
    def transform(self, X):
        # Making sure it will work with DataFrame
        X = pd.DataFrame(X)
        X_transformed = X.copy()

        # For each column, transform it using the dictionary previously populated
        for col in self._columns:
            X_transformed[col] = X[col].map(self._target_means_[col]).fillna(self._global_mean_)
        
        return X_transformed
    
def target_trimming(df: pd.DataFrame, target: str, threshold: float=10000.00):
    """
    This function trims the dataset to contain observations only up to a certain threshold.
    In the collected data, 97% of respondents earned up to R$ 10,000.00, thus it became the standard threshold for this function
    """
    return df.loc[df[target] <= threshold, :]
    

def divide_train_test(df: pd.DataFrame, features: list, target: str, random_state: int=0, test_size: float=0.25, 
                      target_threshold: float=10000.00):
    """This function calls target_trimming and then divides the data into training and testing"""
    trimmed_df = target_trimming(df, target, target_threshold)

    X = trimmed_df[features]
    y = trimmed_df[target]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)

pre_processing = Pipeline(
    steps=[
        ('add region', 
         AddFeature('state', 'region', utils.return_region)),
        ('add white mixed-race', 
         AddFeature('race', 'white_mixed_race', utils.return_white_mixed_race)),
        ('add high school or beyond', 
         AddFeature('highest_educational_level', 'high_school_or_beyond', utils.return_high_school_or_beyond)),
        ('add domestic worker', 
         AddFeature('worker_type', 'domestic_worker', utils.return_domestic_worker)),
        ('add selected segments', 
         AddFeature('work_segment', 'selected_segments', utils.return_selected_segments)),
        ('add age range', 
         AddFeature('age', 'age_range', utils.discretize_age)),
        ('add weekly_worked_hours_v2', 
         AddFeature('weekly_worked_hours_all_jobs', 'weekly_worked_hours_v2', utils.discretize_weekly_worked_hours_all_jobs)),
        ('add studied years', 
         AddFeature('years_studied', 'studied_years_v2', utils.discretize_years_studied)),
        ('target encoder', TargetEncoder())
    ]
)