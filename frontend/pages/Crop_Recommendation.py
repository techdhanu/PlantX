import streamlit as st
import pickle
import numpy as np
import os

def show():
    st.header("🌾 Crop Recommendation System")

    st.markdown("Please enter the required soil and climate values:")

    # Input fields
    nitrogen = st.number_input("Nitrogen (N)", min_value=0)
    phosphorus = st.number_input("Phosphorus (P)", min_value=0)
    potassium = st.number_input("Potassium (K)", min_value=0)
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    ph = st.number_input("pH value")
    rainfall = st.number_input("Rainfall (mm)")

    if st.button("Predict Crop"):
        try:
            # Use relative path to load model
            model_path = os.path.join("models", "crop_recommendation_model.pkl")
            with open(model_path, "rb") as model_file:
                model = pickle.load(model_file)

            # Input for prediction
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

            # Make prediction
            prediction = model.predict(input_data)
            st.success(f"🌱 Recommended Crop: **{prediction[0].capitalize()}**")

        except FileNotFoundError:
            st.error("❌ Model file not found. Please ensure 'crop_recommendation_model.pkl' is inside the 'models/' folder.")
        except Exception as e:
            st.error(f"⚠️ Error while predicting: {e}")
