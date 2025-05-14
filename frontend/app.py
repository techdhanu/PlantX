import streamlit as st
from pages import Crop_Recommendation, Yield_Prediction, Climate_Risk_Alerts

# Sidebar navigation
st.sidebar.title("PlantX - Climate Smart Agriculture")
selection = st.sidebar.radio("Go to", ["Crop Recommendation", "Yield Prediction", "Climate Risk Alerts"])

# Display selected page
if selection == "Crop Recommendation":
    Crop_Recommendation.show()
elif selection == "Yield Prediction":
    Yield_Prediction.show()
else:
    Climate_Risk_Alerts.show()
