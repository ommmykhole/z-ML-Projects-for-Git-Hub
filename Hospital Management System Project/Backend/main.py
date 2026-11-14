from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import engine, get_db
import schemas
import database
from sqlalchemy.exc import IntegrityError
from schemas import ChatRequest
from App_AI import chat_with_ai




app = FastAPI(title="Shivnetra HMS API")

@app.get("/")
def read_root():
    return {"message": "Shivnetra Hospital Management System API is Running! 🚀"}

@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT DATABASE()")).scalar()
        return {
            "status": "Success", 
            "connected_to": result, 
            "message": "Database connection is successful! ✅"
        }
    except Exception as e:
        return {"status": "Failed", "error": str(e)}
    




## Appointments Endpoints

# Appointment Creation Endpoint
@app.post("/appointments/", response_model=schemas.Appointments)
def create_appointment(appointment: schemas.Appointments, db: Session = Depends(get_db)):
    
    existing_id = db.query(database.Appointments).filter(
        database.Appointments.appointment_id == appointment.appointment_id
    ).first()
    
    
    existing_appointment = db.query(database.Appointments).filter(
        database.Appointments.patient_id == appointment.patient_id,
        database.Appointments.doctor_id == appointment.doctor_id,
        database.Appointments.appointment_date == appointment.appointment_date,
        database.Appointments.appointment_time == appointment.appointment_time
    ).first()
    
    if existing_appointment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment already exists for the given patient, doctor, date, and time.")
    
    db_appointment = database.Appointments(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment



# Read Appointments Endpoint
@app.get("/appointments/", response_model=list[schemas.Appointments])
def read_appointments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    appointments = db.query(database.Appointments).offset(skip).limit(limit).all()
    return appointments





# Update Appointment Endpoint
@app.put("/appointments/{appointment_id}", response_model=schemas.Appointments)
def update_appointment(appointment_id: str, appointment: schemas.Appointments, db: Session = Depends(get_db)):
    db_appointment = db.query(database.Appointments).filter(database.Appointments.appointment_id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    for key, value in appointment.model_dump().items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment





#  Delete Appointment Endpoint
@app.delete("/appointments/{appointment_id}", response_model=schemas.Appointments)
def delete_appointment(appointment_id: str, db: Session = Depends(get_db)):
    db_appointment = db.query(database.Appointments).filter(database.Appointments.appointment_id == appointment_id).first()
    if not db_appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    db.delete(db_appointment)
    db.commit()
    return db_appointment







## Billing Endpoints



# Create Billing Endpoint
@app.post("/billing/", response_model=schemas.Billing)
def create_billing(billing: schemas.Billing, db: Session = Depends(get_db)):
    
    
    existing_id = db.query(database.Billing).filter(
        database.Billing.bill_id == billing.bill_id
    ).first()
    
    if existing_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Warning: '{billing.bill_id}' This Id is already in use."
        )

    existing_billing = db.query(database.Billing).filter(
        database.Billing.patient_id == billing.patient_id,
        database.Billing.appointment_id == billing.appointment_id
    ).first()
    
    if existing_billing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Billing record already exists for the given patient and appointment."
        )
    
    db_billing = database.Billing(**billing.model_dump())
    db.add(db_billing)
    db.commit()
    db.refresh(db_billing)
    return db_billing








# Read Billing Endpoint
@app.get("/billing/", response_model=list[schemas.Billing])
def read_billing(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    billing_records = db.query(database.Billing).offset(skip).limit(limit).all()
    return billing_records







# Update Billing Endpoint
@app.put("/billing/{bill_id}", response_model=schemas.Billing)
def update_billing(bill_id: str, billing: schemas.Billing, db: Session = Depends(get_db)):
    db_billing = db.query(database.Billing).filter(database.Billing.bill_id == bill_id).first()
    if not db_billing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing record not found")
    for key, value in billing.model_dump().items():
        setattr(db_billing, key, value)
    db.commit()
    db.refresh(db_billing)
    return db_billing








#  Delete Billing Endpoint
@app.delete("/billing/{bill_id}", response_model=schemas.Billing)
def delete_billing(bill_id: str, db: Session = Depends(get_db)):
    db_billing = db.query(database.Billing).filter(database.Billing.bill_id == bill_id).first()
    if not db_billing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Billing record not found")
    db.delete(db_billing)
    db.commit()
    return db_billing




















## Doctor Endpoints






# Doctor Creation Endpoint
@app.post("/doctors/", response_model=schemas.Doctor)
def create_doctor(doctor: schemas.Doctor, db: Session = Depends(get_db)):
    existing_id = db.query(database.Doctor).filter(
        database.Doctor.doctor_id == doctor.doctor_id
    ).first()
    
    if existing_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Warning: '{doctor.doctor_id}' This Id is already in use."
        )
    
    db_doctor = database.Doctor(**doctor.model_dump())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor












# Read Doctors Endpoint
@app.get("/doctors/", response_model=list[schemas.Doctor])
def read_doctors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    doctors = db.query(database.Doctor).offset(skip).limit(limit).all()
    return doctors







# Update Doctor Endpoint
@app.put("/doctors/{doctor_id}", response_model=schemas.Doctor)
def update_doctor(doctor_id: str, doctor: schemas.Doctor, db: Session = Depends(get_db)):
    db_doctor = db.query(database.Doctor).filter(database.Doctor.doctor_id == doctor_id).first()
    if not db_doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    for key, value in doctor.model_dump().items():
        setattr(db_doctor, key, value)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor











# Delete Doctor Endpoint
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: str, db: Session = Depends(get_db)):
    doctor = db.query(database.Doctor).filter(database.Doctor.doctor_id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    try:
        db.delete(doctor)
        db.commit()
        return {"message": "Doctor deleted successfully"}
    
    except IntegrityError as e:
        db.rollback()  # Rollback the transaction to maintain database integrity
        # Raise a more user-friendly error message
        raise HTTPException(status_code=400, detail="1451: Foreign key constraint. Cannot delete this doctor.")

















##  Patient Endpoints


# Patient Creation Endpoint
@app.post("/patients/", response_model=schemas.Patient)
def create_patient(patient: schemas.Patient, db: Session = Depends(get_db)):
    existing_id = db.query(database.Patient).filter(
        database.Patient.patient_id == patient.patient_id
    ).first()
    
    if existing_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Warning: '{patient.patient_id}' This Id is already in use."
        )
    
    db_patient = database.Patient(**patient.model_dump())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient












# Read Patients Endpoint
@app.get("/patients/", response_model=list[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    patients = db.query(database.Patient).offset(skip).limit(limit).all()
    return patients








# Update Patient Endpoint
@app.put("/patients/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: str, patient: schemas.Patient, db: Session = Depends(get_db)):
    db_patient = db.query(database.Patient).filter(database.Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    for key, value in patient.model_dump().items():
        setattr(db_patient, key, value)
    db.commit()
    db.refresh(db_patient)
    return db_patient








#  Delete Patient Endpoint
@app.delete("/patients/{patient_id}", response_model=schemas.Patient)
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    db_patient = db.query(database.Patient).filter(database.Patient.patient_id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return db_patient













@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    
    try:
        
        bot_reply = chat_with_ai(req.message)
        return {"reply": bot_reply}
    except Exception as e:
        return {"error": str(e)}