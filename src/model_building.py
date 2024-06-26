import config
from utils import read_compressed_data
from preprocessing import pre_processing, target_trimming
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, VotingRegressor
from lightgbm import LGBMRegressor
from joblib import dump

def create_x_y(data_path: str, target: str, features: list):
    df = read_compressed_data(data_path)
    trimmed_df = target_trimming(df, target)
    X = trimmed_df[features]
    y = trimmed_df[target]
    return X, y

def instantiate_final_model():
    random_forest = RandomForestRegressor(min_samples_split=16)
    random_forest_pipeline = Pipeline(steps=[('pre-processing', pre_processing), ('model', random_forest)])
    light_gbm = LGBMRegressor(n_estimators=500, force_row_wise=True, num_leaves=200)
    light_gbm_pipeline = Pipeline(steps=[('pre-processing', pre_processing), ('model', light_gbm)])
    return VotingRegressor(estimators=[('Random Forest', random_forest_pipeline), ('Light GBM', light_gbm_pipeline)])

def train_final_model(final_model, X, y):
    final_model.fit(X, y)
    print('Model trained successfully!')

def save_final_model(final_model, path):
    dump(final_model, path, compress=True)
    print('Model saved successfully!')
    
def main():
    X, y = create_x_y(config.COLLECTED_DATA_PATH, config.TARGET, config.FEATURES)
    final_model = instantiate_final_model()
    train_final_model(final_model, X, y)
    save_final_model(final_model, config.TRAINED_MODEL_PATH)

if __name__ == '__main__':
    main()