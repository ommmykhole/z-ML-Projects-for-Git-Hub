import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Time

load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(20))
    phone = Column(String(20), nullable=True)
    city = Column(String(100))
    blood_group = Column(String(10))
    height_cm = Column(Float)
    weight_kg = Column(Float)
    created_at = Column(DateTime)

class Doctor(Base):
    __tablename__ = "doctors"
    doctor_id = Column(String(100), primary_key=True, index=True)
    name = Column(String(100))
    specialization = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    experience = Column(Integer)
    consultation_fee = Column(Float)
    created_at = Column(DateTime)

class Appointments(Base):
    __tablename__ = "appointments"
    appointment_id = Column(String(100), primary_key=True, index=True)
    patient_id = Column(String(100))
    doctor_id = Column(String(100))
    appointment_date = Column(DateTime)
    appointment_time = Column(Time)
    status = Column(String(50), default="Scheduled")
    reason = Column(String(255), nullable=True)
    created_at = Column(DateTime)

class Billing(Base):
    __tablename__ = "billing"
    bill_id = Column(String(100), primary_key=True, index=True)
    patient_id = Column(String(100))
    appointment_id = Column(String(100))
    amount = Column(Float)
    payment_status = Column(String(50), default="Pending")
    payment_method = Column(String(50), nullable=True)
    bill_date = Column(DateTime)
    created_at = Column(DateTime)