import requests

def get_visualcrossing_weather(location, api_key):
    """
    Fetch weather data for given location (lat,lon or city name) from Visual Crossing API.
    Returns temperature (°C), rainfall (mm), and humidity (%).
    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key=YTZ9ZL9DDNTZCPM6D8T77WGTL&contentType=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        today = data['days'][0]  # today's weather
        weather_info = {
            "temperature": today.get('temp', 0),      # average temperature in °C
            "rainfall": today.get('precip', 0),       # precipitation in mm
            "humidity": today.get('humidity', 0)      # humidity percentage
        }
        return weather_info
    else:
        raise Exception(f"Visual Crossing API error: {response.status_code} - {response.text}")


import requests


def get_soil_data(lat, lon):
    """
    Fetch soil data from the updated SoilGrids REST API v2.0.
    Returns pH, organic carbon, clay, sand, and silt from topsoil layer (0-5cm).
    """
    url = (
        f"https://rest.isric.org/soilgrids/v2.0/properties/query?"
        f"lon={lon}&lat={lat}&property=phh2o&property=ocd&property=clay&property=sand&property=silt&depth=0-5cm"
    )

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        props = data.get("properties", {})

        def extract_value(prop):
            try:
                return prop["layers"][0]["values"]["mean"]
            except:
                return None

        soil_info = {
            "ph": extract_value(props.get("phh2o", {})),
            "organic_carbon": extract_value(props.get("ocd", {})),
            "clay": extract_value(props.get("clay", {})),
            "sand": extract_value(props.get("sand", {})),
            "silt": extract_value(props.get("silt", {})),
        }
        return soil_info
    else:
        raise Exception(f"SoilGrids API error: {response.status_code} - {response.text}")
