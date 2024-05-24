import requests
from tkinter import Tk, Label, Entry, Button


def get_weather(city):
    api_key = "bc60a04d7d03b59ce5c84d3eae44ea49"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}"
    response = requests.get(complete_url)
    return response.json()


def show_weather():
    city = city_entry.get()
    weather = get_weather(city)
    if weather.get("cod") != "404":
        try:
            main = weather["main"]
            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            weather_desc = weather["weather"][0]["description"]
            weather_info = (
                f"Temperature: {temperature}K\n"
                f"Pressure: {pressure}hPa\n"
                f"Humidity: {humidity}%\n"
                f"Description: {weather_desc}"
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

show_button = Button(app, text="Show Weather", command=show_weather)
show_button.pack()

weather_label = Label(app, text="", font=("Helvetica", 14))
weather_label.pack()

app.mainloop()
