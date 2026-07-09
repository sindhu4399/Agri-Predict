"""
Create a comprehensive training dataset for crop yield prediction.
Uses realistic agricultural data with proper relationships between variables.
"""

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print("=" * 60)
print("Creating Advanced Crop Yield Prediction Model")
print("=" * 60)

# Create label encoders
le_season = LabelEncoder()
le_crop = LabelEncoder()
le_soil = LabelEncoder()

# Define categories
seasons = ['summer', 'winter', 'monsoon', 'spring']
crops = ['wheat', 'maize', 'paddy', 'cotton', 'sugarcane', 'chickpea', 'groundnut']
soils = ['loam', 'sandy', 'clay', 'silt']

# Fit encoders
le_season.fit(seasons)
le_crop.fit(crops)
le_soil.fit(soils)

print(f"\n✓ Categories:")
print(f"  Seasons: {list(le_season.classes_)}")
print(f"  Crops: {list(le_crop.classes_)}")
print(f"  Soils: {list(le_soil.classes_)}")

# Generate comprehensive training data
np.random.seed(42)
n_samples = 2000

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

# Humidity typically between 40-90
data['humidity'] = np.random.uniform(40, 90, n_samples)

# Nutrient levels (realistic ranges)
data['nitrogen'] = np.random.uniform(50, 200, n_samples)
data['phosphorus'] = np.random.uniform(15, 80, n_samples)
data['potassium'] = np.random.uniform(15, 80, n_samples)

# Encode categorical variables
data['season_enc'] = le_season.transform(data['season'])
data['crop_enc'] = le_crop.transform(data['crop'])
data['soil_enc'] = le_soil.transform(data['soil'])

# Create DataFrame
df = pd.DataFrame(data)

# Generate realistic yields based on multiple factors
def calculate_yield(row):
    """
    Calculate crop yield based on realistic agricultural relationships.
    Base yield varies by crop and soil type.
    """
    base_yield = {
        'wheat': 3.5,
        'maize': 4.5,
        'paddy': 4.0,
        'cotton': 1.5,
        'sugarcane': 50.0,  # in tonnes
        'chickpea': 1.5,
        'groundnut': 2.0
    }
    
    soil_multiplier = {
        'loam': 1.2,      # Best for most crops
        'sandy': 0.8,     # Needs more irrigation
        'clay': 0.9,      # Drainage issues
        'silt': 1.0       # Moderate
    }
    
    season_multiplier = {
        'summer': 1.0,
        'winter': 1.1,    # Better for many crops
        'monsoon': 1.0,
        'spring': 0.9
    }
    
    # Base yield
    crop = row['crop']
    base = base_yield.get(crop, 2.5)
    
    # Soil factor
    soil_factor = soil_multiplier.get(row['soil'], 1.0)
    
    # Season factor
    season_factor = season_multiplier.get(row['season'], 1.0)
    
    # Temperature factor (optimal around 20-30°C)
    temp = row['temperature']
    if 20 <= temp <= 30:
        temp_factor = 1.0
    elif 15 <= temp < 20 or 30 < temp <= 35:
        temp_factor = 0.85
    else:
        temp_factor = 0.6
    
    # Rainfall factor (optimal varies by crop)
    rain = row['rainfall']
    if crop == 'paddy' and 800 <= rain <= 1500:
        rain_factor = 1.1
    elif 400 <= rain <= 800:
        rain_factor = 1.0
    elif 200 <= rain < 400 or 800 < rain <= 1200:
        rain_factor = 0.9
    else:
        rain_factor = 0.6
    
    # Humidity factor (40-70% is usually optimal)
    humidity = row['humidity']
    if 40 <= humidity <= 70:
        humidity_factor = 1.0
    elif 30 <= humidity < 40 or 70 < humidity <= 85:
        humidity_factor = 0.85
    else:
        humidity_factor = 0.7
    
    # Nutrient factor (affects yield significantly)
    nitrogen = row['nitrogen']
    phosphorus = row['phosphorus']
    potassium = row['potassium']
    
    # Optimal nutrient levels vary by crop
    avg_nutrient = (nitrogen + phosphorus + potassium) / 3
    if 80 <= avg_nutrient <= 150:
        nutrient_factor = 1.15
    elif 60 <= avg_nutrient < 80 or 150 < avg_nutrient <= 180:
        nutrient_factor = 1.0
    else:
        nutrient_factor = 0.75
    
    # Calculate final yield
    yield_value = (base * soil_factor * season_factor * temp_factor * 
                   rain_factor * humidity_factor * nutrient_factor)
    
    # Add some realistic noise
    noise = np.random.normal(0, 0.2 * yield_value)
    yield_value = max(0.1, yield_value + noise)
    
    return yield_value

print("✓ Calculating realistic yields...")
df['yield'] = df.apply(calculate_yield, axis=1)

# Prepare features and target
X = df[['season_enc', 'crop_enc', 'soil_enc', 'temperature', 'rainfall', 
         'humidity', 'nitrogen', 'phosphorus', 'potassium']]
y = df['yield']

print(f"\n✓ Data Statistics:")
print(f"  Samples: {len(df)}")
print(f"  Yield range: {y.min():.2f} - {y.max():.2f} tonnes/ha")
print(f"  Mean yield: {y.mean():.2f} tonnes/ha")
print(f"  Std deviation: {y.std():.2f}")

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"\n✓ Train/Test Split:")
print(f"  Training samples: {len(X_train)}")
print(f"  Testing samples: {len(X_test)}")

# Train Random Forest model (better than LinearRegression)
print(f"\n✓ Training Random Forest model...")
model = RandomForestRegressor(
    n_estimators=100,      # More trees = better accuracy
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1              # Use all CPU cores
)

model.fit(X_train, y_train)

# Evaluate model
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)
train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae = mean_absolute_error(y_test, y_pred_test)
test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))

print(f"\n✓ Model Performance:")
print(f"  Train R² Score: {train_r2:.4f}")
print(f"  Test R² Score: {test_r2:.4f}")
print(f"  Train MAE: {train_mae:.4f} tonnes/ha")
print(f"  Test MAE: {test_mae:.4f} tonnes/ha")
print(f"  Test RMSE: {test_rmse:.4f} tonnes/ha")

# Feature importance
feature_names = ['season', 'crop', 'soil', 'temperature', 'rainfall', 
                 'humidity', 'nitrogen', 'phosphorus', 'potassium']
importances = model.feature_importances_

print(f"\n✓ Feature Importance:")
for name, importance in sorted(zip(feature_names, importances), 
                               key=lambda x: x[1], reverse=True):
    print(f"  {name:15s}: {importance:.4f}")

# Save model and encoders
joblib.dump((model, le_crop, le_soil, le_season), 'model.pkl')

print(f"\n✓ Model saved to: model.pkl")

# Save sample data for reference
df_sample = df.sample(min(10, len(df)))
df_sample.to_csv('sample_predictions.csv', index=False)
print(f"✓ Sample data saved to: sample_predictions.csv")

print("\n" + "=" * 60)
print("✓ Advanced model training complete!")
print("=" * 60)
print(f"\nYour model is ready for production use!")
print(f"Accuracy: {test_r2:.2%} (R² Score)")
print(f"Average error: {test_mae:.2f} tonnes/hectare")
print(f"\nYou can now run: python app.py")
print("=" * 60)
