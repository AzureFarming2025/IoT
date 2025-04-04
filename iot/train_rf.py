import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load your dataset
data = pd.read_csv("C:\Users\valan\OneDrive\Documents\GitHub\IoT\sample_sensor_data.csv")

# Define features and target variable
X = data[["temperature", "humidity", "sunlight", "soil_moisture"]]
y = data["soil_moisture"]  # Change to your prediction target if needed

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Save the model
joblib.dump(rf_model, "random_forest_model.pkl")

print("Random Forest model trained and saved as random_forest_model.pkl")