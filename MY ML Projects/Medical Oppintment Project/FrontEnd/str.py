import streamlit as st
import requests


st.title("Welcome to Shivnetra HMS Patient Appointment Prediction App")


gender_input = st.selectbox("Select Gender", options=["Female", "Male"])
age_input = st.number_input("Enter Age", min_value=0, max_value=120)
scholarship_input = st.selectbox("Scholarship Status", options=["No", "Yes"])
hipertension_input = st.selectbox("Hypertension Status", options=["No", "Yes"])
dibetes_input = st.selectbox("Diabetes Status", options=["No", "Yes"])
alcoholism_input = st.selectbox("Alcoholism Status", options=["No", "Yes"])
handicap_input = st.selectbox("Handicap Status", options=["No", "Yes"])
sms_input = st.selectbox("SMS Received Status", options=["No", "Yes"])
waiting_time_input = st.number_input("Enter Waiting Time (in days)", min_value=0, max_value=365)



patient_data = {
    "gender": 1 if gender_input == "Male" else 0,
    "age": age_input,
    "scholarship": 1 if scholarship_input == "Yes" else 0,
    "hipertension": 1 if hipertension_input == "Yes" else 0,
    "dibetes": 1 if dibetes_input == "Yes" else 0,
    "alcoholism": 1 if alcoholism_input == "Yes" else 0,
    "handicap": 1 if handicap_input == "Yes" else 0,
    "sms": 1 if sms_input == "Yes" else 0,
    "waiting_time": waiting_time_input
}



if st.button("Predict"):
    response = requests.post("http://localhost:8000/predict", json=patient_data)
    
    if response.status_code == 200:
        prediction_result = response.json()
        prediction_value = prediction_result.get("prediction")
        
        if prediction_value == 1:
            st.success("The patient is likely to show up for the appointment.")
        else:
            st.warning("The patient is likely to miss the appointment.")
    else:
        st.error(f"Error: {response.status_code} - {response.text}")

