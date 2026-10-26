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


class Address(BaseModel):
    city: str
    state: str
    pin: int


class PersonBase(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=50,
            title="Name Of The Patient",
            description="Give The Name Of The Patient less Than 50 Char",
            examples=["Om", "APPA"],
        ),
    ]

    age: int = Field(gt=0, lt=120)

    @field_validator("name", mode="before")
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    @field_validator("age", mode="before")
    @classmethod
    def validate_age(cls, value):
        if isinstance(value, int) and 0 < value < 100:
            return value

        raise ValueError("Age Should Be Between 0 and 100")


class Patient(PersonBase):
    email: EmailStr
    linkedin_url: AnyUrl

    weight: Annotated[
        int,
        Field(gt=0, strict=True),
    ]

    height: Annotated[
        float,
        Field(gt=0, strict=True),
    ]

    married: Annotated[
        bool,
        Field(description="Enter The Patient Married Or Not"),
    ]

    allergies: Optional[list[str]] = Field(
        default=None,
        max_length=5,
    )

    contact_details: dict[str, str]
    address: Address

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["hdfc.com", "icici.com"]
        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError("Not in Valid Domain")

        return value

    @model_validator(mode="after")
    def validate_emergency_contact(self):
        if (
            self.age > 60
            and "emergency" not in self.contact_details
        ):
            raise ValueError(
                "If Patient Older Than 60 Emergency Contact Is Important"
            )

        return self

    @computed_field
    @property
    def calculate_bmi(self) -> float:
        return round(
            self.weight / (self.height ** 2),
            2,
        )


class PatientManager:

    @staticmethod
    def insert_patient_data(patient: Patient):
        print(patient.name)
        print(patient.age)
        print(patient.allergies)
        print("Inserted")

    @staticmethod
    def update_patient_data(patient: Patient):
        print(patient.name)
        print(patient.age)
        print(patient.allergies)
        print("Updated")


def main():

    address_data = {
        "city": "Pune",
        "state": "Maharashtra",
        "pin": 415810,
    }

    address = Address(**address_data)

    patient_info = {
        "name": "Anna Kaka",
        "age": 76,
        "email": "patient@hdfc.com",
        "linkedin_url": "https://example.com",
        "weight": 98,
        "height": 1.2,
        "married": True,
        "contact_details": {
            "Email": "patient@hdfc.com",
            "Phone": "98773634",
            "emergency": "98773634",
        },
        "address": address,
    }

    patient = Patient(**patient_info)

    PatientManager.insert_patient_data(patient)

    print("BMI:", patient.calculate_bmi)

    second_patient_name = input("Enter The 2nd Patient Name: ")
    second_patient_age = int(input("Enter The 2nd Patient Age: "))
    second_patient_weight = int(input("Enter The 2nd Patient Weight: "))

    second_patient_info = {
        "name": second_patient_name,
        "age": second_patient_age,
        "email": "patient@icici.com",
        "linkedin_url": "https://example.com",
        "weight": second_patient_weight,
        "height": 1.2,
        "married": False,
        "contact_details": {
            "Email": "Not Provided",
            "Phone": "Not Provided",
            "emergency": "Not Provided",
        },
        "address": address,
    }

    second_patient = Patient(**second_patient_info)

    PatientManager.insert_patient_data(second_patient)
    PatientManager.update_patient_data(second_patient)

    print(second_patient.model_dump_json(indent=4))


if __name__ == "__main__":
    main()
