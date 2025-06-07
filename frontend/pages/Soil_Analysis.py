import streamlit as st
import os
import sys
import time
from PIL import Image
import io
import requests

# Add project root directory to path so we can import from backend
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from backend.soil_classifier import soil_classifier

def show():
    st.header("🌱 Soil Type Analysis")

    # Information banner
    st.markdown("""
    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; margin-bottom: 20px; border-left: 5px solid #2E7D32;">
        <h3 style="color: #2E7D32; margin-top: 0;">AI-Powered Soil Classification</h3>
        <p>Upload an image of your soil to identify its type and receive tailored recommendations for soil management and suitable crops.</p>
    </div>
    """, unsafe_allow_html=True)

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📷 Soil Scanner", "📚 Soil Library", "📊 Analysis Results"])

    with tab1:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### Upload Soil Image")

            # File uploader for soil analysis
            uploaded_file = st.file_uploader(
                "Choose a clear image of your soil:",
                type=["jpg", "jpeg", "png"],
                help="For best results, upload a well-lit, close-up image of soil"
            )

            # Add analyze button
            analyze_col1, analyze_col2 = st.columns([1, 2])
            with analyze_col1:
                analyze_button = st.button("🔍 Analyze Soil", type="primary", use_container_width=True)

        with col2:
            st.markdown("### Tips for Best Results")

            st.markdown("""
            <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                <h4 style="color: #558B2F; margin-top: 0;">📸 Taking Good Soil Photos</h4>
                <ul style="margin-bottom: 0;">
                    <li>Ensure good natural lighting</li>
                    <li>Clear away debris and vegetation</li>
                    <li>Include a few inches depth if possible</li>
                    <li>Avoid shadows or glare</li>
                    <li>Capture the texture and color</li>
                </ul>
            </div>
            
            <div style="background-color: #F1F8E9; padding: 15px; border-radius: 10px;">
                <h4 style="color: #558B2F; margin-top: 0;">🌿 Why Soil Type Matters</h4>
                <ul style="margin-bottom: 0;">
                    <li>Determines water retention</li>
                    <li>Affects nutrient availability</li>
                    <li>Influences root development</li>
                    <li>Guides crop selection</li>
                    <li>Informs fertilization needs</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # Process the image for soil analysis if button clicked
        if analyze_button:
            if uploaded_file is not None:
                # Process the uploaded file
                image_bytes = uploaded_file.getvalue()
                process_soil_analysis(image_bytes)
            else:
                st.warning("Please upload an image first.")

    with tab2:
        st.markdown("### Soil Types Encyclopedia")

        # Display soil types information
        soil_types = {
            "Clay": {
                "image_url": "https://th.bing.com/th/id/OIP.ZDANIkyARHe04g1lXUYAvQAAAA?rs=1&pid=ImgDetMain",
                "description": "Clay soil is made up of very small particles that stick together. When wet, it becomes sticky and heavy; when dry, it becomes hard and can crack.",
                "characteristics": ["High in nutrients", "Slow draining", "Hard to work", "Warms slowly in spring"],
                "suitable_crops": ["Rice", "Wheat", "Cabbage", "Broccoli", "Brussels Sprouts"],
                "management": ["Add organic matter", "Add gypsum", "Avoid working when too wet or too dry"]
            },
            "Sandy": {
                "image_url": "https://th.bing.com/th/id/OIP.iO2zkFHOdmNx5UZGCkoETAHaE7?w=800&h=533&rs=1&pid=ImgDetMain",
                "description": "Sandy soil consists of large particles that allow for good drainage but poor nutrient retention. It feels gritty and doesn't hold its shape when squeezed.",
                "characteristics": ["Fast draining", "Low in nutrients", "Warms quickly in spring", "Easy to work"],
                "suitable_crops": ["Potatoes", "Carrots", "Radishes", "Lettuce", "Strawberries"],
                "management": ["Add organic matter", "Mulch well", "Water frequently", "Add fertilizer regularly"]
            },
            "Loamy": {
                "image_url": "https://s15485.pcdn.co/wp-content/uploads/2023/05/loamy-soil-with-a-rich-dark-color.jpg",
                "description": "Loam is the ideal garden soil, with a balanced mix of clay, sand, and organic material. It retains moisture but also drains well.",
                "characteristics": ["Well-draining", "High in nutrients", "Good structure", "Easy to work"],
                "suitable_crops": ["Most vegetables", "Corn", "Wheat", "Soybeans", "Most fruit trees"],
                "management": ["Maintain with compost", "Regular crop rotation", "Moderate watering"]
            },
            "Silty": {
                "image_url": "https://th.bing.com/th/id/OIP.gYamfO6nNV5XrkmQE47UiwHaE8?rs=1&pid=ImgDetMain",
                "description": "Silty soil feels smooth and silky when wet and has a floury texture when dry. It holds moisture well but can become compacted easily.",
                "characteristics": ["Good moisture retention", "Rich in nutrients", "Prone to compaction", "Moderate drainage"],
                "suitable_crops": ["Wetland plants", "Most vegetables", "Shrubs", "Fruit trees"],
                "management": ["Add organic matter", "Avoid stepping on soil", "Use cover crops"]
            },
            "Peaty": {
                "image_url": "https://img.freepik.com/premium-photo/peat-soil-planting-seedlings-flowers-ovary-closeup-natural-peat-from-swamps-selective-focus_330426-367.jpg?w=826",
                "description": "Peaty soil is dark, spongy and contains a high amount of organic material. It holds water well but can become water-repellent when dry.",
                "characteristics": ["High water retention", "Acidic", "High in organic matter", "Slow to warm in spring"],
                "suitable_crops": ["Blueberries", "Rhododendrons", "Azaleas", "Cranberries"],
                "management": ["Add lime to reduce acidity", "Improve drainage", "Add balanced fertilizers"]
            },
            "Chalky": {
                "image_url": "https://cdn.mos.cms.futurecdn.net/B5SaJnD3PJuNGCuCNvbgMh-1600-80.jpg",
                "description": "Chalky soil is alkaline and often contains visible chunks of white chalk or limestone. It drains quickly and can lack nutrients.",
                "characteristics": ["Fast draining", "Alkaline (high pH)", "Often shallow", "Warms quickly in spring"],
                "suitable_crops": ["Spinach", "Beets", "Cabbage family", "Some herbs"],
                "management": ["Add organic matter", "Use acidifying fertilizers", "Add iron supplements"]
            }
        }

        # Create a selectbox to choose soil type
        selected_soil = st.selectbox(
            "Select soil type to learn more",
            list(soil_types.keys())
        )

        # Display information about selected soil
        if selected_soil in soil_types:
            soil = soil_types[selected_soil]

            # Display in two columns
            col1, col2 = st.columns([1, 1])

            with col1:
                try:
                    st.image(soil["image_url"], caption=f"{selected_soil} Soil", use_container_width=True)
                except:
                    st.error("Image not available")

            with col2:
                st.markdown(f"### {selected_soil} Soil")
                st.markdown(f"**Description:** {soil['description']}")

                st.markdown("**Key Characteristics:**")
                for characteristic in soil["characteristics"]:
                    st.markdown(f"• {characteristic}")

                st.markdown("**Suitable Crops:**")
                for crop in soil["suitable_crops"]:
                    st.markdown(f"• {crop}")

                st.markdown("**Management Tips:**")
                for tip in soil["management"]:
                    st.markdown(f"• {tip}")

    with tab3:
        st.markdown("### Previous Analysis Results")

        # Show previous analysis results if available
        if "soil_analysis_history" in st.session_state and st.session_state.soil_analysis_history:
            for i, result in enumerate(st.session_state.soil_analysis_history):
                with st.expander(f"Analysis {i+1}: {result['soil_type']} ({result['timestamp']})"):
                    st.markdown(f"**Soil Type:** {result['soil_type']}")
                    st.markdown(f"**Confidence:** {result['confidence']:.1f}%")

                    if "characteristics" in result:
                        st.markdown("**Soil Characteristics:**")
                        for key, value in result["characteristics"].items():
                            if key != "suitable_crops" and key != "management_tips":
                                st.markdown(f"• **{key.replace('_', ' ').title()}:** {value}")

                        if "suitable_crops" in result["characteristics"]:
                            st.markdown("**Suitable Crops:**")
                            for crop in result["characteristics"]["suitable_crops"]:
                                st.markdown(f"• {crop}")

                        if "management_tips" in result["characteristics"]:
                            st.markdown("**Management Tips:**")
                            for tip in result["characteristics"]["management_tips"]:
                                st.markdown(f"• {tip}")
        else:
            st.info("No previous soil analysis results available. Upload a soil image to perform analysis.")


def process_soil_analysis(image_bytes):
    """
    Process image for soil analysis

    Args:
        image_bytes: Bytes of the image to analyze
    """
    try:
        with st.spinner("Analyzing soil image..."):
            # Add a slight delay to simulate processing
            time.sleep(1.5)

            # Make prediction using soil classifier
            results = soil_classifier.classify_soil(io.BytesIO(image_bytes))

            if results["success"]:
                predictions = results["predictions"]

                # Display top prediction
                top_prediction = predictions[0]
                confidence = top_prediction["confidence"]
                soil_type = top_prediction["soil_type"]
                soil_characteristics = results.get("soil_characteristics", {})

                # Display result in a visually appealing way
                st.markdown(f"""
                <div style="background-color: #2E7D32; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                    <h2 style="color: white; margin: 0;">Soil Analysis Result</h2>
                    <h1 style="color: white; margin: 10px 0; font-size: 36px;">{soil_type} Soil</h1>
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
                        alt_soil = pred["soil_type"]

                        st.markdown(f"""
                        <div style="background-color: #F1F8E9; padding: 10px; border-radius: 10px; text-align: center; height: 100%;">
                            <p style="font-weight: bold; margin-bottom: 5px;">{alt_soil} Soil</p>
                            <p>Confidence: {prob:.1f}%</p>
                        </div>
                        """, unsafe_allow_html=True)

                # Display soil characteristics info
                if soil_characteristics:
                    st.subheader("Soil Characteristics")

                    # Create two columns
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"""
                        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <h4 style="margin-top: 0;">Physical Properties</h4>
                            <p><strong>Texture:</strong> {soil_characteristics.get('texture', 'Not available')}</p>
                            <p><strong>Water Retention:</strong> {soil_characteristics.get('water_retention', 'Not available')}</p>
                            <p><strong>pH Tendency:</strong> {soil_characteristics.get('pH_tendency', 'Not available')}</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.markdown(f"""
                        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <h4 style="margin-top: 0;">Agricultural Value</h4>
                            <p><strong>Fertility:</strong> {soil_characteristics.get('fertility', 'Not available')}</p>
                            <p><strong>Suitable For:</strong> {', '.join(soil_characteristics.get('suitable_crops', ['Not available'])[:3])}...</p>
                        </div>
                        """, unsafe_allow_html=True)

                    # Show suitable crops with icons
                    st.subheader("Suitable Crops")
                    crop_cols = st.columns(3)

                    suitable_crops = soil_characteristics.get('suitable_crops', [])
                    crop_icons = {
                        "Rice": "🌾", "Wheat": "🌾", "Corn": "🌽", "Potatoes": "🥔",
                        "Carrots": "🥕", "Lettuce": "🥬", "Strawberries": "🍓",
                        "Blueberries": "🫐", "Cabbage": "🥬", "Broccoli": "🥦",
                        "Brussels Sprouts": "🥬", "Soybeans": "🫘", "Watermelon": "🍉"
                    }

                    for i, crop in enumerate(suitable_crops):
                        col_idx = i % 3
                        icon = crop_icons.get(crop, "🌱")
                        with crop_cols[col_idx]:
                            st.markdown(f"""
                            <div style="background-color: #F1F8E9; padding: 10px; border-radius: 10px; text-align: center; margin: 5px 0;">
                                <p style="font-size: 24px; margin: 5px 0;">{icon}</p>
                                <p style="font-weight: bold; margin: 5px 0;">{crop}</p>
                            </div>
                            """, unsafe_allow_html=True)

                    # Management tips in an expander
                    with st.expander("Soil Management Tips", expanded=True):
                        tips = soil_characteristics.get('management_tips', [])
                        for i, tip in enumerate(tips):
                            st.markdown(f"""
                            <div style="background-color: #F1F8E9; padding: 10px; border-radius: 10px; margin: 5px 0;">
                                <p style="margin: 0;"><strong>{i+1}.</strong> {tip}</p>
                            </div>
                            """, unsafe_allow_html=True)

                # Save analysis results to session state
                if "soil_analysis_history" not in st.session_state:
                    st.session_state.soil_analysis_history = []

                # Add current analysis to history
                analysis_record = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                    "soil_type": soil_type,
                    "confidence": confidence,
                    "characteristics": soil_characteristics
                }
                st.session_state.soil_analysis_history.insert(0, analysis_record)

                # Keep only the last 10 records
                if len(st.session_state.soil_analysis_history) > 10:
                    st.session_state.soil_analysis_history = st.session_state.soil_analysis_history[:10]

            else:
                st.error(f"Error during soil analysis: {results.get('error', 'Unknown error')}")
                st.info("Please try again with a clearer image of the soil.")

    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
        st.info("Please make sure the image is valid and try again.")

if __name__ == "__main__":
    show()
