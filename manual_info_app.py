import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the trained model
try:
    model = joblib.load("new_crop_disease_detector.pkl")
except FileNotFoundError:
    st.error("❌ Model file not found. Please make sure 'new_crop_disease_detector.pkl' is in this folder.")
    st.stop()

# Disease information dictionary
disease_info = {
    "Healthy": {
        "description": "Your plant is healthy and showing no signs of disease.",
        "cause": "No issues detected.",
        "solution": "Keep monitoring and maintain good conditions."
    },
    "Fungal": {
        "description": "Fungal diseases are caused by fungi like mildew, rust, or blight.",
        "cause": "Often due to excess moisture, poor air circulation, or infected soil.",
        "solution": "Apply a suitable fungicide, improve drainage and air flow."
    },
    "Bacterial": {
        "description": "Caused by harmful bacteria attacking plant tissues.",
        "cause": "Spread through water, tools, insects or contaminated soil.",
        "solution": "Remove infected parts, apply copper-based sprays."
    },
    "Viral": {
        "description": "Viral infections can deform or discolor leaves and fruits.",
        "cause": "Transmitted by insects or infected tools.",
        "solution": "No cure—remove infected plants and control insects."
    }
}

# App layout
st.set_page_config(page_title="🌿 Manual Crop Prediction + Info", layout="centered")
st.title("🌿 Manual Crop Disease Prediction")
st.write("Enter multiple crop readings below to predict diseases and learn how to treat them.")

# Number of rows input
num_rows = st.number_input("How many rows of crop data do you want to enter?", min_value=1, max_value=20, value=3)

# Input table
input_df = pd.DataFrame({
    "temperature": [0.0] * num_rows,
    "humidity": [0.0] * num_rows,
    "moisture": [0.0] * num_rows
})

edited_df = st.data_editor(input_df, num_rows="dynamic", use_container_width=True)

# Prediction
if st.button("🚀 Predict and Show Info"):
    try:
        input_data = edited_df[["temperature", "humidity", "moisture"]].values
        predictions = model.predict(input_data)
        edited_df["Predicted Disease"] = predictions

        st.success("✅ Predictions completed successfully!")
        st.dataframe(edited_df)

        # Show extra info for each prediction
        st.subheader("🧠 Disease Information")
        for i, disease in enumerate(predictions):
            st.markdown(f"### 🌾 Row {i+1}: **{disease}**")
            info = disease_info.get(disease, None)
            if info:
                st.markdown(f"**🩺 Description:** {info['description']}")
                st.markdown(f"**☣️ Cause:** {info['cause']}")
                st.markdown(f"**🧪 Solution:** {info['solution']}")
            else:
                st.markdown("No extra info found for this disease.")
            st.markdown("---")

        # Download results
        csv_output = edited_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Results with Info",
            data=csv_output,
            file_name="manual_info_predictions.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"⚠️ Error during prediction: {e}")