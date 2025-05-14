import streamlit as st
import pickle
import numpy as np

# Load the trained model
risk_model = pickle.load(open('models/risk_model.pkl', 'rb'))

def show():
    st.title("Climate Risk Alerts")

    # User input fields
    temperature = st.number_input("Temperature")
    rainfall = st.number_input("Rainfall")
    humidity = st.number_input("Humidity")

    # Button for prediction
    if st.button("Check Risk"):
        features = np.array([[temperature, rainfall, humidity]])
        prediction = risk_model.predict(features)[0]
        if prediction == 1:
            st.warning("⚠️ High Climate Risk Detected!")
        else:
            st.success("✅ No Significant Climate Risk")
