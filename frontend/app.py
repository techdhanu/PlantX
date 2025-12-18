import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import page modules
from pages import Crop_Recommendation, Yield_Prediction, Climate_Risk_Alerts, Plant_Disease_Detection, Soil_Analysis

# Import API services
from backend.api_services import get_visualcrossing_weather, get_location_from_ip

# Page configuration
st.set_page_config(
    page_title="PlantX - AI Agriculture Platform",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling matching the enhanced pages
st.markdown("""
<style>
    /* Main container styling with light background for better visibility */
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 20%, #ffffff 100%) !important;
    }

    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8f0f7 100%) !important;
    }

    /* Block container for content */
    .block-container {
        background-color: rgba(255, 255, 255, 0.95) !important;
        padding: 2rem !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }

    /* Force all main content text to be dark and visible */
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #1a1a1a !important;
    }

    .main p {
        color: #2d2d2d !important;
    }

    .main span {
        color: #2d2d2d !important;
    }

    .main div {
        color: #2d2d2d !important;
    }

    .main label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }

    .main li {
        color: #2d2d2d !important;
    }

    /* Input fields should have dark text */
    .main input {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }

    .main textarea {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }

    .main select {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }

    /* Streamlit specific text elements */
    .stMarkdown {
        color: #2d2d2d !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #2d2d2d !important;
    }

    /* Form labels */
    .css-10trblm {
        color: #1a1a1a !important;
    }

    /* Radio and checkbox labels */
    .stRadio label, .stCheckbox label {
        color: #1a1a1a !important;
    }

    /* Selectbox text */
    .stSelectbox label {
        color: #1a1a1a !important;
    }

    /* Number input labels */
    .stNumberInput label {
        color: #1a1a1a !important;
    }

    /* Text input labels */
    .stTextInput label {
        color: #1a1a1a !important;
    }

    /* Slider labels */
    .stSlider label {
        color: #1a1a1a !important;
    }

    /* Button text should be white */
    .stButton>button {
        color: white !important;
        background-color: #2E7D32 !important;
    }

    /* Expander text */
    .streamlit-expanderHeader {
        color: #1a1a1a !important;
    }

    /* Tab text */
    .stTabs [data-baseweb="tab"] {
        color: #1a1a1a !important;
    }

    /* Metric labels and values */
    [data-testid="stMetricLabel"] {
        color: #1a1a1a !important;
    }

    [data-testid="stMetricValue"] {
        color: #2E7D32 !important;
    }

    /* Sidebar styling with modern gradient */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2E7D32 0%, #1B5E20 100%);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }

    /* Sidebar text styling */
    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stRadio > label {
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 1rem;
    }

    /* Sidebar radio button styling */
    section[data-testid="stSidebar"] [role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin: 0.3rem 0;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] {
        background: rgba(255, 255, 255, 0.25);
        border-left: 4px solid #8BC34A;
        font-weight: 700;
    }

    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 100%);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for weather data and location preferences
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'location_data' not in st.session_state:
    st.session_state.location_data = None
if 'user_location_preference' not in st.session_state:
    st.session_state.user_location_preference = None
if 'detected_location' not in st.session_state:
    st.session_state.detected_location = None
if 'weather_location' not in st.session_state:
    st.session_state.weather_location = "New Delhi, India"
if 'selected_latitude' not in st.session_state:
    st.session_state.selected_latitude = 28.6139
if 'selected_longitude' not in st.session_state:
    st.session_state.selected_longitude = 77.2090

# Location to coordinates mapping for major Indian cities
LOCATION_COORDINATES = {
    "New Delhi, India": (28.6139, 77.2090),
    "Mumbai, India": (19.0760, 72.8777),
    "Bengaluru, India": (12.9716, 77.5946),
    "Chennai, India": (13.0827, 80.2707),
    "Kolkata, India": (22.5726, 88.3639),
    "Hyderabad, India": (17.3850, 78.4867),
    "Pune, India": (18.5204, 73.8567),
    "Ahmedabad, India": (23.0225, 72.5714),
    "Jaipur, India": (26.9124, 75.7873),
    "Lucknow, India": (26.8467, 80.9462)
}

# Sidebar Navigation
with st.sidebar:
    # Logo and title
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <h1 style="color: white; font-size: 2.5rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            🌱 PlantX
        </h1>
        <p style="color: rgba(255,255,255,0.9); font-size: 0.9rem; margin: 0.5rem 0 0 0;">
            AI-Powered Agriculture Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Navigation menu
    st.markdown("""
    <p style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 1rem 0 0.5rem 0; text-transform: uppercase; letter-spacing: 1px;">
        Navigation
    </p>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Select Feature",
        ["🏠 Home", "🔬 Plant Disease Detection", "🌱 Soil Analysis",
         "🌾 Crop Recommendation", "📊 Yield Prediction", "🌦️ Climate Risk Alerts"],
        label_visibility="collapsed"
    )

    # Divider
    st.markdown("<hr style='margin: 2rem 0; border-color: rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

    # Location selector and weather display
    st.markdown("""
    <p style="color: rgba(255,255,255,0.8); font-size: 0.85rem; margin: 1rem 0 0.5rem 0; text-transform: uppercase; letter-spacing: 1px;">
        Location & Weather
    </p>
    """, unsafe_allow_html=True)

    # Get detected location if not already done
    if st.session_state.detected_location is None:
        try:
            detected_loc = get_location_from_ip()
            if detected_loc and 'location_string' in detected_loc:
                st.session_state.detected_location = detected_loc['location_string']
                st.session_state.location_data = detected_loc
                # Set initial coordinates from detected location
                st.session_state.selected_latitude = detected_loc.get('latitude', 28.6139)
                st.session_state.selected_longitude = detected_loc.get('longitude', 77.2090)
            else:
                st.session_state.detected_location = "New Delhi, India"
                st.session_state.selected_latitude = 28.6139
                st.session_state.selected_longitude = 77.2090
        except:
            st.session_state.detected_location = "New Delhi, India"
            st.session_state.selected_latitude = 28.6139
            st.session_state.selected_longitude = 77.2090

    # Location options (common farming locations in India)
    location_options = [
        "New Delhi, India",
        "Mumbai, India",
        "Bengaluru, India",
        "Chennai, India",
        "Kolkata, India",
        "Hyderabad, India",
        "Pune, India",
        "Ahmedabad, India",
        "Jaipur, India",
        "Lucknow, India"
    ]

    # Add detected location if not already in the list
    if st.session_state.detected_location and st.session_state.detected_location not in location_options:
        location_options.insert(0, st.session_state.detected_location)

    # Get current selected location
    current_location = st.session_state.user_location_preference or st.session_state.detected_location or "New Delhi, India"

    # Location selector
    selected_location = st.selectbox(
        "📍 Your Location",
        options=location_options,
        index=location_options.index(current_location) if current_location in location_options else 0,
        help="Select your location to get accurate weather data"
    )

    # Update location and fetch weather if changed
    if selected_location != st.session_state.user_location_preference:
        try:
            st.session_state.user_location_preference = selected_location

            # Update latitude and longitude based on selected location
            if selected_location in LOCATION_COORDINATES:
                lat, lon = LOCATION_COORDINATES[selected_location]
                st.session_state.selected_latitude = lat
                st.session_state.selected_longitude = lon
            else:
                # Try to get coordinates from location_data if it's the detected location
                if st.session_state.location_data and selected_location == st.session_state.detected_location:
                    st.session_state.selected_latitude = st.session_state.location_data.get('latitude', 28.6139)
                    st.session_state.selected_longitude = st.session_state.location_data.get('longitude', 77.2090)

            # Fetch updated weather data
            updated_weather = get_visualcrossing_weather(selected_location)
            if updated_weather:
                st.session_state.weather_data = updated_weather
                st.session_state.weather_location = selected_location
                st.rerun()
        except Exception as e:
            st.warning(f"Could not fetch weather for {selected_location}")

    # Display current date and weather
    today = datetime.now().strftime("%B %d, %Y")

    # Get weather info
    weather_info = st.session_state.weather_data
    weather_location = st.session_state.weather_location

    if weather_info and 'temperature' in weather_info:
        weather_display = f"🌡️ {weather_info['temperature']}°C | 💧 {weather_info['humidity']}% | 🌧️ {weather_info['rainfall']}mm"
    else:
        weather_display = "🌤️ Loading weather data..."

    st.markdown(f"""
    <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 15px 0;">
        <p style="color: white; margin-bottom: 8px; font-size: 0.9rem;">📅 {today}</p>
        <p style="color: white; font-size: 0.85rem; margin-bottom: 8px;">{weather_display}</p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.75rem; margin: 0;">📍 {weather_location}</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Info
    st.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 8px; margin-top: 1rem;">
        <p style="font-size: 0.85rem; margin: 0;">
            <strong>📅 Date:</strong> {datetime.now().strftime('%B %d, %Y')}
        </p>
        <p style="font-size: 0.85rem; margin: 0.5rem 0 0 0;">
            <strong>🌍 Platform:</strong> PlantX AI
        </p>
    </div>
    """, unsafe_allow_html=True)

# Main content area
if page == "🏠 Home":
    # Home Page with modern design
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="font-size: 3.5rem; font-weight: 700; margin-bottom: 0.5rem; 
                   color: #2E7D32 !important;">
            Welcome to PlantX
        </h1>
        <p style="font-size: 1.3rem; color: #666; margin: 0;">
            Your Complete AI-Powered Agriculture Solution
        </p>
        <div style="width: 100px; height: 4px; background: linear-gradient(90deg, #2E7D32, #8BC34A); 
                    margin: 1.5rem auto; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                padding: 2.5rem; border-radius: 16px; margin-bottom: 2rem;
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(46, 125, 50, 0.1); text-align: center;">
        <h2 style="color: #2E7D32; margin: 0 0 1rem 0; font-size: 2rem;">
            🚀 Empowering Farmers with AI Technology
        </h2>
        <p style="color: #333; line-height: 1.8; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
            PlantX combines cutting-edge artificial intelligence with agricultural expertise to help you make 
            <strong>data-driven decisions</strong> for optimal crop management, disease prevention, and yield maximization.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Features Grid
    st.markdown("""
    <h2 style="color: #2E7D32; text-align: center; margin: 3rem 0 2rem 0; font-size: 2rem;">
        🌟 Key Features
    </h2>
    """, unsafe_allow_html=True)

    # Feature cards in columns
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 2rem; border-radius: 12px; height: 100%;
                    border-left: 4px solid #1976D2;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
                    transition: transform 0.3s ease;">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">🔬</div>
            <h3 style="color: #1976D2; text-align: center; margin-bottom: 1rem;">Disease Detection</h3>
            <p style="color: #333; line-height: 1.6; text-align: center;">
                AI-powered identification of plant diseases with treatment recommendations
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 100%); 
                    padding: 2rem; border-radius: 12px; height: 100%;
                    border-left: 4px solid #8B4513;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">🌱</div>
            <h3 style="color: #8B4513; text-align: center; margin-bottom: 1rem;">Soil Analysis</h3>
            <p style="color: #333; line-height: 1.6; text-align: center;">
                Instant soil classification with tailored crop and management suggestions
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); 
                    padding: 2rem; border-radius: 12px; height: 100%;
                    border-left: 4px solid #558B2F;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">🌾</div>
            <h3 style="color: #558B2F; text-align: center; margin-bottom: 1rem;">Crop Recommendation</h3>
            <p style="color: #333; line-height: 1.6; text-align: center;">
                Smart crop selection based on soil nutrients and climate conditions
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                    padding: 2rem; border-radius: 12px; height: 100%;
                    border-left: 4px solid #F57C00;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #F57C00; text-align: center; margin-bottom: 1rem;">Yield Prediction</h3>
            <p style="color: #333; line-height: 1.6; text-align: center;">
                Accurate harvest forecasting for better production planning
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                    padding: 2rem; border-radius: 12px; height: 100%;
                    border-left: 4px solid #1976D2;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">🌦️</div>
            <h3 style="color: #1976D2; text-align: center; margin-bottom: 1rem;">Climate Risk Alerts</h3>
            <p style="color: #333; line-height: 1.6; text-align: center;">
                Early warning system for weather-related crop risks
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%); 
                    padding: 2rem; border-radius: 12px; height: 100%;
                    border-left: 4px solid #2E7D32;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">🤖</div>
            <h3 style="color: #2E7D32; text-align: center; margin-bottom: 1rem;">AI Technology</h3>
            <p style="color: #333; line-height: 1.6; text-align: center;">
                Machine learning models trained on extensive agricultural data
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Quick Start Guide
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
                padding: 2rem; border-radius: 12px; margin: 2rem 0;
                border-left: 4px solid #FF9800;
                box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
        <h3 style="color: #E65100; margin-top: 0;">🚀 Getting Started</h3>
        <div style="color: #333; line-height: 2;">
            <p style="margin: 0.5rem 0;"><strong>1.</strong> Select a feature from the sidebar navigation</p>
            <p style="margin: 0.5rem 0;"><strong>2.</strong> Upload images or enter your data</p>
            <p style="margin: 0.5rem 0;"><strong>3.</strong> Get instant AI-powered insights and recommendations</p>
            <p style="margin: 0.5rem 0;"><strong>4.</strong> Take action based on personalized guidance</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stats section
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h2 style="color: #2E7D32; margin: 0; font-size: 2.5rem; font-weight: 700;">38+</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Disease Types</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF8DC 0%, #FAEBD7 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h2 style="color: #8B4513; margin: 0; font-size: 2.5rem; font-weight: 700;">10</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Soil Types</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h2 style="color: #558B2F; margin: 0; font-size: 2.5rem; font-weight: 700;">55+</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Crop Types</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
                    padding: 1.5rem; border-radius: 10px; text-align: center;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
            <h2 style="color: #1976D2; margin: 0; font-size: 2.5rem; font-weight: 700;">30+</h2>
            <p style="color: #666; margin: 0.5rem 0 0 0; font-size: 0.9rem;">Indian States</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "🔬 Plant Disease Detection":
    Plant_Disease_Detection.show()

elif page == "🌱 Soil Analysis":
    Soil_Analysis.show()

elif page == "🌾 Crop Recommendation":
    Crop_Recommendation.show()

elif page == "📊 Yield Prediction":
    Yield_Prediction.show()

elif page == "🌦️ Climate Risk Alerts":
    # Use the selected location from dropdown
    location_to_use = st.session_state.user_location_preference or st.session_state.detected_location or "New Delhi, India"

    # Fetch weather data if not already available or if location changed
    if st.session_state.weather_data is None or st.session_state.weather_location != location_to_use:
        try:
            print(f"[DEBUG] Fetching weather for: {location_to_use}")
            weather_data = get_visualcrossing_weather(location_to_use)
            if weather_data:
                st.session_state.weather_data = weather_data
                st.session_state.weather_location = location_to_use
                print(f"[DEBUG] Weather data fetched successfully!")
            else:
                print(f"[DEBUG] Failed to fetch weather data")
                # Try fallback if it fails
                weather_data = get_visualcrossing_weather("New Delhi, India")
                if weather_data:
                    st.session_state.weather_data = weather_data
                    st.session_state.weather_location = "New Delhi, India"
        except Exception as e:
            print(f"[DEBUG] Error fetching weather: {str(e)}")
            # Try fallback location
            try:
                weather_data = get_visualcrossing_weather("New Delhi, India")
                if weather_data:
                    st.session_state.weather_data = weather_data
                    st.session_state.weather_location = "New Delhi, India"
            except:
                pass  # Silently fail, page will handle missing data

    Climate_Risk_Alerts.show()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem 0 1rem 0; border-top: 2px solid #E0E0E0; margin-top: 3rem;">
    <p style="color: #666; font-size: 0.9rem; margin: 0;">
        © 2025 PlantX - AI-Powered Agriculture Platform
    </p>
    <p style="color: #999; font-size: 0.85rem; margin: 0.5rem 0 0 0;">
        Empowering farmers with intelligent technology
    </p>
</div>
""", unsafe_allow_html=True)

