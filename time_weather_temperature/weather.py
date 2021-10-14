import requests
import time
import json

api_key = "d563c8e8cb8c162ebd6b8898f7b93b74"


class Weather(object):
    def __init__(self, api_credentials):
        self.api_key = api_credentials
        self.base_url = "https://api.openweathermap.org"

    def construct_one_call_query(self, latitude, longitude, exclude):
        """
        Documentation: https://openweathermap.org/api/one-call-api
        Return: Returns the constructed url for one-call
        """
        api_subscribed = "/data/2.5/onecall?"
        if exclude == "":
            query = f"lat={latitude}&lon={longitude}&appid={self.api_key}"
        else:
            query = f"lat={latitude}&lon={longitude}&exclude={exclude}&appid={self.api_key}"

        url = f"{self.base_url}{api_subscribed}{query}"

        return url

    def construct_weather_data_query(self, city):
        """
        Documentation: https://openweathermap.org/current
        Return: Returns the constructed url of current weather data of the city
        """
        api_subscribed = "/data/2.5/weather?"
        query = f"q={city}&appid={self.api_key}"
        url = f"{self.base_url}{api_subscribed}{query}"

        return url

    def convert_to_celsius(self, kelvin):
        celsius = round((kelvin - 273.15), 2)
        # celsius = (fahrenheit - 32) * 5.0 / 9.0
        return celsius

    def get_time(self, epoch):
        time_conv = time.strftime('%H:%M:%S', time.localtime(epoch))
        return time_conv

    def get_date(self, epoch):
        date_conv = time.strftime('%d-%m-%Y', time.localtime(epoch))
        return date_conv

    def get_weather_info(self, api_selected, lat=None, lon=None, city_name=None):
        if api_selected == "one_call":
            url = self.construct_one_call_query(latitude=lat, longitude=lon, exclude='minutely,hourly')
        elif api_selected == "current_weather":
            url = self.construct_weather_data_query(city=city)
        else:
            raise("select the right api...")
        resp = requests.post(url)
        print("Response Code: ", resp.status_code)
        data = json.loads(resp.text)
        print(data)
        print("\n")
        print("Date: ", data["dt"])
        print("Date Converted: ", self.get_date(epoch=data["dt"]))
        print("City Name: ", data['name'])
        print("Weather: ", data["weather"])
        print("Co-ordinates: ", data["coord"])
        print("Weather: ", data["weather"][0]["main"])
        print("Temperature: ", data["main"]["temp"])
        print("Temperature in Celsius: ", self.convert_to_celsius(kelvin=data["main"]["temp"]))
        print("Min Temp: ", data["main"]["temp_min"])
        print("Max Temp: ", data["main"]["temp_max"])
        print("Wind: ", data["wind"])
        print("System: ", data["sys"])
        print("System: ", data["sys"]["sunrise"])
        print("System: ", data["sys"]["sunset"])
        print("Epoch converted: ", self.get_time(epoch=data["sys"]["sunset"]))

weather_obj = Weather(api_credentials=api_key)
api_sel = "current_weather"
city = "Chennai"
weather_obj.get_weather_info(api_selected=api_sel, city_name=city)
