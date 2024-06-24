# Income Prediction Based on Sociodemographic Variables

## Objective

This project aims to develop a machine learning model to estimate the monthly income of individuals based on sociodemographic and occupational variables, using microdata from the National Household Sample Survey (PNAD) collected by the Brazilian Institute of Geography and Statistics (IBGE).

## Problem and Relevance

Accurate income prediction is essential for:

- **Market Segmentation:** Enhancing targeted marketing and increasing ROI.
- **Credit Policies:** Reducing default rates and improving credit portfolio profitability
- **Product Personalization:** Tailoring offers to consumer purchasing power, boosting customer satisfaction.

## Key Results
- **Accuracy and Final Estimated MAE:** Around 70% of predictions fall within a R$ 780 Mean Absolute Error.
- **Limitations:**
   - Time: Model was trained for the year 2023 only.
   - Income Scope: Considered salaries up to R$ 10,000/month (which represented 97% of the dataset ~ 770,000 observations)
   - Predictions Confidence: Lower salary ranges (up to R$ 4,000 or ~ 85% of the dataset) had significantly lower MAE (< R$ 1000). 

## Project Structure

1. **Data Collection**
   - **Initial Selection:** Chose relavant columns based on domain knowledge, intuition and the available data dictionaries. 
   - **Data Retrieval:** Used SQL through Python to request data from Base dos Dados public Data Lake on BigQuery.
   - **Results:** Collected 794,507 rows and 15 columns, saving in a compressed CSV file 
   - **Performance**: Query completed in approximately 2 minutes

2. **Exploratory Data Analysis**
   - **Data Cleaning**: 
      - Identified and removed outliers across the entire using unsupervised learning (Isolation Tree Method).
   - **Univariate Analysis**: 
      - Analyzed income to understand its distribution and key statistics.
      - Found that nearly 100% of respondents earned up to R$ 10,000 per month.
      ![Income Cumulative Distribution](./images/income%20cumulative%20distribution.png)
   - **Bivariate Analysis**: 
      - Explored relationships between pairs of variables using scatterplots, strip plots, and heatmaps.
      - Applied mutual information and hypothesis testing to assess the strength of associations.
      ![Heatmap Numeric Columns](./images/spearman%20corr.png)
   - **Multivariate Analysis**: 
      - Examined interactions among multiple variables using pairplots.
      - Focused on key segments to identify patterns and correlations.
      ![Pairplot between main variables](./images/pairplot.png)
   - **Feature Engineering**: 
      - Developed new features to capture hidden relationships within the data.
      - Example: Created a feature to discretize studied years.
      ![New feature to discretize studied years](./images/discretized%20years%20studied.png)

3. **Model Production**
   - **Pre-processing:** Created a Sklearn Pipeline for feature engineering and target encoding to avoid data leakage.
   - **Model Selection:** Tested 4 tree-based models because the reasoning to determine salary follows a tree-thought process:
      - Random Forest (RF)
      - LightGBM (LGBM)
      - Stacked (RF first, then LGBM)
      - Averaged (RF and LGBM at the same time)
      ![4 Models Evaluation](./images/mae%20per%20fold%20per%20model.png)

   - **Model Evaluation:** Employed cross_validation, data visualization, hypothesis testing, and a combination of metrics to assess model performance.
      - Hypothesis testing + CV:
      ![Post Hoc p-values](./images/post-hoc%20p-values.png)
      - Sample Analysis:
      ![Real x Predicted 100 Sample](./images/real%20x%20predicted.png)
      - MAE Analysis:
      ![MAE Analysis](./images/mae%20x%20cumulative%20%20x%20income%20range.png)

   - **Future Improvements:**
      - Bring data from different survey questions.
      - Advanced feature engineering.
      - Using other class of models (e.g., neural networks).
      - Training complementary models specialized in higher income ranges.

4. **API Development:**
   - In construction..


## Technologies Used

- **Programming Language:** Python (3.9.19), HTML
- **Data Science Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn, LGBM, Scipy
- **API Framework:** Flask
- **Deployment Platforms:** Heroku

## Installation

To install the necessary dependencies, run the following command:
```sh
pip install -r requirements.txt
```

## Contribution
Feel free to contribute with suggestions, improvements, or corrections. To contribute:

1. Fork this repository.
2. Create a branch with your feature (git checkout -b feature/new-feature).
3. Commit your changes (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature/new-feature).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For more information, contact me at [my email](mailto:v.suares.s@hotmail.com).