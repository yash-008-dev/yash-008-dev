# Traffic Demand Prediction Using Geospatial, Temporal, and Environmental Features

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![CatBoost](https://img.shields.io/badge/CatBoost-FFCC00?style=for-the-badge)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

</div>

<div align="center">

Geospatial Analytics • Traffic Forecasting • Machine Learning • Feature Engineering • Regression Modeling

</div>

---

## Overview

Traffic congestion remains one of the most critical challenges in modern urban transportation systems. Accurate traffic demand forecasting enables transportation authorities, ride-sharing platforms, logistics providers, and city planners to optimize infrastructure utilization, improve route planning, reduce congestion, and enhance commuter experiences.

This project presents an end-to-end machine learning solution for predicting traffic demand using a combination of:

- Geospatial information
- Temporal patterns
- Road infrastructure characteristics
- Environmental conditions
- Traffic-related contextual features

The solution leverages advanced feature engineering and gradient boosting techniques to capture nonlinear relationships influencing traffic flow and demand.

---

## Problem Statement

The objective of this project is to predict traffic demand for a given location and timestamp using historical transportation and environmental data.

Each observation contains:

- Geographical location encoded using geohashes
- Temporal information
- Road network characteristics
- Environmental attributes
- Traffic-related contextual features

The target variable is a continuous demand score representing expected traffic intensity at a specific location and time.

### Evaluation Metric

Model performance is evaluated using the **Coefficient of Determination (R² Score)**.

A higher R² score indicates better predictive capability and stronger generalization on unseen data.

---

## Dataset Overview

### Training Dataset

| Property | Value |
|-----------|---------|
| Records | 77,299 |
| Features | 10 |
| Target Variable | demand |

### Test Dataset

| Property | Value |
|-----------|---------|
| Records | 41,778 |
| Features | 10 |

---

## Feature Description

| Feature | Description |
|----------|-------------|
| Index | Unique identifier |
| geohash | Encoded geographical location |
| day | Day identifier |
| timestamp | Time at which observation was recorded |
| RoadType | Type of nearby road |
| NumberofLanes | Number of available traffic lanes |
| LargeVehicles | Whether large vehicles are permitted |
| Landmarks | Presence of nearby landmarks |
| Temperature | Environmental temperature |
| Weather | Weather condition |
| demand | Traffic demand score (Target Variable) |

---

## Exploratory Data Analysis

Comprehensive exploratory data analysis was conducted to understand:

- Missing value distributions
- Feature cardinality
- Temporal traffic patterns
- Spatial demand variations
- Target variable behavior
- Correlations among numerical features

### Key Findings

#### High Geographical Diversity

The dataset contains more than 1200 unique geohash locations, indicating strong spatial variation in traffic behavior.

#### Missing Values

Missing values were observed in:

- RoadType
- Temperature
- Weather

These were handled using robust statistical imputation strategies.

#### Target Distribution

The demand variable exhibited:

- Positive skewness
- Long-tail behavior
- Dense concentration near lower demand values

To improve learning stability, a logarithmic transformation was applied.

---

## Data Preprocessing Pipeline

### Missing Value Treatment

#### Numerical Features

Median imputation:

- Temperature

#### Categorical Features

Mode imputation:

- RoadType
- Weather

---

### Timestamp Decomposition

The timestamp column was decomposed into:

- Hour
- Minute

to capture intra-day traffic fluctuations.

---

### Cyclical Time Encoding

To preserve temporal continuity:

```python
hour_sin = np.sin(2 * np.pi * hour / 24)
hour_cos = np.cos(2 * np.pi * hour / 24)
```

This allows the model to correctly understand cyclical relationships such as:

```text
23:00 → 00:00
```

which standard numerical encoding cannot represent effectively.

---

### Geospatial Feature Engineering

Hierarchical location information was extracted through geohash decomposition.

```text
geohash
├── gh3
└── gh4
```

These engineered features help capture:

- Regional traffic patterns
- Spatial clustering effects
- Location-specific demand trends

---

## Feature Engineering

The final feature set consists of multiple feature groups.

### Temporal Features

- hour
- minute
- hour_sin
- hour_cos
- time_period

### Spatial Features

- geohash
- gh3
- gh4

### Infrastructure Features

- RoadType
- NumberofLanes
- LargeVehicles
- Landmarks

### Environmental Features

- Temperature
- Weather

### Interaction Features

- veh_lanes
- road_lanes
- land_veh
- weather_temp

---

## Model Selection

Several machine learning algorithms were considered:

- Linear Regression
- Random Forest Regressor
- XGBoost
- LightGBM
- CatBoost

CatBoost was selected due to:

- Native categorical feature handling
- Strong performance on tabular datasets
- Reduced preprocessing requirements
- Excellent handling of high-cardinality features
- Robust generalization capabilities

---

## Model Configuration

```text
Algorithm: CatBoostRegressor

Iterations: 1500
Learning Rate: 0.07
Depth: 8
L2 Regularization: 5
Subsample: 0.8
Early Stopping Rounds: 80
Loss Function: RMSE
Random State: 42
```

---

## Validation Strategy

To ensure robust model evaluation, K-Fold Cross Validation was employed.

### Configuration

```text
Number of Folds: 3
Shuffle: True
Random State: 42
```

Each fold produced an independent model and validation score.

Final test predictions were generated using ensemble averaging across all fold models.

---

## Results

### Cross Validation Performance

| Fold | R² Score |
|--------|----------|
| Fold 1 | 0.9409 |
| Fold 2 | 0.9387 |
| Fold 3 | 0.9389 |

### Overall Performance

```text
Mean R² Score : 0.9395
Standard Deviation : 0.0010
```

The low standard deviation indicates strong model consistency and stable generalization performance.

---

## Feature Importance Analysis

Top features identified by CatBoost:

| Rank | Feature |
|--------|---------|
| 1 | RoadType |
| 2 | geohash |
| 3 | gh4 |
| 4 | NumberofLanes |
| 5 | road_lanes |
| 6 | time_period |
| 7 | veh_lanes |
| 8 | RoadType_enc |
| 9 | hour_sin |
| 10 | hour_cos |

These findings indicate that spatial information and road infrastructure characteristics play a dominant role in traffic demand prediction.

---

## Project Structure

```text
traffic-demand-prediction/
│
├── dataset/
│   ├── train.csv
│   ├── test.csv
│   └── sample_submission.csv
│
├── eda.py
├── train.py
├── full_pipeline.py
├── submission.csv
├── README.md
├── requirements.txt
│
├── catboost_info/
│   ├── learn_error.tsv
│   ├── test_error.tsv
│   ├── time_left.tsv
│   └── catboost_training.json
│
└── outputs/
```

---

## Future Enhancements

Potential future improvements include:

- Hyperparameter optimization using Optuna
- LightGBM and XGBoost ensemble models
- Stacked generalization frameworks
- Advanced geohash target encoding
- Temporal sequence modeling
- Bayesian optimization
- Automated feature selection
- Spatial clustering techniques
- Real-time deployment through REST APIs

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-Learn
- CatBoost
- Git
- GitHub

---

## Author

**Adhyatma**

Machine Learning | Data Science | Software Development

This project demonstrates the application of feature engineering, geospatial analytics, and gradient boosting techniques for large-scale traffic demand forecasting and predictive modeling.
