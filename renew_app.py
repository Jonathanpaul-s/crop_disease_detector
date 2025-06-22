<<<<<<< HEAD
import streamlit as st
import numpy as np
import joblib

# Load the model
try:
    model = joblib.load("new_crop_disease_detector.pkl")
except FileNotFoundError:
    st.error("❌ Model file not found! Make sure 'new_crop_disease_detector.pkl' is in the same folder.")
    st.stop()

# Disease descriptions and tips
disease_info = {
    "Bacterial": {
        "description": "Caused by harmful bacteria that infect plant tissues and block nutrient flow.",
        "tips": "Use copper-based bactericides. Ensure good air circulation and avoid overhead watering."
    },
    "Fungal": {
        "description": "Triggered by fungal spores, often due to wet leaves and humid environments.",
        "tips": "Apply recommended fungicides. Avoid overwatering and prune affected leaves."
    },
    "Viral": {
        "description": "Viruses are spread through insect carriers or infected tools.",
        "tips": "Remove infected plants early. Control insect pests like aphids and whiteflies."
    },
    "Healthy": {
        "description": "The plant shows no visible symptoms of disease.",
        "tips": "Keep monitoring and continue good farming practices."
    }
}

# App title
st.title("🌾 Crop Disease Detection AI")
st.write("Enter your crop's environmental conditions below:")

# Set default values in session_state
if "temperature" not in st.session_state:
    st.session_state.temperature = 25.0
if "humidity" not in st.session_state:
    st.session_state.humidity = 50.0
if "moisture" not in st.session_state:
    st.session_state.moisture = 30.0

# Input fields
temperature = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=100.0, key="temperature")
humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, key="humidity")
moisture = st.number_input("🌱 Soil Moisture (%)", min_value=0.0, max_value=100.0, key="moisture")

# Predict Button
if st.button("🔍 Predict Disease"):
    try:
        input_data = np.array([[temperature, humidity, moisture]])
        prediction = model.predict(input_data)
        predicted_disease = prediction[0]

        # Show result
        st.success(f"✅ Predicted Disease: {predicted_disease}")

        # Show extra info
        if predicted_disease in disease_info:
            st.info(f"🦠 Description: {disease_info[predicted_disease]['description']}")
            st.warning(f"🛡️ Tips: {disease_info[predicted_disease]['tips']}")
        else:
            st.info("No additional information available for this disease.")

    except Exception as e:
        st.error(f"⚠️ Error during prediction: {e}")

# Reset Button
if st.button("🔁 Reset Inputs"):
    st.session_state.temperature = 25.0
    st.st.experimental_rerun()
    st.session_state.moisture = 30.0
=======
import streamlit as st
import joblib
import numpy as np

# Load the saved model
model = joblib.load("new_crop_disease_detector.pkl")

st.set_page_config(page_title="AI Crop Disease Detector", layout="centered")

st.title("🌾 AI Crop Disease Detector")
st.markdown("Enter the values below to predict the crop disease:")

# Initialize session state for inputs
if "temperature" not in st.session_state:
    st.session_state.temperature = 25.0
if "humidity" not in st.session_state:
    st.session_state.humidity = 70.0
if "soil_moisture" not in st.session_state:
    st.session_state.soil_moisture = 30.0
if "ph" not in st.session_state:
    st.session_state.ph = 6.5
if "rainfall" not in st.session_state:
    st.session_state.rainfall = 150.0

# Input fields
st.session_state.temperature = st.slider("🌡️ Temperature (°C)", 0.0, 50.0, st.session_state.temperature)
st.session_state.humidity = st.slider("💧 Humidity (%)", 0.0, 100.0, st.session_state.humidity)
st.session_state.soil_moisture = st.slider("🌱 Soil Moisture (%)", 0.0, 100.0, st.session_state.soil_moisture)
st.session_state.ph = st.slider("🧪 pH Level", 0.0, 14.0, st.session_state.ph)
st.session_state.rainfall = st.slider("🌧️ Rainfall (mm)", 0.0, 500.0, st.session_state.rainfall)

# Predict button
if st.button("🔍 Predict Disease"):
    input_data = np.array([
        st.session_state.temperature,
        st.session_state.humidity,
        st.session_state.soil_moisture,
        st.session_state.ph,
        st.session_state.rainfall
    ]).reshape(1, -1)

    prediction = model.predict(input_data)[0]
    st.success(f"🦠 Predicted Disease: **{prediction}**")

# Reset button
if st.button("🔄 Reset Inputs"):
    st.session_state.temperature = 25.0
    st.session_state.humidity = 70.0
    st.session_state.soil_moisture = 30.0
    st.session_state.ph = 6.5
    st.session_state.rainfall = 150.0
>>>>>>> 7bd8d18 (Add renew_app.py)
    st.experimental_rerun()