"""
Ensemble Machine Learning Model - Combines 5 different algorithms.
Uses voting ensemble for better accuracy.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor
from sklearn.svm import SVR
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🤖 ENSEMBLE MACHINE LEARNING MODEL - Multi-Algorithm Approach")
print("=" * 70)

# Create label encoders
le_season = LabelEncoder()
le_crop = LabelEncoder()
le_soil = LabelEncoder()

# Define categories
seasons = ['summer', 'winter', 'monsoon', 'spring']
crops = ['wheat', 'maize', 'paddy', 'cotton', 'sugarcane', 'chickpea', 'groundnut']
soils = ['loam', 'sandy', 'clay', 'silt']

le_season.fit(seasons)
le_crop.fit(crops)
le_soil.fit(soils)

print(f"\n✓ Categories:")
print(f"  Seasons: {list(le_season.classes_)}")
print(f"  Crops: {list(le_crop.classes_)}")
print(f"  Soils: {list(le_soil.classes_)}")

# Generate comprehensive training data
np.random.seed(42)
n_samples = 3000

print(f"\n✓ Generating {n_samples} training samples...")

# Create base data
data = {
    'season': np.random.choice(seasons, n_samples),
    'crop': np.random.choice(crops, n_samples),
    'soil': np.random.choice(soils, n_samples),
}

# Temperature ranges based on season
season_temp_ranges = {
    'summer': (25, 40),
    'winter': (10, 25),
    'monsoon': (20, 35),
    'spring': (15, 30)
}

data['temperature'] = np.array([
    np.random.uniform(*season_temp_ranges[s]) for s in data['season']
])

# Rainfall based on season
season_rainfall_ranges = {
    'summer': (200, 800),
    'winter': (100, 500),
    'monsoon': (800, 2000),
    'spring': (300, 1000)
}

data['rainfall'] = np.array([
    np.random.uniform(*season_rainfall_ranges[s]) for s in data['season']
])

data['humidity'] = np.random.uniform(40, 90, n_samples)
data['nitrogen'] = np.random.uniform(50, 200, n_samples)
data['phosphorus'] = np.random.uniform(15, 80, n_samples)
data['potassium'] = np.random.uniform(15, 80, n_samples)

# Encode categorical variables
data['season_enc'] = le_season.transform(data['season'])
data['crop_enc'] = le_crop.transform(data['crop'])
data['soil_enc'] = le_soil.transform(data['soil'])

df = pd.DataFrame(data)

# Advanced yield calculation
def calculate_yield(row):
    base_yield = {
        'wheat': 3.5, 'maize': 4.5, 'paddy': 4.0, 'cotton': 1.5,
        'sugarcane': 50.0, 'chickpea': 1.5, 'groundnut': 2.0
    }
    
    soil_multiplier = {'loam': 1.2, 'sandy': 0.8, 'clay': 0.9, 'silt': 1.0}
    season_multiplier = {'summer': 1.0, 'winter': 1.1, 'monsoon': 1.0, 'spring': 0.9}
    
    crop = row['crop']
    base = base_yield.get(crop, 2.5)
    soil_factor = soil_multiplier.get(row['soil'], 1.0)
    season_factor = season_multiplier.get(row['season'], 1.0)
    
    temp = row['temperature']
    if 20 <= temp <= 30:
        temp_factor = 1.0
    elif 15 <= temp < 20 or 30 < temp <= 35:
        temp_factor = 0.85
    else:
        temp_factor = 0.6
    
    rain = row['rainfall']
    if crop == 'paddy' and 800 <= rain <= 1500:
        rain_factor = 1.1
    elif 400 <= rain <= 800:
        rain_factor = 1.0
    elif 200 <= rain < 400 or 800 < rain <= 1200:
        rain_factor = 0.9
    else:
        rain_factor = 0.6
    
    humidity = row['humidity']
    if 40 <= humidity <= 70:
        humidity_factor = 1.0
    elif 30 <= humidity < 40 or 70 < humidity <= 85:
        humidity_factor = 0.85
    else:
        humidity_factor = 0.7
    
    avg_nutrient = (row['nitrogen'] + row['phosphorus'] + row['potassium']) / 3
    if 80 <= avg_nutrient <= 150:
        nutrient_factor = 1.15
    elif 60 <= avg_nutrient < 80 or 150 < avg_nutrient <= 180:
        nutrient_factor = 1.0
    else:
        nutrient_factor = 0.75
    
    yield_value = (base * soil_factor * season_factor * temp_factor * 
                   rain_factor * humidity_factor * nutrient_factor)
    
    noise = np.random.normal(0, 0.2 * yield_value)
    yield_value = max(0.1, yield_value + noise)
    
    return yield_value

print("✓ Calculating realistic yields...")
df['yield'] = df.apply(calculate_yield, axis=1)

X = df[['season_enc', 'crop_enc', 'soil_enc', 'temperature', 'rainfall', 
         'humidity', 'nitrogen', 'phosphorus', 'potassium']]
y = df['yield']

print(f"\n✓ Data Statistics:")
print(f"  Total samples: {len(df)}")
print(f"  Yield range: {y.min():.2f} - {y.max():.2f} tonnes/ha")
print(f"  Mean yield: {y.mean():.2f} tonnes/ha")

# Scale features for SVR
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"\n✓ Train/Test Split: {len(X_train)} train, {len(X_test)} test")

# Train individual models
print(f"\n{'=' * 70}")
print("🔧 Training Individual Models:")
print(f"{'=' * 70}")

# Model 1: Random Forest
print("\n1️⃣ Random Forest Regressor...")
rf_model = RandomForestRegressor(
    n_estimators=150,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_r2 = r2_score(y_test, rf_pred)
rf_mae = mean_absolute_error(y_test, rf_pred)
print(f"   ✓ R² Score: {rf_r2:.4f}")
print(f"   ✓ MAE: {rf_mae:.4f} tonnes/ha")

# Model 2: Gradient Boosting
print("\n2️⃣ Gradient Boosting Regressor...")
gb_model = GradientBoostingRegressor(
    n_estimators=150,
    learning_rate=0.1,
    max_depth=7,
    min_samples_split=5,
    random_state=42
)
gb_model.fit(X_train, y_train)
gb_pred = gb_model.predict(X_test)
gb_r2 = r2_score(y_test, gb_pred)
gb_mae = mean_absolute_error(y_test, gb_pred)
print(f"   ✓ R² Score: {gb_r2:.4f}")
print(f"   ✓ MAE: {gb_mae:.4f} tonnes/ha")

# Model 3: Support Vector Regression
print("\n3️⃣ Support Vector Regression (SVR)...")
svr_model = SVR(kernel='rbf', C=100, gamma='scale', epsilon=0.1)
svr_model.fit(X_train, y_train)
svr_pred = svr_model.predict(X_test)
svr_r2 = r2_score(y_test, svr_pred)
svr_mae = mean_absolute_error(y_test, svr_pred)
print(f"   ✓ R² Score: {svr_r2:.4f}")
print(f"   ✓ MAE: {svr_mae:.4f} tonnes/ha")

# Model 4: Ridge Regression
print("\n4️⃣ Ridge Regression...")
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
ridge_pred = ridge_model.predict(X_test)
ridge_r2 = r2_score(y_test, ridge_pred)
ridge_mae = mean_absolute_error(y_test, ridge_pred)
print(f"   ✓ R² Score: {ridge_r2:.4f}")
print(f"   ✓ MAE: {ridge_mae:.4f} tonnes/ha")

# Model 5: Decision Tree
print("\n5️⃣ Decision Tree Regressor...")
dt_model = DecisionTreeRegressor(
    max_depth=20,
    min_samples_split=5,
    random_state=42
)
dt_model.fit(X_train, y_train)
dt_pred = dt_model.predict(X_test)
dt_r2 = r2_score(y_test, dt_pred)
dt_mae = mean_absolute_error(y_test, dt_pred)
print(f"   ✓ R² Score: {dt_r2:.4f}")
print(f"   ✓ MAE: {dt_mae:.4f} tonnes/ha")

# Create Ensemble (Voting Regressor)
print(f"\n{'=' * 70}")
print("🎯 Creating ENSEMBLE Model (Voting Regressor):")
print(f"{'=' * 70}")

ensemble_model = VotingRegressor(
    estimators=[
        ('rf', rf_model),
        ('gb', gb_model),
        ('svr', svr_model),
        ('ridge', ridge_model),
        ('dt', dt_model)
    ],
    weights=[0.25, 0.30, 0.20, 0.15, 0.10]  # Higher weights for better models
)

ensemble_pred = ensemble_model.predict(X_test)
ensemble_r2 = r2_score(y_test, ensemble_pred)
ensemble_mae = mean_absolute_error(y_test, ensemble_pred)
ensemble_rmse = np.sqrt(mean_squared_error(y_test, ensemble_pred))

print(f"\n✓ Ensemble R² Score: {ensemble_r2:.4f}")
print(f"✓ Ensemble MAE: {ensemble_mae:.4f} tonnes/ha")
print(f"✓ Ensemble RMSE: {ensemble_rmse:.4f} tonnes/ha")

# Compare all models
print(f"\n{'=' * 70}")
print("📊 Model Comparison:")
print(f"{'=' * 70}")

results = [
    ('Random Forest', rf_r2, rf_mae),
    ('Gradient Boosting', gb_r2, gb_mae),
    ('SVR', svr_r2, svr_mae),
    ('Ridge', ridge_r2, ridge_mae),
    ('Decision Tree', dt_r2, dt_mae),
    ('ENSEMBLE', ensemble_r2, ensemble_mae)
]

for name, r2, mae in sorted(results, key=lambda x: x[1], reverse=True):
    star = "🏆" if name == 'ENSEMBLE' else "  "
    print(f"{star} {name:20s} | R²: {r2:.4f} | MAE: {mae:.4f}")

print(f"\n✓ Accuracy Improvement:")
best_single = max([r[1] for r in results[:-1]])
improvement = ((ensemble_r2 - best_single) / best_single) * 100
print(f"  Ensemble vs Best Single: {improvement:+.2f}%")

# Save all models
print(f"\n{'=' * 70}")
print("💾 Saving Models:")
print(f"{'=' * 70}")

models_dict = {
    'ensemble': ensemble_model,
    'rf': rf_model,
    'gb': gb_model,
    'svr': svr_model,
    'ridge': ridge_model,
    'dt': dt_model
}

joblib.dump((ensemble_model, le_crop, le_soil, le_season, scaler), 'model.pkl')
joblib.dump(models_dict, 'all_models.pkl')

print(f"\n✓ Main model saved: model.pkl (Ensemble)")
print(f"✓ All models saved: all_models.pkl (for analysis)")

print(f"\n{'=' * 70}")
print("✅ ENSEMBLE MODEL TRAINING COMPLETE!")
print(f"{'=' * 70}")
print(f"\n🎯 Final Results:")
print(f"  Accuracy: {ensemble_r2:.2%} (R² Score)")
print(f"  Avg Error: {ensemble_mae:.2f} tonnes/hectare")
print(f"  Root Mean Squared Error: {ensemble_rmse:.2f}")
print(f"\n🚀 Ready for production!")
print(f"   Run: python app.py")
print(f"{'=' * 70}\n")
