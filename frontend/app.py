import streamlit as st
from pages import Crop_Recommendation, Yield_Prediction, Climate_Risk_Alerts

# App Title
st.set_page_config(page_title="PlantX - Climate Smart Agriculture", layout="wide")
st.title("🌱 PlantX - Climate Smart Agriculture Platform")

# Sidebar navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["Crop Recommendation", "Yield Prediction", "Climate Risk Alerts"])

# Display selected page
if selection == "Crop Recommendation":
    Crop_Recommendation.show()
elif selection == "Yield Prediction":
    Yield_Prediction.show()
elif selection == "Climate Risk Alerts":
    Climate_Risk_Alerts.show()
