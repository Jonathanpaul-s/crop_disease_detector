import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
try:
    model = joblib.load("new_crop_disease_detector.pkl")
except FileNotFoundError:
    st.error("❌ Model file not found. Make sure 'new_crop_disease_detector.pkl' is in the same folder.")
    st.stop()

# Page title
st.set_page_config(page_title="🌿 Crop Disease Detection from CSV", layout="centered")
st.title("🌿 Batch Crop Disease Detection from CSV")
st.write("Upload a CSV file with crop environmental data to predict possible diseases.")

# File uploader
uploaded_file = st.file_uploader("📤 Upload CSV File", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Check required columns
        required_columns = {"temperature", "humidity", "moisture"}
        if not required_columns.issubset(df.columns):
            st.error(f"❌ CSV file must contain these columns: {required_columns}")
            st.stop()

        # Predict
        input_data = df[["temperature", "humidity", "moisture"]]
        predictions = model.predict(input_data)

        # Add predictions to the DataFrame
        df["Predicted Disease"] = predictions

        # Show results
        st.success("✅ Predictions completed successfully!")
        st.dataframe(df)

        # Download link
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Results as CSV", data=csv, file_name="crop_disease_predictions.csv", mime="text/csv")

    except Exception as e:
        st.error(f"⚠️ An error occurred while processing the file: {e}")
else:
    st.warning("📌 Please upload a CSV file to begin.")