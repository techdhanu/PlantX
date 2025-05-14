import streamlit as st
import pickle
import numpy as np

# Load the trained model
crop_model = pickle.load(open('models/crop_model.pkl', 'rb'))

def show():
    st.title("Crop Recommendation")

    # User input fields
    nitrogen = st.number_input("Nitrogen")
    phosphorus = st.number_input("Phosphorus")
    potassium = st.number_input("Potassium")
    temperature = st.number_input("Temperature")
    humidity = st.number_input("Humidity")
    ph = st.number_input("Soil pH")
    rainfall = st.number_input("Rainfall")

    # Button for prediction
    if st.button("Recommend Crop"):
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        prediction = crop_model.predict(features)[0]
        st.success(f"✅ Recommended Crop: {prediction}")
