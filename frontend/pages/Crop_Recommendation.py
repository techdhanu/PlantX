import streamlit as st
import pickle
import numpy as np
import os
import time
import pandas as pd

def show():
    st.header("🌾 Crop Recommendation System")

    # Add instructional information and explanation
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2E7D32;">
        <h3 style="color: #2E7D32; margin-top: 0;">How it works</h3>
        <p>Our AI model analyzes your soil composition and local climate conditions to recommend the most suitable crops for optimal growth and yield. Enter the values below to get personalized recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Soil and Climate Parameters")
        st.markdown("Enter accurate values for best recommendations:")

        # Create a visually appealing form with tooltips and ranges
        with st.form("crop_recommendation_form"):
            # NPK values
            npk_col1, npk_col2, npk_col3 = st.columns(3)

            with npk_col1:
                nitrogen = st.number_input(
                    "Nitrogen (N) mg/kg",
                    min_value=0,
                    max_value=150,
                    value=40,
                    help="Nitrogen content in soil (typical range: 0-140 mg/kg)"
                )

            with npk_col2:
                phosphorus = st.number_input(
                    "Phosphorus (P) mg/kg",
                    min_value=0,
                    max_value=150,
                    value=30,
                    help="Phosphorus content in soil (typical range: 5-100 mg/kg)"
                )

            with npk_col3:
                potassium = st.number_input(
                    "Potassium (K) mg/kg",
                    min_value=0,
                    max_value=210,
                    value=40,
                    help="Potassium content in soil (typical range: 5-200 mg/kg)"
                )

            # Environmental factors
            st.markdown("#### 🌤️ Environmental Conditions")
            env_col1, env_col2, env_col3 = st.columns(3)

            with env_col1:
                temperature = st.slider(
                    "Temperature (°C)",
                    min_value=0.0,
                    max_value=45.0,
                    value=25.0,
                    step=0.1,
                    help="Average temperature in your region"
                )

            with env_col2:
                humidity = st.slider(
                    "Humidity (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=65.0,
                    step=1.0,
                    help="Average relative humidity in percentage"
                )

            with env_col3:
                ph = st.slider(
                    "pH value",
                    min_value=3.0,
                    max_value=10.0,
                    value=6.5,
                    step=0.1,
                    help="Soil pH level (7 is neutral, below 7 is acidic, above 7 is alkaline)"
                )

            rainfall = st.slider(
                "Rainfall (mm per year)",
                min_value=0.0,
                max_value=3000.0,
                value=1000.0,
                step=10.0,
                help="Annual rainfall in millimeters"
            )

            # Add a visual pH scale
            ph_scale = """
            <div style="margin-top: 5px; margin-bottom: 15px;">
                <p style="margin-bottom: 5px; font-size: 14px;"><strong>pH Scale Reference:</strong></p>
                <div style="display: flex; width: 100%; height: 20px; border-radius: 5px; overflow: hidden;">
                    <div style="flex: 1; background: linear-gradient(to right, #FF4500, #FFA500);" title="Acidic (3-6)"></div>
                    <div style="flex: 0.5; background: #7CFC00;" title="Neutral (6-7.5)"></div>
                    <div style="flex: 1; background: linear-gradient(to right, #00BFFF, #0000FF);" title="Alkaline (7.5-10)"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px;">
                    <span>Acidic (3.0)</span>
                    <span>Neutral (7.0)</span>
                    <span>Alkaline (10.0)</span>
                </div>
            </div>
            """
            st.markdown(ph_scale, unsafe_allow_html=True)

            # Submit button
            submitted = st.form_submit_button(
                "🌱 Predict Best Crop",
                use_container_width=True,
                type="primary"
            )

    with col2:
        st.markdown("### 📖 NPK Guide")
        st.markdown("""
        <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; margin-bottom: 15px; font-size: 14px;">
            <h4 style="color: #2E7D32; margin-top: 0;">Nitrogen (N)</h4>
            <p style="margin-bottom: 5px;">• Essential for leaf growth</p>
            <p style="margin-bottom: 5px;">• Influences protein production</p>
            <p style="margin-bottom: 0;">• Affects green color intensity</p>
        </div>
        
        <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; margin-bottom: 15px; font-size: 14px;">
            <h4 style="color: #2E7D32; margin-top: 0;">Phosphorus (P)</h4>
            <p style="margin-bottom: 5px;">• Important for root development</p>
            <p style="margin-bottom: 5px;">• Crucial for flower and seed formation</p>
            <p style="margin-bottom: 0;">• Helps in energy transfer processes</p>
        </div>
        
        <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; font-size: 14px;">
            <h4 style="color: #2E7D32; margin-top: 0;">Potassium (K)</h4>
            <p style="margin-bottom: 5px;">• Regulates water content</p>
            <p style="margin-bottom: 5px;">• Improves disease resistance</p>
            <p style="margin-bottom: 0;">• Enhances fruit quality</p>
        </div>
        """, unsafe_allow_html=True)

    # Process prediction
    if 'submitted' in locals() and submitted:
        with st.spinner('Analyzing soil and environmental conditions...'):
            time.sleep(1)  # Simulate processing time

        try:
            # Use relative path to load model
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models", "crop_recommendation_model.pkl")

            with open(model_path, "rb") as model_file:
                model = pickle.load(model_file)

            # Input for prediction
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

            # Make prediction
            prediction = model.predict(input_data)
            recommended_crop = prediction[0].capitalize()

            # Display result with animation
            st.balloons()

            # Display recommended crop in a visually appealing card
            st.markdown(f"""
            <div style="background-color: #2E7D32; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                <h2 style="color: white; margin: 0;">Recommended Crop</h2>
                <h1 style="color: white; margin: 10px 0; font-size: 36px;">{recommended_crop}</h1>
                <p style="color: white; font-style: italic;">Best suited for your soil and climate conditions</p>
            </div>
            """, unsafe_allow_html=True)

            # Create a function to display crop information based on prediction
            def display_crop_info(crop_name):
                # Dictionary of crop information
                crop_info = {
                    'Rice': {
                        'image_url': 'https://images.unsplash.com/photo-1569132891433-0ee04818151e?q=80&w=1170&auto=format&fit=crop',
                        'description': 'Rice thrives in wet environments and requires flooded fields for optimal growth. It\'s a staple crop in many cultures.',
                        'growing_season': 'Typically 3-6 months, depending on variety',
                        'soil_preference': 'Clay soils that retain water well',
                        'water_needs': 'Very high - requires flooded conditions',
                        'special_notes': 'Needs consistent water levels and warm temperatures'
                    },
                    'Wheat': {
                        'image_url': 'https://images.unsplash.com/photo-1627634777225-55cdcbce5e34?q=80&w=1170&auto=format&fit=crop',
                        'description': 'Wheat is adaptable to various conditions and is one of the world\'s most important food crops.',
                        'growing_season': 'Winter wheat: planted in fall, harvested in summer; Spring wheat: planted in spring, harvested in fall',
                        'soil_preference': 'Well-draining loamy soil',
                        'water_needs': 'Moderate - about 450-650mm during growing season',
                        'special_notes': 'Drought-tolerant once established'
                    },
                    'Maize': {
                        'image_url': 'https://images.unsplash.com/photo-1598196333442-9405be60fc54?q=80&w=774&auto=format&fit=crop',
                        'description': 'Maize (corn) is a versatile crop used for food, feed, and industrial products. It requires warm conditions.',
                        'growing_season': '90-120 days depending on variety',
                        'soil_preference': 'Well-drained, fertile soils',
                        'water_needs': 'High - consistent moisture especially during silking',
                        'special_notes': 'Sensitive to frost; needs warm nights'
                    },
                    # Add more crops as needed
                }

                # Default information if crop not in dictionary
                default_info = {
                    'image_url': 'https://images.unsplash.com/photo-1517768692594-a8221d437002?q=80&w=1170&auto=format&fit=crop',
                    'description': f'{crop_name} is well-suited for your soil conditions and local climate according to our AI model.',
                    'growing_season': 'Varies by region and variety',
                    'soil_preference': 'As indicated by your soil analysis',
                    'water_needs': 'Follow local agricultural extension guidance',
                    'special_notes': 'Consult with local agricultural experts for specific cultivation advice'
                }

                # Get info for this crop (or use default)
                info = crop_info.get(crop_name, default_info)

                # Create an expander with crop details
                with st.expander("View Crop Details", expanded=True):
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.image(info['image_url'], caption=f"{crop_name}", use_column_width=True)

                    with col2:
                        st.markdown(f"**Description:** {info['description']}")
                        st.markdown(f"**Growing Season:** {info['growing_season']}")
                        st.markdown(f"**Soil Preference:** {info['soil_preference']}")
                        st.markdown(f"**Water Needs:** {info['water_needs']}")
                        st.markdown(f"**Special Notes:** {info['special_notes']}")

                # Display next steps and recommendations
                st.markdown("### 📝 Recommendations")
                st.markdown("""
                <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <h4 style="color: #2E7D32; margin-top: 0;">Next Steps</h4>
                    <ul>
                        <li>Check best planting times for your specific region</li>
                        <li>Consider crop rotation benefits for soil health</li>
                        <li>Use our Yield Prediction tool to forecast harvest potential</li>
                        <li>Set up Climate Risk Alerts to protect your crops</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            # Display crop information
            display_crop_info(recommended_crop)

        except FileNotFoundError:
            st.error("❌ Model file not found. Please ensure 'crop_recommendation_model.pkl' is inside the 'models/' folder.")
        except Exception as e:
            st.error(f"⚠️ Error while predicting: {e}")

    # Always show some guidance information at the bottom
    with st.expander("ℹ️ About Crop Recommendation AI"):
        st.markdown("""
        Our crop recommendation system uses a sophisticated machine learning model trained on thousands of agricultural data points. 
        The model considers the following factors:
        
        - **Soil Nutrients (NPK)**: Different crops require different nutrient profiles.
        - **pH Level**: Every crop has an optimal soil pH range for nutrient absorption.
        - **Climate Conditions**: Temperature, humidity, and rainfall patterns affect crop growth.
        
        The AI analyzes these parameters collectively to determine which crop would be most successful in your specific conditions.
        
        For best results:
        1. Use accurate soil test results rather than estimates
        2. Enter climate data based on annual averages for your region
        3. Consider seasonal variations in your planning
        """)
