import requests
from tkinter import Tk, Label, Entry, Button, StringVar, Frame, Canvas
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
from io import BytesIO  # Import BytesIO

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
            icon_code = weather["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            temperature_unit = "C" if unit == "Celsius" else "F"
            temperature = main["temp"]
            feels_like = main["feels_like"]
            temp_min = main["temp_min"]
            temp_max = main["temp_max"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            wind_speed = wind["speed"]
            wind_deg = wind.get("deg", 0)
            visibility = weather.get("visibility", 0)
            cloudiness = weather["clouds"]["all"]
            sunrise = datetime.utcfromtimestamp(sys["sunrise"]).strftime('%Y-%m-%d %H:%M:%S')
            sunset = datetime.utcfromtimestamp(sys["sunset"]).strftime('%Y-%m-%d %H:%M:%S')

            weather_info = (
                f"Weather: {weather_desc.capitalize()}\n"
                f"Temperature: {temperature}°{temperature_unit} (Feels like: {feels_like}°{temperature_unit})\n"
                f"Min/Max Temperature: {temp_min}°{temperature_unit}/{temp_max}°{temperature_unit}\n"
                f"Pressure: {pressure} hPa\n"
                f"Humidity: {humidity}%\n"
                f"Wind: {wind_speed} m/s at {wind_deg}°\n"
                f"Visibility: {visibility} m\n"
                f"Cloudiness: {cloudiness}%\n"
                f"Sunrise: {sunrise} UTC\n"
                f"Sunset: {sunset} UTC"
            )

            weather_label.config(text=weather_info)
            display_weather_icon(icon_url)

        except KeyError as e:
            weather_info = f"Key error: {e}. Response was: {weather}"
            weather_label.config(text=weather_info)
    else:
        weather_info = "City Not Found!"
        weather_label.config(text=weather_info)

def display_weather_icon(icon_url):
    response = requests.get(icon_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    icon_canvas.create_image(50, 50, anchor='center', image=img)
    icon_canvas.image = img

app = Tk()
app.title("Weather App")
app.geometry("600x600")

# Set background color
app.configure(bg="#282C34")

style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 14), background="#282C34", foreground="#FFFFFF")
style.configure("TButton", font=("Helvetica", 14), background="#61AFEF", foreground="#FFFFFF")

frame = ttk.Frame(app, padding="10", style="TFrame")
frame.pack(fill="both", expand=True)

city_label = ttk.Label(frame, text="City Name:")
city_label.pack(pady=5)

city_entry = ttk.Entry(frame, font=("Helvetica", 14))
city_entry.pack(pady=5)

unit_var = StringVar(app)
unit_var.set("Celsius")  # default value

unit_label = ttk.Label(frame, text="Select Temperature Unit:")
unit_label.pack(pady=5)

unit_menu = ttk.OptionMenu(frame, unit_var, "Celsius", "Fahrenheit")
unit_menu.pack(pady=5)

show_button = ttk.Button(frame, text="Show Weather", command=show_weather)
show_button.pack(pady=10)

weather_label = ttk.Label(frame, text="", font=("Helvetica", 14), wraplength=500)
weather_label.pack(pady=10)

icon_canvas = Canvas(frame, width=100, height=100, bg="#282C34", highlightthickness=0)
icon_canvas.pack(pady=10)

app.mainloop()
