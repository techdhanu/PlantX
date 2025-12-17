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
        with st.spinner('🔬 Analyzing soil composition...'):
            time.sleep(1)  # Simulate processing
            # Debug: Log image processing start
            logging.debug("Starting soil image analysis.")

            # Get predictions from the model
            predictions = soil_classifier.classify_soil(image_bytes)

            # Debug: Log predictions
            logging.debug(f"Predictions received: {predictions}")

            if predictions and len(predictions) > 0:
                top_prediction = predictions[0]
                soil_type = top_prediction["soil_type"]
                confidence = top_prediction["confidence"]

                # Separator
                st.markdown("---")

                # Color based on confidence level
                if confidence >= 80:
                    status_color = "#8B4513"  # Brown
                    status_text = "High Confidence"
                elif confidence >= 60:
                    status_color = "#D2691E"  # Chocolate
                    status_text = "Good Confidence"
                else:
                    status_color = "#CD853F"  # Peru
                    status_text = "Moderate Confidence"

                # Display result in a visually appealing way
                st.markdown(f"""
                <div style="background-color: {status_color}; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                    <h2 style="color: white; margin: 0;">Analysis Result</h2>
                    <h1 style="color: white; margin: 10px 0; font-size: 36px;">{soil_type}</h1>
                    <p style="color: white; font-weight: bold;">Confidence: {confidence:.1f}%</p>
                    <p style="color: white; font-size: 0.9rem; margin: 5px 0 0 0;">{status_text}</p>
                </div>
                """, unsafe_allow_html=True)

                # Show top 3 predictions as alternatives
                if len(predictions) > 1:
                    st.markdown("### 🔄 Alternative Possibilities")

                    # Create columns for alternatives
                    alt_predictions = predictions[1:4]  # Get next 3
                    cols = st.columns(len(alt_predictions))

                    for col, pred in zip(cols, alt_predictions):
                        with col:
                            prob = pred["confidence"]
                            alt_soil = pred["soil_type"]

                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 100%); 
                                        padding: 15px; border-radius: 10px; text-align: center; height: 100%;
                                        border: 1px solid rgba(139, 69, 19, 0.2);">
                                <p style="font-weight: bold; margin-bottom: 5px; color: #8B4513;">{alt_soil}</p>
                                <p style="color: #666;">Confidence: {prob:.1f}%</p>
                            </div>
                            """, unsafe_allow_html=True)

                # Get soil properties
                soil_properties = get_soil_properties(soil_type)

                # Create tabs for detailed information
                info_tab1, info_tab2, info_tab3 = st.tabs([
                    "📋 Overview",
                    "🌾 Best Crops",
                    "💧 Management"
                ])

                with info_tab1:
                    st.markdown("<h3 style='color: #8B4513;'>🌱 Soil Properties</h3>", unsafe_allow_html=True)

                    prop_col1, prop_col2 = st.columns(2)

                    properties_list = list(soil_properties.items())
                    mid = len(properties_list) // 2

                    with prop_col1:
                        for key, value in properties_list[:mid]:
                            if key != 'Best For' and key != 'Management':
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #ffffff 0%, #FFF8DC 100%); 
                                            padding: 15px; border-radius: 10px; margin: 8px 0;
                                            border: 1px solid rgba(139, 69, 19, 0.1);">
                                    <p style="margin: 0; color: #8B4513; font-weight: 600;">{key}</p>
                                    <p style="margin: 5px 0 0 0; color: #333;">{value}</p>
                                </div>
                                """, unsafe_allow_html=True)

                    with prop_col2:
                        for key, value in properties_list[mid:]:
                            if key != 'Best For' and key != 'Management':
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #ffffff 0%, #FFF8DC 100%); 
                                            padding: 15px; border-radius: 10px; margin: 8px 0;
                                            border: 1px solid rgba(139, 69, 19, 0.1);">
                                    <p style="margin: 0; color: #8B4513; font-weight: 600;">{key}</p>
                                    <p style="margin: 5px 0 0 0; color: #333;">{value}</p>
                                </div>
                                """, unsafe_allow_html=True)

                with info_tab2:
                    best_crops = soil_properties.get('Best For', 'Not specified')
                    st.markdown("<h3 style='color: #8B4513;'>🌾 Recommended Crops</h3>", unsafe_allow_html=True)

                    if best_crops and best_crops != 'Not specified':
                        # Split crops by comma
                        crops_list = [crop.strip() for crop in best_crops.split(',')]

                        # Display crops in a grid
                        crop_cols = st.columns(2)
                        for i, crop in enumerate(crops_list):
                            with crop_cols[i % 2]:
                                st.markdown(f"""
                                <div style="background: linear-gradient(135deg, #ffffff 0%, #FFF8DC 100%); 
                                            padding: 12px; border-radius: 8px; margin: 5px 0; text-align: center;
                                            border: 1px solid rgba(139, 69, 19, 0.2);
                                            box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                                    <p style="margin: 0; font-weight: 600; color: #8B4513;">🌱 {crop}</p>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info("No specific crop recommendations available.")

                with info_tab3:
                    management = soil_properties.get('Management', 'Not specified')
                    st.markdown("<h3 style='color: #8B4513;'>💧 Soil Management Tips</h3>", unsafe_allow_html=True)

                    if management and management != 'Not specified':
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 100%); 
                                    padding: 20px; border-radius: 10px; margin: 10px 0;
                                    border-left: 4px solid #8B4513;">
                            <p style="margin: 0; color: #333; line-height: 1.8;">{management}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("No specific management tips available.")

            else:
                st.warning("No predictions could be made. Please try with a clearer soil image.")

    except Exception as e:
        # Debug: Log errors
        logging.error(f"An error occurred during analysis: {str(e)}")
        st.error(f"An error occurred during analysis: {str(e)}")
        st.info("Please make sure the image is valid and try again.")


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
    # Enhanced header with modern design
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #8B4513, #D2691E);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🌱 Soil Type Analysis
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0;">
            AI-Powered Soil Classification & Management Recommendations
        </p>
        <div style="width: 80px; height: 4px; background: linear-gradient(90deg, #8B4513, #D2691E); 
                    margin: 1rem auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced information banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 100%);
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(139, 69, 19, 0.1); position: relative;">
        <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; 
                    background: linear-gradient(180deg, #8B4513, #D2691E); border-radius: 0 4px 4px 0;"></div>
        <div style="display: flex; align-items: start; gap: 1.5rem;">
            <div style="font-size: 3rem;">🤖</div>
            <div>
                <h3 style="color: #8B4513; margin: 0 0 1rem 0; font-size: 1.5rem;">Advanced AI Soil Classification</h3>
                <p style="margin: 0 0 1rem 0; line-height: 1.6; font-size: 1.05rem;">
                    Upload clear images of your soil to instantly identify its type and receive comprehensive management recommendations.
                    Our state-of-the-art AI model recognizes <strong>10 different soil types</strong> with tailored crop suggestions.
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
                    <div style="background: rgba(139, 69, 19, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #8B4513;">
                        🏜️ Alluvial Soil
                    </div>
                    <div style="background: rgba(139, 69, 19, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #8B4513;">
                        🌑 Black Soil
                    </div>
                    <div style="background: rgba(139, 69, 19, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #8B4513;">
                        🟤 Clay Soil
                    </div>
                    <div style="background: rgba(139, 69, 19, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #8B4513;">
                        🟫 Loamy Soil
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state for tracking uploaded images
    if 'last_uploaded_file_id' not in st.session_state:
        st.session_state.last_uploaded_file_id = None
    if 'soil_predictions' not in st.session_state:
        st.session_state.soil_predictions = None

    # Create tabs
    tab1, tab2 = st.tabs(["📷 Soil Scanner", "📚 Soil Library"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="color: #8B4513; margin-bottom: 0.5rem;">📤 Upload Soil Image</h3>
                <p style="color: #666; font-size: 0.95rem;">Upload a clear image of your soil for instant AI analysis</p>
            </div>
            """, unsafe_allow_html=True)

            # Enhanced file uploader
            uploaded_file = st.file_uploader(
                "Choose a clear image of your soil:",
                type=["jpg", "jpeg", "png"],
                help="Supported formats: JPG, JPEG, PNG | Max size: 10MB",
                key="soil_uploader",
                label_visibility="collapsed"
            )

            # Check if a new file was uploaded
            current_file_id = None
            if uploaded_file is not None:
                current_file_id = uploaded_file.file_id if hasattr(uploaded_file, 'file_id') else str(
                    hash(uploaded_file.name + str(uploaded_file.size)))

                # Display the uploaded image with enhanced styling
                st.markdown("#### 🖼️ Uploaded Image")
                st.image(uploaded_file, caption="Ready for analysis", use_container_width=True)
            else:
                # Show upload instructions
                st.markdown("""
                <div style="border: 2px dashed #D2691E; border-radius: 12px; padding: 2rem; text-align: center; margin: 1rem 0;
                            background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 100%);">
                    <div style="font-size: 3rem; margin-bottom: 1rem; color: #8B4513;">📷</div>
                    <p style="margin: 0; color: #8B4513; font-weight: 600;">Drag and drop your soil image here</p>
                    <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 0.9rem;">or click to browse files</p>
                </div>
                """, unsafe_allow_html=True)

            analyze_col1, analyze_col2 = st.columns([1, 2])
            with analyze_col1:
                analyze_button = st.button("🔍 Analyze Soil", type="primary", use_container_width=True)

        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ffffff 0%, #FFF8DC 100%);
                        padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border: 1px solid rgba(139, 69, 19, 0.1);">
                <h4 style="color: #8B4513; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    📸 Photo Guidelines
                </h4>
                <div style="display: grid; gap: 0.8rem;">
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(139, 69, 19, 0.05); border-radius: 8px;">
                        <div style="color: #8B4513; font-size: 1.2rem;">💡</div>
                        <span style="font-size: 0.95rem;">Ensure good natural lighting</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(139, 69, 19, 0.05); border-radius: 8px;">
                        <div style="color: #8B4513; font-size: 1.2rem;">🧹</div>
                        <span style="font-size: 0.95rem;">Clear away debris and vegetation</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(139, 69, 19, 0.05); border-radius: 8px;">
                        <div style="color: #8B4513; font-size: 1.2rem;">📏</div>
                        <span style="font-size: 0.95rem;">Include a few inches depth</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(139, 69, 19, 0.05); border-radius: 8px;">
                        <div style="color: #8B4513; font-size: 1.2rem;">🌞</div>
                        <span style="font-size: 0.95rem;">Avoid shadows or glare</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; 
                                background: rgba(139, 69, 19, 0.05); border-radius: 8px;">
                        <div style="color: #8B4513; font-size: 1.2rem;">🎨</div>
                        <span style="font-size: 0.95rem;">Capture texture and color</span>
                    </div>
                </div>
            </div>

            <div style="background: linear-gradient(135deg, #ffffff 0%, #FFF8DC 100%);
                        padding: 1.5rem; border-radius: 16px;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border: 1px solid rgba(139, 69, 19, 0.1);">
                <h4 style="color: #8B4513; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                    🌱 Soil Characteristics
                </h4>
                <div style="display: grid; gap: 0.6rem; font-size: 0.95rem;">
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #8B4513; border-radius: 50%;"></div>
                        <span>Color and texture</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #8B4513; border-radius: 50%;"></div>
                        <span>Moisture content</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #8B4513; border-radius: 50%;"></div>
                        <span>Particle size</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #8B4513; border-radius: 50%;"></div>
                        <span>Organic matter visible</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 0.8rem;">
                        <div style="width: 8px; height: 8px; background: #8B4513; border-radius: 50%;"></div>
                        <span>Drainage patterns</span>
                    </div>
                </div>
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
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="color: #8B4513; margin-bottom: 0.5rem;">📚 Soil Types Encyclopedia</h2>
            <p style="color: #666; font-size: 1rem;">Explore different soil types and their characteristics</p>
        </div>
        """, unsafe_allow_html=True)

        # Display information about all soil types
        soil_types_info = {
            "Alluvial soil": {
                "emoji": "🏜️",
                "description": "Deposited by water, very fertile soil found in river plains and deltas.",
                "characteristics": ["Rich in minerals", "Good drainage", "High fertility", "Easy to cultivate"],
                "common_locations": "River valleys and deltas"
            },
            "Black Soil": {
                "emoji": "🌑",
                "description": "Rich in calcium carbonate, iron, and magnesium, excellent for cotton cultivation.",
                "characteristics": ["High water retention", "Rich in minerals", "Self-ploughing nature",
                                    "Good for cotton"],
                "common_locations": "Deccan plateau regions"
            },
            "Cinder Soil": {
                "emoji": "🌋",
                "description": "Formed from volcanic debris, well-draining but low in nutrients.",
                "characteristics": ["Excellent drainage", "Low nutrient content", "Light weight", "Porous"],
                "common_locations": "Volcanic regions"
            },
            "Clay soil": {
                "emoji": "🟤",
                "description": "Dense, heavy soil with high nutrient content but poor drainage.",
                "characteristics": ["High water retention", "Rich in nutrients", "Poor drainage", "Hard when dry"],
                "common_locations": "Low-lying areas"
            },
            "Laterite Soil": {
                "emoji": "🔴",
                "description": "Rich in iron oxides and aluminum, formed in tropical regions.",
                "characteristics": ["Poor fertility", "Good drainage", "Rich in iron", "Acidic"],
                "common_locations": "Tropical regions with high rainfall"
            },
            "Loamy soil": {
                "emoji": "🟫",
                "description": "Perfect balance of sand, silt, and clay, ideal for most plants.",
                "characteristics": ["Good drainage", "High fertility", "Easy to work", "Good structure"],
                "common_locations": "Temperate regions"
            },
            "Peat Soil": {
                "emoji": "🟤",
                "description": "High in organic matter, formed from partially decomposed vegetation.",
                "characteristics": ["High organic content", "High water retention", "Acidic", "Low in minerals"],
                "common_locations": "Wetland areas"
            },
            "Red soil": {
                "emoji": "🔸",
                "description": "Rich in iron oxides, giving it a distinctive red color.",
                "characteristics": ["Good drainage", "Poor fertility", "Iron-rich", "Acidic"],
                "common_locations": "Tropical and subtropical regions"
            },
            "Sandy soil": {
                "emoji": "🏖️",
                "description": "Coarse-textured, well-draining soil with large particles.",
                "characteristics": ["Excellent drainage", "Low fertility", "Low water retention", "Easy to work"],
                "common_locations": "Coastal and arid regions"
            },
            "Yellow Soil": {
                "emoji": "🟡",
                "description": "Yellowish soil, intermediate between red and laterite soils.",
                "characteristics": ["Medium fertility", "Good drainage", "Sandy loam texture", "Slightly acidic"],
                "common_locations": "Eastern and southeastern regions"
            }
        }

        # Create a grid display for soil types
        soil_cols = st.columns(2)

        for i, (soil_type, info) in enumerate(soil_types_info.items()):
            with soil_cols[i % 2]:
                with st.expander(f"{info['emoji']} **{soil_type}**", expanded=False):
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 100%); 
                                padding: 15px; border-radius: 10px; margin: 10px 0;
                                border: 1px solid rgba(139, 69, 19, 0.1);">
                        <h4 style="margin-top: 0; color: #8B4513;">Description</h4>
                        <p style="color: #333; line-height: 1.6;">{info['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("**Characteristics:**")
                    for char in info['characteristics']:
                        st.markdown(f"""
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin: 5px 0;">
                            <div style="width: 6px; height: 6px; background: #8B4513; border-radius: 50%;"></div>
                            <span style="color: #333;">{char}</span>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div style="background: rgba(139, 69, 19, 0.05); 
                                padding: 10px; border-radius: 8px; margin: 10px 0;
                                border-left: 3px solid #8B4513;">
                        <p style="margin: 0; color: #8B4513; font-weight: 600;">📍 Common Locations</p>
                        <p style="margin: 5px 0 0 0; color: #333;">{info['common_locations']}</p>
                    </div>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show()
