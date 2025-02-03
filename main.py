from dotenv import load_dotenv
import os
import google.generativeai as genai
import streamlit as st

load_dotenv(override=True)
API_KEY = os.getenv('API_KEY')

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_itinerary(destination):
    res = model.generate_content(f"Give me a 3-day travel itinerary for {destination}")
    return res.text

st.title("Travel Itinerary Generator")

destination = st.text_input("Enter Destination: ")

if st.button("Get Itinerary"):
    if destination:
        itinerary = generate_itinerary(destination)
        st.markdown(itinerary)
    else:
        st.warning("Please enter a destination.")
