import streamlit as st
import numpy as np
import joblib

# Load the model
model = joblib.load("new_crop_disease_detector.pkl")

# Title
st.title("🌾 AI Crop Disease Detector (Manual Inputs)")

# Initialize default values if not in session state
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

# Input Fields
st.session_state.temperature = st.slider("🌡 Temperature (°C)", 0.0, 50.0, st.session_state.temperature)
st.session_state.humidity = st.slider("💧 Humidity (%)", 0.0, 100.0, st.session_state.humidity)
st.session_state.soil_moisture = st.slider("🌱 Soil Moisture (%)", 0.0, 100.0, st.session_state.soil_moisture)
st.session_state.ph = st.slider("⚗️ pH Level", 0.0, 14.0, st.session_state.ph)
st.session_state.rainfall = st.slider("🌧 Rainfall (mm)", 0.0, 500.0, st.session_state.rainfall)

# Predict Button
if st.button("🚀 Predict Disease"):
    input_data = np.array([
        st.session_state.temperature,
        st.session_state.humidity,
        st.session_state.soil_moisture,
        st.session_state.ph,
        st.session_state.rainfall
    ]).reshape(1, -1)
    prediction = model.predict(input_data)[0]
    st.success(f"🌿 Predicted Disease: **{prediction}**")

# Reset Button
if st.button("🔄 Reset Inputs"):
    st.session_state.temperature = 25.0
    st.session_state.humidity = 70.0
    st.session_state.soil_moisture = 30.0
    st.session_state.ph = 6.5
    st.session_state.rainfall = 150.0
    st.experimental_rerun()state.rainfall = 150.0
    st.experimental_rerun()