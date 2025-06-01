import streamlit as st
import joblib
import numpy as np

# Load trained AdaBoost model
model = joblib.load('models/ada_best_yield__model.pkl')

st.set_page_config(page_title="PlantX Yield Predictor", page_icon="🌾")
st.title("🌾 Crop Yield Prediction - PlantX")
st.markdown("Predict expected **crop yield** (tons/hectare) using climate and soil data.")

st.header("Enter Input Features:")

# --- User inputs ---
crop = st.selectbox("Crop", ["Wheat", "Rice", "Maize"])  # Extend list as needed
state = st.selectbox("State", ["Karnataka", "Punjab", "Tamil Nadu"])  # Extend list as needed
year = st.number_input("Year", min_value=2000, max_value=2030, value=2024)
area = st.number_input("Area (in hectares)", min_value=0.1, value=1.0)
temperature = st.number_input("Average Temperature (°C)", value=28.0)
rainfall = st.number_input("Total Rainfall (mm)", value=900.0)
humidity = st.number_input("Humidity (%)", value=70.0)
soil_ph = st.number_input("Soil pH", value=6.5)
organic_carbon = st.number_input("Organic Carbon (%)", value=0.8)

# --- Manual encoding (must match training) ---
crop_dict = {"Wheat": 0, "Rice": 1, "Maize": 2}
state_dict = {"Karnataka": 0, "Punjab": 1, "Tamil Nadu": 2}

# --- Prepare input array ---
input_features = np.array([[
    crop_dict[crop],
    state_dict[state],
    year,
    area,
    temperature,
    rainfall,
    humidity,
    soil_ph,
    organic_carbon
]])

# --- Predict ---
if st.button("Predict Yield"):
    prediction = model.predict(input_features)
    st.success(f"🌱 **Predicted Crop Yield:** {prediction[0]:.2f} tons/hectare")

def show():
    st.write("Use the form above to input crop and climate data, then click 'Predict Yield' to see the expected yield.")
if __name__ == "__main__":
    show()
