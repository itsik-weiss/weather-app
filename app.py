from flask import Flask, jsonify, render_template_string, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #00b4d8, #0077b6);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 400px;
            width: 100%;
        }
        h1 {
            color: #1d3557;
            margin-bottom: 20px;
        }
        .weather-icon {
            width: 100px;
            height: 100px;
            margin: 20px 0;
        }
        .temperature {
            font-size: 48px;
            color: #1d3557;
            margin: 10px 0;
        }
        .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
            text-align: left;
        }
        .detail-item {
            background: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .detail-icon {
            width: 24px;
            height: 24px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ city }}</h1>
        <img src="{{ weather_icon }}" alt="Weather Icon" class="weather-icon">
        <div class="temperature">{{ temperature }}°C</div>
        <p>{{ description }}</p>
        <div class="details">
            <div class="detail-item">
                <img src="https://cdn-icons-png.flaticon.com/512/2011/2011448.png" class="detail-icon" alt="Wind">
                <span>Wind: {{ wind_speed }} km/h</span>
            </div>
            <div class="detail-item">
                <img src="https://cdn-icons-png.flaticon.com/512/728/728093.png" class="detail-icon" alt="Humidity">
                <span>Humidity: {{ humidity }}%</span>
            </div>
        </div>
    </div>
</body>
</html>
"""

def get_weather_icon(code):
    # Weather code to icon mapping
    icons = {
        0: "https://cdn-icons-png.flaticon.com/512/6974/6974833.png",  # Clear sky
        1: "https://cdn-icons-png.flaticon.com/512/1163/1163661.png",  # Mainly clear
        2: "https://cdn-icons-png.flaticon.com/512/1146/1146869.png",  # Partly cloudy
        3: "https://cdn-icons-png.flaticon.com/512/1146/1146858.png",  # Overcast
        45: "https://cdn-icons-png.flaticon.com/512/4005/4005901.png",  # Foggy
        48: "https://cdn-icons-png.flaticon.com/512/4005/4005901.png",  # Rime fog
        51: "https://cdn-icons-png.flaticon.com/512/3351/3351979.png",  # Light drizzle
        53: "https://cdn-icons-png.flaticon.com/512/3351/3351979.png",  # Drizzle
        55: "https://cdn-icons-png.flaticon.com/512/3351/3351979.png",  # Heavy drizzle
        61: "https://cdn-icons-png.flaticon.com/512/3351/3351979.png",  # Light rain
        63: "https://cdn-icons-png.flaticon.com/512/3351/3351979.png",  # Rain
        65: "https://cdn-icons-png.flaticon.com/512/3351/3351979.png",  # Heavy rain
        71: "https://cdn-icons-png.flaticon.com/512/642/642000.png",    # Snow
        73: "https://cdn-icons-png.flaticon.com/512/642/642000.png",    # Snow
        75: "https://cdn-icons-png.flaticon.com/512/642/642000.png",    # Heavy snow
        95: "https://cdn-icons-png.flaticon.com/512/3351/3351983.png",  # Thunderstorm
    }
    return icons.get(code, icons[0])

def get_weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        95: "Thunderstorm"
    }
    return descriptions.get(code, "Unknown")

@app.route('/api/weather', methods=['GET'])
@app.route('/', methods=['GET'])
def get_weather():
    try:
        # Get city name from environment variable
        city = os.getenv('CITY_NAME', 'Jerusalem')  # Default to Jerusalem if not set
        if not city:
            return jsonify({'error': 'City name not set in environment variables'}), 400

        # Step 1: Get coordinates for the city using Open-Meteo's Geocoding API
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geocode_url)
        geo_data = geo_response.json()

        if not geo_data.get('results'):
            return jsonify({'error': 'City not found'}), 404

        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']

        # Step 2: Get weather data using Open-Meteo's Weather API
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        # Step 3: Extract relevant weather information
        current_weather = weather_data['current']
        weather_code = current_weather['weather_code']
        
        response_data = {
            'city': city,
            'temperature': round(current_weather['temperature_2m']),
            'wind_speed': round(current_weather['wind_speed_10m']),
            'humidity': round(current_weather['relative_humidity_2m']),
            'weather_code': weather_code,
            'description': get_weather_description(weather_code),
            'weather_icon': get_weather_icon(weather_code)
        }

        # Return HTML for browser requests, JSON for API requests
        if request.headers.get('accept') == 'application/json':
            return jsonify(response_data)
        return render_template_string(HTML_TEMPLATE, **response_data)

    except Exception as e:
        error_message = str(e)
        if request.headers.get('accept') == 'application/json':
            return jsonify({'error': error_message}), 500
        return f"<h1>Error</h1><p>{error_message}</p>", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
