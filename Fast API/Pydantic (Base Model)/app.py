from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated


class Address(BaseModel):
    
    city: str
    state: str
    pin: int

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title="Name Of The Patient", description="Give The Name Of The Patient less Than 50 Char", examples=["Om","APPA"])]
    email: EmailStr
    linkedin_url: AnyUrl
    age: int = Field(gt=0, lt=120)
    weight: Annotated[int, Field(gt=0, strict=True)]
    height: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(description="Enter The Patient Married Or Not")]
    allergies: Optional[List[str]] = Field(max_length=5)
    contact_details: Dict[str, str]
    address: Address
    
    
    @field_validator("email")
    @classmethod
    def email_validator(cls,value):
        
        valid_domain = ['hdfc.com', 'icici.com']
        # abc@gmail.com
        domain_name = value.split('@')[-1]
        
        if domain_name not in valid_domain:
            raise ValueError('Not in Valid Domain')
        return value
    
    @field_validator(name, mode="before")
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    
    @field_validator(age, mode="before")
    @classmethod
    def validate_age(cls,value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age Should Be Between In 0 or 100")
        
        
    @model_validator(model="after")
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError("If Patient Older Than 60 Emergency Contact In Important")
        return model
    
    
    @computed_field
    @property
    def calculate_bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

address_dict = {"city":"Pune","State":"Maharastra","Pin":415810}
address1 = Address(**address_dict)

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("Inserted")


def update_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print("Updated")


patient_info = {
    "name": "Anna Kaka",
    "age": 76,
    "email": "kholeom15@gmail.com",
    "linkedin_url": "https://youtu.be/lRArylZCeOs?list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ",
    "weight": 98,
    "height": 1.2,
    "married": True,
    "contact_details": {
        "Email": "khole@gmail.com",
        "Phone": "98773634"
    }
}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)


second_patient_name = input("Enter The 2nd Patient Name: ")
second_patient_age = int(input("Enter The 2nd Patient Age: "))
second_patient_weight = float(input("Enter The 2nd Patient Weight: "))


second_patient_info = {
    "name": second_patient_name,
    "age": second_patient_age,
    "email": "example@gmail.com",
    "linkedin_url": "https://example.com",
    "weight": second_patient_weight,
    "height":1.2,
    "married": False,
    "contact_details": {
        "Email": "Not Provided",
        "Phone": "Not Provided"
    }
}


patient2 = Patient(**second_patient_info)

insert_patient_data(patient2)
update_patient_data(patient2)




temp = Patient.model_dump_json()

print(temp)
print(type(temp))