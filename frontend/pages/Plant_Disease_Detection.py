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
    # Enhanced header with modern design
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #2E7D32, #4CAF50);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🔬 Plant Disease Detection
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0;">
            AI-Powered Disease Diagnosis & Treatment Recommendations
        </p>
        <div style="width: 80px; height: 4px; background: linear-gradient(90deg, #2E7D32, #4CAF50); 
                    margin: 1rem auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced information banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #f0f9ff 100%);
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(46, 125, 50, 0.1); position: relative;">
        <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; 
                    background: linear-gradient(180deg, #2E7D32, #4CAF50); border-radius: 0 4px 4px 0;"></div>
        <div style="display: flex; align-items: start; gap: 1.5rem;">
            <div style="font-size: 3rem;">🤖</div>
            <div>
                <h3 style="color: #2E7D32; margin: 0 0 1rem 0; font-size: 1.5rem;">Advanced AI Disease Diagnosis</h3>
                <p style="margin: 0 0 1rem 0; line-height: 1.6; font-size: 1.05rem;">
                    Upload clear images of your plant leaves to instantly identify diseases and receive comprehensive treatment recommendations.
                    Our state-of-the-art AI model recognizes over <strong>38 different plant diseases</strong> across multiple crop types.
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
                    <div style="background: rgba(46, 125, 50, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #2E7D32;">
                        🍅 Tomato Diseases
                    </div>
                    <div style="background: rgba(46, 125, 50, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #2E7D32;">
                        🥔 Potato Diseases
                    </div>
                    <div style="background: rgba(46, 125, 50, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #2E7D32;">
                        🍎 Apple Diseases
                    </div>
                    <div style="background: rgba(46, 125, 50, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #2E7D32;">
                        🌽 Corn Diseases
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📷 Disease Scanner", "📚 Disease Library", "📊 Statistics"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="color: #2E7D32; margin-bottom: 0.5rem;">📤 Upload Plant Image</h3>
                <p style="color: #666; font-size: 0.95rem;">Upload a clear image of your plant for instant AI analysis</p>
            </div>
            """, unsafe_allow_html=True)

            # Enhanced file uploader
            uploaded_file = st.file_uploader(
                "Choose a clear image of the affected plant part:",
                type=["jpg", "jpeg", "png"],
                help="Supported formats: JPG, JPEG, PNG | Max size: 10MB",
                label_visibility="collapsed"
            )

            # Show upload instructions
            if not uploaded_file:
                st.markdown("""
                <div style="border: 2px dashed #81C784; border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;
                            background: linear-gradient(135deg, #F1F8E9 0%, #E8F5E9 100%);">
                    <div style="font-size: 3rem; margin-bottom: 1rem; color: #2E7D32;">📷</div>
                    <p style="margin: 0; color: #2E7D32; font-weight: 600;">Drag and drop your plant image here</p>
                    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">or click to browse files</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Display uploaded image with enhanced styling
                st.markdown("#### 🖼️ Uploaded Image")
                st.image(uploaded_file, caption="Ready for analysis", use_container_width=True)

            # Enhanced Sample images section
            st.markdown("---")
            st.markdown("""
            <div style="text-align: center; margin: 2rem 0 1rem 0;">
                <h3 style="color: #2E7D32; margin-bottom: 0.5rem;">🖼️ Try Sample Images</h3>
                <p style="color: #666; font-size: 0.95rem;">Click on any sample to test our AI detection system</p>
            </div>
            """, unsafe_allow_html=True)

            sample_col1, sample_col2, sample_col3 = st.columns(3)

            # Sample images - using relative paths from assets folder (works both locally and when deployed)
            assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
            sample_images = {
                "Tomato Late Blight": {
                    "path": os.path.join(assets_dir, "tomato_late_blight.jpeg"),
                    "emoji": "🍅",
                    "description": "Tomato Late Blight"
                },
                "Apple Scab": {
                    "path": os.path.join(assets_dir, "apple_scab.jpg"),
                    "emoji": "🍎",
                    "description": "Apple Scab Disease"
                },
                "Corn Rust": {
                    "path": os.path.join(assets_dir, "corn_rust.jpg"),
                    "emoji": "🌽",
                    "description": "Corn Rust Disease"
                }
            }

            # Create enhanced sample buttons
            with sample_col1:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
                            padding: 1rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid rgba(46, 125, 50, 0.1);
                            margin-bottom: 0.5rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🍅</div>
                    <div style="font-weight: 600; color: #2E7D32; font-size: 0.9rem;">Tomato Late Blight</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔍 Analyze Tomato Sample", key="tomato_sample", use_container_width=True):
                    st.session_state.sample_img = sample_images["Tomato Late Blight"]["path"]

            with sample_col2:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
                            padding: 1rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid rgba(46, 125, 50, 0.1);
                            margin-bottom: 0.5rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🍎</div>
                    <div style="font-weight: 600; color: #2E7D32; font-size: 0.9rem;">Apple Scab</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔍 Analyze Apple Sample", key="apple_sample", use_container_width=True):
                    st.session_state.sample_img = sample_images["Apple Scab"]["path"]

            with sample_col3:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
                            padding: 1rem; border-radius: 12px; text-align: center;
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 1px solid rgba(46, 125, 50, 0.1);
                            margin-bottom: 0.5rem;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌽</div>
                    <div style="font-weight: 600; color: #2E7D32; font-size: 0.9rem;">Corn Rust</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🔍 Analyze Corn Sample", key="corn_sample", use_container_width=True):
                    st.session_state.sample_img = sample_images["Corn Rust"]["path"]

            # Display selected sample image if applicable
            if "sample_img" in st.session_state and st.session_state.sample_img:
                try:
                    # Check if it's a URL or local file path
                    if st.session_state.sample_img.startswith("http"):
                        response = requests.get(st.session_state.sample_img)
                        img = Image.open(io.BytesIO(response.content))
                    else:
                        # Load from local file
                        img = Image.open(st.session_state.sample_img)

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
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
                        padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border: 1px solid rgba(46, 125, 50, 0.1);">
                <h4 style="color: #2E7D32; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    📸 Photo Guidelines
                </h4>
                <div style="display: grid; gap: 0.8rem;">
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(46, 125, 50, 0.05); border-radius: 8px;">
                        <div style="color: #2E7D32; font-size: 1.2rem;">💡</div>
                        <span style="font-size: 0.95rem;">Ensure good natural lighting</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(46, 125, 50, 0.05); border-radius: 8px;">
                        <div style="color: #2E7D32; font-size: 1.2rem;">🔍</div>
                        <span style="font-size: 0.95rem;">Get close-ups of symptoms</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(46, 125, 50, 0.05); border-radius: 8px;">
                        <div style="color: #2E7D32; font-size: 1.2rem;">🌱</div>
                        <span style="font-size: 0.95rem;">Include healthy & affected areas</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(46, 125, 50, 0.05); border-radius: 8px;">
                        <div style="color: #2E7D32; font-size: 1.2rem;">📐</div>
                        <span style="font-size: 0.95rem;">Capture multiple angles</span>
                    </div>
                </div>
            </div>

            <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
                        padding: 1.5rem; border-radius: 16px;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border: 1px solid rgba(46, 125, 50, 0.1);">
                <h4 style="color: #2E7D32; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    🌿 Disease Symptoms
                </h4>
                <div style="display: grid; gap: 0.6rem; font-size: 0.95rem;">
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #2E7D32; border-radius: 50%;"></div>
                        <span>Spots or lesions on leaves</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #2E7D32; border-radius: 50%;"></div>
                        <span>Discoloration or yellowing</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #2E7D32; border-radius: 50%;"></div>
                        <span>Wilting or curling</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #2E7D32; border-radius: 50%;"></div>
                        <span>Unusual growth patterns</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #2E7D32; border-radius: 50%;"></div>
                        <span>White powdery coatings</span>
                    </div>
                </div>
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
                    "symptoms": ["Dark brown spots on leaves", "White fuzzy growth on leaf undersides",
                                 "Fast spreading lesions", "Brown patches on stems",
                                 "Fruit develops greasy gray spots"],
                    "management": ["Apply copper-based fungicides", "Remove and destroy infected plants",
                                   "Improve air circulation", "Avoid overhead watering", "Plant resistant varieties"]
                },
                "Early Blight": {
                    "image_url": "https://extension.umn.edu/sites/extension.umn.edu/files/styles/optimized/public/early-blight-tomato-MBurrows.jpg",
                    "description": "A common fungal disease that begins on older leaves and progresses upward. Caused by Alternaria solani.",
                    "symptoms": ["Dark concentric rings on leaves", "Yellowing around lesions",
                                 "Brown spots with target-like appearance", "Lower leaves affected first",
                                 "Dark lesions on stems"],
                    "management": ["Remove infected leaves", "Apply fungicides preventatively", "Mulch around plants",
                                   "Ensure adequate spacing", "Rotate crops"]
                },
                "Leaf Mold": {
                    "image_url": "https://www.almanac.com/sites/default/files/styles/max_1300x1300/public/image_nodes/tomato_leaf-mold_-rutsmetbloemen-ss.jpg",
                    "description": "Common in humid environments, especially in greenhouses. Caused by the fungus Passalora fulva.",
                    "symptoms": ["Yellow patches on upper leaf surface",
                                 "Olive-green to brown velvety mold on leaf undersides", "Leaves curl and wither",
                                 "Reduced fruit yield"],
                    "management": ["Improve air circulation", "Reduce humidity", "Apply fungicides",
                                   "Remove infected leaves", "Use resistant varieties"]
                }
            })
        elif selected_plant == "Apple":
            display_disease_info({
                "Apple Scab": {
                    "image_url": "https://extension.umn.edu/sites/extension.umn.edu/files/Apple-leaf-scab-MBurrows.jpg",
                    "description": "Most common apple disease, caused by the fungus Venturia inaequalis.",
                    "symptoms": ["Olive-green to brown spots on leaves", "Scabby dark lesions on fruit",
                                 "Premature leaf drop", "Deformed fruit", "Cracks in fruit skin"],
                    "management": ["Apply fungicides preventatively", "Remove and destroy fallen leaves",
                                   "Prune trees for better air circulation", "Plant resistant varieties",
                                   "Apply dormant sprays before bud break"]
                }
            })

    with tab3:
        st.markdown("### 📊 Detection Statistics & History")

        # Check if there's detection history
        if "disease_detection_history" in st.session_state and st.session_state.disease_detection_history:
            history = st.session_state.disease_detection_history

            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Detections", len(history))

            with col2:
                healthy_count = sum(1 for item in history if "Healthy" in item["disease"])
                st.metric("Healthy Plants", healthy_count)

            with col3:
                diseased_count = len(history) - healthy_count
                st.metric("Diseased Plants", diseased_count)

            with col4:
                avg_confidence = sum(item["confidence"] for item in history) / len(history)
                st.metric("Avg Confidence", f"{avg_confidence:.1f}%")

            st.markdown("---")

            # Recent detections
            st.markdown("### 🕒 Recent Detection History")
            for i, detection in enumerate(history[:5]):  # Show last 5 detections
                status_color = "#4CAF50" if "Healthy" in detection["disease"] else "#F44336"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fffe 100%);
                            padding: 1rem; border-radius: 12px; margin: 0.5rem 0;
                            border-left: 4px solid {status_color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: {status_color};">{detection["disease"]}</strong>
                            <br><small style="color: #666;">Confidence: {detection["confidence"]:.1f}%</small>
                        </div>
                        <div style="text-align: right; color: #666; font-size: 0.9rem;">
                            {detection["timestamp"]}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Disease frequency chart
            if len(history) > 1:
                st.markdown("### 📈 Disease Frequency Analysis")
                disease_counts = {}
                for detection in history:
                    disease = detection["disease"]
                    disease_counts[disease] = disease_counts.get(disease, 0) + 1

                # Create a simple bar chart representation
                for disease, count in sorted(disease_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / len(history)) * 100
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
                            <span style="font-weight: 600;">{disease}</span>
                            <span>{count} ({percentage:.1f}%)</span>
                        </div>
                        <div style="background: #E8F5E9; height: 8px; border-radius: 4px;">
                            <div style="background: linear-gradient(90deg, #2E7D32, #4CAF50); 
                                        width: {percentage}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No detection history available yet. Start by analyzing some plant images!")
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #666;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📊</div>
                <p>Your detection statistics and history will appear here after you start using the disease scanner.</p>
            </div>
            """, unsafe_allow_html=True)

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

