from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st
import requests

load_dotenv(override=True)
API_KEY = os.getenv('API_KEY')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def get_weather(destination):
    weather_api_key = os.getenv('WEATHER_API_KEY')
    url = f"http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={destination}&days=3"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        forecast = data.get("forecast", {}).get("forecastday", [])
        weather_info = "\n".join([f"Day {i+1}: {day['day']['condition']['text']}, Temp: {day['day']['avgtemp_c']}°C" for i, day in enumerate(forecast)])
        return weather_info
    return "Weather data not available."

def generate_itinerary(destination):
    weather = get_weather(destination)
    res = model.generate_content(f"Give me a 3-day travel itinerary for {destination}. Also consider the following weather conditions: {weather}")
    return res.text

st.title("Travel Itinerary Generator")

destination = st.text_input("Enter Destination: ")

if st.button("Get Itinerary"):
    if destination:
        itinerary = generate_itinerary(destination)
        st.markdown(itinerary)
    else:
        st.warning("Please enter a destination.")
