import streamlit as st

# Function to create a reusable input form for Crop Recommendation
def crop_input_form():
    nitrogen = st.number_input("Nitrogen")
    phosphorus = st.number_input("Phosphorus")
    potassium = st.number_input("Potassium")
    temperature = st.number_input("Temperature")
    humidity = st.number_input("Humidity")
    ph = st.number_input("Soil pH")
    rainfall = st.number_input("Rainfall")
    return [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]
