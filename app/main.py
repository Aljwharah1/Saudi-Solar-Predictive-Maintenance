from fastapi import FastAPI , HTTPException
import joblib 
from pydantic import BaseModel, Field
import pandas as pd 
import numpy as np 


# 1. Load the saved model and scaler
try:

 model = joblib.load('app/solar_maintenance_model.pkl')
 scaler = joblib.load('app/data_scaler.pkl')
except Exception as e : 
 print(f"Error loading model {e} ")

class SolarData(BaseModel):
   
   ambient_temp : float = Field(..., example=30.5, description="Ambient temperature in Celsius")
   module_temp: float = Field(..., example=55.2, description="Module temperature in Celsius")
   irradiation: float = Field(..., example=0.8, description="Solar irradiation level")
   dust_level: float = Field(..., example=0.6, description="Dust accumulation level (0 to 1)")

app = FastAPI (
   
   title = "Sudair Solar Plant AI", 
   description = "API for predicting Solar panel maintenance need using Machien Learning "
)

@app.get("/")
def home():
   return {"status" : "Online" , "model_version":"1.0.0" }

@app.post("/predict")
def predict_maintenance(data: SolarData):
    try:
        # 1. Convert input to DataFrame (Keeping column names intact)
        input_df = pd.DataFrame([data.dict().values()], columns=data.dict().keys())
        
        # 2. Apply the same scaling used in training
        scaled_data = scaler.transform(input_df)
        
        # 3. Get the prediction and the confidence level
        prediction = model.predict(scaled_data)[0]
        probability = model.predict_proba(scaled_data)[0][prediction]
        
        # 4. Professional Response
        return {
            "need_maintenance": int(prediction),
            "confidence": f"{probability * 100:.2f}%",
            "system_status": "Action Required: Initiate Cleaning" if prediction == 1 else "Optimal Performance: No Action Needed"
        }
        
    except Exception as e:
        # Log the error for debugging
        print(f"Prediction Error: {e}")
        raise HTTPException(status_code=500, detail="Internal AI Engine Error")