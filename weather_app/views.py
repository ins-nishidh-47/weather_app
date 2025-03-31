from django.shortcuts import render, redirect
import requests
from .models import City

API_KEY = "438c255e9c8d7763e12016f83efe73d4"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

def index(request):
    if request.method == "POST":
        city_name = request.POST["city"]
        if city_name:
            City.objects.get_or_create(name=city_name)
        return redirect("index")

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(WEATHER_URL.format(city.name, API_KEY)).json()
        print(response)
        if response.get("cod") != 200:
            continue  # Skip invalid cities

        weather_info = {
            "city": city.name,
            "temperature": response["main"]["temp"],
            "feels_like": response["main"]["feels_like"],
            "humidity": response["main"]["humidity"],
            "wind_speed": response["wind"]["speed"],
            "description": response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"],
        }
        weather_data.append(weather_info)

    return render(request, "weather_app/index.html", {"weather_data": weather_data, "cities": cities})

def delete_city(request, city_name):
    City.objects.filter(name=city_name).delete()
    return redirect("index")
