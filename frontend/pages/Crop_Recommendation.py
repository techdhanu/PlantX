import streamlit as st
import pickle
import numpy as np
import os
import time
import pandas as pd


def show():
    # Enhanced header with modern design
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #558B2F, #8BC34A);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🌾 Crop Recommendation System
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0;">
            AI-Powered Crop Selection Based on Soil & Climate Analysis
        </p>
        <div style="width: 80px; height: 4px; background: linear-gradient(90deg, #558B2F, #8BC34A); 
                    margin: 1rem auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced information banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%);
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(85, 139, 47, 0.1); position: relative;">
        <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; 
                    background: linear-gradient(180deg, #558B2F, #8BC34A); border-radius: 0 4px 4px 0;"></div>
        <div style="display: flex; align-items: start; gap: 1.5rem;">
            <div style="font-size: 3rem;">🤖</div>
            <div>
                <h3 style="color: #558B2F; margin: 0 0 1rem 0; font-size: 1.5rem;">AI-Powered Crop Selection</h3>
                <p style="margin: 0 0 1rem 0; line-height: 1.6; font-size: 1.05rem;">
                    Our advanced AI model analyzes your <strong>soil composition and local climate conditions</strong> to recommend 
                    the most suitable crops for optimal growth and yield. Get <strong>personalized recommendations</strong> based on 
                    scientific data and machine learning algorithms.
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
                    <div style="background: rgba(85, 139, 47, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #558B2F;">
                        🌱 NPK Analysis
                    </div>
                    <div style="background: rgba(85, 139, 47, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #558B2F;">
                        🌡️ Climate Matching
                    </div>
                    <div style="background: rgba(85, 139, 47, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #558B2F;">
                        💧 Water Requirements
                    </div>
                    <div style="background: rgba(85, 139, 47, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #558B2F;">
                        🧪 pH Compatibility
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h3 style="color: #558B2F; margin-bottom: 0.5rem;">📊 Soil and Climate Parameters</h3>
            <p style="color: #666; font-size: 0.95rem;">Enter accurate values for best recommendations</p>
        </div>
        """, unsafe_allow_html=True)

        # Create a visually appealing form with tooltips and ranges
        with st.form("crop_recommendation_form"):
            # NPK values with enhanced header
            st.markdown("""
            <div style="background: linear-gradient(90deg, #558B2F, #8BC34A); 
                        padding: 8px 15px; border-radius: 8px; margin: 15px 0 10px 0;">
                <h4 style="color: white; margin: 0; font-size: 1rem;">🧪 NPK Soil Nutrients</h4>
            </div>
            """, unsafe_allow_html=True)

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

            # Environmental factors with enhanced header
            st.markdown("""
            <div style="background: linear-gradient(90deg, #558B2F, #8BC34A); 
                        padding: 8px 15px; border-radius: 8px; margin: 15px 0 10px 0;">
                <h4 style="color: white; margin: 0; font-size: 1rem;">🌤️ Environmental Conditions</h4>
            </div>
            """, unsafe_allow_html=True)

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

            # Add an enhanced visual pH scale
            ph_scale = """
            <div style="margin-top: 15px; margin-bottom: 20px; padding: 15px; 
                        background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); 
                        border-radius: 10px; border-left: 4px solid #558B2F;">
                <p style="margin-bottom: 10px; font-size: 15px; font-weight: 600; color: #558B2F;">
                    📊 pH Scale Reference
                </p>
                <div style="display: flex; width: 100%; height: 24px; border-radius: 8px; overflow: hidden; 
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <div style="flex: 1; background: linear-gradient(to right, #FF4500, #FFA500);" title="Acidic (3-6)"></div>
                    <div style="flex: 0.5; background: #7CFC00;" title="Neutral (6-7.5)"></div>
                    <div style="flex: 1; background: linear-gradient(to right, #00BFFF, #0000FF);" title="Alkaline (7.5-10)"></div>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 8px; color: #666;">
                    <span><strong>Acidic</strong> (3.0)</span>
                    <span><strong>Neutral</strong> (7.0)</span>
                    <span><strong>Alkaline</strong> (10.0)</span>
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
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #F1F8E9 100%);
                    padding: 1.5rem; border-radius: 16px; margin-bottom: 1.5rem;
                    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08); border: 1px solid rgba(85, 139, 47, 0.1);">
            <h4 style="color: #558B2F; margin: 0 0 1rem 0; display: flex; align-items: center; gap: 0.5rem;">
                📖 NPK Guide
            </h4>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); 
                    padding: 18px; border-radius: 12px; margin-bottom: 15px;
                    border-left: 4px solid #558B2F;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h4 style="color: #558B2F; margin-top: 0; font-size: 1.1rem;">🅽 Nitrogen (N)</h4>
            <p style="margin: 8px 0; color: #333;">• Essential for leaf growth</p>
            <p style="margin: 8px 0; color: #333;">• Influences protein production</p>
            <p style="margin: 0; color: #333;">• Affects green color intensity</p>
        </div>

        <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                    padding: 18px; border-radius: 12px; margin-bottom: 15px;
                    border-left: 4px solid #FF9800;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h4 style="color: #E65100; margin-top: 0; font-size: 1.1rem;">🅿️ Phosphorus (P)</h4>
            <p style="margin: 8px 0; color: #333;">• Important for root development</p>
            <p style="margin: 8px 0; color: #333;">• Crucial for flower and seed formation</p>
            <p style="margin: 0; color: #333;">• Helps in energy transfer processes</p>
        </div>

        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 18px; border-radius: 12px;
                    border-left: 4px solid #1976D2;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h4 style="color: #1976D2; margin-top: 0; font-size: 1.1rem;">🅺 Potassium (K)</h4>
            <p style="margin: 8px 0; color: #333;">• Regulates water content</p>
            <p style="margin: 8px 0; color: #333;">• Improves disease resistance</p>
            <p style="margin: 0; color: #333;">• Enhances fruit quality</p>
        </div>
        """, unsafe_allow_html=True)

    # Process prediction
    if 'submitted' in locals() and submitted:
        with st.spinner('Analyzing soil and environmental conditions...'):
            time.sleep(1)  # Simulate processing time

        try:
            # Use relative path to load model
            model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                      "models", "crop_recommendation_model.pkl")

            with open(model_path, "rb") as model_file:
                model = pickle.load(model_file)

            # Input for prediction
            input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

            # Make prediction
            prediction = model.predict(input_data)
            recommended_crop = prediction[0].capitalize()

            # Display result with animation
            st.balloons()

            # Add separator
            st.markdown(
                "<hr style='margin: 30px 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, #558B2F, transparent);'>",
                unsafe_allow_html=True)

            # Display recommended crop in an enhanced visually appealing card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #558B2F 0%, #8BC34A 100%); 
                        padding: 30px; border-radius: 12px; text-align: center; margin: 20px 0;
                        box-shadow: 0 8px 24px rgba(0,0,0,0.15);">
                <h2 style="color: white; margin: 0; font-size: 1.5rem;">✨ Recommended Crop</h2>
                <h1 style="color: white; margin: 15px 0; font-size: 48px; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">{recommended_crop}</h1>
                <p style="color: white; font-style: italic; font-size: 1.1rem; margin: 0;">Best suited for your soil and climate conditions</p>
            </div>
            """, unsafe_allow_html=True)

            # Create a function to display crop information based on prediction
            def display_crop_info(crop_name):
                # Dictionary of crop information
                crop_info = {
                    'Rice': {
                        'image_url': 'https://cdn.britannica.com/89/140889-050-EC3F00BF/Ripening-heads-rice-Oryza-sativa.jpg',
                        'description': 'Rice thrives in wet environments and requires flooded fields for optimal growth. It\'s a staple crop in many cultures.',
                        'growing_season': 'Typically 3-6 months, depending on variety',
                        'soil_preference': 'Clay soils that retain water well',
                        'water_needs': 'Very high - requires flooded conditions',
                        'special_notes': 'Needs consistent water levels and warm temperatures'
                    },
                    'Wheat': {
                        'image_url': 'https://www.worldatlas.com/r/w1200/upload/d8/f0/68/shutterstock-116527159.jpg',
                        'description': 'Wheat is adaptable to various conditions and is one of the world\'s most important food crops.',
                        'growing_season': 'Winter wheat: planted in fall, harvested in summer; Spring wheat: planted in spring, harvested in fall',
                        'soil_preference': 'Well-draining loamy soil',
                        'water_needs': 'Moderate - about 450-650mm during growing season',
                        'special_notes': 'Drought-tolerant once established'
                    },
                    'Maize': {
                        'image_url': 'https://cdn.pixabay.com/photo/2014/02/23/13/11/maize-272894_1280.jpg',
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
                    'image_url': 'https://cdn.pixabay.com/photo/2014/02/23/13/11/maize-272894_1280.jpg',
                    'description': f'{crop_name} is well-suited for your soil conditions and local climate according to our AI model.',
                    'growing_season': 'Varies by region and variety',
                    'soil_preference': 'As indicated by your soil analysis',
                    'water_needs': 'Follow local agricultural extension guidance',
                    'special_notes': 'Consult with local agricultural experts for specific cultivation advice'
                }

                # Get info for this crop (or use default)
                info = crop_info.get(crop_name, default_info)

                # Create an enhanced expander with crop details
                st.markdown("""
                <h3 style="color: #558B2F; margin: 30px 0 15px 0;">📋 Crop Details</h3>
                """, unsafe_allow_html=True)

                with st.expander("View Complete Crop Information", expanded=True):
                    col1, col2 = st.columns([1, 1])

                    with col1:
                        st.image(info['image_url'], caption=f"{crop_name}", use_column_width=True)

                    with col2:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); 
                                    padding: 15px; border-radius: 10px; margin-bottom: 10px;
                                    border-left: 4px solid #558B2F;">
                            <p style="margin: 5px 0; color: #333;"><strong style="color: #558B2F;">Description:</strong> {info['description']}</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                                    padding: 12px; border-radius: 8px; margin-bottom: 8px;
                                    border-left: 3px solid #1976D2;">
                            <p style="margin: 0; color: #333;"><strong style="color: #1976D2;">🌱 Growing Season:</strong> {info['growing_season']}</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                                    padding: 12px; border-radius: 8px; margin-bottom: 8px;
                                    border-left: 3px solid #FF9800;">
                            <p style="margin: 0; color: #333;"><strong style="color: #E65100;">🌍 Soil Preference:</strong> {info['soil_preference']}</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #E1F5FE 0%, #B3E5FC 100%); 
                                    padding: 12px; border-radius: 8px; margin-bottom: 8px;
                                    border-left: 3px solid #0288D1;">
                            <p style="margin: 0; color: #333;"><strong style="color: #0288D1;">💧 Water Needs:</strong> {info['water_needs']}</p>
                        </div>
                        <div style="background: linear-gradient(135deg, #FCE4EC 0%, #F8BBD0 100%); 
                                    padding: 12px; border-radius: 8px;
                                    border-left: 3px solid #C2185B;">
                            <p style="margin: 0; color: #333;"><strong style="color: #C2185B;">📌 Special Notes:</strong> {info['special_notes']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Display enhanced next steps and recommendations
                st.markdown("""
                <h3 style="color: #558B2F; margin: 30px 0 15px 0;">📝 Next Steps & Recommendations</h3>
                """, unsafe_allow_html=True)

                st.markdown("""
                <div style="background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); 
                            padding: 20px; border-radius: 12px; margin: 15px 0;
                            border-left: 4px solid #558B2F;
                            box-shadow: 0 2px 12px rgba(0,0,0,0.08);">
                    <h4 style="color: #558B2F; margin-top: 0;">🎯 Action Plan</h4>
                    <div style="margin: 15px 0;">
                        <p style="margin: 10px 0; color: #333;">✓ Check best planting times for your specific region</p>
                        <p style="margin: 10px 0; color: #333;">✓ Consider crop rotation benefits for soil health</p>
                        <p style="margin: 10px 0; color: #333;">✓ Use our Yield Prediction tool to forecast harvest potential</p>
                        <p style="margin: 10px 0; color: #333;">✓ Set up Climate Risk Alerts to protect your crops</p>
                        <p style="margin: 10px 0; color: #333;">✓ Consult with local agricultural extension services</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Display crop information
            display_crop_info(recommended_crop)

        except FileNotFoundError:
            st.error(
                "❌ Model file not found. Please ensure 'crop_recommendation_model.pkl' is inside the 'models/' folder.")
        except Exception as e:
            st.error(f"⚠️ Error while predicting: {e}")

    # Always show enhanced guidance information at the bottom
    st.markdown(
        "<hr style='margin: 40px 0 20px 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, #558B2F, transparent);'>",
        unsafe_allow_html=True)

    with st.expander("ℹ️ About Crop Recommendation AI", expanded=False):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); 
                    padding: 20px; border-radius: 12px;
                    border-left: 4px solid #558B2F;">
            <p style="color: #333; line-height: 1.8;">
                Our crop recommendation system uses a <strong>sophisticated machine learning model</strong> trained on thousands of agricultural data points. 
                The model considers the following factors:
            </p>

            <div style="margin: 20px 0;">
                <div style="background: rgba(85, 139, 47, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0;">
                    <p style="margin: 0; color: #333;"><strong style="color: #558B2F;">🧪 Soil Nutrients (NPK):</strong> Different crops require different nutrient profiles for optimal growth.</p>
                </div>
                <div style="background: rgba(85, 139, 47, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0;">
                    <p style="margin: 0; color: #333;"><strong style="color: #558B2F;">📊 pH Level:</strong> Every crop has an optimal soil pH range for maximum nutrient absorption.</p>
                </div>
                <div style="background: rgba(85, 139, 47, 0.1); padding: 12px; border-radius: 8px; margin: 10px 0;">
                    <p style="margin: 0; color: #333;"><strong style="color: #558B2F;">🌤️ Climate Conditions:</strong> Temperature, humidity, and rainfall patterns significantly affect crop growth and yield.</p>
                </div>
            </div>

            <p style="color: #333; margin-top: 15px;">
                The AI analyzes these parameters <strong>collectively</strong> to determine which crop would be most successful in your specific conditions.
            </p>

            <div style="background: rgba(255, 152, 0, 0.1); padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 3px solid #FF9800;">
                <h4 style="color: #E65100; margin-top: 0;">💡 For Best Results:</h4>
                <p style="margin: 8px 0; color: #333;">1. Use accurate soil test results rather than estimates</p>
                <p style="margin: 8px 0; color: #333;">2. Enter climate data based on annual averages for your region</p>
                <p style="margin: 8px 0; color: #333;">3. Consider seasonal variations in your planning</p>
                <p style="margin: 8px 0 0 0; color: #333;">4. Consult with local agricultural extension services for region-specific advice</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
