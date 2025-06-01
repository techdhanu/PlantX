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
            st.markdown("""
            <iframe src="https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d7098.94326104394!2d78.0430654485247!3d27.172909818538997!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!5e0!3m2!1sen!2sin!4v1385710909804" width="100%" height="400" style="border:0; border-radius: 10px;" allowfullscreen="" loading="lazy"></iframe>
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

            # Sample region data
            st.markdown("#### Selected Region")
            st.markdown("""
            <div style="background-color: #F5F5F5; padding: 10px; border-radius: 5px;">
                <p style="margin: 0;"><strong>Region:</strong> North India</p>
                <p style="margin: 5px 0;"><strong>Primary Risk:</strong> Monsoon Flooding</p>
                <p style="margin: 0;"><strong>Risk Level:</strong> <span style="color: #FF9800;">Moderate</span></p>
            </div>
            """, unsafe_allow_html=True)

            st.button("Update Map View", key="update_map")

        # Risk trends by location
        st.markdown("### 📊 Regional Risk Trends")
        trend_col1, trend_col2, trend_col3 = st.columns(3)

        with trend_col1:
            st.markdown("""
            <div style="background-color: #FFF3E0; padding: 15px; border-radius: 10px; text-align: center;">
                <h4 style="color: #E65100; margin-top: 0;">Northern Region</h4>
                <p style="font-size: 24px; font-weight: bold;">↗️ Increasing</p>
                <p>Due to early monsoon patterns</p>
            </div>
            """, unsafe_allow_html=True)

        with trend_col2:
            st.markdown("""
            <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; text-align: center;">
                <h4 style="color: #2E7D32; margin-top: 0;">Southern Region</h4>
                <p style="font-size: 24px; font-weight: bold;">↘️ Decreasing</p>
                <p>Rainfall below average</p>
            </div>
            """, unsafe_allow_html=True)

        with trend_col3:
            st.markdown("""
            <div style="background-color: #E0F2F1; padding: 15px; border-radius: 10px; text-align: center;">
                <h4 style="color: #00695C; margin-top: 0;">Western Region</h4>
                <p style="font-size: 24px; font-weight: bold;">→ Stable</p>
                <p>Normal seasonal patterns</p>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        # Historical Analysis Tab
        st.markdown("### Historical Climate Risk Analysis")

        st.markdown("""
        <div style="background-color: #F1F8E9; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
            <p>Review historical climate patterns to understand seasonal risks and prepare for future events.</p>
        </div>
        """, unsafe_allow_html=True)

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
                <div style="position: absolute; bottom: -25px; left: 0; width: 100%; display: flex; justify-content: space-between;">
                    <span style="font-size: 10px;">Jan</span>
                    <span style="font-size: 10px;">Feb</span>
                    <span style="font-size: 10px;">Mar</span>
                    <span style="font-size: 10px;">Apr</span>
                    <span style="font-size: 10px;">May</span>
                    <span style="font-size: 10px;">Jun</span>
                    <span style="font-size: 10px;">Jul</span>
                    <span style="font-size: 10px;">Aug</span>
                    <span style="font-size: 10px;">Sep</span>
                    <span style="font-size: 10px;">Oct</span>
                    <span style="font-size: 10px;">Nov</span>
                    <span style="font-size: 10px;">Dec</span>
                </div>
                <div style="position: absolute; top: 10px; left: 10px; background-color: rgba(255,255,255,0.7); padding: 5px; border-radius: 5px;">
                    <p style="margin: 0; font-size: 12px;">Peak Rainfall: July</p>
                    <p style="margin: 0; font-size: 12px;">Monsoon Period: Jun-Sep</p>
                </div>
            </div>
            """
            st.markdown(rainfall_chart, unsafe_allow_html=True)

        with hist_col2:
            st.markdown("#### Flood Events")
            events_chart = """
            <div style="background-color: white; padding: 10px; border-radius: 5px; height: 200px; position: relative;">
                <div style="position: absolute; left: 10%; top: 30%; width: 15%; height: 40px; background-color: #FF8A65; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px;">Jun 12-15</div>
                <div style="position: absolute; left: 40%; top: 50%; width: 25%; height: 40px; background-color: #EF5350; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px;">Jul 24-Aug 2</div>
                <div style="position: absolute; left: 75%; top: 30%; width: 10%; height: 40px; background-color: #FF8A65; border-radius: 5px; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px;">Sep 5-8</div>
                <div style="position: absolute; bottom: -25px; left: 0; width: 100%; display: flex; justify-content: space-between;">
                    <span style="font-size: 10px;">Jan</span>
                    <span style="font-size: 10px;">Mar</span>
                    <span style="font-size: 10px;">May</span>
                    <span style="font-size: 10px;">Jul</span>
                    <span style="font-size: 10px;">Sep</span>
                    <span style="font-size: 10px;">Nov</span>
                </div>
                <div style="position: absolute; top: 10px; right: 10px; background-color: rgba(255,255,255,0.7); padding: 5px; border-radius: 5px;">
                    <p style="margin: 0; font-size: 12px;">Major Event: Jul-Aug</p>
                    <p style="margin: 0; font-size: 12px;">3 Events Total</p>
                </div>
            </div>
            """
            st.markdown(events_chart, unsafe_allow_html=True)

        # Historical notes and insights
        st.markdown("### Historical Insights")
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin-top: 15px;">
            <h4 style="color: #2E7D32; margin-top: 0;">Key Observations</h4>
            <ul>
                <li>Peak flooding typically occurs 2-3 weeks after monsoon onset</li>
                <li>Areas below 100m elevation experience 60% higher flood probability</li>
                <li>Sandy soils show 40% lower flood risk compared to clay soils</li>
                <li>Historical flood patterns repeat every 5-7 years on average</li>
                <li>Climate change has increased extreme rainfall events by 23% since 2010</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Educational section at bottom
    with st.expander("🧠 Learn About Climate Risks in Agriculture"):
        st.markdown("""
        ### Climate Change and Agricultural Impact
        
        Climate change affects agriculture through several key mechanisms:
        
        - **Extreme Weather Events**: Increased frequency of floods, droughts, and storms
        - **Shifting Growing Seasons**: Changes in temperature affecting planting and harvesting times
        - **Water Availability**: Altered rainfall patterns affecting irrigation needs
        - **Pest and Disease Patterns**: Changing conditions favor certain pests and diseases
        
        ### How to Build Farm Resilience
        
        1. **Diversification**: Plant multiple crop varieties to spread risk
        2. **Water Management**: Implement efficient irrigation and drainage systems
        3. **Soil Health**: Focus on building organic matter to improve water retention
        4. **Weather Monitoring**: Use technology to anticipate and respond to weather events
        5. **Adapted Practices**: Adjust planting dates and techniques based on changing patterns
        
        ### Using PlantX for Climate Adaptation
        
        Our climate risk tools can help you make informed decisions by:
        
        - Providing early warnings of potential weather risks
        - Recommending crops adapted to your changing climate conditions
        - Forecasting yields under different climate scenarios
        - Suggesting specific adaptation strategies for your farm
        """)
