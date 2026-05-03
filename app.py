import streamlit as st
import requests

BACKEND_URL = "https://itinerary-generator-ax29.onrender.com"

st.title("AI Itinerary Generator")

destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
travel_style = st.text_input("Travel Style")
dietary_prefs = st.text_input("Dietary Preferences", placeholder="e.g., no raw shellfish")
budget = st.selectbox("Budget Level", ["budget", "mid-range", "luxury"])

if st.button("Generate Itinerary"):
    #Frontend validation
    if not destination.strip():
        st.error("Please enter a destination")
    elif not dietary_prefs.strip():
        st.error("Please enter your dietary preference")
    elif end_date <= start_date:
        st.error("End date must be after start date")
    else:
        try:
            with st.spinner("Building your itinerary..."):
                response=requests.post(f"{BACKEND_URL}/generate", json={
                    "destination": destination,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "travel_style": travel_style,
                    "dietary_prefs": dietary_prefs,
                    "budget": budget
                    },
                    timeout=120 # Give Groq up to 2 minutes to respond
                )
                if response.status_code == 200:
                    st.markdown(response.text)
                elif response.status_code == 422:
                    st.error("Invalid input. Please check your dates and fields")
                else:
                    st.error(f"Something went wrong. Please try again. (Error: {response.status_code})")
        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend. Make sure uvicorn is running")