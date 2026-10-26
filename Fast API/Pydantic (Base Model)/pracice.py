from typing import Annotated, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    AnyUrl,
    Field,
    field_validator,
    model_validator,
    computed_field,
)



class Address("BaseModel"):
    city: str
    state: str
    pin: int


class Patient("BaseModel"):
    name: str
    age: int
    address: Address



def patient_info(patient: Patient):
    print("Patient Name, ",Patient.name)
    print("Patient Age: ",Patient.age)
    print("Patient Address: ",Patient.address)



patient_data = {
    "Name":"Anna Kaka",
    "Age": 21,
    "Address": "Pune Maharastra India"
}


patient = Patient(**patient_data)

patient_info(patient)







