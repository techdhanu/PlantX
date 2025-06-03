import requests

def get_location_from_ip():
    """
    Get the user's location based on their IP address.
    Returns the user's city and country as a string.
    """
    try:
        # Using ipinfo.io to get location data from IP
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            city = data.get("city", "Unknown")
            region = data.get("region", "")
            country = data.get("country", "")

            # Construct location string
            if city != "Unknown":
                location = f"{city}, {country}"
                return location
            else:
                return "New Delhi, India"  # Default fallback
        else:
            return "New Delhi, India"  # Default fallback
    except Exception:
        return "New Delhi, India"  # Default fallback


def get_visualcrossing_weather(location, api_key):
    """
    Fetch weather data for given location (lat,lon or city name) from Visual Crossing API.
    Returns temperature (°C), rainfall (mm), and humidity (%) for today and forecast.
    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key=YTZ9ZL9DDNTZCPM6D8T77WGTL&contentType=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        today = data['days'][0]  # today's weather

        # Get current weather
        weather_info = {
            "temperature": today.get('temp', 0),      # average temperature in °C
            "rainfall": today.get('precip', 0),       # precipitation in mm
            "humidity": today.get('humidity', 0)      # humidity percentage
        }

        # Get forecast data for next 7 days
        forecast = []
        for i in range(0, 7):  # 0 is today, 1-7 are the next 7 days
            if i < len(data['days']):
                day = data['days'][i]
                forecast_day = {
                    "date": day.get('datetime', ''),
                    "temperature": day.get('temp', 0),
                    "tempMin": day.get('tempmin', 0),
                    "tempMax": day.get('tempmax', 0),
                    "rainfall": day.get('precip', 0),
                    "humidity": day.get('humidity', 0),
                    "conditions": day.get('conditions', ''),
                    "description": day.get('description', ''),
                    "icon": day.get('icon', 'cloudy')
                }
                forecast.append(forecast_day)

        # Add forecast to the response
        weather_info['forecast'] = forecast

        return weather_info
    else:
        raise Exception(f"Visual Crossing API error: {response.status_code} - {response.text}")


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


def geocode_location(place_name):
    """
    Convert a place name into latitude and longitude coordinates.
    Returns a tuple of (latitude, longitude) or None if geocoding fails.
    """
    try:
        # Using the free Nominatim geocoding service by OpenStreetMap
        url = f"https://nominatim.openstreetmap.org/search?q={place_name}&format=json&limit=1"
        headers = {'User-Agent': 'PlantX Climate Risk App'}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lat, lon)
            else:
                return None
        else:
            return None
    except Exception:
        return None

# For troubleshooting import issues
if __name__ == "__main__":
    print("API services module loaded successfully")
    print(f"Available functions: get_location_from_ip, get_visualcrossing_weather, get_soil_data, geocode_location")
