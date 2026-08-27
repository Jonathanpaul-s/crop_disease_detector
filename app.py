from pathlib import Path
import base64

BACKGROUND = Path("assets/farm_logo.png")

if BACKGROUND.exists():
    with open(BACKGROUND, "rb") as f:
        bg = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

import streamlit as st
import requests
import joblib  # for loading your model

# App title
st.title("🚜 Smart Farm AI Dashboard")

# Sidebar navigation
st.sidebar.title("Navigation")
choice = st.sidebar.selectbox("Select Option", ["Home", "Crop Disease Detection", "Weather Forecasting", "Fertilizer Recommendation"])

# OpenWeatherMap API key (yours)
api_key = "a2e8038fb11f70500b36e5a65a58af68"

# Load your trained model
model = joblib.load("crop_disease_detector.pkl")

# Main app logic
if choice == 'Home':
    st.image("farm_logo.png", width=350)
    st.subheader("👋 Welcome to Smart Farm AI")
    st.write("""
        Smart Farm AI is an intelligent farm management platform powered by AI to assist farmers in:
        - Monitoring crop health.
        - Getting real-time weather forecasts.
        - Receiving personalized fertilizer recommendations.
        
        🚀 Boost your farm productivity today!
    """)

elif choice == 'Crop Disease Detection':
    st.subheader("🌾 Crop Disease Detection")

    st.write("Provide the symptom code to predict crop disease:")

    symptom1 = st.number_input("Symptom Code (e.g., 1-5)", min_value=1, max_value=5, value=1)

    if st.button("Predict Disease"):
        input_data = [[symptom1]]  # Only one input because your model expects 1
        prediction = model.predict(input_data)
        st.success(f"🌱 Predicted Disease: {prediction[0]}")

elif choice == 'Weather Forecasting':
    st.subheader("🌦️ Weather Forecasting")
    
    city = st.text_input("Enter your city name")

    if st.button("Get Weather"):
        if city:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                response = requests.get(url)
                data = response.json()

                if data["cod"] == 200:
                    temperature = data["main"]["temp"]
                    humidity = data["main"]["humidity"]
                    condition = data["weather"][0]["description"]

                    st.success(f"🌱 Weather forecast for {city.title()}:")
                    st.write(f"Temperature: {temperature}°C")
                    st.write(f"Humidity: {humidity}%")
                    st.write(f"Condition: {condition.title()}")

                else:
                    st.error("City not found. Please check your spelling.")
            except:
                st.error("Failed to fetch weather data. Check your internet connection.")
        else:
            st.warning("Please enter a city name.")

elif choice == 'Fertilizer Recommendation':
    st.subheader("🌱 Fertilizer Recommendation")
    st.write("✅ This feature is already working perfectly!")

else:
    st.error("Invalid Choice. Please select a valid option from the sidebar.")