import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the model
try:
    model = joblib.load("new_crop_disease_detector.pkl")
except FileNotFoundError:
    st.error("❌ Model file not found. Make sure 'new_crop_disease_detector.pkl' is in the same folder.")
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

# Title and intro
st.title("🌿 Manual Crop Disease Prediction + Chart")
st.write("Enter multiple crop readings below to predict diseases, view extra info, and see a chart.")

# Number of rows input
num_rows = st.number_input("How many rows of crop data do you want to enter?", min_value=1, max_value=20, value=3)

# Create input table
input_df = pd.DataFrame({
    "temperature": [0.0] * num_rows,
    "humidity": [0.0] * num_rows,
    "moisture": [0.0] * num_rows
})

# Editable input
edited_df = st.data_editor(input_df, num_rows="dynamic", use_container_width=True)

# Predict and Show Info
if st.button("🔍 Predict and Show Info"):
    try:
        input_data = edited_df[["temperature", "humidity", "moisture"]].values
        predictions = model.predict(input_data)
        edited_df["Predicted Disease"] = predictions

        st.success("✅ Predictions completed successfully!")
        st.dataframe(edited_df)

        # Show extra info
        st.subheader("🧬 Disease Information")
        for i, disease in enumerate(predictions):
            st.markdown(f"### 🔹 Row {i+1}: **{disease}**")
            info = disease_info.get(disease, None)
            if info:
                st.markdown(f"**📝 Description:** {info['description']}")
                st.markdown(f"**💥 Cause:** {info['cause']}")
                st.markdown(f"**🌱 Solution:** {info['solution']}")
            else:
                st.markdown("No extra info found for this disease.")
            st.markdown("---")

        # Chart
        st.subheader("📊 Disease Prediction Chart")
        chart_data = edited_df["Predicted Disease"].value_counts().reset_index()
        chart_data.columns = ["Disease", "Count"]
        st.bar_chart(chart_data.set_index("Disease"))

        # Download option
        csv_output = edited_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Results with Info",
            data=csv_output,
            file_name="manual_info_predictions.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"⚠️ Error during prediction: {e}")