from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)
def convert_utc_to_ist(utc_time_str):
    # Parse UTC time string to datetime object
    utc_time = datetime.strptime(utc_time_str, "%H:%M")
    
    # Add 5 hours and 30 minutes to convert to IST
    ist_time = utc_time + timedelta(hours=5, minutes=30)
    
    # Format IST time as HH:MM string
    ist_time_str = ist_time.strftime("%H:%M")
    
    return ist_time_str

def get_weather_data(city, country):
    url = "https://api.weatherbit.io/v2.0/current"
    params = {
        "key": "0249bb0f331f4fcc851919a5d3deef78",
        "lang": "en",
        "units": "M",
        "city": city,
        "country": country
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
    return response.json()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the form is submitted, get the city from the form data
        city = request.form['city']
        country = 'IN'  # Assuming the country is always India for this example
    else:
        # If the page is first loaded, use default city
        city = 'Sehore'
        country = 'IN'

    try:
        # Fetch weather data based on the provided city
        weather_data = get_weather_data(city, country)

        # Extracting required stats from API response
        required_stats = {
            'app_temp': weather_data['data'][0]['app_temp'],
            'aqi': weather_data['data'][0].get('aqi', None),
            'city_name': weather_data['data'][0]['city_name'],
            'country_code': weather_data['data'][0]['country_code'],
            'datetime': weather_data['data'][0]['ob_time'],
            'lat': weather_data['data'][0]['lat'],
            'lon': weather_data['data'][0]['lon'],
            'sunrise': convert_utc_to_ist(weather_data['data'][0]['sunrise']),
            'sunset': convert_utc_to_ist(weather_data['data'][0]['sunset']),
            'temp': weather_data['data'][0]['temp'],
            'timezone': weather_data['data'][0]['timezone'],
            'weather': {'description': weather_data['data'][0]['weather']['description']},
            'wind_cdir_full': weather_data['data'][0]['wind_cdir_full'],
            'wind_spd': weather_data['data'][0]['wind_spd'],
            'rh': weather_data['data'][0]['rh'],
        }

        return render_template('index.html', weather_data=required_stats)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run()