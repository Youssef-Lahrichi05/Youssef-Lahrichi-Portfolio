# 🎓 Student GPA Prediction using Linear Regression

## 📌 Project Overview
This project aims to predict students' academic performance (GPA) based on a dataset of social, personal, and educational variables. The model applies **multiple linear regression** with variable selection using the **stepwise (progressive) method**, ensuring the most significant predictors are included.

The analysis was implemented in **Python** without relying on built-in regression libraries, focusing instead on the mathematical foundations of regression.

---

## 📂 Dataset
- Source: Kaggle (2392 observations, 13 variables)
- Key features:  
  - Age, gender, origin, parental education  
  - Study time (weekly), number of absences  
  - Tutor support, parental support, extracurricular activities  
  - Sport, music, volunteer work  

**Target Variable**: GPA (Grade Point Average, 0–4 scale)

---

## 🛠️ Methods
- Manual implementation of the regression formula:  
  \[
  \hat{A} = (X'X)^{-1}X'Y
  \]
- Calculation of **R²** and **adjusted R²**
- Stepwise variable selection with correlation & Fisher test
- Model diagnostics: QQ-plot for normality, residual analysis for homoscedasticity

---

## 📊 Results
- **R² = 0.95** → Model explains 95% of GPA variance  
- Best model (stepwise) excluded volunteer variable  
- Predicted GPA for a sample student = **3.58**

**Key insights**:
- Absences, parental support, tutor involvement, and student well-being have higher influence than study hours or parental education.

---

## 📈 Visualizations
- QQ Plot → residuals approximately normal  
- Residuals vs. fitted → no heteroscedasticity observed  

---

## 🚀 Tech Stack
- Python (NumPy, pandas, matplotlib, seaborn)

---

## 📌 Conclusion
A strong linear relationship exists between social/educational factors and GPA. The model can be used to predict GPA and highlight key drivers of academic success.

