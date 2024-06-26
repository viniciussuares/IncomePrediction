# Adding src to the system path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask, request, render_template, jsonify
from joblib import load
import config
import numpy as np
import pandas as pd

app = Flask(__name__)

model = load(config.TRAINED_MODEL_PATH)

# Render HTML
@app.route('/')
def home():
    return render_template('index.html')

# Predict
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Coleta os dados do formulário e tenta convertê-los para inteiros (exceto 'state')
        features = [
            request.form['state'],
            int(request.form['age']),
            int(request.form['sex']),
            int(request.form['race']),
            int(request.form['literate']),
            int(request.form['educational_level']),
            int(request.form['studied_years']),
            int(request.form['worker_type']),
            int(request.form['work_segment']),
            int(request.form['occupation_group']),
            int(request.form['tax_payer']),
            int(request.form['hours_range']),
            int(request.form['hours_value']),
        ]
    except (ValueError, KeyError) as e:
        return jsonify({'error': 'Invalid input data', 'details': str(e)}), 422

    # Validação dos valores de entrada
    if (features[0] not in config.STATES or
        not (14 <= features[1] <= 120) or
        features[2] not in [1, 2] or
        features[3] not in [1, 2, 3, 4, 5, 9] or
        features[4] not in [1, 2] or
        features[5] not in range(1, 8) or
        features[6] not in range(0, 17) or
        features[7] not in range(1, 10) or
        features[8] not in range(1, 13) or
        features[9] not in range(1, 12) or
        features[10] not in [1, 2] or
        features[11] not in range(1, 6) or
        not (0 <= features[12] <= 120)):
        return jsonify({'error': 'Invalid input values', 'features': features}), 422

    # Converts input to a DataFrame
    try:
        valid_input = pd.DataFrame([features], columns=[
            'state', 'age', 'sex', 'race', 'literate', 'highest_educational_level',
            'years_studied', 'worker_type', 'work_segment', 'occupation_group',
            'tax_payer', 'weekly_worked_hours', 'weekly_worked_hours_all_jobs'])
        
        # Predicts
        prediction = model.predict(valid_input)
    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e), 'features': features}), 500

    # Dummy values for additional outputs for testing purposes
    prediction_2023 = prediction[0]
    prediction_adjusted = prediction_2023 * 1.05  # Example adjustment
    prediction_2023_usd = prediction_2023 / 5.0   # Example conversion rate
    prediction_adjusted_usd = prediction_adjusted / 5.0

    return jsonify({
        'prediction_2023': prediction_2023,
        'prediction_adjusted': prediction_adjusted,
        'prediction_2023_usd': prediction_2023_usd,
        'prediction_adjusted_usd': prediction_adjusted_usd
    })

if __name__ == '__main__':
    app.run(debug=config.DEBUG_MODE)
