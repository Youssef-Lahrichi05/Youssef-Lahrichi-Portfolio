# 🌿 NDVI Analysis in Morocco (2010–2024)
### Satellite Data Extraction (Google Earth Engine) • Data Cleaning • Power BI Dashboard

---

## 📌 Project Overview

This project analyzes the evolution of vegetation in Morocco between **2010 and 2024** using satellite data extracted from **Google Earth Engine (GEE)**.  
The main indicator studied is the **Normalized Difference Vegetation Index (NDVI)**, combined with key climatic and environmental variables:

- 🌧 Precipitation (CHIRPS)
- 🌡 Temperature (ERA5-Land)
- ☀️ Luminosity (VIIRS radiance)
- 🏭 CO₂ emissions

The objective is to explore:

- NDVI trends over time  
- Regional vegetation disparities  
- Seasonal patterns  
- Correlation between NDVI and climatic factors  
- Impact of drought and climate variations on vegetation dynamics  

Data extraction, processing, and visualization are documented in detail in the project report. :contentReference[oaicite:0]{index=0}

---

## 🛰 1. Data Extraction (Google Earth Engine)

Satellite data is extracted entirely using **Python + Google Earth Engine API**, following the workflow in the report.

### ✔ Datasets Used
- **Administrative boundaries:**  
  `FAO/GAUL_SIMPLIFIED_500m/2015/level1`
- **NDVI:** MODIS NDVI collection
- **Precipitation:** CHIRPS (monthly sum)
- **Temperature:** ERA5-Land (monthly mean)
- **CO₂:** CO₂ concentration dataset
- **Luminosity:** VIIRS Nighttime Lights (monthly mean radiance)

### ✔ Extraction Logic
For each year (2010–2024) and month (1–12), the script:

1. Filters each dataset by date  
2. Computes monthly mean for NDVI, temperature, CO₂, luminosity  
3. Computes monthly sum for precipitation  
4. Combines all variables into a single multiband image  
5. Reduces it over Moroccan regions  
6. Outputs a clean monthly panel  
7. Flattens and exports everything to CSV on Google Drive  

The exact Python script is shown in pages 4–6 of the PDF. :contentReference[oaicite:1]{index=1}

---

## 📁 2. Dataset Structure

The extracted CSV (p. 7) contains the following columns: :contentReference[oaicite:2]{index=2}

| Column | Description |
|--------|-------------|
| `AD0_NAME` | Country (Morocco) |
| `ADM1_NAME` | Region |
| `year` | Year (2010–2024) |
| `month` | Month (1–12) |
| `ndvi` | NDVI monthly mean |
| `precip_mm` | Precipitation sum (mm) |
| `t2m_c` | Temperature (°C) |
| `co_col_mol_m2` | CO₂ concentration |
| `viirs_rad` | Luminosity (VIIRS radiance) |

Notes:  
- Luminosity available only from **July 2011** onward  
- CO₂ available only from **2018** onward  

---

## 🧹 3. Data Cleaning (Power BI)

Cleaning and feature engineering were performed in **Power BI**, as described on page 8 of the report. :contentReference[oaicite:3]{index=3}

### Added Features:
- **Date** (Year–Month combined)
- **Season** (Winter, Spring, Summer, Autumn)
- **Variation** (Δ NDVI between year *k* and *k–1*)
- **Variation Category** (Increase / Decrease / No Change)

After cleaning, the dataset is ready for visualization.

---

## 📊 4. Data Visualization (Power BI Dashboard)

The dashboard includes:

### ✔ General NDVI Analysis
- Overall NDVI mean, max, min (p. 9)
- NDVI by region  
- NDVI by month  
- NDVI by season  
- NDVI by year  
- Maps showing regional vegetation strength  

Key insights:
- NDVI is **higher in north & west** regions  
- NDVI is **lower in south & east**  
- Strong seasonality in northern regions (max in winter–spring)  
- Minimal seasonality in southern regions  
- NDVI reached minimum values in **2022–2024** due to drought

---

## 🔗 5. Correlation With Climatic Factors

Correlation results (pp. 12–16): :contentReference[oaicite:4]{index=4}

| Factor | Correlation with NDVI | Interpretation |
|--------|------------------------|----------------|
| **Precipitation** | **+0.90** | Very strong positive correlation |
| **Luminosity (VIIRS)** | **+0.86** | Strong positive correlation |
| **Temperature** | **–0.36** | Moderate negative correlation |
| **CO₂ emissions** | Negative (after removing outliers) | CO₂ harms vegetation |

---

## 🧾 6. Summary of Findings

From 2010 to 2024 (p. 17): :contentReference[oaicite:5]{index=5}

- Morocco experienced **more NDVI decreases than increases**  
- Major NDVI drop in **2016**, explained by minimal precipitation in **2015**  
- NDVI decline from **2022 → 2024** confirmed by drought data  
- NDVI is strongly influenced by rainfall and luminosity  
- Vegetation is significantly healthier in **northern and western** regions  

---

## 🧭 7. Conclusion

This project provides a clear overview of Morocco’s vegetation dynamics, highlights climatic impacts, and identifies regions with the highest potential for vegetation development.  
It also establishes a strong foundation for future environmental monitoring and data-driven agricultural planning.

---

## 🧑‍💻 Author
**Lahrichi Youssef – Data Science – INSEA**  
NDVI Vegetation Report (2010–2024)

---

