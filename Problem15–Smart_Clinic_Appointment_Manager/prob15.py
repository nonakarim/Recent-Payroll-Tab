import streamlit as st
from datetime import date
import re
import time

# Initializing appointment data list, because we need to save appointent for later
if "appoinment_data" not in st.session_state:
    st.session_state.appoinment_data = []

col1,col2,col3 = st.columns([1, 40, 1])

# Title
with col2:
    st.title(" Smart Clinic Appointment Manager 🏥", text_alignment="center")

def side_bar():
    """Defines Sidebar Code (User Guide), so the user understands everything"""
    with st.sidebar:
        st.header("Clinic Data")

        # Clinic Name
        st.subheader("Clinic Name: ")
        st.info("Hana's Clinic")

        # Current Date
        st.subheader("Current Date: ")
        st.info(date.today())

        # Information Section
        st.subheader("Navigation/information section: ")
        st.markdown("""
        - The Receptionist Can:
            - Book appointments.\n
            - View all appointments.\n
            - Search for appointments.\n
            - Cancel appointments.\n
            - View today's schedule.\n
            - View clinic statistics.\n
            - Prevent appointment conflicts.""")

def time_check(text):
    pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d$"
    return bool(re.match(pattern, text))

def validation(patient_name, reason_for_visit, appointment_time):
    if(patient_name == ""):
        return "Cannot Leave Space Empty"
    if(not time_check(appointment_time)):
        return "Please Enter Time in a Clear Format"
    if(reason_for_visit == ""):
        return "Cannot Leave Space Empty"

    return True

def book_appointment_tab():
    with st.form("Enter Info"):
        patient_name = st.text_input("Patient Name: ")
        doctor_name = st.selectbox("Doctor Name: ",
                    [ "DR. Marwa",
                     "Dr. Aya",
                     "Dr. Ahmed"])
        appointment_date = st.date_input("Appointment Date: ")
        appointment_time = st.text_input("Appointment Time: ")
        reason_for_visit = st.text_input("Reason For Visit: ")
        book_appointment = st.form_submit_button("Book Appointment")

        if(book_appointment == True):
            if(validation(patient_name, reason_for_visit, appointment_time) != True):
                st.error(validation(patient_name, reason_for_visit, appointment_time))
            else:
                result = False
                for user in st.session_state.appoinment_data:
                    if(user.get("doctor") == doctor_name 
                       and user.get("date") == appointment_date 
                       and user.get("time") == appointment_time):
                            st.warning("An Appointment At The Same Time Is Scheduled")
                            result=True
                            break
                if not result:
                    st.session_state.appoinment_data.append({"name": patient_name,
                                                                "doctor": doctor_name,
                                                                "date": appointment_date,
                                                                "time": appointment_time,
                                                                "reason": reason_for_visit,
                                                                "status": "Scheduled"})

                    st.spinner(" ")
                    time.sleep(2)
                    st.success("Appointment Booked Successfully")

def search_tab():
    patient_name = st.text_input("Patient Name: ")
    doctor_name = st.selectbox("Doctor Name: ",
                [ "DR. Marwa",
                    "Dr. Aya",
                    "Dr. Ahmed"])
    appointment_date = st.date_input("Appointment Date: ")
    submit = st.button("Submit")

    search_list = []
    if submit:
        for user in st.session_state.appoinment_data:
            if(user.get("name") == patient_name 
            and user.get("doctor") == doctor_name
            and user.get("date") == appointment_date):
                    search_list.append({"name": user.get("name"), 
                                        "doctor": user.get("doctor"),
                                        "date": user.get("date"),
                                        "time": user.get("time"),
                                        "reason": user.get("reason"),
                                        "status": user.get("status")})

        if search_list == []:
            st.info("No Matching Appointments")
        else:
            st.table(search_list)

def cancel_appointment_tab():
    

side_bar()

tab1, tab2, tab3, tab4 = st.tabs(["Book Appointment", "View Appointments", "Search", "Cancel Appointments", "Statistics"])

with tab1:
    book_appointment_tab()

with tab2:
    if st.session_state.appoinment_data != []:
        st.table(st.session_state.appoinment_data)
    else:
        st.info("No Appointments Booked Yet")

with tab3:
    search_tab()



