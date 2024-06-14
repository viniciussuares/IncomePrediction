import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OrdinalEncoder
import utils
import config

class CategoricalTargetEncoder(BaseEstimator, TransformerMixin):
    """This class builds a transformer to encode categorical columns based on the target mean for each value"""

    def __init__(self, columns=None, smoothing=1):
        self.columns = columns  # columns from estimator
        self.smoothing = smoothing  # term to smooth the average
        self._target_means_ = {}  # dict to be populated during fit
        self._global_mean_ = None  # will be assigned during fit 
    
    def fit(self, X, y):
        # Making sure it will work with DataFrame and Series
        X = pd.DataFrame(X)
        y = pd.Series(y)

        # Finds global mean and updates self
        self._global_mean_ = y.mean()

        # For each column, obtain the grouped mean, smooth it, and populate the target means dictionary
        for col in self.columns:
            col_means = X.groupby(col)[y.name].mean()
            counts = X.groupby(col).size()
            smoothed_means = (counts * col_means + self.smoothing * self._global_mean_) / (counts + self.smoothing)
            self._target_means_[col] = smoothed_means
        
        return self
    
    def transform(self, X):
        # Making sure it will work with DataFrame
        X = pd.DataFrame(X)
        X_transformed = X.copy()

        # For each column, transform it using the dictionary previously populated
        for col in self.columns:
            X_transformed[col] = X[col].map(self._target_means_[col]).fillna(self._global_mean_)
        
        return X_transformed