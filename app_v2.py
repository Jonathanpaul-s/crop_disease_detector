import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Smart Farm AI",
    page_icon="🌾",
    layout="wide"
)

DATA_FILE = Path("smartfarm_data.json")


def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            pass

    return {
        "farmer": {},
        "crops": []
    }


def save_data(data):
    with open("smartfarm_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


data = load_data()

st.title("🌾 Smart Farm AI")

menu = st.sidebar.selectbox(
    "📖 Main Menu",
    [
        "🏡 Home",
        "👤 User Account",
        "🌿 Farm Management",
        "📊 Productivity & Records"
    ],
    key="main_menu"
)


if menu == "🏡 Home":

    st.subheader("🏡 Home")

    if data["farmer"]:
        st.success(
            "Welcome back, "
            + data["farmer"]["name"]
        )
    else:
        st.info("Please create your farmer profile.")


elif menu == "👤 User Account":

    st.subheader("👤 Farmer Profile")

    name = st.text_input("Full Name")
    country = st.text_input("Country")
    primary_crop = st.text_input("Primary Crop")

    if st.button(
        "💾 Save Farmer Profile",
        key="save_profile"
    ):

        if name.strip() == "":
            st.error("Please enter your name.")

        else:

            data["farmer"] = {
                "name": name,
                "country": country,
                "primary_crop": primary_crop
            }

            save_data(data)

            st.success(
                "✅ Farmer profile saved successfully."
            )


elif menu == "🌿 Farm Management":

    st.subheader("🌿 Farm Management")

    st.write(
        "Record and manage crops on your farm."
    )

    st.markdown("---")

    st.subheader("🌱 Add Crop Record")

    crop_name = st.text_input(
        "Crop Name",
        key="crop_name"
    )

    variety = st.text_input(
        "Crop Variety",
        key="crop_variety"
    )

    planting_date = st.date_input(
        "Planting Date",
        key="planting_date"
    )

    area = st.number_input(
        "Farm Area (hectares)",
        min_value=0.0,
        step=0.1,
        key="crop_area"
    )

    status = st.selectbox(
        "Crop Status",
        [
            "Planted",
            "Growing",
            "Ready for Harvest",
            "Harvested"
        ],
        key="crop_status"
    )

    if st.button(
        "💾 Save Crop Record",
        key="save_crop"
    ):

        if crop_name.strip() == "":
            st.error("Please enter a crop name.")

        else:

            crop_record = {
                "crop_name": crop_name,
                "variety": variety,
                "planting_date": str(planting_date),
                "area_hectares": area,
                "status": status
            }

            data["crops"].append(crop_record)

            save_data(data)

            st.success(
                "✅ Crop record saved successfully."
            )

    st.markdown("---")

    st.subheader("📋 Saved Crop Records")

    if len(data["crops"]) == 0:

        st.info("No crop records have been added yet.")

    else:

        for number, crop in enumerate(
            data["crops"],
            start=1
        ):

            st.write(
                f"{number}. 🌱 {crop['crop_name']}"
            )

            st.write(
                "Variety:",
                crop["variety"]
            )

            st.write(
                "Planting Date:",
                crop["planting_date"]
            )

            st.write(
                "Area:",
                crop["area_hectares"],
                "hectares"
            )

            st.write(
                "Status:",
                crop["status"]
            )

            st.markdown("---")


elif menu == "📊 Productivity & Records":

    st.subheader("📊 Productivity & Records")