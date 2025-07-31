# Weather App

A beautiful weather application that displays current weather conditions for any city. Built with Python Flask and featuring a modern, responsive UI.

![Weather App Screenshot](https://github.com/itsik-weiss/weather-app/raw/main/screenshot.png)

## Features

- 🌡️ Real-time weather data
- 🏙️ City-based weather lookup
- 🎨 Beautiful, responsive UI
- 📊 Detailed weather information including:
  - Temperature
  - Wind speed
  - Humidity
  - Weather conditions
- 🐳 Docker support

## Quick Start

### Running Locally

1. Clone the repository:
```bash
git clone https://github.com/itsik-weiss/weather-app.git
cd weather-app
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file to set your preferred city
```

5. Run the application:
```bash
python app.py
```

6. Open in your browser:
```
http://localhost:3000
```

## Environment Variables

1. CITY_NAME 

### Using Docker

1. Build the image:
```bash
docker build -t weather-app .
```

2. Run the container:
```bash
docker run -p 3000:3000 weather-app
```

3. Build with a custom city:
```bash
docker build --build-arg CITY_NAME=paris -t weather-app .
```

### Docker Compose

Run the application:
```bash
docker-compose up
```

With a custom city:
```bash
CITY_NAME=london docker-compose up
```

### Docker Testing

Run tests in Docker:
```bash
docker build -f Dockerfile.test -t weather-app-test .
docker run weather-app-test
```

## API Endpoint

The application provides a JSON API endpoint:

```
GET /api/weather
```

Example response:
```json
{
    "city": "Kuwait",
    "temperature": 42,
    "wind_speed": 15,
    "humidity": 30,
    "weather_code": 1,
    "description": "Clear sky"
}
```

## Technologies Used

- Python 3.9
- Flask
- Open-Meteo API
- Docker
- HTML5/CSS3

## Testing

Simple tests to check if the app works correctly.

### Running Tests

Run the basic tests:
```bash
python simple_test.py
```

### Test Coverage

The tests check:
- ✅ Weather icon mapping
- ✅ Weather description mapping
- ✅ Basic API response
- ✅ Error handling for invalid cities
