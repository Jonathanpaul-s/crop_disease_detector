import streamlit as st
import pandas as pd
import numpy as np
import joblib
import time

# Load model
try:
    model = joblib.load("new_crop_disease_detector.pkl")
except FileNotFoundError:
    st.error("❌ Model file not found!")
    st.stop()

# Disease information
disease_info = {
    "Bacterial": {
        "description": "Bacterial diseases are caused by pathogenic bacteria.",
        "cause": "Caused by bacteria infecting the crop through wounds or natural openings.",
        "solution": "Use copper-based bactericides and crop rotation."
    },
    "Fungal": {
        "description": "Fungal diseases result from various fungi.",
        "cause": "Caused by spores spreading in humid environments.",
        "solution": "Apply appropriate fungicides and ensure proper spacing between crops."
    },
    "Viral": {
        "description": "Viral diseases are spread by insects or contact.",
        "cause": "Caused by viruses carried by pests like aphids.",
        "solution": "Control pests and remove infected plants."
    },
    "Healthy": {
        "description": "No disease detected. The crop is healthy.",
        "cause": "No pathogenic influence.",
        "solution": "Continue good farming practices."
    }
}

# App title
st.title("📡 Live Sensor Data: Crop Disease Detection")

# Simulate new data on every refresh
temperature = round(np.random.uniform(20, 40), 2)
humidity = round(np.random.uniform(40, 90), 2)
moisture = round(np.random.uniform(20, 80), 2)

# Display simulated data
st.subheader("🌡️ Live Sensor Readings")
st.write(f"**Temperature:** {temperature} °C")
st.write(f"**Humidity:** {humidity} %")
st.write(f"**Moisture:** {moisture} %")

# Predict using the model
input_data = np.array([[temperature, humidity, moisture]])
prediction = model.predict(input_data)[0]

# Display prediction
st.subheader("🩺 Predicted Disease")
st.success(f"**{prediction}**")

# Show additional info
info = disease_info.get(prediction)
if info:
    st.subheader("📘 Disease Information")
    st.markdown(f"**📝 Description:** {info['description']}")
    st.markdown(f"**💥 Cause:** {info['cause']}")
    st.markdown(f"**🌱 Solution:** {info['solution']}")

# Auto-refresh every 5 seconds
st.caption("🔄 Auto-refreshes every 5 seconds for new simulated sensor readings.")
st.experimental_rerun() if st.button("⏱ Refresh Now") else time.sleep(5)
st.rerun()