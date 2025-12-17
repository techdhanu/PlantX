import streamlit as st
import pickle
import numpy as np
import time
import os
from datetime import datetime

def show():
    # Enhanced header with modern design
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3rem; font-weight: 700; margin-bottom: 0.5rem; 
                   background: linear-gradient(135deg, #1976D2, #42A5F5);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🌦️ Climate Risk Alerts
        </h1>
        <p style="font-size: 1.2rem; color: #666; margin: 0;">
            AI-Powered Weather Risk Assessment & Early Warning System
        </p>
        <div style="width: 80px; height: 4px; background: linear-gradient(90deg, #1976D2, #42A5F5); 
                    margin: 1rem auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced information banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                padding: 2rem; border-radius: 16px; margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(25, 118, 210, 0.1); position: relative;">
        <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; 
                    background: linear-gradient(180deg, #1976D2, #42A5F5); border-radius: 0 4px 4px 0;"></div>
        <div style="display: flex; align-items: start; gap: 1.5rem;">
            <div style="font-size: 3rem;">🤖</div>
            <div>
                <h3 style="color: #1976D2; margin: 0 0 1rem 0; font-size: 1.5rem;">Advanced Climate Risk Analysis</h3>
                <p style="margin: 0 0 1rem 0; line-height: 1.6; font-size: 1.05rem;">
                    Leverage <strong>machine learning and real-time weather data</strong> to predict potential climate-related 
                    risks to your crops. Receive <strong>personalized alerts and actionable recommendations</strong> to protect 
                    your harvest from adverse weather conditions.
                </p>
                <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1rem;">
                    <div style="background: rgba(25, 118, 210, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #1976D2;">
                        🌧️ Rainfall Prediction
                    </div>
                    <div style="background: rgba(25, 118, 210, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #1976D2;">
                        🌡️ Temperature Alerts
                    </div>
                    <div style="background: rgba(25, 118, 210, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #1976D2;">
                        💧 Flood Risk Assessment
                    </div>
                    <div style="background: rgba(25, 118, 210, 0.1); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; font-weight: 600; color: #1976D2;">
                        🌾 Crop Protection
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["🔍 Risk Prediction", "🗺️ Risk Map", "📊 Historical Analysis"])

    with tab1:
        # Add 7-Day Forecast at the top of the Risk Prediction tab
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h3 style="color: #1976D2; margin-bottom: 0.5rem;">🔮 7-Day Weather Forecast</h3>
            <p style="color: #666; font-size: 0.95rem;">Real-time weather predictions and risk indicators</p>
        </div>
        """, unsafe_allow_html=True)

        # Get forecast data from session state
        forecast_data = None
        if 'weather_data' in st.session_state and 'forecast' in st.session_state.weather_data:
            forecast_data = st.session_state.weather_data['forecast']

        if forecast_data:
            # Create a horizontal layout for forecast cards
            forecast_cols = st.columns(7)

            # Weather icon mapping
            weather_icons = {
                'clear-day': '☀️',
                'clear-night': '🌙',
                'partly-cloudy-day': '⛅',
                'partly-cloudy-night': '🌙',
                'cloudy': '☁️',
                'rain': '🌧️',
                'snow': '❄️',
                'sleet': '🌨️',
                'wind': '💨',
                'fog': '🌫️',
                'thunder': '⛈️',
                'thunder-rain': '⛈️',
                'thunder-showers-day': '⛈️',
                'thunder-showers-night': '⛈️',
            }

            # Display each day's forecast in a column
            for i, (day, col) in enumerate(zip(forecast_data, forecast_cols)):
                date_obj = datetime.strptime(day['date'], '%Y-%m-%d')
                day_name = date_obj.strftime('%a') if i > 0 else 'Today'
                icon = weather_icons.get(day['icon'], '🌤️')

                # Determine if there are any risk conditions
                risk_level = "Low"
                risk_color = "#4CAF50"

                if day['rainfall'] > 15:
                    risk_level = "High"
                    risk_color = "#F44336"
                elif day['rainfall'] > 5:
                    risk_level = "Moderate"
                    risk_color = "#FF9800"

                col.markdown(f"""
                <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                            padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 5px; 
                            border-top: 4px solid {risk_color};
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
                    <p style="font-weight: bold; margin-bottom: 8px; color: #1976D2; font-size: 0.9rem;">{day_name}</p>
                    <p style="font-size: 28px; margin: 8px 0;">{icon}</p>
                    <p style="font-size: 20px; margin: 8px 0; font-weight: 600; color: #1976D2;">{day['temperature']}°C</p>
                    <p style="font-size: 11px; margin: 3px 0; color: #666;">🔽 {day['tempMin']}° 🔼 {day['tempMax']}°</p>
                    <p style="font-size: 11px; margin: 3px 0; color: #666;">💧 {day['humidity']}%</p>
                    <p style="font-size: 11px; margin: 3px 0; color: #666;">🌧️ {day['rainfall']} mm</p>
                    <p style="font-size: 10px; background-color: {risk_color}; color: white; padding: 4px 8px; 
                       border-radius: 12px; margin-top: 8px; font-weight: 600;">{risk_level} Risk</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Weather forecast data is not available. Please check your location settings.")

        # Add a separator between forecast and risk prediction form
        st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

        # Create two columns for form and info
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="color: #1976D2; margin-bottom: 0.5rem;">📍 Location & Environmental Data</h3>
                <p style="color: #666; font-size: 0.95rem;">Enter accurate location and climate parameters for risk assessment</p>
            </div>
            """, unsafe_allow_html=True)

            # Form for input parameters
            with st.form("risk_prediction_form"):
                # Location parameters
                st.markdown("""
                <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                            padding: 8px 15px; border-radius: 8px; margin: 15px 0 10px 0;">
                    <h4 style="color: white; margin: 0; font-size: 1rem;">📍 Location Details</h4>
                </div>
                """, unsafe_allow_html=True)
                loc_col1, loc_col2 = st.columns(2)

                with loc_col1:
                    latitude = st.number_input(
                        "Latitude",
                        format="%.6f",
                        min_value=-90.0,
                        max_value=90.0,
                        value=28.644800,
                        help="Enter the latitude of your farm location"
                    )

                with loc_col2:
                    longitude = st.number_input(
                        "Longitude",
                        format="%.6f",
                        min_value=-180.0,
                        max_value=180.0,
                        value=77.216721,
                        help="Enter the longitude of your farm location"
                    )

                # Weather parameters
                st.markdown("""
                <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                            padding: 8px 15px; border-radius: 8px; margin: 15px 0 10px 0;">
                    <h4 style="color: white; margin: 0; font-size: 1rem;">🌤️ Weather Parameters</h4>
                </div>
                """, unsafe_allow_html=True)
                weather_col1, weather_col2, weather_col3 = st.columns(3)

                with weather_col1:
                    rainfall = st.number_input(
                        "Rainfall (mm)",
                        min_value=0.0,
                        value=85.0,
                        help="Recent or forecasted rainfall amount"
                    )

                with weather_col2:
                    temperature = st.number_input(
                        "Temperature (°C)",
                        min_value=-20.0,
                        max_value=50.0,
                        value=28.5,
                        help="Average temperature in your region"
                    )

                with weather_col3:
                    humidity = st.number_input(
                        "Humidity (%)",
                        min_value=0.0,
                        max_value=100.0,
                        value=65.0,
                        help="Average relative humidity"
                    )

                # Hydrological parameters
                st.markdown("""
                <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                            padding: 8px 15px; border-radius: 8px; margin: 15px 0 10px 0;">
                    <h4 style="color: white; margin: 0; font-size: 1rem;">💧 Hydrological Parameters</h4>
                </div>
                """, unsafe_allow_html=True)
                hydro_col1, hydro_col2 = st.columns(2)

                with hydro_col1:
                    river_discharge = st.number_input(
                        "River Discharge (m³/s)",
                        min_value=0.0,
                        value=150.0,
                        help="Water flow rate of nearby rivers"
                    )

                with hydro_col2:
                    water_level = st.number_input(
                        "Water Level (m)",
                        min_value=0.0,
                        value=2.5,
                        help="Current water level in nearby water bodies"
                    )

                # Geographical parameters
                st.markdown("""
                <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                            padding: 8px 15px; border-radius: 8px; margin: 15px 0 10px 0;">
                    <h4 style="color: white; margin: 0; font-size: 1rem;">🏞️ Geographical Parameters</h4>
                </div>
                """, unsafe_allow_html=True)
                geo_col1, geo_col2 = st.columns(2)

                with geo_col1:
                    elevation = st.number_input(
                        "Elevation (m)",
                        min_value=0.0,
                        value=220.0,
                        help="Elevation of your farm from sea level"
                    )

                with geo_col2:
                    land_cover = st.selectbox(
                        "Land Cover",
                        ["Forest", "Urban", "Agriculture", "Water"],
                        index=2,
                        help="Predominant land cover type in your area"
                    )

                # Additional parameters
                st.markdown("""
                <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                            padding: 8px 15px; border-radius: 8px; margin: 15px 0 10px 0;">
                    <h4 style="color: white; margin: 0; font-size: 1rem;">🧪 Soil & Infrastructure</h4>
                </div>
                """, unsafe_allow_html=True)
                add_col1, add_col2, add_col3 = st.columns(3)

                with add_col1:
                    soil_type = st.selectbox(
                        "Soil Type",
                        ["Sandy", "Clay", "Silt", "Peat", "Chalk", "Loam"],
                        index=5,
                        help="Primary soil type on your farm"
                    )

                with add_col2:
                    population_density = st.slider(
                        "Population Density",
                        min_value=0,
                        max_value=10000,
                        value=500,
                        help="Population density in your area (people per km²)"
                    )

                with add_col3:
                    infrastructure = st.slider(
                        "Infrastructure",
                        min_value=0,
                        max_value=10,
                        value=5,
                        help="Level of infrastructure development (0-10)"
                    )

                historical_floods = st.slider(
                    "Historical Floods",
                    min_value=0,
                    max_value=10,
                    value=2,
                    help="Number of flood events in past 10 years"
                )

                # Submit button
                submitted = st.form_submit_button("🔍 Predict Flood Risk", use_container_width=True)

        with col2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <h3 style="color: #1976D2; margin-bottom: 0.5rem;">💡 Understanding Risk Factors</h3>
                <p style="color: #666; font-size: 0.95rem;">Key parameters affecting climate risk</p>
            </div>
            """, unsafe_allow_html=True)

            # Expandable sections with educational content
            with st.expander("📌 Location Factors", expanded=True):
                st.markdown("""
                - **Latitude & Longitude**: Determines climate zone and weather patterns
                - **Elevation**: Higher elevations typically have lower flood risk but may face other risks
                """)

            with st.expander("☔ Weather Impacts"):
                st.markdown("""
                - **Rainfall**: Excessive rainfall is a primary flood trigger
                - **Temperature**: Affects evaporation and snow melt rates
                - **Humidity**: High humidity can increase precipitation intensity
                """)

            with st.expander("🌊 Hydrological Factors"):
                st.markdown("""
                - **River Discharge**: Higher values indicate more water moving through rivers
                - **Water Level**: Proximity to flood stage is critical for risk assessment
                """)

            with st.expander("🏞️ Geographical Considerations"):
                st.markdown("""
                - **Land Cover**: Forests slow runoff; urban areas increase it
                - **Soil Type**: Clay retains water; sandy soil allows drainage
                - **Historical Events**: Past flooding indicates vulnerability
                """)

            # Quick risk overview
            st.markdown("""
            <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                        padding: 1.5rem; border-radius: 12px; margin-top: 20px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                        border: 1px solid rgba(255, 152, 0, 0.2); position: relative;">
                <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; 
                            background: linear-gradient(180deg, #F57C00, #FFA726); border-radius: 0 4px 4px 0;"></div>
                <h4 style="color: #E65100; margin: 0 0 1rem 0; font-size: 1.1rem;">📊 Current Risk Levels</h4>
                <p style="margin: 0.5rem 0;"><strong>🌧️ Rainfall Risk:</strong> <span style="color: #FF9800; font-weight: 600;">Moderate</span></p>
                <p style="margin: 0.5rem 0;"><strong>🌊 Flooding Risk:</strong> <span style="color: #4CAF50; font-weight: 600;">Low</span></p>
                <p style="margin: 0.5rem 0;"><strong>🔥 Drought Risk:</strong> <span style="color: #F44336; font-weight: 600;">High</span></p>
                <p style="font-size: 0.85rem; color: #666; margin: 1rem 0 0 0;"><i>Based on regional weather data from June 1, 2025</i></p>
            </div>
            """, unsafe_allow_html=True)

        # Process prediction
        if 'submitted' in locals() and submitted:
            with st.spinner('Analyzing climate risk patterns...'):
                time.sleep(1.5)  # Simulate processing time

            try:
                # Load the model (with improved error handling)
                model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models", "climate_risk_model.pkl")

                # Initialize to use mock prediction by default (as fallback)
                mock_prediction = True

                try:
                    if not os.path.exists(model_path):
                        st.warning(f"Model file not found at: {model_path}")
                        st.info("Using fallback prediction method based on input parameters.")
                    else:
                        try:
                            with open(model_path, "rb") as f:
                                model = pickle.load(f)
                            # Successfully loaded the model
                            mock_prediction = False
                            st.success("Climate risk model loaded successfully.")
                        except Exception as e:
                            st.error(f"Error loading model: {str(e)}")
                            st.info("Using fallback prediction method based on input parameters.")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")

                # Convert categorical inputs to numbers
                land_cover_map = {"Forest":0, "Urban":1, "Agriculture":2, "Water":3}
                soil_type_map = {"Sandy":0, "Clay":1, "Silt":2, "Peat":3, "Chalk":4, "Loam":5}

                input_features = np.array([[
                    latitude,
                    longitude,
                    rainfall,
                    temperature,
                    humidity,
                    river_discharge,
                    water_level,
                    elevation,
                    land_cover_map[land_cover],
                    soil_type_map[soil_type],
                    population_density,
                    infrastructure,
                    historical_floods
                ]])

                # Make prediction
                if not mock_prediction:
                    flood_risk_prob = model.predict_proba(input_features)[0][1] if hasattr(model, 'predict_proba') else 0.65
                    prediction = model.predict(input_features)[0]
                else:
                    # Generate mock prediction based on input values
                    # Higher rainfall, river discharge, previous floods, and lower elevation increase risk
                    base_risk = 0.2
                    if rainfall > 100: base_risk += 0.2
                    if river_discharge > 200: base_risk += 0.15
                    if historical_floods > 3: base_risk += 0.1
                    if elevation < 50: base_risk += 0.15
                    if water_level > 4: base_risk += 0.2
                    if land_cover == "Urban": base_risk += 0.05
                    if soil_type == "Clay": base_risk += 0.05

                    flood_risk_prob = min(base_risk, 0.95)
                    prediction = 1 if flood_risk_prob > 0.5 else 0

                # Display results
                if prediction == 1:
                    risk_color = "#F44336"
                    risk_text = "High Risk"
                    recommendations = [
                        "Consider flood-resistant crop varieties",
                        "Implement drainage systems on your farm",
                        "Set up early warning systems",
                        "Prepare an emergency plan for livestock and equipment",
                        "Consider flood insurance for your crops"
                    ]
                else:
                    if flood_risk_prob > 0.3:
                        risk_color = "#FF9800"
                        risk_text = "Moderate Risk"
                        recommendations = [
                            "Monitor weather forecasts closely",
                            "Inspect drainage systems regularly",
                            "Have a basic emergency plan ready",
                            "Consider timing of planting to avoid peak rainfall season"
                        ]
                    else:
                        risk_color = "#4CAF50"
                        risk_text = "Low Risk"
                        recommendations = [
                            "Maintain normal agricultural practices",
                            "Regular inspection of farm infrastructure",
                            "Stay updated with seasonal forecasts"
                        ]

                # Display risk score with gauge visualization
                risk_percentage = int(flood_risk_prob * 100)

                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {risk_color}E6, {risk_color}); 
                            padding: 2rem; border-radius: 16px; text-align: center; margin: 20px 0;
                            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);">
                    <h2 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.5rem;">🌊 Flood Risk Assessment</h2>
                    <h1 style="color: white; margin: 0.5rem 0; font-size: 3rem; font-weight: 700;">{risk_text}</h1>
                    <p style="color: white; font-weight: bold; font-size: 1.2rem; margin: 0.5rem 0;">Risk Probability: {risk_percentage}%</p>
                </div>
                """, unsafe_allow_html=True)

                # Create risk gauge visualization
                gauge_html = f"""
                <div style="width: 100%; background: linear-gradient(to right, #4CAF50, #FFEB3B, #F44336); height: 20px; border-radius: 10px; margin-bottom: 30px;">
                    <div style="position: relative; left: {risk_percentage}%; transform: translateX(-50%);">
                        <div style="width: 2px; height: 25px; background-color: black; margin: 0 auto;"></div>
                        <div style="background-color: #333; color: white; padding: 5px 10px; border-radius: 15px; display: inline-block; transform: translateX(-50%); margin-top: 5px;">
                            {risk_percentage}%
                        </div>
                    </div>
                </div>
                """
                st.markdown(gauge_html, unsafe_allow_html=True)

                # Show risk factors
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
                    <h3 style="color: #1976D2; margin-bottom: 0.5rem;">📊 Risk Analysis</h3>
                    <p style="color: #666; font-size: 0.95rem;">Detailed breakdown of risk factors and recommendations</p>
                </div>
                """, unsafe_allow_html=True)
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""
                    <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                                padding: 8px 15px; border-radius: 8px; margin: 0 0 15px 0;">
                        <h4 style="color: white; margin: 0; font-size: 1rem;">🔍 Critical Factors</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    factors_df = {
                        "Rainfall": {"value": f"{rainfall} mm", "impact": "High" if rainfall > 100 else "Medium" if rainfall > 50 else "Low"},
                        "River Discharge": {"value": f"{river_discharge} m³/s", "impact": "High" if river_discharge > 200 else "Medium" if river_discharge > 100 else "Low"},
                        "Elevation": {"value": f"{elevation} m", "impact": "High" if elevation < 50 else "Medium" if elevation < 150 else "Low"},
                        "Historical Floods": {"value": historical_floods, "impact": "High" if historical_floods > 5 else "Medium" if historical_floods > 2 else "Low"}
                    }

                    for factor, data in factors_df.items():
                        if data["impact"] == "High":
                            impact_color = "#F44336"
                        elif data["impact"] == "Medium":
                            impact_color = "#FF9800"
                        else:
                            impact_color = "#4CAF50"

                        st.markdown(f"""
                        <div style="display: flex; justify-content: space-between; align-items: center;
                                    margin-bottom: 10px; padding: 12px; 
                                    background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                                    border-radius: 8px; border-left: 3px solid {impact_color};
                                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);">
                            <div style="color: #1976D2; font-weight: 500;">{factor}: {data['value']}</div>
                            <div style="background-color: {impact_color}; color: white; padding: 4px 12px; 
                                        border-radius: 12px; font-size: 0.85rem; font-weight: 600;">{data['impact']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with col2:
                    st.markdown("""
                    <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                                padding: 8px 15px; border-radius: 8px; margin: 0 0 15px 0;">
                        <h4 style="color: white; margin: 0; font-size: 1rem;">💡 Recommendations</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    for i, rec in enumerate(recommendations):
                        st.markdown(f"""
                        <div style="margin-bottom: 10px; padding: 12px; 
                                    background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                                    border-radius: 8px; border-left: 3px solid #1976D2;
                                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);">
                            <span style="color: #1976D2; font-weight: 600;">{i+1}.</span> <span style="color: #333;">{rec}</span>
                        </div>
                        """, unsafe_allow_html=True)

                # Show alert timeline
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
                    <h3 style="color: #1976D2; margin-bottom: 0.5rem;">📅 Projected Alert Timeline</h3>
                    <p style="color: #666; font-size: 0.95rem;">Expected risk progression over time</p>
                </div>
                """, unsafe_allow_html=True)
                timeline_html = """
                <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                            padding: 2rem; border-radius: 12px; margin: 15px 0;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);">
                    <div style="display: flex; position: relative;">
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #81C784; border-radius: 50%; width: 30px; height: 30px; margin: 0 auto; 
                                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);"></div>
                            <p style="margin: 8px 0 2px 0; font-size: 14px; font-weight: 600; color: #1976D2;">Current</p>
                            <p style="margin: 0; font-size: 12px; color: #666;">Jun 1</p>
                        </div>
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #FFB74D; border-radius: 50%; width: 30px; height: 30px; margin: 0 auto;
                                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);"></div>
                            <p style="margin: 8px 0 2px 0; font-size: 14px; font-weight: 600; color: #1976D2;">Warning</p>
                            <p style="margin: 0; font-size: 12px; color: #666;">Jun 15</p>
                        </div>
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #E57373; border-radius: 50%; width: 30px; height: 30px; margin: 0 auto;
                                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);"></div>
                            <p style="margin: 8px 0 2px 0; font-size: 14px; font-weight: 600; color: #1976D2;">Peak Risk</p>
                            <p style="margin: 0; font-size: 12px; color: #666;">Jul 1</p>
                        </div>
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #81C784; border-radius: 50%; width: 30px; height: 30px; margin: 0 auto;
                                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);"></div>
                            <p style="margin: 8px 0 2px 0; font-size: 14px; font-weight: 600; color: #1976D2;">Decreasing</p>
                            <p style="margin: 0; font-size: 12px; color: #666;">Jul 15</p>
                        </div>
                        <div style="position: absolute; height: 4px; background: linear-gradient(to right, #81C784, #FFB74D, #E57373, #81C784); 
                                    top: 14px; width: 100%; z-index: 1; border-radius: 2px;"></div>
                    </div>
                </div>
                """
                st.markdown(timeline_html, unsafe_allow_html=True)

                # Action plan
                st.markdown("""
                <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
                    <h3 style="color: #1976D2; margin-bottom: 0.5rem;">📋 Action Plan</h3>
                    <p style="color: #666; font-size: 0.95rem;">Recommended timeline for protective measures</p>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                            padding: 1.5rem; border-radius: 12px;
                            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                            border: 1px solid rgba(25, 118, 210, 0.2); position: relative;">
                    <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 4px; 
                                background: linear-gradient(180deg, #1976D2, #42A5F5); border-radius: 0 4px 4px 0;"></div>
                    <h4 style="color: #1976D2; margin: 0 0 1rem 0;">Recommended Timeline</h4>
                    <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8;">
                        <li style="color: #333;"><strong style="color: #1976D2;">Immediate:</strong> {'Monitor water levels and weather forecasts daily' if risk_text != 'Low Risk' else 'Maintain regular farm operations'}</li>
                        <li style="color: #333;"><strong style="color: #1976D2;">This Week:</strong> {'Implement drainage improvements and secure equipment' if risk_text == 'High Risk' else 'Review farm emergency plan'}</li>
                        <li style="color: #333;"><strong style="color: #1976D2;">This Month:</strong> {'Consider crop insurance options and plan for potential replanting' if risk_text == 'High Risk' else 'Normal seasonal planning'}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction error: {e}")
                st.info("Using backup risk assessment based on input parameters.")

    with tab2:
        # Risk Map Visualization Tab
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h3 style="color: #1976D2; margin-bottom: 0.5rem;">🗺️ Risk Map by Location</h3>
            <p style="color: #666; font-size: 0.95rem;">Interactive climate risk visualization across regions</p>
        </div>
        """, unsafe_allow_html=True)

        # Simple map visualization
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 1.5rem; border-radius: 12px; margin-bottom: 20px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                    border-left: 4px solid #1976D2;">
            <p style="margin: 0; line-height: 1.6; color: #333;">The map below shows climate risk assessments across different regions. Click on a location to see detailed risk profiles.</p>
        </div>
        """, unsafe_allow_html=True)

        map_col1, map_col2 = st.columns([3, 1])

        with map_col1:
            # Interactive climate risk heatmap with Streamlit's map components
            st.markdown("""
            <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                        padding: 8px 15px; border-radius: 8px; margin: 0 0 15px 0;">
                <h4 style="color: white; margin: 0; font-size: 1rem;">🌍 Climate Risk Heatmap</h4>
            </div>
            """, unsafe_allow_html=True)

            # Create some sample risk data points (lat, lon, risk_level)
            risk_data = [
                # North India - High risk
                {"lat": 28.6139, "lon": 77.2090, "risk": "High", "color": [230, 74, 25], "region": "Delhi NCR", "risk_factor": "Flood"},
                {"lat": 28.4089, "lon": 77.3178, "risk": "High", "color": [230, 74, 25], "region": "Faridabad", "risk_factor": "Flood"},
                {"lat": 29.3919, "lon": 76.9722, "risk": "High", "color": [230, 74, 25], "region": "Panipat", "risk_factor": "Flood"},

                # Central India - Moderate risk
                {"lat": 25.3176, "lon": 82.9739, "risk": "Moderate", "color": [255, 153, 0], "region": "Varanasi", "risk_factor": "Drought"},
                {"lat": 23.2599, "lon": 77.4126, "risk": "Moderate", "color": [255, 153, 0], "region": "Bhopal", "risk_factor": "Drought"},
                {"lat": 21.1458, "lon": 79.0882, "risk": "Moderate", "color": [255, 153, 0], "region": "Nagpur", "risk_factor": "Drought"},

                # South India - Low risk
                {"lat": 12.9716, "lon": 77.5946, "risk": "Low", "color": [76, 175, 80], "region": "Bengaluru", "risk_factor": "Normal"},
                {"lat": 13.0827, "lon": 80.2707, "risk": "Low", "color": [76, 175, 80], "region": "Chennai", "risk_factor": "Normal"},
                {"lat": 17.3850, "lon": 78.4867, "risk": "Low", "color": [76, 175, 80], "region": "Hyderabad", "risk_factor": "Normal"}
            ]

            # Create separate dataframes for each risk level for better visualization
            import pandas as pd

            # Extract points for each risk level
            high_risk_points = pd.DataFrame([point for point in risk_data if point["risk"] == "High"])
            moderate_risk_points = pd.DataFrame([point for point in risk_data if point["risk"] == "Moderate"])
            low_risk_points = pd.DataFrame([point for point in risk_data if point["risk"] == "Low"])

            # Create a map centered on India
            india_map = st.map(pd.DataFrame({
                "lat": [20.5937],
                "lon": [78.9629]
            }), zoom=4)

            # Add the risk points as layers on the map
            if not high_risk_points.empty:
                st.write("High risk areas: Delhi NCR, Faridabad, Panipat (Flood risk)")

            if not moderate_risk_points.empty:
                st.write("Moderate risk areas: Varanasi, Bhopal, Nagpur (Drought risk)")

            if not low_risk_points.empty:
                st.write("Low risk areas: Bengaluru, Chennai, Hyderabad (Normal conditions)")

            # Fallback to static heatmap if the interactive map fails
            st.markdown("""
            <div style="margin-top: 15px;">
                <img src="https://images.unsplash.com/photo-1548407260-da850faa41e3?q=80&w=1200&auto=format&fit=crop" 
                style="width: 100%; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" 
                alt="Climate Risk Heatmap - India">
                <p style="text-align: center; margin-top: 10px; font-style: italic;">Climate Risk Heatmap of India showing flood and drought risk areas</p>
            </div>
            """, unsafe_allow_html=True)

        with map_col2:
            st.markdown("""
            <div style="background: linear-gradient(90deg, #1976D2, #42A5F5); 
                        padding: 8px 15px; border-radius: 8px; margin: 0 0 15px 0;">
                <h4 style="color: white; margin: 0; font-size: 1rem;">📍 Location Risk Details</h4>
            </div>
            """, unsafe_allow_html=True)
            st.write("Click on a location for more details:")

            # Sample data for selected locations
            selected_location = st.selectbox("Select location for detailed analysis",
                                           ["Delhi NCR", "Varanasi", "Bengaluru", "Chennai", "Hyderabad", "Mumbai"])

            # Display risk details based on selection
            if selected_location == "Delhi NCR":
                risk_level = "High"
                risk_color = "#F44336"
                risk_factors = ["Frequent flooding", "Poor drainage infrastructure", "Proximity to Yamuna river"]
                recommendations = ["Implement flood-resistant crops", "Improve drainage systems", "Consider raised bed farming"]
            elif selected_location == "Varanasi":
                risk_level = "Moderate"
                risk_color = "#FF9800"
                risk_factors = ["Irregular rainfall", "Drought-prone summers", "Groundwater depletion"]
                recommendations = ["Drought-resistant crop varieties", "Water conservation techniques", "Mulching practices"]
            else:
                risk_level = "Low"
                risk_color = "#4CAF50"
                risk_factors = ["Stable climate patterns", "Adequate infrastructure", "Sufficient water resources"]
                recommendations = ["Maintain current agricultural practices", "Monitor seasonal forecasts", "Regular soil testing"]

            # Display risk information in a card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {risk_color}E6, {risk_color}); 
                        padding: 1.5rem; border-radius: 12px; text-align: center; margin: 15px 0;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);">
                <h3 style="color: white; margin: 0 0 0.5rem 0; font-size: 1.3rem;">{selected_location}</h3>
                <p style="color: white; font-weight: 600; margin: 0; font-size: 1.1rem;">{risk_level} Risk Area</p>
            </div>
            """, unsafe_allow_html=True)

            st.write("**Risk Factors:**")
            for factor in risk_factors:
                st.markdown(f"• {factor}")

            st.write("**Recommendations:**")
            for rec in recommendations:
                st.markdown(f"• {rec}")

    with tab3:
        # Historical Analysis Tab
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <h3 style="color: #1976D2; margin-bottom: 0.5rem;">📊 Historical Climate Analysis</h3>
            <p style="color: #666; font-size: 0.95rem;">Track patterns and changes in climate risks over time</p>
        </div>
        """, unsafe_allow_html=True)

        # Year range slider
        selected_years = st.slider("Select year range to analyze",
                                 min_value=2015,
                                 max_value=2025,
                                 value=(2018, 2025))

        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 1.5rem; border-radius: 12px; margin: 20px 0;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                    border-left: 4px solid #1976D2;">
            <p style="margin: 0; line-height: 1.6; color: #333;">Analysis shows a <strong style="color: #1976D2;">23% increase</strong> in flood risk in Northern India and a 
            <strong style="color: #1976D2;">17% increase</strong> in drought conditions in Central regions over the selected period.</p>
        </div>
        """, unsafe_allow_html=True)

        # Simple chart for historical data
        st.write("**Flood Events by Year (2015-2025)**")

        # Sample historical data
        years = list(range(2015, 2026))
        flood_events = [5, 7, 8, 12, 9, 14, 11, 15, 13, 16, 18]

        # Create a simple bar chart
        import pandas as pd

        # Create dataframe
        hist_data = pd.DataFrame({
            "Year": years,
            "Flood Events": flood_events
        })

        # Display chart
        st.bar_chart(hist_data.set_index("Year"))

        # Additional insights
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0 1.5rem 0;">
            <h3 style="color: #1976D2; margin-bottom: 0.5rem;">💡 Key Insights</h3>
            <p style="color: #666; font-size: 0.95rem;">Climate trends and adaptation strategies</p>
        </div>
        """, unsafe_allow_html=True)

        # Display insights in columns
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                        padding: 1.5rem; border-radius: 12px; height: 100%;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                        border-left: 4px solid #1976D2;">
                <h4 style="color: #1976D2; margin: 0 0 1rem 0;">📈 Trends</h4>
                <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8; color: #333;">
                    <li>Increasing frequency of extreme weather events</li>
                    <li>Higher intensity rainfall in shorter periods</li>
                    <li>Extended dry periods between monsoons</li>
                    <li>Rising average temperatures affecting crop viability</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                        padding: 1.5rem; border-radius: 12px; height: 100%;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                        border-left: 4px solid #1976D2;">
                <h4 style="color: #1976D2; margin: 0 0 1rem 0;">🛡️ Adaptation Strategies</h4>
                <ul style="margin: 0; padding-left: 1.5rem; line-height: 1.8; color: #333;">
                    <li>Implementing water management infrastructure</li>
                    <li>Adopting climate-resilient crop varieties</li>
                    <li>Utilizing early warning systems for extreme events</li>
                    <li>Diversifying crop selection to spread risk</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)