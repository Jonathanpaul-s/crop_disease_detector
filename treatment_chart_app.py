import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("🧪 Crop Disease Treatment Chart")

# Sample treatment data
treatment_data = {
    "Disease": ["Bacterial", "Fungal", "Viral", "Nutrient Deficiency"],
    "Treatment": ["Use copper-based bactericides and crop rotation",
                  "Apply fungicides and improve drainage",
                  "Remove infected plants and use resistant varieties",
                  "Apply balanced fertilizers and improve soil health"]
}

# Convert to DataFrame
df = pd.DataFrame(treatment_data)

# Display table
st.subheader("📋 Treatment Table")
st.dataframe(df)

# Grouped bar chart
st.subheader("📊 Treatment Options Chart")
treatment_counts = df['Treatment'].value_counts()
fig, ax = plt.subplots()
treatment_counts.plot(kind='barh', ax=ax, color="skyblue")
ax.set_xlabel("Number of Diseases Using Treatment")
ax.set_ylabel("Treatment Description")
st.pyplot(fig)