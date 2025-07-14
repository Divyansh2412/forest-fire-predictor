import requests
from datetime import datetime

def fetch_weather_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,precipitation,windspeed_10m&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max&timezone=auto"
    response = requests.get(url)
    data = response.json()

    # Get index for current hour
    current_time = datetime.now().strftime('%Y-%m-%dT%H:00')
    hourly_time_index = data['hourly']['time'].index(current_time)

    weather = {
        'current_temp': data['hourly']['temperature_2m'][hourly_time_index],
        'humidity': float(data['hourly']['relative_humidity_2m'][hourly_time_index]),
        'precipitation': data['hourly']['precipitation'][hourly_time_index],
        'windspeed': data['hourly']['windspeed_10m'][hourly_time_index],
        'max_temp': data['daily']['temperature_2m_max'][0],
        'min_temp': data['daily']['temperature_2m_min'][0],
        'avg_temp': (data['daily']['temperature_2m_max'][0] + data['daily']['temperature_2m_min'][0]) / 2,
    }

    return weather


def predict_fire_risk(weather):
    temp_score = (weather['avg_temp'] - 10) * 2
    wind_score = weather['windspeed']
    humidity_score = 100 - weather['humidity']
    precip_score = -weather['precipitation'] * 10

    fire_risk = temp_score + wind_score + humidity_score + precip_score
    return max(0, min(100, round(fire_risk, 2)))