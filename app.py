from flask import Flask, render_template, request
from fire_model import fetch_weather_data, predict_fire_risk
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    city_data = pd.read_csv("locations.csv")

    city_data.rename(columns={'city': 'City', 'lat': 'Latitude', 'lng': 'Longitude'}, inplace=True)

    city_list = city_data.to_dict(orient='records')

    return render_template('index.html', city_list=city_list)

@app.route('/predict', methods=['POST'])
def predict():
    lat = float(request.form['latitude'])
    lon = float(request.form['longitude'])

    weather = fetch_weather_data(lat, lon)
    if weather is None:
        return render_template('result.html', error="Weather data not available for given coordinates.")

    fire_prob = predict_fire_risk(weather)
    return render_template('result.html', weather=weather, fire_prob=fire_prob)

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    