"""
Create a test/demo model for development purposes.
This creates a simple scikit-learn model that can make basic predictions.
"""

import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
import pandas as pd

print("Creating test model for development...")

# Create label encoders for categorical variables
le_season = LabelEncoder()
le_crop = LabelEncoder()
le_soil = LabelEncoder()

# Fit encoders with common values
seasons = ['summer', 'winter', 'monsoon', 'spring']
crops = ['wheat', 'maize', 'paddy', 'cotton', 'sugarcane']
soils = ['loam', 'sandy', 'clay', 'silt']

le_season.fit(seasons)
le_crop.fit(crops)
le_soil.fit(soils)

# Create a simple training dataset
np.random.seed(42)
n_samples = 100

# Generate synthetic training data
X_train = pd.DataFrame({
    'season_enc': np.random.randint(0, len(seasons), n_samples),
    'crop_enc': np.random.randint(0, len(crops), n_samples),
    'soil_enc': np.random.randint(0, len(soils), n_samples),
    'temperature': np.random.uniform(15, 35, n_samples),
    'rainfall': np.random.uniform(400, 1000, n_samples),
    'humidity': np.random.uniform(40, 90, n_samples),
    'nitrogen': np.random.uniform(50, 150, n_samples),
    'phosphorus': np.random.uniform(20, 80, n_samples),
    'potassium': np.random.uniform(20, 80, n_samples),
})

# Generate synthetic target (yield in tons per hectare)
# Simple formula: base yield + effects of various factors
y_train = (
    2.5 +  # base yield
    0.05 * X_train['temperature'] +
    0.002 * X_train['rainfall'] +
    0.01 * X_train['humidity'] +
    0.01 * X_train['nitrogen'] +
    0.005 * X_train['phosphorus'] +
    0.005 * X_train['potassium'] +
    np.random.normal(0, 0.3, n_samples)  # noise
)

# Ensure yields are positive
y_train = np.clip(y_train, 0.5, 10)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

print(f"✓ Model trained with {n_samples} samples")
print(f"  R² Score: {model.score(X_train, y_train):.3f}")

# Save model and encoders
joblib.dump((model, le_crop, le_soil, le_season), 'model.pkl')

print("✓ Model saved to: model.pkl")
print("\nTest model ready! You can now run: python app.py")
print("\nNote: This is a demo model for development.")
print("For production, replace with your trained model.")
