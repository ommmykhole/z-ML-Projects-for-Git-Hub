import streamlit as st
import requests  # For making API requests
import pandas as pd  # For data manipulation
from dashboard_page import show_dashboard  # Import the dashboard function





st.set_page_config(page_title="Hospital Management Application", page_icon="🏥", layout="wide")


st.sidebar.title("Hospital Management Application")
st.sidebar.subheader("Navigation")



menu = ["Appointments", "Billing","Doctors","Patient","Dashboard","AI"]

choice = st.sidebar.selectbox("Select an option", menu)





if choice == "Appointments":
    st.title("📅 Appointments Management")
    st.write("Manage appointments here.")
    
    url = "http://127.0.0.1:8000/appointments/"
    
    # --------------------------------------------------
    # 1. View Appointments
    # --------------------------------------------------
    st.subheader("View Appointments")
    get_url = f"{url}?limit=1000"  # Fetch all appointments with a limit of 1000
    response = requests.get(get_url)
    if response.status_code == 200:
        appointments = response.json()
        if appointments: # data is not empty
            df_appointments = pd.DataFrame(appointments)
            st.dataframe(df_appointments, use_container_width=True, height=500)
        else:
            st.info("No appointments found.")
    else:
        st.error("Failed to fetch appointments data.")
    
    # --------------------------------------------------
    # 2. Add Appointment Form
    # --------------------------------------------------
    st.subheader("Add New Appointment")
    with st.form(key='appointment_form'):
        appointment_id = st.text_input("Appointment ID")
        patient_id = st.text_input("Patient ID")
        doctor_id = st.text_input("Doctor ID")
        appointment_date = st.date_input("Appointment Date")
        appointment_time = st.time_input("Appointment Time")
        status = st.selectbox("Status", ["Scheduled", "Completed", "Cancelled"])
        reason = st.text_area("Reason for Appointment")
        created_at = st.date_input("Created At")
        submit_button = st.form_submit_button(label='Add Appointment')

        if submit_button:
            appointment_data = {
                "appointment_id": appointment_id,
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "appointment_date": str(appointment_date),
                "appointment_time": str(appointment_time),
                "status": status,
                "reason": reason,
                "created_at": str(created_at)
            }
            response = requests.post(url, json=appointment_data)
            if response.status_code in [201, 200]:
                st.toast("✅ Appointment added successfully!", icon="🎉")
            else:
                # error handling: try to get the error message from the response, if it's JSON, otherwise fallback to raw text
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text  # if response is not JSON, fallback to raw text
                
                st.error(f"❌ Failed: {error_msg}")
    
    # --------------------------------------------------
    # 3. Update Appointment Form
    # --------------------------------------------------
    st.subheader("Update Appointment")
    with st.form(key='update_appointment_form'):
        appointment_id_to_update = st.text_input("Appointment ID to Update")
        new_patient_id = st.text_input("New Patient ID")
        new_doctor_id = st.text_input("New Doctor ID")
        new_appointment_date = st.date_input("New Appointment Date")
        new_appointment_time = st.time_input("New Appointment Time")
        new_status = st.selectbox("New Status", ["Scheduled", "Completed", "Cancelled"])
        new_reason = st.text_area("New Reason for Appointment")
        new_created_at = st.date_input("New Created At")
        update_button = st.form_submit_button(label='Update Appointment')

        if update_button:
            update_data = {
                "appointment_id": appointment_id_to_update,
                "patient_id": new_patient_id,
                "doctor_id": new_doctor_id,
                "appointment_date": str(new_appointment_date),
                "appointment_time": str(new_appointment_time),
                "status": new_status,
                "reason": new_reason,
                "created_at": str(new_created_at)
            }
            update_url = f"{url}{appointment_id_to_update}" # <--- extra slash removed
            response = requests.put(update_url, json=update_data)
            if response.status_code in [200, 204]:
                st.success("✅ Appointment updated successfully!")
                
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed to update: {error_msg}")
    
    # --------------------------------------------------
    # 4. Delete Appointment Form
    # --------------------------------------------------
    st.subheader("Delete Appointment")
    with st.form(key='delete_appointment_form'):
        delete_appointment_id = st.text_input("Appointment ID to Delete")
        delete_button = st.form_submit_button(label='Delete Appointment')

        if delete_button:
            delete_url = f"{url}{delete_appointment_id}" # extra slash removed
            response = requests.delete(delete_url)
            if response.status_code in [200, 204]:
                st.toast("✅ Appointment deleted successfully!", icon="🎉")
                
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed to delete: {error_msg}")










## Billing Section

elif choice == "Billing":
    st.title("💰 Billing Management")
    st.write("Manage billing here.")
    
    url = "http://localhost:8000/billing/"
    
    
    
    #=--------------------------------------------------
    # 1. View Billing
    # --------------------------------------------------
    st.subheader("View Billing")
    get_url = f"{url}?limit=1000"  # Fetch all billing records with a limit of 1000
    response = requests.get(get_url)
    if response.status_code == 200:
        billing_records = response.json()
        if billing_records: # data is not empty
            df_billing = pd.DataFrame(billing_records)
            st.dataframe(df_billing, use_container_width=True, height=500)
        else:
            st.info("No billing records found.")





#--------------------------------------------------
# 2. Add Billing Form
# --------------------------------------------------
    st.subheader("Add New Billing Record")
    with st.form(key='billing_form'):
        bill_id = st.text_input("Billing ID")
        patient_id = st.text_input("Patient ID")
        appointment_id = st.text_input("Appointment ID")
        amount = st.number_input("Amount", min_value=0.0, step=0.01)
        payment_status = st.selectbox("Payment Status", ["Paid", "Pending"])
        payment_method = st.selectbox("Payment Method", ["Cash", "Credit Card", "Insurance"])
        bill_date = st.date_input("Billing Date")
        created_at = st.date_input("Created At")
        submit_button = st.form_submit_button(label='Add Billing Record')

        if submit_button:
            billing_data = {
                "bill_id": bill_id,
                "patient_id": patient_id,
                "appointment_id": appointment_id,
                "amount": amount,
                "payment_status": payment_status,
                "payment_method": payment_method,
                "bill_date": str(bill_date),
                "created_at": str(created_at)
            }
            response = requests.post(url, json=billing_data)
            if response.status_code in [201, 200]:
                st.toast("✅ Billing record added successfully!", icon="🎉")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed: {error_msg}")
    
    
    
    
    
    
#--------------------------------------------------
# 3. Update Billing Form
# --------------------------------------------------
    st.subheader("Update Billing Record")
    with st.form(key='update_billing_form'):
        billing_id_to_update = st.text_input("Billing ID to Update")
        new_patient_id = st.text_input("New Patient ID")
        new_appointment_id = st.text_input("New Appointment ID")
        new_amount = st.number_input("New Amount", min_value=0.0, step=0.01)
        new_payment_status = st.selectbox("New Payment Status", ["Paid", "Pending"])
        new_payment_method = st.selectbox("New Payment Method", ["Cash","Card","UPI","Net Banking"])
        new_bill_date = st.date_input("New Billing Date")
        new_created_at = st.date_input("New Created At")
        update_button = st.form_submit_button(label='Update Billing Record')

        if update_button:
            update_data = {
                "bill_id": billing_id_to_update,
                "patient_id": new_patient_id,
                "appointment_id": new_appointment_id,
                "amount": new_amount,
                "payment_status": new_payment_status,
                "payment_method": new_payment_method,
                "bill_date": str(new_bill_date),
                "created_at": str(new_created_at)
            }
            update_url = f"{url}{billing_id_to_update}" # extra slash removed
            response = requests.put(update_url, json=update_data)
            if response.status_code in [200, 204]:
                st.success("✅ Billing record updated successfully!")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed to update: {error_msg}")








#--------------------------------------------------
# 4. Delete Billing Form
# --------------------------------------------------
    st.subheader("Delete Billing Record")
    with st.form(key='delete_billing_form'):
        delete_billing_id = st.text_input("Billing ID to Delete")
        delete_button = st.form_submit_button(label='Delete Billing Record')

        if delete_button:
            delete_url = f"{url}{delete_billing_id}" # extra slash removed
            response = requests.delete(delete_url)
            if response.status_code in [200, 204]:
                st.toast("✅ Billing record deleted successfully!", icon="🎉")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed to delete: {error_msg}")














##  Doctors Section

elif choice == "Doctors":
    st.title("👨‍⚕️ Doctors Management")
    st.write("Manage doctors here.")
    
    url = "http://localhost:8000/doctors/"
    
    # --------------------------------------------------
    # 1. View Doctors
    # --------------------------------------------------
    st.subheader("View Doctors")
    get_url = f"{url}?limit=1000"  # Fetch all doctors with a limit of 1000
    response = requests.get(get_url)
    if response.status_code == 200:
        doctors = response.json()
        if doctors: # data is not empty
            df_doctors = pd.DataFrame(doctors)
            st.dataframe(df_doctors, use_container_width=True, height=500)
        else:
            st.info("No doctors found.")
    
    
    
    
    
#--------------------------------------------------
# 2. Add Doctor Form
# --------------------------------------------------
    st.subheader("Add New Doctor")
    with st.form(key='doctor_form'):
        doctor_id = st.text_input("Doctor ID")
        name = st.text_input("Name")
        specialization = st.text_input("Specialization")
        phone = st.text_input("Contact Number")
        email = st.text_input("Email")
        experience = st.number_input("Experience (in years)", min_value=0, step=1)
        consultation_fee = st.number_input("Consultation Fee", min_value=0.0, step=0.01)
        created_at = st.date_input("Created At")
        submit_button = st.form_submit_button(label='Add Doctor')

        if submit_button:
            doctor_data = {
                "doctor_id": doctor_id,
                "name": name,
                "specialization": specialization,
                "phone": phone,
                "email": email,
                "experience": experience,
                "consultation_fee": consultation_fee,
                "created_at": str(created_at)
            }
            response = requests.post(url, json=doctor_data)
            if response.status_code in [201, 200]:
                st.toast("✅ Doctor added successfully!", icon="🎉")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed: {error_msg}")





#--------------------------------------------------
# 3. Update Doctor Form
# --------------------------------------------------
    st.subheader("Update Doctor")
    with st.form(key='update_doctor_form'):
        doctor_id_to_update = st.text_input("Doctor ID to Update")
        new_name = st.text_input("New Name")
        new_specialization = st.text_input("New Specialization")
        new_phone = st.text_input("New Contact Number")
        new_email = st.text_input("New Email")
        new_experience = st.number_input("New Experience (in years)", min_value=0, step=1)
        new_consultation_fee = st.number_input("New Consultation Fee", min_value=0.0, step=0.01)
        new_created_at = st.date_input("New Created At")
        update_button = st.form_submit_button(label='Update Doctor')

        if update_button:
            update_data = {
                "doctor_id": doctor_id_to_update,
                "name": new_name,
                "specialization": new_specialization,
                "phone": new_phone,
                "email": new_email,
                "experience": new_experience,
                "consultation_fee": new_consultation_fee,
                "created_at": str(new_created_at)
            }
            update_url = f"{url}{doctor_id_to_update}" # extra slash removed
            response = requests.put(update_url, json=update_data)
            if response.status_code in [200, 204]:
                st.success("✅ Doctor updated successfully!")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed to update: {error_msg}")









#--------------------------------------------------
# 4. Delete Doctor Form
# --------------------------------------------------
    st.subheader("Delete Doctor")
    with st.form(key='delete_doctor_form'):
        delete_doctor_id = st.text_input("Doctor ID to Delete")
        delete_button = st.form_submit_button(label='Delete Doctor')

        if delete_button:
            delete_url = f"{url}{delete_doctor_id}" # extra slash removed
            response = requests.delete(delete_url)
            if response.status_code in [200, 204]:
                st.toast("✅ Doctor deleted successfully!", icon="🎉")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                
                # Handle foreign key constraint error specifically for doctors with scheduled appointments
                if "Foreign key constraint" in error_msg or "1451" in error_msg:
                    st.error("❌ Failed to delete: You cannot delete this doctor because they have scheduled appointments. Please delete or reassign their appointments first.")
                else:
                    st.error(f"❌ Failed to delete: {error_msg}")












##  Patient Section

elif choice == "Patient":
    st.title("🧑‍⚕️ Patient Management")
    st.write("Manage patients here.")
    
    url = "http://localhost:8000/patients/"
    
    # --------------------------------------------------
    # 1. View Patients
    # --------------------------------------------------
    st.subheader("View Patients")
    get_url = f"{url}?limit=1000"  # Fetch all patients with a limit of 1000
    response = requests.get(get_url)
    if response.status_code == 200:
        patients = response.json()
        if patients: # data is not empty
            df_patients = pd.DataFrame(patients)
            st.dataframe(df_patients, use_container_width=True, height=500)
        else:
            st.info("No patients found.")






#--------------------------------------------------
# 2. Add Patient Form
# --------------------------------------------------
    st.subheader("Add New Patient")
    with st.form(key='patient_form'):
        patient_id = st.text_input("Patient ID")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        phone = st.text_input("Contact Number")
        city = st.text_input("City")
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        height_cm = st.number_input("Height (in cm)", min_value=0.0, step=0.1)
        weight_kg = st.number_input("Weight (in kg)", min_value=0.0, step=0.1)
        created_at = st.date_input("Created At")
        submit_button = st.form_submit_button(label='Add Patient')

        if submit_button:
            patient_data = {
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "city": city,
                "blood_group": blood_group,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "created_at": str(created_at)
            }
            response = requests.post(url, json=patient_data)
            if response.status_code in [201, 200]:
                st.toast("✅ Patient added successfully!", icon="🎉")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed: {error_msg}")









#--------------------------------------------------
# 3. Update Patient Form
# --------------------------------------------------
    st.subheader("Update Patient")
    with st.form(key='update_patient_form'):
        patient_id_to_update = st.text_input("Patient ID to Update")
        new_name = st.text_input("New Name")
        new_age = st.number_input("New Age", min_value=0, step=1)
        new_gender = st.selectbox("New Gender", ["Male", "Female"])
        new_phone = st.text_input("New Contact Number")
        new_city = st.text_input("New City")
        new_blood_group = st.selectbox("New Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
        new_height_cm = st.number_input("New Height (in cm)", min_value=0.0, step=0.1)
        new_weight_kg = st.number_input("New Weight (in kg)", min_value=0.0, step=0.1)
        new_created_at = st.date_input("New Created At")
        update_button = st.form_submit_button(label='Update Patient')

        if update_button:
            update_data = {
                "patient_id": patient_id_to_update,
                "name": new_name,
                "age": new_age,
                "gender": new_gender,
                "phone": new_phone,
                "city": new_city,
                "blood_group": new_blood_group,
                "height_cm": new_height_cm,
                "weight_kg": new_weight_kg,
                "created_at": str(new_created_at)
            }
            update_url = f"{url}{patient_id_to_update}" # extra slash removed
            response = requests.put(update_url, json=update_data)
            if response.status_code in [200, 204]:
                st.success("✅ Patient updated successfully!")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                st.error(f"❌ Failed to update: {error_msg}")








#--------------------------------------------------
# 4. Delete Patient Form
# --------------------------------------------------
    st.subheader("Delete Patient")
    with st.form(key='delete_patient_form'):
        delete_patient_id = st.text_input("Patient ID to Delete")
        delete_button = st.form_submit_button(label='Delete Patient')

        if delete_button:
            delete_url = f"{url}{delete_patient_id}" # extra slash removed
            response = requests.delete(delete_url)
            if response.status_code in [200, 204]:
                st.toast("✅ Patient deleted successfully!", icon="🎉")
            else:
                try:
                    error_msg = response.json().get("detail", "Unknown Error")
                except:
                    error_msg = response.text
                
                # Handle foreign key constraint error specifically for patients with scheduled appointments
                if "Foreign key constraint" in error_msg or "1451" in error_msg:
                    st.error("❌ Failed to delete: You cannot delete this patient because they have scheduled appointments. Please delete or reassign their appointments first.")
                else:
                    st.error(f"❌ Failed to delete: {error_msg}")









elif choice == "Dashboard":
    show_dashboard()  # Call the function to display the dashboard







elif choice == "AI":
        st.title("🤖 Shivnetra Hospital AI")
        st.caption("Advanced Agentic AI - Led by Legacy. Driven by Innovation.")

        # Initialize chat history in Streamlit Session State
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display previous chat messages on the screen
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input from the chat interface
        if prompt := st.chat_input("Ask Shivnetra AI anything... (e.g., 'Add a new patient')"):
            
            # 1. Display user message in chat container
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # 2. Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})

            # 3. Send message to AI (FastAPI backend) and fetch response
            with st.chat_message("assistant"):
                with st.spinner("Shivnetra AI is processing..."):  
                    try:
                        # Make sure 'import requests' is at the top of your file
                        res = requests.post(
                            "http://localhost:8000/api/chat",
                            json={"message": prompt}
                        )
                        
                        if res.status_code == 200:
                            bot_reply = res.json().get("reply", "No response received.")
                        else:
                            bot_reply = f"⚠️ Server Error: {res.text}"
                            
                        st.markdown(bot_reply)
                        
                        # Add assistant response to chat history
                        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                        
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Backend server (FastAPI) is not running. Please start it using uvicorn.")
                    except Exception as e:
                        st.error(f"❌ An error occurred: {e}")