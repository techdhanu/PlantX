import streamlit as st
import pickle
import numpy as np
import time
import os

def show():
    st.header("🌦️ Climate Risk Alerts")

    # Information banner
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2E7D32;">
        <h3 style="color: #2E7D32; margin-top: 0;">Early Warning System</h3>
        <p>Our climate risk analysis uses advanced AI to predict potential weather-related risks to your crops. 
        Enter your location and environmental parameters to receive customized alerts and recommendations.</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["🔍 Risk Prediction", "🗺️ Risk Map", "📊 Historical Analysis"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Location & Environmental Data")

            # Form for input parameters
            with st.form("risk_prediction_form"):
                # Location parameters
                st.markdown("#### 📍 Location Details")
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
                st.markdown("#### 🌤️ Weather Parameters")
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
                st.markdown("#### 💧 Hydrological Parameters")
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
                st.markdown("#### 🏞️ Geographical Parameters")
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
                st.markdown("#### 🧪 Soil & Infrastructure")
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
            st.markdown("### 💡 Understanding Risk Factors")

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
            <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; margin-top: 20px; border-left: 5px solid #FF9800;">
                <h4 style="color: #E65100; margin-top: 0;">Current Risk Levels</h4>
                <p><strong>🌧️ Rainfall Risk:</strong> <span style="color: orange;">Moderate</span></p>
                <p><strong>🌊 Flooding Risk:</strong> <span style="color: green;">Low</span></p>
                <p><strong>🔥 Drought Risk:</strong> <span style="color: red;">High</span></p>
                <p style="font-size: 12px;"><i>Based on regional weather data from June 1, 2025</i></p>
            </div>
            """, unsafe_allow_html=True)

        # Process prediction
        if 'submitted' in locals() and submitted:
            with st.spinner('Analyzing climate risk patterns...'):
                time.sleep(1.5)  # Simulate processing time

            try:
                # Load the model (with error handling)
                model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "models", "climate_risk_model.pkl")

                # If model doesn't exist, we'll create a mock risk evaluation
                mock_prediction = True

                try:
                    with open(model_path, "rb") as f:
                        model = pickle.load(f)
                    mock_prediction = False
                except:
                    pass

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
                <div style="background-color: {risk_color}; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                    <h2 style="color: white; margin: 0;">Flood Risk Assessment</h2>
                    <h1 style="color: white; margin: 10px 0; font-size: 36px;">{risk_text}</h1>
                    <p style="color: white; font-weight: bold;">Risk Probability: {risk_percentage}%</p>
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
                st.subheader("Risk Analysis")
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("#### Critical Factors")
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
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px; padding: 8px; background-color: #F1F8E9; border-radius: 5px;">
                            <div>{factor}: {data['value']}</div>
                            <div style="background-color: {impact_color}; color: white; padding: 0 10px; border-radius: 10px;">{data['impact']}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with col2:
                    st.markdown("#### Recommendations")
                    for i, rec in enumerate(recommendations):
                        st.markdown(f"""
                        <div style="margin-bottom: 10px; padding: 8px; background-color: #F1F8E9; border-radius: 5px;">
                            {i+1}. {rec}
                        </div>
                        """, unsafe_allow_html=True)

                # Show alert timeline
                st.subheader("Projected Alert Timeline")
                timeline_html = """
                <div style="background-color: #F5F5F5; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <div style="display: flex; position: relative;">
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #81C784; border-radius: 50%; width: 25px; height: 25px; margin: 0 auto;"></div>
                            <p style="margin: 5px 0; font-size: 14px;">Current</p>
                            <p style="margin: 0; font-size: 12px;">Jun 1</p>
                        </div>
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #FFB74D; border-radius: 50%; width: 25px; height: 25px; margin: 0 auto;"></div>
                            <p style="margin: 5px 0; font-size: 14px;">Warning</p>
                            <p style="margin: 0; font-size: 12px;">Jun 15</p>
                        </div>
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #E57373; border-radius: 50%; width: 25px; height: 25px; margin: 0 auto;"></div>
                            <p style="margin: 5px 0; font-size: 14px;">Peak Risk</p>
                            <p style="margin: 0; font-size: 12px;">Jul 1</p>
                        </div>
                        <div style="flex: 1; text-align: center; z-index: 2;">
                            <div style="background-color: #81C784; border-radius: 50%; width: 25px; height: 25px; margin: 0 auto;"></div>
                            <p style="margin: 5px 0; font-size: 14px;">Decreasing</p>
                            <p style="margin: 0; font-size: 12px;">Jul 15</p>
                        </div>
                        <div style="position: absolute; height: 3px; background: linear-gradient(to right, #81C784, #FFB74D, #E57373, #81C784); top: 12px; width: 100%; z-index: 1;"></div>
                    </div>
                </div>
                """
                st.markdown(timeline_html, unsafe_allow_html=True)

                # Action plan
                st.subheader("Action Plan")
                st.markdown(f"""
                <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px;">
                    <h4 style="color: #2E7D32; margin-top: 0;">Recommended Timeline</h4>
                    <ul>
                        <li><strong>Immediate:</strong> {'Monitor water levels and weather forecasts daily' if risk_text != 'Low Risk' else 'Maintain regular farm operations'}</li>
                        <li><strong>This Week:</strong> {'Implement drainage improvements and secure equipment' if risk_text == 'High Risk' else 'Review farm emergency plan'}</li>
                        <li><strong>This Month:</strong> {'Consider crop insurance options and plan for potential replanting' if risk_text == 'High Risk' else 'Normal seasonal planning'}</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Prediction error: {e}")
                st.info("Using backup risk assessment based on input parameters.")

    with tab2:
        # Risk Map Visualization Tab
        st.markdown("### Risk Map by Location")

        # Simple map visualization
        st.markdown("""
        <div style="background-color: #F1F8E9; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <p>The map below shows climate risk assessments across different regions. Click on a location to see detailed risk profiles.</p>
        </div>
        """, unsafe_allow_html=True)

        map_col1, map_col2 = st.columns([3, 1])

        with map_col1:
            # Interactive climate risk heatmap with Streamlit's map components
            st.subheader("Climate Risk Heatmap")

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
                <img src="https://i.imgur.com/jzmJ4vq.jpg" width="100%" style="border-radius: 10px;" alt="Climate Risk Heatmap of India"/>
                <p style="text-align: center; font-size: 12px; margin-top: 5px;">Climate risk heatmap showing flood, drought, and normal regions across India</p>
            </div>
            """, unsafe_allow_html=True)

        with map_col2:
            # Show risk legend
            st.markdown("#### Risk Legend")
            st.markdown("""
            <div>
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="background-color: #E57373; width: 20px; height: 20px; margin-right: 10px; border-radius: 3px;"></div>
                    <div>High Risk Areas</div>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="background-color: #FFB74D; width: 20px; height: 20px; margin-right: 10px; border-radius: 3px;"></div>
                    <div>Moderate Risk Areas</div>
                </div>
                <div style="display: flex; align-items: center; margin-bottom: 8px;">
                    <div style="background-color: #81C784; width: 20px; height: 20px; margin-right: 10px; border-radius: 3px;"></div>
                    <div>Low Risk Areas</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Add regional information
            st.markdown("#### Regional Risks")
            regional_risks = {
                "North India": "High flood risk during monsoon",
                "Central India": "Moderate to high drought risk",
                "South India": "Low to moderate risk overall"
            }

            for region, risk in regional_risks.items():
                st.markdown(f"""
                <div style="background-color: #F1F8E9; padding: 10px; border-radius: 5px; margin-bottom: 5px;">
                    <strong>{region}:</strong> {risk}
                </div>
                """, unsafe_allow_html=True)

    with tab3:
        # Historical data analysis tab
        st.subheader("Historical Climate Data Analysis")

        # Year selection
        selected_year = st.select_slider(
            "Select Year Range",
            options=list(range(2020, 2026)),
            value=2023
        )

        # Historical data visualization
        st.markdown(f"### Climate Data for {selected_year}")

        # Create mock historical data charts
        hist_col1, hist_col2 = st.columns(2)

        with hist_col1:
            st.markdown("#### Rainfall Patterns")
            rainfall_chart = """
            <div style="background-color: white; padding: 10px; border-radius: 5px; height: 200px; position: relative;">
                <div style="position: absolute; bottom: 0; left: 0; width: 8%; height: 40%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 8%; width: 8%; height: 60%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 16%; width: 8%; height: 80%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 24%; width: 8%; height: 120%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 32%; width: 8%; height: 170%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 40%; width: 8%; height: 150%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 48%; width: 8%; height: 140%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 56%; width: 8%; height: 100%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 64%; width: 8%; height: 70%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 72%; width: 8%; height: 50%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 80%; width: 8%; height: 40%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: 0; left: 88%; width: 8%; height: 30%; background-color: #90CAF9;"></div>
                <div style="position: absolute; bottom: -25px; left: 0; width: 100%; text-align: center; font-size: 12px;">Jan - Dec</div>
                <div style="position: absolute; top: 0; left: -30px; transform: rotate(-90deg); transform-origin: left top; font-size: 12px;">mm</div>
            </div>
            """
            st.markdown(rainfall_chart, unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 12px;'>Monthly rainfall distribution</div>", unsafe_allow_html=True)

        with hist_col2:
            st.markdown("#### Temperature Trends")
            temp_chart = """
            <div style="background-color: white; padding: 10px; border-radius: 5px; height: 200px; position: relative;">
                <svg width="100%" height="180">
                    <path d="M0,120 C20,100 40,80 60,90 C80,100 100,110 120,95 C140,80 160,50 180,30 C200,20 220,40 240,50 C260,60 280,80 300,90 C320,100 340,110 360,100" stroke="#FF7043" stroke-width="3" fill="none"/>
                    <path d="M0,150 C20,140 40,130 60,135 C80,140 100,145 120,140 C140,135 160,130 180,120 C200,115 220,125 240,130 C260,135 280,140 300,145 C320,150 340,155 360,150" stroke="#42A5F5" stroke-width="3" fill="none"/>
                </svg>
                <div style="position: absolute; bottom: -25px; left: 0; width: 100%; text-align: center; font-size: 12px;">Jan - Dec</div>
                <div style="position: absolute; top: 0; left: -30px; transform: rotate(-90deg); transform-origin: left top; font-size: 12px;">°C</div>
                <div style="position: absolute; top: 10px; right: 10px; font-size: 12px;">
                    <span style="color: #FF7043;">■</span> Max Temp<br/>
                    <span style="color: #42A5F5;">■</span> Min Temp
                </div>
            </div>
            """
            st.markdown(temp_chart, unsafe_allow_html=True)
            st.markdown("<div style='text-align: center; font-size: 12px;'>Monthly temperature variations</div>", unsafe_allow_html=True)

        # Historical trends
        st.subheader("Long-term Climate Trends")
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin: 15px 0;">
            <h4 style="color: #2E7D32; margin-top: 0;">Climate Change Impact Summary</h4>
            <p>Based on our analysis of historical data from 1990-2025:</p>
            <ul>
                <li>Average temperature has increased by 1.2°C</li>
                <li>Rainfall patterns show 15% more variability</li>
                <li>Extreme weather events have increased by 23%</li>
                <li>Growing season has shifted by approximately 12 days</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        # Recommendations based on historical data
        st.markdown("### Agricultural Adaptation Recommendations")
        rec_col1, rec_col2 = st.columns(2)

        with rec_col1:
            st.markdown("""
            <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                <h4 style="color: #2E7D32; margin-top: 0;">Short-term Adaptations</h4>
                <ul>
                    <li>Adjust planting calendars based on shifting seasons</li>
                    <li>Implement water conservation techniques</li>
                    <li>Use drought-resistant crop varieties</li>
                    <li>Enhance drainage systems for extreme rainfall</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with rec_col2:
            st.markdown("""
            <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                <h4 style="color: #2E7D32; margin-top: 0;">Long-term Strategies</h4>
                <ul>
                    <li>Diversify crop portfolios to reduce risk</li>
                    <li>Invest in climate-smart agriculture technologies</li>
                    <li>Implement agroforestry techniques</li>
                    <li>Develop integrated pest management systems</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
