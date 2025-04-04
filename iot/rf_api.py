from fastapi import FastAPI
import pandas as pd
import joblib
from pydantic import BaseModel

# Load the trained model
model = joblib.load("random_forest_model.pkl")

# Create a FastAPI app
app = FastAPI()

# Define the request body format
class SensorData(BaseModel):
    temperature: float
    humidity: float
    sunlight: float
    soil_moisture: float

@app.post("/predict")
def predict_moisture(data: SensorData):
    # Convert input to DataFrame
    input_data = pd.DataFrame([data.dict()])

    # Make a prediction
    prediction = model.predict(input_data)[0]
 
    return {"predicted_moisture": prediction}

