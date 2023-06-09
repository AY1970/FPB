import requests

# Function to get weather information
def get_weather_info(place_name):
    location_url = "https://geocoding-api.open-meteo.com/v1/search"
    weather_url = "https://api.open-meteo.com/v1/forecast"

    try:
        location_params = {"name": place_name}
        location_response = requests.get(location_url, params=location_params)

        if location_response.status_code != 200:
            return f"Error getting location data for {place_name}. Status code: {location_response.status_code}"

        location_data = location_response.json()
        latitude = location_data["results"][0]["latitude"]
        longitude = location_data["results"][0]["longitude"]

    except (KeyError, IndexError):
        return "Input Error. Please enter a valid place."

    weather_params = {"latitude": latitude, "longitude": longitude, "current_weather": True}
    weather_response = requests.get(weather_url, params=weather_params)

    if weather_response.status_code != 200:
        return f"Error getting weather data for {place_name}. Status code: {weather_response.status_code}"

    weather_data = weather_response.json()
    temperature = weather_data.get("current_weather", {}).get("temperature", None)

    if temperature is None:
        return "Error getting weather data."

    return f"Current weather for {place_name}:\nTemperature: {temperature}°C"