import streamlit as st
from pages import Crop_Recommendation, Yield_Prediction, Climate_Risk_Alerts, Plant_Disease_Detection, Soil_Analysis
import base64
from PIL import Image
import os
import time
from datetime import datetime
import sys
import requests
import json
from utils import display_logo, create_animated_header, create_feature_card, create_info_banner, create_metric_card, add_floating_action_button

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import API services
from backend.api_services import get_visualcrossing_weather, get_location_from_ip

# Page configuration
st.set_page_config(
    page_title="PlantX - AI-Powered Agricultural Assistant",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced custom styling
def add_custom_styling():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
        }
        
        .main-container {
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .block-container {
            background: transparent;
            padding: 1rem !important;
        }
        
        /* Typography */
        * {
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #2E7D32;
            font-weight: 600;
        }
        
        h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #2E7D32, #4CAF50);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        }
        
        .css-17eq0hr {
            background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
        }
        
        [data-testid="stSidebar"] .css-ng1t4o {
            background: transparent;
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: white !important;
            font-weight: 500;
            font-size: 1.1rem;
        }
        
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            background: rgba(46, 125, 50, 0.1);
            border-radius: 10px;
            padding: 5px;
            gap: 5px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 8px;
            color: #2E7D32;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(46, 125, 50, 0.1);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2E7D32, #4CAF50) !important;
            color: white !important;
        }
        
        /* Card Animations */
        .feature-card {
            animation: slideInUp 0.6s ease-out;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* File Uploader Styling */
        .stFileUploader {
            background: rgba(76, 175, 80, 0.05);
            border: 2px dashed #4CAF50;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            background: rgba(76, 175, 80, 0.1);
            border-color: #2E7D32;
        }
        
        /* Progress Bars */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #4CAF50, #2E7D32);
            border-radius: 10px;
        }
        
        /* Metrics */
        [data-testid="metric-container"] {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 15px;
            padding: 1rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            border-top: 4px solid #4CAF50;
            transition: all 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        /* Success/Error Messages */
        .stSuccess {
            background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
            border-left: 5px solid #4CAF50;
            border-radius: 10px;
        }
        
        .stError {
            background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
            border-left: 5px solid #F44336;
            border-radius: 10px;
        }
        
        .stWarning {
            background: linear-gradient(135deg, #FFF3E0, #FFE0B2);
            border-left: 5px solid #FF9800;
            border-radius: 10px;
        }
        
        /* Loading Spinner */
        .stSpinner {
            color: #4CAF50 !important;
        }
        
        /* Hide Streamlit Footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #4CAF50, #2E7D32);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #2E7D32;
        }
        </style>
    """, unsafe_allow_html=True)

def display_weather_info():
    """Display current weather information"""
    try:
        location_data = get_location_from_ip()
        if location_data and 'city' in location_data:
            city = location_data['city']
            weather_data = get_visualcrossing_weather(city)

            if weather_data and 'currentConditions' in weather_data:
                current = weather_data['currentConditions']

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(create_metric_card(
                        "Temperature",
                        f"{current.get('temp', 'N/A')}",
                        "°C",
                        "🌡️"
                    ), unsafe_allow_html=True)

                with col2:
                    st.markdown(create_metric_card(
                        "Humidity",
                        f"{current.get('humidity', 'N/A')}",
                        "%",
                        "💧"
                    ), unsafe_allow_html=True)

                with col3:
                    st.markdown(create_metric_card(
                        "Wind Speed",
                        f"{current.get('windspeed', 'N/A')}",
                        "km/h",
                        "💨"
                    ), unsafe_allow_html=True)

                with col4:
                    conditions = current.get('conditions', 'Unknown')
                    icon = "☀️" if "clear" in conditions.lower() else "☁️" if "cloud" in conditions.lower() else "🌧️" if "rain" in conditions.lower() else "🌤️"
                    st.markdown(create_metric_card(
                        "Conditions",
                        conditions,
                        "",
                        icon
                    ), unsafe_allow_html=True)

                return True
    except Exception as e:
        st.markdown(create_info_banner(
            "Weather Unavailable",
            f"Unable to fetch weather data: {str(e)}",
            "warning"
        ), unsafe_allow_html=True)

    return False

def main():
    add_custom_styling()

    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Sidebar with logo and navigation
    with st.sidebar:
        st.markdown(display_logo(150), unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h2 style="color: white; margin: 0;">PlantX</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 5px 0 0 0;">AI Agricultural Assistant</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Navigation
        selected_page = st.radio(
            "Navigate to:",
            [
                "🏠 Dashboard",
                "🌾 Crop Recommendation",
                "📈 Yield Prediction",
                "🌡️ Climate Risk Alerts",
                "🔬 Plant Disease Detection",
                "🌱 Soil Analysis"
            ]
        )

        st.markdown("---")

        # Quick stats
        st.markdown("""
        <div style="text-align: center; margin-top: 30px;">
            <h4 style="color: white;">Today's Quick Stats</h4>
        </div>
        """, unsafe_allow_html=True)

        # Current time
        current_time = datetime.now().strftime("%H:%M")
        current_date = datetime.now().strftime("%B %d, %Y")

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 10px 0; text-align: center;">
            <div style="color: white; font-size: 1.5rem; font-weight: bold;">{current_time}</div>
            <div style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">{current_date}</div>
        </div>
        """, unsafe_allow_html=True)

    # Main content area
    if selected_page == "🏠 Dashboard":
        # Dashboard header
        st.markdown(create_animated_header(
            "PlantX Dashboard",
            "Your AI-Powered Agricultural Assistant",
            "🌾"
        ), unsafe_allow_html=True)

        # Welcome message
        st.markdown(create_info_banner(
            "Welcome to PlantX!",
            "Harness the power of AI to optimize your agricultural decisions. Get crop recommendations, predict yields, detect diseases, and much more!",
            "success"
        ), unsafe_allow_html=True)

        # Weather information
        st.markdown("## 🌤️ Current Weather")
        weather_displayed = display_weather_info()

        if not weather_displayed:
            st.markdown("Weather information unavailable at the moment.")

        st.markdown("---")

        # Feature showcase
        st.markdown("## 🚀 Available Features")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(create_feature_card(
                "Crop Recommendation",
                "Get AI-powered recommendations for the best crops to grow based on your soil and climate conditions.",
                "🌾",
                "#2E7D32"
            ), unsafe_allow_html=True)

            st.markdown(create_feature_card(
                "Climate Risk Alerts",
                "Stay ahead of weather patterns and receive alerts about potential risks to your crops.",
                "🌡️",
                "#FF9800"
            ), unsafe_allow_html=True)

            st.markdown(create_feature_card(
                "Soil Analysis",
                "Upload soil images to identify soil type and get tailored management recommendations.",
                "🌱",
                "#795548"
            ), unsafe_allow_html=True)

        with col2:
            st.markdown(create_feature_card(
                "Yield Prediction",
                "Predict crop yields using advanced machine learning models to plan your harvest better.",
                "📈",
                "#1976D2"
            ), unsafe_allow_html=True)

            st.markdown(create_feature_card(
                "Disease Detection",
                "Upload plant images to detect diseases early and get treatment recommendations.",
                "🔬",
                "#D32F2F"
            ), unsafe_allow_html=True)

            st.markdown(create_feature_card(
                "Real-time Insights",
                "Get real-time weather data and agricultural insights to make informed decisions.",
                "📊",
                "#7B1FA2"
            ), unsafe_allow_html=True)

        # Quick start guide
        st.markdown("---")
        st.markdown("## 🎯 Quick Start Guide")

        steps = [
            ("📍", "Choose Location", "Select your location for accurate weather and climate data"),
            ("🌾", "Select Crop", "Choose the crop you want to analyze or get recommendations for"),
            ("📸", "Upload Images", "Upload soil or plant images for AI analysis"),
            ("📊", "Get Results", "Receive AI-powered insights and recommendations")
        ]

        for i, (icon, title, description) in enumerate(steps):
            col_icon, col_content = st.columns([1, 4])
            with col_icon:
                st.markdown(f"""
                <div style="
                    width: 50px; 
                    height: 50px; 
                    background: linear-gradient(135deg, #4CAF50, #2E7D32);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-size: 1.5rem;
                    margin: 10px 0;
                ">{icon}</div>
                """, unsafe_allow_html=True)

            with col_content:
                st.markdown(f"""
                <div style="margin: 15px 0;">
                    <h4 style="color: #2E7D32; margin: 0;">{title}</h4>
                    <p style="color: #666; margin: 5px 0 0 0;">{description}</p>
                </div>
                """, unsafe_allow_html=True)

    elif selected_page == "🌾 Crop Recommendation":
        Crop_Recommendation.show()
    elif selected_page == "📈 Yield Prediction":
        Yield_Prediction.show()
    elif selected_page == "🌡️ Climate Risk Alerts":
        Climate_Risk_Alerts.show()
    elif selected_page == "🔬 Plant Disease Detection":
        Plant_Disease_Detection.show()
    elif selected_page == "🌱 Soil Analysis":
        Soil_Analysis.show()

    # Floating action button
    st.markdown(add_floating_action_button(), unsafe_allow_html=True)

    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>Made with ❤️ using AI • PlantX © 2025 • Empowering Agriculture with Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
