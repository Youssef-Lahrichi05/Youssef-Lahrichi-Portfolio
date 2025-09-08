# 📈 Time Series Forecasting of Product Sales (ARIMA/SARIMA)

## 📌 Project Overview
This project applies the **Box–Jenkins methodology** to model and forecast monthly product sales using ARIMA and SARIMA models. The goal is to anticipate demand trends, identify seasonality, and provide reliable short- and medium-term forecasts.

---

## 📂 Dataset
- Source: Kaggle  
- Period: **January 1964 – September 1972**  
- Variables: Date (monthly), Sales (units sold)  

---

## 🛠️ Methods
1. **Data Preparation**  
   - Date parsing, duplicate removal  
   - Handling missing values via linear interpolation  
   - Train-test split (90% train, 10% test)

2. **Exploratory Analysis**  
   - Trend: clear upward growth in sales  
   - Seasonality: yearly peaks observed  

3. **Stationarity Check**  
   - Augmented Dickey-Fuller test  
   - Differencing (d=1) applied → stationarity achieved  

4. **Model Identification (Box–Jenkins)**  
   - ACF/PACF inspection → SARIMA candidate models  
   - Tested models:  
     - SARIMA(1,1,1)(1,1,0,12)  
     - SARIMA(1,1,0)(1,1,0,12)  
     - SARIMA(0,1,1)(1,1,0,12)  

5. **Model Selection & Validation**  
   - Chosen model: **SARIMA(1,1,1)(1,1,0,12)**  
   - Criteria: lowest AIC, significant coefficients, Ljung–Box test passed  

---

## 📊 Results
- Performance on test set:  
  - **RMSE = 531.74**  
  - **MAE = 430.79**  
- Forecasts capture both trend and seasonality well  
- 2-year forecast: sales between **2000 – 13,500 units**  

---

## 📈 Visualizations
- Sales trends & seasonality plots  
- ACF/PACF graphs  
- Predicted vs. actual values with 95% confidence intervals  

---

## 🚀 Tech Stack
- Python (pandas, numpy, statsmodels, matplotlib, seaborn)  

---

## 📌 Conclusion
The SARIMA(1,1,1)(1,1,0,12) model effectively predicts sales, confirming the presence of trend and yearly seasonality. This approach provides valuable insights for inventory management, production planning, and marketing decisions.
