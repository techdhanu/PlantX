import streamlit as st
import pickle
import numpy as np

# Load the trained model
yield_model = pickle.load(open('models/yield_model.pkl', 'rb'))

def show():
    st.title("Yield Prediction")

    # User input fields
    area = st.number_input("Area (in hectares)")
    temperature = st.number_input("Temperature")
    rainfall = st.number_input("Rainfall")
    soil_quality = st.number_input("Soil Quality (1-10)")

    # Button for prediction
    if st.button("Predict Yield"):
        features = np.array([[area, temperature, rainfall, soil_quality]])
        prediction = yield_model.predict(features)[0]
        st.success(f"✅ Predicted Yield: {prediction} tons per hectare")
