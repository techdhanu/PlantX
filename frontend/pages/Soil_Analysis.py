import streamlit as st
import os
import sys
import time
from PIL import Image
import io
import requests
import logging

# Add project root directory to path so we can import from backend
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from backend.soil_classifier import soil_classifier

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def process_soil_analysis(image_bytes):
    """Process the soil image and display results"""
    try:
        with st.spinner('Analyzing soil image...'):
            # Debug: Log image processing start
            logging.debug("Starting soil image analysis.")

            # Get predictions from the model
            predictions = soil_classifier.classify_soil(image_bytes)

            # Debug: Log predictions
            logging.debug(f"Predictions received: {predictions}")

            if predictions and len(predictions) > 0:
                top_prediction = predictions[0]

                # Display results
                st.success(f"Analysis Complete!")

                # Create columns for results
                col1, col2 = st.columns([3, 2])

                with col1:
                    st.markdown("### 📊 Soil Classification Results")

                    # Display top 3 predictions with confidence bars
                    for pred in predictions[:3]:
                        soil_type = pred["soil_type"]
                        confidence = pred["confidence"]
                        st.markdown(f"**{soil_type}**")
                        st.progress(confidence/100)
                        st.caption(f"Confidence: {confidence:.1f}%")

                with col2:
                    st.markdown("### 🌱 Soil Properties")
                    soil_properties = get_soil_properties(top_prediction["soil_type"])
                    for key, value in soil_properties.items():
                        st.markdown(f"**{key}:** {value}")

    except Exception as e:
        # Debug: Log errors
        logging.error(f"An error occurred during analysis: {str(e)}")
        st.error(f"An error occurred during analysis: {str(e)}")

def get_soil_properties(soil_type):
    """Get properties for different soil types"""
    properties = {
        'Alluvial soil': {
            'Water Retention': 'Good',
            'Fertility': 'High',
            'Best For': 'Rice, Wheat, Sugarcane, Jute',
            'Management': 'Regular irrigation, balanced fertilization'
        },
        'Black Soil': {
            'Water Retention': 'Very High',
            'Fertility': 'High',
            'Best For': 'Cotton, Soybeans, Wheat',
            'Management': 'Proper drainage, careful tillage when wet'
        },
        'Cinder Soil': {
            'Water Retention': 'Low',
            'Fertility': 'Low',
            'Best For': 'Succulents, Cacti',
            'Management': 'Add organic matter, frequent watering'
        },
        'Clay soil': {
            'Water Retention': 'High',
            'Fertility': 'High',
            'Best For': 'Rice, Wheat, Corn',
            'Management': 'Improve drainage, add organic matter'
        },
        'Laterite Soil': {
            'Water Retention': 'Poor',
            'Fertility': 'Low',
            'Best For': 'Cashews, Tea, Coffee',
            'Management': 'Regular fertilization, soil amendments'
        },
        'Loamy soil': {
            'Water Retention': 'Balanced',
            'Fertility': 'High',
            'Best For': 'Most crops and vegetables',
            'Management': 'Maintain organic matter content'
        },
        'Peat Soil': {
            'Water Retention': 'Very High',
            'Fertility': 'High in organic matter',
            'Best For': 'Vegetables, berries',
            'Management': 'Manage water table, pH adjustment'
        },
        'Red soil': {
            'Water Retention': 'Medium',
            'Fertility': 'Medium',
            'Best For': 'Groundnuts, Potatoes, Citrus fruits',
            'Management': 'Add organic matter, proper irrigation'
        },
        'Sandy soil': {
            'Water Retention': 'Low',
            'Fertility': 'Low',
            'Best For': 'Root vegetables, carrots',
            'Management': 'Add organic matter, frequent watering'
        },
        'Yellow Soil': {
            'Water Retention': 'Medium',
            'Fertility': 'Medium to Low',
            'Best For': 'Rice, Vegetables, Fruits',
            'Management': 'Regular fertilization, pH management'
        }
    }
    return properties.get(soil_type, {
        'Water Retention': 'Unknown',
        'Fertility': 'Unknown',
        'Best For': 'Unknown',
        'Management': 'Conduct soil test for specific recommendations'
    })

def show():
    st.header("🌱 Soil Type Analysis")

    # Initialize session state for tracking uploaded images
    if 'last_uploaded_file_id' not in st.session_state:
        st.session_state.last_uploaded_file_id = None
    if 'soil_predictions' not in st.session_state:
        st.session_state.soil_predictions = None

    # Information banner
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2E7D32;">
        <h3 style="color: #2E7D32; margin-top: 0;">AI-Powered Soil Classification</h3>
        <p>Upload an image of your soil to identify its type and receive tailored recommendations for soil management and suitable crops.</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2 = st.tabs(["📷 Soil Scanner", "📚 Soil Library"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Upload Soil Image")
            uploaded_file = st.file_uploader(
                "Choose a clear image of your soil:",
                type=["jpg", "jpeg", "png"],
                help="For best results, upload a well-lit, close-up image of soil",
                key="soil_uploader"
            )

            # Check if a new file was uploaded
            current_file_id = None
            if uploaded_file is not None:
                current_file_id = uploaded_file.file_id if hasattr(uploaded_file, 'file_id') else str(hash(uploaded_file.name + str(uploaded_file.size)))

                # Display the uploaded image
                st.image(uploaded_file, caption="Uploaded Soil Image", use_container_width=True)

            analyze_col1, analyze_col2 = st.columns([1, 2])
            with analyze_col1:
                analyze_button = st.button("🔍 Analyze Soil", type="primary", use_container_width=True)

        with col2:
            st.markdown("### Tips for Best Results")
            st.markdown("""
            <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h4 style="color: #558B2F; margin-top: 0;">📸 Taking Good Soil Photos</h4>
                <ul style="margin-bottom: 0;">
                    <li>Ensure good natural lighting</li>
                    <li>Clear away debris and vegetation</li>
                    <li>Include a few inches depth if possible</li>
                    <li>Avoid shadows or glare</li>
                    <li>Capture the texture and color</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Process analysis when button is clicked or new file is uploaded
        if analyze_button and uploaded_file is not None:
            # Clear previous predictions if new file
            if current_file_id != st.session_state.last_uploaded_file_id:
                st.session_state.soil_predictions = None
                st.session_state.last_uploaded_file_id = current_file_id

            # Reset the uploaded file position for reading
            uploaded_file.seek(0)
            image_bytes = uploaded_file.getvalue()

            # Debug: Log file upload
            logging.debug(f"Image uploaded for analysis. File ID: {current_file_id}")

            # Process the image
            process_soil_analysis(image_bytes)

        elif analyze_button:
            st.warning("Please upload an image first.")

    with tab2:
        st.markdown("### Soil Types Encyclopedia")

        # Display information about all soil types
        soil_types_info = {
            "Alluvial soil": {
                "description": "Deposited by water, very fertile soil found in river plains and deltas.",
                "characteristics": ["Rich in minerals", "Good drainage", "High fertility", "Easy to cultivate"],
                "common_locations": "River valleys and deltas"
            },
            "Black Soil": {
                "description": "Rich in calcium carbonate, iron, and magnesium, excellent for cotton cultivation.",
                "characteristics": ["High water retention", "Rich in minerals", "Self-ploughing nature", "Good for cotton"],
                "common_locations": "Deccan plateau regions"
            },
            "Cinder Soil": {
                "description": "Formed from volcanic debris, well-draining but low in nutrients.",
                "characteristics": ["Excellent drainage", "Low nutrient content", "Light weight", "Porous"],
                "common_locations": "Volcanic regions"
            },
            "Clay soil": {
                "description": "Dense, heavy soil with high nutrient content but poor drainage.",
                "characteristics": ["High water retention", "Rich in nutrients", "Poor drainage", "Hard when dry"],
                "common_locations": "Low-lying areas"
            },
            "Laterite Soil": {
                "description": "Rich in iron oxides and aluminum, formed in tropical regions.",
                "characteristics": ["Poor fertility", "Good drainage", "Rich in iron", "Acidic"],
                "common_locations": "Tropical regions with high rainfall"
            },
            "Loamy soil": {
                "description": "Perfect balance of sand, silt, and clay, ideal for most plants.",
                "characteristics": ["Good drainage", "High fertility", "Easy to work", "Good structure"],
                "common_locations": "Temperate regions"
            },
            "Peat Soil": {
                "description": "High in organic matter, formed from partially decomposed vegetation.",
                "characteristics": ["High organic content", "High water retention", "Acidic", "Low in minerals"],
                "common_locations": "Wetland areas"
            },
            "Red soil": {
                "description": "Rich in iron oxides, giving it a distinctive red color.",
                "characteristics": ["Good drainage", "Poor fertility", "Iron-rich", "Acidic"],
                "common_locations": "Tropical and subtropical regions"
            },
            "Sandy soil": {
                "description": "Light and free draining, warms up quickly in spring.",
                "characteristics": ["Excellent drainage", "Low fertility", "Easy to work", "Warms quickly"],
                "common_locations": "Coastal areas and deserts"
            },
            "Yellow Soil": {
                "description": "Similar to red soil but with lower iron oxide content.",
                "characteristics": ["Moderate drainage", "Medium fertility", "Iron deficient", "Acidic"],
                "common_locations": "Moderate rainfall regions"
            }
        }

        # Create an expandable section for each soil type
        for soil_type, info in soil_types_info.items():
            with st.expander(f"🌿 {soil_type}"):
                st.markdown(f"**Description:** {info['description']}")
                st.markdown("**Key Characteristics:**")
                for char in info['characteristics']:
                    st.markdown(f"- {char}")
                st.markdown(f"**Typically Found In:** {info['common_locations']}")

                properties = get_soil_properties(soil_type)
                st.markdown("**Agricultural Properties:**")
                for key, value in properties.items():
                    st.markdown(f"- **{key}:** {value}")
