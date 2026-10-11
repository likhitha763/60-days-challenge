"""
Global Weather Intelligence Client (APIs)
=========================================
Phase: APIs

Description:
A global weather agency needs a smart dashboard to fetch and display live weather 
reports from cities worldwide. This script communicates with public REST APIs, 
parses JSON responses, handles network failures gracefully, and presents clean, 
formatted weather insights.

Real-World Impact:
- Modern Architecture: APIs enable seamless communication between decoupled cloud systems.
- Enterprise Integrations: Powering travel booking apps, logistics tracking, and IoT dashboards.
"""

import urllib.request
import urllib.error
import json

def get_city_coordinates(city_name: str) -> tuple[float, float, str] | None:
    """
    Fetches latitude and longitude for a given city name using the Open-Meteo Geocoding API.
    Returns (latitude, longitude, formatted_name) or None if not found or API fails.
    """
    formatted_city = city_name.strip().title()
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.request.quote(formatted_city)}&count=1&language=en&format=json"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'WeatherIntelligenceClient/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get('results')
            
            if not results:
                print(f"[API WARNING] City '{formatted_city}' could not be located.")
                return None
                
            match = results[0]
            lat = match.get('latitude')
            lon = match.get('longitude')
            country = match.get('country', 'Unknown Country')
            name = match.get('name', formatted_city)
            
            return lat, lon, f"{name}, {country}"
            
    except urllib.error.URLError as e:
        print(f"[NETWORK ERROR] Failed to connect to geocoding service: {e.reason}")
        return None
    except json.JSONDecodeError:
        print("[PARSING ERROR] Failed to decode JSON response from geocoding API.")
        return None
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        return None


def fetch_live_weather(city_name: str):
    """
    Coordinates geocoding and live weather fetching, parses JSON, 
    and displays a formatted summary with robust error handling.
    """
    print(f"\n--- Fetching Weather Report for: {city_name} ---")
    
    # Step 1: Get coordinates for the city
    location_data = get_city_coordinates(city_name)
    if not location_data:
        print(f"[STATUS] Could not retrieve weather for '{city_name}' due to lookup failure.")
        return
        
    lat, lon, location_string = location_data
    
    # Step 2: Fetch current weather forecast
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    
    try:
        req = urllib.request.Request(
            weather_url, 
            headers={'User-Agent': 'WeatherIntelligenceClient/1.0'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            weather_data = json.loads(response.read().decode('utf-8'))
            current = weather_data.get('current_weather')
            
            if not current:
                print(f"[DATA ERROR] Weather metrics unavailable for {location_string}.")
                return
                
            temperature = current.get('temperature')
            windspeed = current.get('windspeed')
            winddirection = current.get('winddirection')
            weathercode = current.get('weathercode')
            time_recorded = current.get('time')
            
            # Map weather codes to readable descriptions (WMO Weather interpretation)
            condition = interpret_weather_code(weathercode)
            
            # Step 3: Display formatted summary
            print(f"========================================")
            print(f" 🌍 LOCATION: {location_string}")
            print(f" 🌡️  TEMPERATURE: {temperature}°C")
            print(f" ☁️  CONDITION:   {condition} (Code: {weathercode})")
            print(f" 💨 WIND SPEED:  {windspeed} km/h (Dir: {winddirection}°)")
            print(f" ⏱️  TIMESTAMP:   {time_recorded}")
            print(f"========================================")
            
    except urllib.error.HTTPError as e:
        print(f"[HTTP ERROR] Server returned status {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"[NETWORK ERROR] Connection failed: {e.reason}. Please check your internet connection.")
    except json.JSONDecodeError:
        print("[PARSING ERROR] Malformed JSON received from weather API.")
    except Exception as e:
        print(f"[SYSTEM ERROR] An unexpected error occurred: {e}")


def interpret_weather_code(code: int) -> str:
    """Translates WMO weather codes into human-readable descriptions."""
    weather_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        71: "Slight snow fall",
        95: "Thunderstorm"
    }
    return weather_map.get(code, "Variable / Fair")


# --- Execution and Testing Suite ---
if __name__ == "__main__":
    print("=== GLOBAL WEATHER INTELLIGENCE DASHBOARD ===")
    
    # List of test cities to query via live public APIs
    target_cities = ["Tokyo", "London", "New York", "Bengaluru", "NonExistentCity123"]
    
    for city in target_cities:
        fetch_live_weather(city)


"""
--- LINKEDIN REFLECTION ---
Post Title: Connecting Systems: Building a Live Weather Intelligence Client 🌐⛅

APIs are the invisible glue of modern software engineering. They allow independent systems, 
servers, and microservices to talk to each other in milliseconds. Today, for the ABTalks 
Challenge, I built a Weather Intelligence Client in Python that connects to public REST APIs 
without relying on external dependencies.

Key engineering highlights of today's build:
1. Zero-Key Public API Integration: Leveraging Open-Meteo's geocoding and forecast endpoints.
2. Robust JSON Parsing & Mapping: Extracting raw metrics and translating WMO weather codes into readable summaries.
3. Graceful Error Handling: Implementing robust try-except blocks for HTTP errors, network timeouts, and invalid city lookups to prevent app crashes.

Whether you're building financial dashboards, payment gateways, or AI wrapper tools, mastering API integration and fault tolerance is non-negotiable!

#SoftwareEngineering #APIs #Python #BackendDevelopment #CloudComputing #CodingJourney
"""
