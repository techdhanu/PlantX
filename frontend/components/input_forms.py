import streamlit as st
import io

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

# Function to create a reusable input form for Plant Disease Detection
def plant_disease_input_form():
    """
    Create a reusable input form for plant disease detection
    Returns:
        bytes: Image data if uploaded, otherwise None
    """
    uploaded_file = st.file_uploader(
        "Upload a clear image of your plant:",
        type=["jpg", "jpeg", "png"],
        help="For best results, upload a well-lit, close-up image of the affected leaves or plant parts"
    )

    # Display image preview if uploaded
    if uploaded_file is not None:
        image_bytes = uploaded_file.getvalue()
        st.image(image_bytes, caption="Uploaded Image", use_column_width=True)
        return image_bytes

    return None

# Function to display disease detection tips
def display_disease_detection_tips():
    """Display helpful tips for better disease detection results"""
    st.markdown("""
    ### Tips for Better Disease Detection
    
    1. **Clear Images**: Take photos in good lighting conditions
    2. **Close-ups**: Capture detailed views of the affected areas
    3. **Multiple Photos**: Upload several images of different affected parts if needed
    4. **Include Context**: Show both healthy and diseased parts for comparison
    5. **Recent Photos**: Use the most recent images of the plant symptoms
    """)

