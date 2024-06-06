# Income Prediction Based on Sociodemographic Variables

## Overview

This project aims to develop a machine learning model to estimate the annual income of individuals based on sociodemographic and occupational variables, using microdata from the National Household Sample Survey (PNAD) collected by the Brazilian Institute of Geography and Statistics (IBGE).

## Problem Description and Understanding

Income prediction is a crucial tool for businesses and financial institutions aiming to optimize their marketing strategies, market segmentation, and credit policies. The ability to accurately predict an individual's income can result in significant improvements in the efficiency and effectiveness of advertising campaigns and credit granting.

### Importance and Relevance
- **Market Segmentation:** Enables the creation of targeted marketing campaigns, increasing conversion rates and optimizing return on investment (ROI).
- **Credit Policies:** Helps financial institutions reduce default rates and improve the profitability of credit portfolios.
- **Product Personalization:** Companies can adjust offers and products according to consumers' purchasing power, increasing customer satisfaction.

## Project Structure

1. **Data Collection**
   - Used intuition and common sense to select a few initial relevant columns
   - Requested data from BigQuery Data Lake using a SQL string through Python
   - Collected 2,207,251 rows and 17 columns, saving in a compressed CSV file 
   - Took around 5 minutes for the query to complete

2. **Exploratory Data Analysis**
   - Visualizations to understand the distribution of variables and their relationship with income.
   - Calculation of correlation between independent variables and income.

3. **Modeling**
   - Split data into training and testing sets.
   - Test various machine learning models (Linear Regression, Random Forest, Gradient Boosting).
   - Evaluate model performance (MAE, RMSE, R²).

4. **API Development**
   - Develop API using Flask or FastAPI.
   - Create endpoints for data input and income estimation output.
   - Deploy API on cloud platforms (AWS, Heroku, Azure).

5. **API Testing and Validation**
   - Unit and integration testing to ensure API functionality.
   - Collect user feedback for continuous improvement.

## Technologies Used

- **Programming Language:** Python
- **Data Science Libraries:** Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
- **API Framework:** Flask or FastAPI
- **Deployment Platforms:** AWS, Heroku, Azure

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