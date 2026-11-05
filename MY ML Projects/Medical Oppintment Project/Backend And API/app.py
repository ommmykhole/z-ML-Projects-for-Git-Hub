from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib

app = FastAPI()


model = joblib.load('hospital_noshow_model.pkl')

class Patient(BaseModel):
    gender: int = Field(..., description="Gender of the patient (0 for female, 1 for male)")
    age: int = Field(..., description="Age of the patient in years")
    scholarship: int = Field(..., description="Scholarship status (0 for no, 1 for yes)")
    hipertension: int = Field(..., description="Hypertension status (0 for no, 1 for yes)")
    dibetes: int = Field(..., description="Diabetes status (0 for no, 1 for yes)")
    alcoholism: int = Field(..., description="Alcoholism status (0 for no, 1 for yes)")
    handicap: int = Field(..., description="Handicap status (0 for no, 1 for yes)")
    sms: int = Field(..., description="SMS received status (0 for no, 1 for yes)")
    waiting_time: int = Field(..., description="Waiting time in days before the appointment")

@app.get("/")
def home():
    return {"message": "Welcome to the Shivnetra HMS Patient Appointment API!"}

@app.post("/predict")
def predict(patient: Patient):
    
    data = [[
        patient.gender,
        patient.age,
        patient.scholarship,
        patient.hipertension,
        patient.dibetes,
        patient.alcoholism,
        patient.handicap,
        patient.sms,
        patient.waiting_time
    ]]
    
    
    prediction = model.predict(data) 
    pred_value  = int(prediction[0])
    
    if pred_value not in [0, 1]:
        raise HTTPException(status_code=400, detail="Invalid prediction value. Expected 0 or 1.")
    else:
        return {"prediction": pred_value}
    
    if pred_value == 1:
        return {"prediction": 1, "message": "The patient is likely to show up for the appointment."}
    else:
        return {"prediction": 0, "message": "The patient is likely to miss the appointment."}
    
    return {"prediction": int(prediction[0])}

    