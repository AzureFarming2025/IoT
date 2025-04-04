
# using random forest

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

#  CSV file 
df = pd.read_csv("C:/Users/valan/Downloads/sensor_data_with_sunlight.csv")

# scaling data
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)

# Define i/p feature (X) andtarget var (y)
X = df_scaled[["temperature", "humidity", "sunlight", "soil_moisture"]]
y = df_scaled["target_moisture"]

# spliting the data into training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)

# training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# prediction
predictions = model.predict(X_test)

# evaluate model
mae = mean_absolute_error(y_test, predictions)
mse = mean_squared_error(y_test, predictions)
print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error (MSE): {mse}")

# feature importance analysis
importances = model.feature_importances_
feature_names = X.columns

# plot feature importances
plt.figure(figsize=(8,5))
plt.barh(feature_names, importances, color='teal')
plt.xlabel("Feature Importance")
plt.ylabel("Sensor Features")
plt.title("Feature Importance in Moisture Prediction")
plt.show()


