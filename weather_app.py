import requests
from tkinter import Tk, Label, Entry, Button, StringVar, OptionMenu
from datetime import datetime

def get_weather(city, unit):
    api_key = "bc60a04d7d03b59ce5c84d3eae44ea49"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    units = "metric" if unit == "Celsius" else "imperial"
    complete_url = f"{base_url}q={city}&appid={api_key}&units={units}"
    response = requests.get(complete_url)
    return response.json()

def show_weather():
    city = city_entry.get()
    unit = unit_var.get()
    weather = get_weather(city, unit)
    if weather.get("cod") != "404":
        try:
            main = weather["main"]
            wind = weather["wind"]
            sys = weather["sys"]
            weather_desc = weather["weather"][0]["description"]
            temperature_unit = "C" if unit == "Celsius" else "F"
            temperature = main["temp"]
            feels_like = main["feels_like"]
            temp_min = main["temp_min"]
            temp_max = main["temp_max"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]
            visibility = weather.get("visibility", 0)
            cloudiness = weather["clouds"]["all"]
            sunrise = datetime.utcfromtimestamp(sys["sunrise"]).strftime('%Y-%m-%d %H:%M:%S')
            sunset = datetime.utcfromtimestamp(sys["sunset"]).strftime('%Y-%m-%d %H:%M:%S')

            weather_info = (
                f"Weather: {weather_desc.capitalize()}\n"
                f"Temperature: {temperature}°{temperature_unit} (Feels like: {feels_like}°{temperature_unit})\n"
                f"Min/Max Temperature: {temp_min}°{temperature_unit}/{temp_max}°{temperature_unit}\n"
                f"Humidity: {humidity}%\n"
                f"Wind: {wind_speed} m/s\n"
                f"Visibility: {visibility} m\n"
                f"Cloudiness: {cloudiness}%\n"
                f"Sunrise: {sunrise} UTC\n"
                f"Sunset: {sunset} UTC"
            )
        except KeyError as e:
            weather_info = f"Key error: {e}. Response was: {weather}"
    else:
        weather_info = "City Not Found!"
    weather_label.config(text=weather_info)

app = Tk()
app.title("Weather App")

city_label = Label(app, text="City Name:")
city_label.pack()

city_entry = Entry(app)
city_entry.pack()

unit_var = StringVar(app)
unit_var.set("Celsius")  # default value

unit_label = Label(app, text="Select Temperature Unit:")
unit_label.pack()

unit_menu = OptionMenu(app, unit_var, "Celsius", "Fahrenheit")
unit_menu.pack()

show_button = Button(app, text="Show Weather", command=show_weather)
show_button.pack()

weather_label = Label(app, text="", font=("Helvetica", 14))
weather_label.pack()

app.mainloop()
