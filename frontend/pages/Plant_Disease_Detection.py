import streamlit as st
import os
import time
from PIL import Image
import numpy as np
import io
import sys
import base64
import requests
from datetime import datetime

# Add project root directory to path so we can import from backend
# Get the absolute path to the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from backend.disease_detection import disease_detector

def show():
    st.header("🔬 Plant Disease Detection")

    # Information banner
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2E7D32;">
        <h3 style="color: #2E7D32; margin-top: 0;">AI-Powered Disease Diagnosis</h3>
        <p>Upload an image of your plant leaves to instantly identify diseases and receive treatment recommendations.
        Our AI model can recognize over 38 different plant diseases across various crops including tomato, potato, apple, corn, and more.</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📷 Disease Scanner", "📚 Disease Library", "📊 Statistics"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Upload Plant Image")

            # File uploader for disease detection
            uploaded_file = st.file_uploader(
                "Choose a clear image of the affected plant part:",
                type=["jpg", "jpeg", "png"],
                help="For best results, upload a well-lit, close-up image of the affected leaves or plant parts"
            )

            # Sample images
            st.markdown("### Or try a sample image")
            sample_col1, sample_col2, sample_col3 = st.columns(3)

            # Sample images - you would need to replace these with actual URLs or local files
            sample_images = {
                "Tomato Leaf (Late Blight)": "https://www.goodhousekeeping.com/content/dam/gh/pages/tomato-plant-diseases/Late-Blight-Tomato-GettyImages-698761786.jpg",
                "Apple Leaf (Scab)": "https://extension.umn.edu/sites/extension.umn.edu/files/Apple-leaf-scab-MBurrows.jpg",
                "Corn Leaf (Rust)": "https://upload.wikimedia.org/wikipedia/commons/5/58/Common_rust_%28Puccinia_sorghi%29_on_corn.jpg"
            }

            # Create buttons with sample images
            with sample_col1:
                if st.button("Tomato - Late Blight"):
                    st.session_state.sample_img = sample_images["Tomato Leaf (Late Blight)"]

            with sample_col2:
                if st.button("Apple - Scab"):
                    st.session_state.sample_img = sample_images["Apple Leaf (Scab)"]

            with sample_col3:
                if st.button("Corn - Rust"):
                    st.session_state.sample_img = sample_images["Corn Leaf (Rust)"]

            # Display selected sample image if applicable
            if "sample_img" in st.session_state and st.session_state.sample_img:
                try:
                    response = requests.get(st.session_state.sample_img)
                    img = Image.open(io.BytesIO(response.content))
                    st.image(img, caption="Selected Sample Image", use_container_width=True)

                    # Store image in session state as bytes
                    buf = io.BytesIO()
                    img.save(buf, format="JPEG")
                    st.session_state.sample_img_bytes = buf.getvalue()
                except Exception as e:
                    st.error(f"Error loading sample image: {str(e)}")

            # Add a detect button
            detect_col1, detect_col2 = st.columns([1, 2])
            with detect_col1:
                detect_button = st.button("🔍 Detect Disease", type="primary", use_container_width=True)

        with col2:
            st.markdown("### Tips for Best Results")

            st.markdown("""
            <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h4 style="color: #558B2F; margin-top: 0;">📸 Taking Good Photos</h4>
                <ul style="margin-bottom: 0;">
                    <li>Ensure good lighting</li>
                    <li>Get close-ups of symptoms</li>
                    <li>Include both healthy and affected areas</li>
                    <li>Capture multiple angles if needed</li>
                </ul>
            </div>
            
            <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                <h4 style="color: #558B2F; margin-top: 0;">🌿 Common Symptoms</h4>
                <ul style="margin-bottom: 0;">
                    <li>Spots or lesions on leaves</li>
                    <li>Discoloration or yellowing</li>
                    <li>Wilting or curling</li>
                    <li>Unusual growth patterns</li>
                    <li>White powdery or fuzzy coatings</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Process the image for disease detection if button clicked
        if detect_button:
            if uploaded_file is not None:
                # Process the uploaded file
                image_bytes = uploaded_file.getvalue()
                process_disease_detection(image_bytes)
            elif "sample_img_bytes" in st.session_state and st.session_state.sample_img_bytes:
                # Process the sample image
                process_disease_detection(st.session_state.sample_img_bytes)
            else:
                st.warning("Please upload an image or select a sample image first.")

    with tab2:
        st.markdown("### Common Plant Diseases Encyclopedia")

        # Disease categories organized by plant type
        plant_types = [
            "Tomato", "Apple", "Potato", "Corn", "Grape",
            "Strawberry", "Bell Pepper", "Cherry", "Peach", "Soybean"
        ]

        selected_plant = st.selectbox(
            "Select plant type",
            plant_types
        )

        # Show information about common diseases for the selected plant
        if selected_plant == "Tomato":
            display_disease_info({
                "Late Blight": {
                    "image_url": "https://www.goodhousekeeping.com/content/dam/gh/pages/tomato-plant-diseases/Late-Blight-Tomato-GettyImages-698761786.jpg",
                    "description": "One of the most devastating tomato diseases, late blight can destroy plants within days. It's caused by the water mold Phytophthora infestans.",
                    "symptoms": ["Dark brown spots on leaves", "White fuzzy growth on leaf undersides", "Fast spreading lesions", "Brown patches on stems", "Fruit develops greasy gray spots"],
                    "management": ["Apply copper-based fungicides", "Remove and destroy infected plants", "Improve air circulation", "Avoid overhead watering", "Plant resistant varieties"]
                },
                "Early Blight": {
                    "image_url": "https://extension.umn.edu/sites/extension.umn.edu/files/styles/optimized/public/early-blight-tomato-MBurrows.jpg",
                    "description": "A common fungal disease that begins on older leaves and progresses upward. Caused by Alternaria solani.",
                    "symptoms": ["Dark concentric rings on leaves", "Yellowing around lesions", "Brown spots with target-like appearance", "Lower leaves affected first", "Dark lesions on stems"],
                    "management": ["Remove infected leaves", "Apply fungicides preventatively", "Mulch around plants", "Ensure adequate spacing", "Rotate crops"]
                },
                "Leaf Mold": {
                    "image_url": "https://www.almanac.com/sites/default/files/styles/max_1300x1300/public/image_nodes/tomato_leaf-mold_-rutsmetbloemen-ss.jpg",
                    "description": "Common in humid environments, especially in greenhouses. Caused by the fungus Passalora fulva.",
                    "symptoms": ["Yellow patches on upper leaf surface", "Olive-green to brown velvety mold on leaf undersides", "Leaves curl and wither", "Reduced fruit yield"],
                    "management": ["Improve air circulation", "Reduce humidity", "Apply fungicides", "Remove infected leaves", "Use resistant varieties"]
                }
            })
        elif selected_plant == "Apple":
            display_disease_info({
                "Apple Scab": {
                    "image_url": "https://extension.umn.edu/sites/extension.umn.edu/files/Apple-leaf-scab-MBurrows.jpg",
                    "description": "Most common apple disease, caused by the fungus Venturia inaequalis.",
                    "symptoms": ["Olive-green to brown spots on leaves", "Scabby dark lesions on fruit", "Premature leaf drop", "Deformed fruit", "Cracks in fruit skin"],
                    "management": ["Apply fungicides preventatively", "Remove and destroy fallen leaves", "Prune trees for better air circulation", "Plant resistant varieties", "Apply dormant sprays before bud break"]
                }
            })

def process_disease_detection(image_bytes):
    """
    Process image for disease detection

    Args:
        image_bytes: Bytes of the image to analyze
    """
    try:
        with st.spinner("Analyzing leaf image..."):
            # Add a slight delay to simulate processing
            time.sleep(1.5)

            # Make prediction using disease detector
            # Pass image bytes directly without re-opening (it's already loaded as bytes)
            results = disease_detector.detect_disease(io.BytesIO(image_bytes))

            if results["success"]:
                predictions = results["predictions"]

                # Display top prediction
                top_prediction = predictions[0]
                confidence = top_prediction["confidence"]
                disease_name = top_prediction["disease"]

                # Determine status color based on confidence
                if "Healthy" in disease_name:
                    status_color = "#4CAF50"  # Green
                    status_text = "Healthy Plant"
                else:
                    status_color = "#F44336"  # Red
                    status_text = "Disease Detected"

                # Display result in a visually appealing way
                st.markdown(f"""
                <div style="background-color: {status_color}; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                    <h2 style="color: white; margin: 0;">Diagnosis Result</h2>
                    <h1 style="color: white; margin: 10px 0; font-size: 36px;">{disease_name}</h1>
                    <p style="color: white; font-weight: bold;">Confidence: {confidence:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)

                # Show top 3 predictions as options
                st.subheader("Alternative Possibilities:")

                # Create columns for each alternative
                cols = st.columns(len(predictions) - 1) if len(predictions) > 1 else [st.container()]

                # Display alternatives (skip the first one as it's already displayed)
                for i, (col, pred) in enumerate(zip(cols, predictions[1:])):
                    with col:
                        prob = pred["confidence"]
                        alt_disease = pred["disease"]

                        background_color = "#F1F8E9" if "Healthy" in alt_disease else "#FFF3E0"

                        st.markdown(f"""
                        <div style="background-color: {background_color}; padding: 10px; border-radius: 10px; text-align: center; height: 100%;">
                            <p style="font-weight: bold; margin-bottom: 5px;">{alt_disease}</p>
                            <p>Confidence: {prob:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Get treatment information for the detected disease
                treatment_info = disease_detector.get_treatment_info(disease_name)

                # Display treatment information if available
                if treatment_info["success"]:
                    info = treatment_info["treatment_info"]

                    # Create tabs for treatment information
                    info_tab1, info_tab2, info_tab3 = st.tabs(["📋 Overview", "💊 Treatment", "🛡️ Prevention"])

                    with info_tab1:
                        st.markdown(f"""
                        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <h3 style="margin-top: 0;">Disease Information</h3>
                            <p><strong>Cause:</strong> {info.get('cause', 'Not available')}</p>
                            <p><strong>Symptoms:</strong> {info.get('symptoms', 'Not available')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with info_tab2:
                        treatments = info.get('treatment', [])
                        if treatments:
                            st.markdown("<h3>Recommended Treatments</h3>", unsafe_allow_html=True)
                            for i, treatment in enumerate(treatments):
                                st.markdown(f"""
                                <div style="background-color: #F1F8E9; padding: 10px; border-radius: 10px; margin: 5px 0;">
                                    <p style="margin: 0;"><strong>{i+1}.</strong> {treatment}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.info("No specific treatment information available.")

                    with info_tab3:
                        prevention = info.get('prevention', 'Not available')
                        st.markdown(f"""
                        <div style="background-color: #FFF8E1; padding: 15px; border-radius: 10px;">
                            <h3 style="margin-top: 0;">Prevention</h3>
                            <p>{prevention}</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No specific treatment information is available for this condition.")

                # Save detection results to session state
                if "disease_detection_history" not in st.session_state:
                    st.session_state.disease_detection_history = []

                # Add current detection to history
                detection_record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "disease": disease_name,
                    "confidence": confidence
                }
                st.session_state.disease_detection_history.insert(0, detection_record)

                # Keep only the last 10 records
                if len(st.session_state.disease_detection_history) > 10:
                    st.session_state.disease_detection_history = st.session_state.disease_detection_history[:10]

            else:
                st.error(f"Error during disease detection: {results.get('error', 'Unknown error')}")
                st.info("Please try again with a clearer image.")

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please make sure the image is valid and try again.")

def display_disease_info(disease_dict):
    """
    Display information about diseases in a visually appealing way

    Args:
        disease_dict: Dictionary with disease information
    """
    for disease_name, info in disease_dict.items():
        with st.expander(f"{disease_name}", expanded=True if len(disease_dict) == 1 else False):
            col1, col2 = st.columns([1, 1])

            with col1:
                try:
                    st.image(info["image_url"], caption=disease_name, use_container_width=True)
                except:
                    st.error("Image not available")

            with col2:
                st.markdown(f"**Description**: {info['description']}")

                st.markdown("**Symptoms:**")
                for symptom in info["symptoms"]:
                    st.markdown(f"• {symptom}")

                st.markdown("**Management:**")
                for management in info["management"]:
                    st.markdown(f"• {management}")

