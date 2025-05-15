import streamlit as st
import pickle
import numpy as np

def show():
    st.header("🌦️ Climate Risk Alerts")

    # User inputs for features (adjust based on your dataset)
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    rainfall = st.number_input("Rainfall (mm)")
    temperature = st.number_input("Temperature (°C)")
    humidity = st.number_input("Humidity (%)")
    river_discharge = st.number_input("River Discharge (m³/s)")
    water_level = st.number_input("Water Level (m)")
    elevation = st.number_input("Elevation (m)")
    # For categorical, you might want dropdowns - here are example categories
    land_cover = st.selectbox("Land Cover", ["Forest", "Urban", "Agriculture", "Water"])
    soil_type = st.selectbox("Soil Type", ["Sandy", "Clay", "Silt", "Peat", "Chalk", "Loam"])
    population_density = st.number_input("Population Density")
    infrastructure = st.number_input("Infrastructure")
    historical_floods = st.number_input("Historical Floods")

    if st.button("Predict Flood Risk"):
        try:
            # Load the model (ensure correct path)
            with open("models/climate_risk_model.pkl", "rb") as f:
                model = pickle.load(f)

            # Convert categorical inputs to numbers (simple example: map them)
            land_cover_map = {"Forest":0, "Urban":1, "Agriculture":2, "Water":3}
            soil_type_map = {"Sandy":0, "Clay":1, "Silt":2, "Peat":3, "Chalk":4, "Loam":5}

            input_features = np.array([[
                latitude,
                longitude,
                rainfall,
                temperature,
                humidity,
                river_discharge,
                water_level,
                elevation,
                land_cover_map[land_cover],
                soil_type_map[soil_type],
                population_density,
                infrastructure,
                historical_floods
            ]])

            # Predict (if your model expects scaled data, scale here as well)
            prediction = model.predict(input_features)

            result = "Flood Risk: Yes" if prediction[0] == 1 else "Flood Risk: No"
            st.success(result)
        except Exception as e:
            st.error(f"Prediction error: {e}")
