import requests
import json

OPENWEATHER_URL_CURRENT = 'http://api.openweathermap.org/data/2.5/weather'
OPENWEATHER_URL_FORECAST = 'http://api.openweathermap.org/data/2.5/forecast'

class Location(object):
    def __init__(self, current_weather_data):
        self.lon = current_weather_data['coord']['lon']
        self.lat = current_weather_data['coord']['lat']
        self.country = current_weather_data['sys']['country']
        self.city = current_weather_data['name']

class Access(object):
    def __init__(self, api_key, units):
        self.units = units
        self.api_key = api_key

        self.params = {
                'APPID' : api_key,
                'q' : 'Prague',
                'units' : units
        }

    def request_current_data(self, location):
        self.params['q'] = location

        request = requests.get(OPENWEATHER_URL_CURRENT, params = self.params)

        json_data = request.json()
        location = Location(json_data)
        return json_data, location

    def request_forecast_data(self, location):
        self.params['q'] = location

        request = requests.get(OPENWEATHER_URL_FORECAST, params = self.params)
        json_data = request.json()

        return json_data
        
