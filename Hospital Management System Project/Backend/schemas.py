from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    AnyUrl,
    HttpUrl,
    IPvAnyAddress,
    PositiveInt,
    PositiveFloat,
    NonNegativeInt,
    NonNegativeFloat,
    StrictStr,
    StrictInt,
    StrictFloat,
    model_validator
)



from datetime import (
    datetime,
    date,
    time,
    timedelta
)

from typing import (
    Optional,
    Annotated,
    List,
    Dict,
    Set,
    Tuple,
    Union,
    Literal
)

from uuid import UUID, uuid4





#  Appointments Schema
class Appointments(BaseModel):
    appointment_id: str = Field(..., description="Unique ID of the appointment")
    patient_id: str = Field(..., description="ID of the patient")
    doctor_id: str = Field(..., description="ID of the doctor")
    appointment_date: datetime = Field(..., description="Date and time of the appointment")
    appointment_time: time = Field(..., description="Time of the appointment")
    status: Optional[str] = Field(default="Scheduled", description="Status of the appointment (Scheduled, Completed, Cancelled)")
    reason: Optional[str] = Field(default=None, description="Reason for the appointment")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the appointment was created")
    



#  Billing Schema
class Billing(BaseModel):
    bill_id: str = Field(..., description="Unique ID of the billing record")
    patient_id: str = Field(..., description="ID of the patient")
    appointment_id: str = Field(..., description="ID of the appointment")
    amount: float = Field(..., description="Billing amount")
    payment_status: Optional[str] = Field(default="Pending", description="Payment status (Pending, Paid, Failed)")
    payment_method: Optional[str] = Field(default=None, description="Payment method (Cash, Card, Online)")
    bill_date: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Date of the bill")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the billing record was created")







#  Doctor Schema
class Doctor(BaseModel):
    doctor_id : str = Field(..., description="Unique ID of the doctor")
    name : str = Field(..., description="Name of the doctor")
    specialization : str = Field(..., description="Specialization of the doctor")
    phone : Optional[str] = Field(default=None, description="Contact number of the patient")
    email : EmailStr  = Field(..., description="Email address of the doctor")
    experience : int = Field(..., description="Years of experience of the doctor")
    consultation_fee : float = Field(..., description="Consultation fee of the doctor")
    created_at : Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the doctor record was created")










# Patient Schema
class Patient(BaseModel):
    patient_id : str = Field(..., description="Unique ID of the patient")
    name : str = Field(..., description="Name of the patient")
    age : int = Field(..., description="Age of the patient")
    gender : str = Field(..., description="Gender of the patient")
    phone : str = Field(..., description="Contact number of the patient")
    city : str = Field(..., description="City of the patient")
    blood_group : str = Field(..., description="Blood group of the patient")
    height_cm : float = Field(..., description="Height of the patient in centimeters")
    weight_kg : float = Field(..., description="Weight of the patient in kilograms")
    created_at : Optional[datetime] = Field(default_factory=datetime.utcnow, description="Timestamp when the patient record was created")
    
    
    @classmethod
    def bmi(cls, height_cm: float, weight_kg: float) -> float:
        """Calculate BMI (Body Mass Index)"""
        height_m = height_cm / 100  # Convert height to meters
        return weight_kg / (height_m ** 2) if height_m > 0 else 0.0
    
    
    @model_validator(mode='after')
    def check_phone_for_old_age(self):
        if self.age >= 60 and not self.phone:
            raise ValueError("Senior citizens (age 60+) must provide a phone number for emergency contact. Entry Denied.")
        return self








class ChatRequest(BaseModel):
    message: str