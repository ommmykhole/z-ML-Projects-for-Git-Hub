from fastapi import FastAPI, Path, HTTPException, Query
import json 
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of The Patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name Of The Patient")]
    city: Annotated[str, Field(..., description="Patient City Name")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age Of The Patient")]
    # Updated to lowercase to match your patients.json data
    gender: Annotated[Literal["male", "female", "others"], Field(..., description="Gender Of Patient")]
    height: Annotated[float, Field(..., gt=0, description="Height Of The Patient In Mtr")]
    weight: Annotated[float, Field(... , gt=0, description="Weight Of Patient In KGs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"  # Fixed from "Normal"
        else:
            return "Obese"

def load_data():
    # Fixed filename to patients.json
    with open('patient.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    # Fixed filename to patients.json
    with open("patient.json", "w") as f:
        json.dump(data, f)

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient Already Exists")
    
    data[patient.id] = patient.model_dump(exclude=["id"])
    
    save_data(data)
    
    return JSONResponse(status_code=201, content={"Message": "Patient Created Successfully"})