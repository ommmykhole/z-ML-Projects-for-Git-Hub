from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional


app = FastAPI()


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of The Patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name Of The Patient")]
    city: Annotated[str, Field(..., description="Patient City Name")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age Of The Patient")]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender Of Patient")
    ]
    height: Annotated[
        float,
        Field(..., gt=0, description="Height Of The Patient In Mtr")
    ]
    weight: Annotated[
        float,
        Field(..., gt=0, description="Weight Of Patient In KGs")
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"


class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[
        Optional[Literal["male", "female", "others"]],
        Field(default=None)
    ]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("patient.json", "r") as f:
        data = json.load(f)
    return data


def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f)


@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient Already Exists")

    data[patient.id] = patient.model_dump(exclude=["id"])

    save_data(data)

    return JSONResponse(
        status_code=201,
        content={"Message": "Patient Created Successfully"}
    )


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info["id"] = patient_id

    patient_pydantic_obj = Patient(**existing_patient_info)

    existing_patient_info = patient_pydantic_obj.model_dump(exclude=["id"])

    data[patient_id] = existing_patient_info

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient Updated Successfully"}
    )


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient Not Found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": "Patient Deleted"}
    )





