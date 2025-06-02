import streamlit as st
from pages import Crop_Recommendation, Yield_Prediction, Climate_Risk_Alerts
import base64
from PIL import Image
import os
import time
from datetime import datetime
import sys
import requests
import json

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import API services
from backend.api_services import get_visualcrossing_weather, get_location_from_ip

# Function to add background image and enhanced styling
def add_custom_styling():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=1932&auto=format&fit=crop");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.95); /* Increased opacity for better contrast */
            padding: 3rem !important;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            color: #333; /* Default text color for better visibility */
        }}
        h1, h2, h3 {{
            color: #2E7D32;
            font-family: 'Segoe UI', sans-serif;
        }}
        p, li, label, span, div {{
            color: #333; /* Ensuring all text elements are dark by default */
        }}
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            border-bottom: 2px solid #81C784;
            padding-bottom: 0.5rem;
        }}
        h2 {{
            font-size: 1.8rem;
        }}
        .stButton > button {{
            background-color: #2E7D32;
            color: white !important; /* Force white text on buttons */
            border-radius: 8px;
            padding: 0.5rem 1.2rem;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            background-color: #388E3C;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        /* Improved sidebar styling */
        [data-testid="stSidebar"] {{
            background-image: linear-gradient(to bottom, #2E7D32, #1B5E20);
            padding-top: 1rem;
        }}
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] span, 
        [data-testid="stSidebar"] div:not(.info-banner), 
        [data-testid="stSidebar"] label {{
            color: #f0f2f6 !important;
            text-shadow: 0px 1px 2px rgba(0,0,0,0.1);
        }}
        [data-testid="stSidebar"] .stRadio label {{
            color: #f0f2f6 !important;
        }}
        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 10px;
        }}
        [data-testid="stSidebar"] hr {{
            border-color: rgba(255,255,255,0.2);
            margin: 15px 0;
        }}
        [data-testid="stSidebar"] div[data-testid="stMarkdownContainer"] > div {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            margin-bottom: 1rem;
        }}
        /* Original sidebar style can be removed as we're using a better selector */
        .sidebar .sidebar-content {{
            /* Keeping for backward compatibility but not needed */
            background-image: none;
        }}
        .feature-card {{
            background-color: #F1F8E9;
            padding: 20px;
            border-radius: 15px;
            height: 220px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-left: 5px solid #558B2F;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        }}
        .feature-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
        }}
        .info-banner {{
            background-color: #E8F5E9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 5px solid #2E7D32;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }}
        .stMetric {{
            background-color: #F1F8E9;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }}
        .stMetric label {{
            color: #333 !important; /* Force dark color on metric labels */
            font-weight: 500;
        }}
        .stMetric .css-1uixxvy {{
            color: #2E7D32 !important; /* Force green color on metric values */
        }}
        .stProgress > div > div > div > div {{
            background-color: #4CAF50;
        }}
        /* Better tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            background-color: #F1F8E9;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            color: #2E7D32;
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: #2E7D32 !important;
            color: white !important;
        }}
        /* Form field improvements */
        .stNumberInput input, .stTextInput input, .stSelectbox, .stSlider {{
            border-color: #81C784;
        }}
        .stSlider [data-baseweb="slider"] div::after {{
            background-color: #2E7D32;
        }}
        
        /* Enhanced dropdown styling */
        .stSelectbox [data-baseweb="select"] div[role="button"] {{
            background-color: #F9FBE7 !important;
            border-color: #81C784 !important;
            color: #2E7D32 !important;
            font-weight: 500;
        }}
        
        .stSelectbox [data-baseweb="select"] div[role="listbox"] div {{
            color: #2E7D32 !important;
            background-color: #F9FBE7;
        }}
        
        .stSelectbox [data-baseweb="select"] div[role="listbox"] div:hover {{
            background-color: #E8F5E9;
        }}
        
        .stSelectbox [data-baseweb="select"] div[role="listbox"] div[aria-selected="true"] {{
            background-color: #C8E6C9;
        }}
        
        .stSelectbox [data-baseweb="select"] svg {{
            color: #2E7D32 !important;
        }}
        
        /* Additional styling for better dropdown visibility */
        .stSelectbox [data-baseweb="select"] span {{
            color: #2E7D32 !important;
            font-weight: 500;
        }}
        
        .stSelectbox [data-baseweb="popover"] {{
            background-color: #F9FBE7 !important;
            border: 1px solid #81C784 !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
        }}
        
        .stSelectbox [data-baseweb="select"] div[role="option"] {{
            color: #2E7D32 !important;
            background-color: #F9FBE7 !important;
        }}
        
        .stSelectbox [data-baseweb="select"] div[role="option"]:hover {{
            background-color: #E8F5E9 !important;
        }}
        
        /* Styling for multiselect dropdowns */
        .stMultiSelect [data-baseweb="tag"] {{
            background-color: #E8F5E9 !important;
            color: #2E7D32 !important;
            border: 1px solid #81C784 !important;
        }}
        
        .stMultiSelect [data-baseweb="select"] input {{
            color: #2E7D32 !important;
        }}
        
        /* Make label text more visible */
        .css-1ekf893 label, .css-16huue1 label {{
            font-weight: 500 !important;
            color: #2E7D32 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# App configuration with favicon
st.set_page_config(
    page_title="PlantX - Climate Smart Agriculture",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom styling
add_custom_styling()

# Initialize session state for page navigation and weather data
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Initialize location preferences
if 'user_location_preference' not in st.session_state:
    st.session_state.user_location_preference = None

# Explicitly initialize detected_location in session state
if 'detected_location' not in st.session_state:
    st.session_state.detected_location = None

# Initialize weather data in session state if not present
if 'weather_data' not in st.session_state:
    try:
        # Default location - can be changed to user's preferred location
        default_location = "New Delhi, India"
        # Using the API to get weather data - no need for API key as it's hardcoded in the function
        user_location = get_location_from_ip()
        st.session_state.detected_location = user_location

        # Use user's preferred location if set, otherwise use detected location
        location_to_use = st.session_state.user_location_preference or user_location

        weather_data = get_visualcrossing_weather(location_to_use, None)
        st.session_state.weather_data = weather_data
        st.session_state.weather_location = location_to_use
        st.session_state.weather_error = None
    except Exception as e:
        st.session_state.weather_data = {"temperature": 25, "humidity": 65, "rainfall": 0}
        st.session_state.weather_location = default_location
        st.session_state.detected_location = default_location
        st.session_state.weather_error = str(e)

# Sidebar with enhanced logo, weather display and navigation
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: white; margin-bottom: 0; font-size: 2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);">
            🌱 PlantX
        </h1>
        <p style="color: white; font-style: italic;">Climate Smart Agriculture</p>
        <hr style="margin: 15px 0; border-color: rgba(255,255,255,0.2);">
    </div>
    """, unsafe_allow_html=True)

    # Display current date and weather
    today = datetime.now().strftime("%B %d, %Y")
    weather_info = st.session_state.weather_data
    weather_location = st.session_state.weather_location
    weather_error = st.session_state.weather_error

    # Get the detected location
    detected_location = st.session_state.detected_location

    # Location options (common farming locations in India)
    location_options = [
        "Select Your Location...",
        "Bengaluru, India",
        "New Delhi, India",
        "Mumbai, India",
        "Chennai, India",
        "Kolkata, India",
        "Hyderabad, India",
        "Pune, India"
    ]

    # Add detected location if not already in the list
    if detected_location not in location_options:
        location_options.insert(1, detected_location)

    # Get current selected location
    current_location = st.session_state.user_location_preference or "Select Your Location..."

    # Location selector
    selected_location = st.selectbox(
        "📍 Your Location",
        options=location_options,
        index=location_options.index(current_location) if current_location in location_options else 0
    )

    # Update location if changed
    if selected_location != "Select Your Location..." and selected_location != st.session_state.user_location_preference:
        try:
            st.session_state.user_location_preference = selected_location
            # Get updated weather data
            updated_weather = get_visualcrossing_weather(selected_location, None)
            st.session_state.weather_data = updated_weather
            st.session_state.weather_location = selected_location
            st.session_state.weather_error = None
            # Add a rerun to refresh the page with new weather data
            st.rerun()
        except Exception as e:
            st.error(f"Error updating weather: {e}")

    # Show info about detected vs selected location
    if weather_error:
        weather_display = f"🌤️ Weather data unavailable: {weather_error}"
    else:
        weather_display = f"🌡️ {weather_info['temperature']}°C | 💧 {weather_info['humidity']}% | 🌧️ {weather_info['rainfall']}mm"

    st.markdown(f"""
    <div style="background-color: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
        <p style="color: white; margin-bottom: 5px;">📅 {today}</p>
        <p style="color: white; font-size: 14px;">{weather_display}</p>
        <p style="color: white; font-size: 12px;">Location: {weather_location}</p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation options with icons
    st.markdown("""
    <p style="color: white; font-weight: 500; margin-bottom: 10px;">NAVIGATION</p>
    """, unsafe_allow_html=True)

    # Map emojis to page names for proper selection
    page_map = {
        "Home": "🏠 Home",
        "Crop Recommendation": "🌾 Crop Recommendation",
        "Yield Prediction": "📊 Yield Prediction",
        "Climate Risk Alerts": "🌦️ Climate Risk Alerts"
    }

    # Find the current index based on session state page
    current_emoji_page = page_map.get(st.session_state.page, "🏠 Home")
    default_index = ["🏠 Home", "🌾 Crop Recommendation", "📊 Yield Prediction", "🌦️ Climate Risk Alerts"].index(current_emoji_page)

    selection = st.radio(
        "Navigation",
        ["🏠 Home", "🌾 Crop Recommendation", "📊 Yield Prediction", "🌦️ Climate Risk Alerts"],
        index=default_index,
        label_visibility="collapsed"
    )

    # Progress indicator
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<p style="color: white; font-size: 14px;">AI System Status</p>""", unsafe_allow_html=True)
    st.progress(0.98, "Models ready (98%)")

    # User profile section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;">
        <p style="color: white; font-size: 14px; margin-bottom: 5px;">👨‍🌾 Farmer's Portal</p>
        <p style="color: white; font-size: 12px;">Connected to local weather stations</p>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="position: absolute; bottom: 20px; text-align: center; width: 85%;">
        <p style="color: white; font-size: 12px;">© 2025 PlantX | Smart Agriculture</p>
    </div>
    """, unsafe_allow_html=True)

# Process the selection - strip the emoji from the selection
clean_selection = selection
if selection.startswith('🏠'):
    clean_selection = "Home"
elif selection.startswith('🌾'):
    clean_selection = "Crop Recommendation"
elif selection.startswith('📊'):
    clean_selection = "Yield Prediction"
elif selection.startswith('🌦️'):
    clean_selection = "Climate Risk Alerts"

# Update the session state page
st.session_state.page = clean_selection

# Display selected page
if clean_selection == "Home":
    # Create a loading animation for 0.5 seconds
    with st.spinner('Loading PlantX Dashboard...'):
        time.sleep(0.5)

    # Home page content
    st.title("🌱 PlantX - Climate Smart Agriculture Platform")

    # Welcome banner with subtle animation
    st.markdown("""
    <div class="info-banner">
        <h2 style="color: #2E7D32;">Welcome to PlantX AI</h2>
        <p>Your AI-powered assistant for climate-smart agriculture. Make informed decisions, optimize yields, and adapt to changing climate conditions.</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick stats
    st.markdown("### 📈 Farm Intelligence Dashboard")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

    with metrics_col1:
        st.metric(label="Crops Analyzed", value="15.2K+", delta="↑ 12%")
    with metrics_col2:
        st.metric(label="Weather Patterns", value="23+", delta="3 new")
    with metrics_col3:
        st.metric(label="Yield Accuracy", value="92%", delta="↑ 3.5%")
    with metrics_col4:
        st.metric(label="Risk Predictions", value="98%", delta="↑ 1.2%")

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards with enhanced styling
    st.markdown("### 🔍 Explore PlantX Services")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #558B2F;">🌾 Crop Recommendation</h3>
            <p>Get AI-powered recommendations for the most suitable crops based on your soil characteristics and local climate conditions.</p>
            <br>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Crop Recommendation →", key="crop_rec_btn"):
            st.session_state.page = "Crop Recommendation"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #558B2F;">📊 Yield Prediction</h3>
            <p>Forecast your harvest potential with our advanced machine learning models that analyze environmental factors and agricultural practices.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Yield Prediction →", key="yield_pred_btn"):
            st.session_state.page = "Yield Prediction"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #558B2F;">🌦️ Climate Risk Alerts</h3>
            <p>Stay one step ahead of weather events with early warning system that helps you protect crops and optimize farming operations.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Climate Risk Alerts →", key="climate_risk_btn"):
            st.session_state.page = "Climate Risk Alerts"
            st.rerun()

    # Testimonial section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💬 Farmer Success Stories")

    testimonial_col1, testimonial_col2 = st.columns(2)

    with testimonial_col1:
        st.markdown("""
        <div style="background-color: #F9FBE7; padding: 20px; border-radius: 10px; position: relative; margin-top: 10px;">
            <p style="font-style: italic;">"PlantX helped me increase my crop yield by 27% in just one season by recommending the perfect crop rotation strategy for my soil conditions."</p>
            <p style="text-align: right; margin-bottom: 0; font-weight: bold;">- James Wilson</p>
            <p style="text-align: right; margin-top: 0; color: #558B2F; font-size: 14px;">Corn Farmer, Iowa</p>
        </div>
        """, unsafe_allow_html=True)

    with testimonial_col2:
        st.markdown("""
        <div style="background-color: #F9FBE7; padding: 20px; border-radius: 10px; position: relative; margin-top: 10px;">
            <p style="font-style: italic;">"The climate risk alerts warned me about an upcoming frost two days before it hit, giving me enough time to protect my vineyard. This saved my entire harvest!"</p>
            <p style="text-align: right; margin-bottom: 0; font-weight: bold;">- Maria Rodriguez</p>
            <p style="text-align: right; margin-top: 0; color: #558B2F; font-size: 14px;">Vineyard Owner, California</p>
        </div>
        """, unsafe_allow_html=True)

    # About section with enhanced design
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 25px; border-radius: 15px; margin-top: 30px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);">
        <h2 style="color: #2E7D32;">About PlantX Technology</h2>
        <p>PlantX combines cutting-edge machine learning algorithms with decades of agricultural science to provide actionable insights for sustainable farming. Our platform analyzes soil composition, climate patterns, historical yield data, and real-time weather information to help you:</p>
        <ul>
            <li><strong>Optimize crop selection</strong> based on your specific field conditions</li>
            <li><strong>Predict potential yields</strong> with high accuracy before planting</li>
            <li><strong>Anticipate climate risks</strong> that could affect your crops</li>
            <li><strong>Reduce environmental impact</strong> while maximizing productivity</li>
        </ul>
        <p>Join thousands of farmers who are already using PlantX to transform their agricultural practices and adapt to our changing climate.</p>
    </div>
    """, unsafe_allow_html=True)

    # Call to action
    st.markdown("<br>", unsafe_allow_html=True)
    cta_col1, cta_col2 = st.columns([2, 1])

    with cta_col2:
        st.markdown("""
        <div style="background-color: #2E7D32; padding: 20px; border-radius: 10px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h3 style="color: white; margin-top: 0;">Ready to get started?</h3>
            <p style="color: white;">Explore our tools and see the difference PlantX can make for your farm.</p>
        </div>
        """, unsafe_allow_html=True)

    with cta_col1:
        st.image("https://images.unsplash.com/photo-1574943320219-89283140739e?q=80&w=1932&auto=format&fit=crop",
                 caption="AI-driven farming - The future of agriculture")

elif clean_selection == "Crop Recommendation":
    with st.spinner('Loading Crop Recommendation System...'):
        time.sleep(0.5)
    Crop_Recommendation.show()
elif clean_selection == "Yield Prediction":
    with st.spinner('Loading Yield Prediction System...'):
        time.sleep(0.5)
    Yield_Prediction.show()
elif clean_selection == "Climate Risk Alerts":
    with st.spinner('Loading Climate Risk Alert System...'):
        time.sleep(0.5)
    Climate_Risk_Alerts.show()
