import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src')) # Adding src to the system path
from flask import Flask, request, render_template, jsonify
from joblib import load
import config
import pandas as pd
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Declare Objects
app = Flask(__name__)
model = load(config.TRAINED_MODEL_PATH)

# App util functions
def validate_features(input_features: dict, validation_dict: dict=config.INPUT_VALIDATION):
    """
    This function validates if input features are in accordance with validation_dict
    Input: input_features: features from HTML/JSON, validation_dict: dict with all possible values for each feature
    Output: whether all features are valid, error message, features"""
    # Initialize variables
    features_are_valid = True
    error = None
    return_features = {key: int(value) if key != 'state' else value for key, value in input_features.items()} # converts to input to int

    # Validates
    for key in return_features.keys():
        if return_features[key] not in validation_dict[key]:
            features_are_valid = False
            error = {'error': f'{return_features[key]} not in acceptable values for {key}'}
            logging.debug(f"Input Error: {error}")  # Debug: Log prediction error
            return_features = None
            return features_are_valid, error, return_features
    
    logging.debug('All input features were valid')
    return features_are_valid, error, return_features

def make_prediction(valid_input: dict, features_names: list=config.FEATURES):
    """
    This function makes predictions based on features provided
    Input: A valid input dictionary, and a feature names list
    Output: prediction: float, error: dict"""
    try:
        X = pd.DataFrame([valid_input]) # converts input dictionary in a list and them in a DF with 13 columns and 1 row
        X.columns = features_names
        prediction = model.predict(X)
    except Exception as e:
        error = {'error_message': 'Prediction failed', 'details': str(e)}
        logging.debug(f"Prediction Error: {error}")  # Debug: Log prediction error
        return None, error
    
    logging.debug('Prediction made succesfully')
    return prediction[0], None

def adjust_prediction(prediction_2023: float):
    """
    This function adjusts the 2023 prediction to the current year
    """
    current_year = datetime.now().year
    years_to_ajust = current_year - 2023
    return prediction_2023 + years_to_ajust * 115.10836311843748

# App Routes

@app.route('/')
def home():
    """Renders homepage"""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Predicts monthly income"""
    features_are_valid, error, return_features = validate_features(dict(request.form))
    if features_are_valid:
        prediction, error = make_prediction(return_features)

        if error:
            return jsonify(error), 500
        
        # Declare return variables
        prediction_2023 = prediction
        prediction_adjusted = adjust_prediction(prediction_2023)
        prediction_2023_usd = prediction_2023 / 5
        prediction_adjusted_usd = prediction_adjusted / 5

        logging.debug('Response returned successfully')
        return jsonify({
            'prediction_2023': prediction_2023,
            'prediction_adjusted': prediction_adjusted,
            'prediction_2023_usd': prediction_2023_usd,
            'prediction_adjusted_usd': prediction_adjusted_usd
        })
    
    else:
        logging.debug('Request failed')
        return jsonify(error), 422

if __name__ == '__main__':
    app.run(debug=config.DEBUG_MODE)