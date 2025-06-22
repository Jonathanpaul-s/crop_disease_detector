import streamlit as st
import numpy as np
import joblib

# Load the model
try:
    model = joblib.load("new_crop_disease_detector.pkl")
except FileNotFoundError:
    st.error("❌ Model file not found! Make sure 'new_crop_disease_detector.pkl' is in the same folder.")
    st.stop()

# Title
st.title("🌾 Crop Disease Detection AI")

st.write("Enter the crop's environmental data below:")

# Inputs
temperature = st.number_input("🌡️ Temperature (°C)", min_value=0.0, max_value=100.0, value=25.0)
humidity = st.number_input("💧 Humidity (%)", min_value=0.0, max_value=100.0, value=50.0)
moisture = st.number_input("🌱 Soil Moisture (%)", min_value=0.0, max_value=100.0, value=30.0)

# Predict
if st.button("🔍 Predict Disease"):
    try:
        input_data = np.array([[temperature, humidity, moisture]])
        prediction = model.predict(input_data)
        st.success(f"✅ Predicted Disease: {prediction[0]}")st.
    excest.error(f"An error occurred during prediction: {e}")ong during prediction: {e}")