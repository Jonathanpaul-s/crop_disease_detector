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
    "crops": [],
    "equipment": [],
    "productivity": [],
    "production_records": [],
    "sales": [],
    "expenses": []
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


    if len(data["expenses"]) == 0:

            st.info(
                "No expense records have been added yet."
            )

    else:

            for number, expense in enumerate(
                data["expenses"],
                start=1
            ):

                st.write(
                    f"{number}. 💳 {expense['category']}"
                )

                st.write(
                    "Description:",
                    expense["description"]
                )

                st.write(
                    "Date:",
                    expense["date"]
                )

                st.write(
                    "Amount:",
                    expense["amount"]
                )

                st.markdown("---")


    # ========================================================
    # PROFIT CALCULATION
    # ========================================================

elif menu == "📊 Productivity & Records":

    productivity_option = st.sidebar.selectbox(
        "📊 Productivity Options",
        [
            "📊 Farm Productivity",
            "🌾 Crop Production Records",
            "📈 Yield Records",
            "💰 Sales Records",
            "💸 Expense Records",
            "📊 Profit Calculation"
        ],
        key="productivity_option"
    )

    if productivity_option == "📊 Farm Productivity":

        st.subheader("📊 Farm Productivity")

        # Put your existing Farm Productivity code here


    elif productivity_option == "🌾 Crop Production Records":

        st.subheader("🌾 Crop Production Records")

        # Put your existing Crop Production Records code here


    elif productivity_option == "📈 Yield Records":

        st.subheader("📈 Yield Records")

        # Put your existing Yield Records code here


    elif productivity_option == "💰 Sales Records":

        st.subheader("💰 Sales Records")

        # Put your existing Sales Records code here


    elif productivity_option == "💸 Expense Records":

        st.subheader("💸 Expense Records")

        # Put your existing Expense Records code here


    elif productivity_option == "📊 Profit Calculation":

        st.subheader("📊 Farm Profit Calculation")

        if "sales" not in data:
            data["sales"] = []

        if "expenses" not in data:
            data["expenses"] = []

        total_sales = sum(
            float(sale.get("total", 0))
            for sale in data["sales"]
        )

        total_expenses = sum(
            float(expense.get("amount", 0))
            for expense in data["expenses"]
        )

        profit = total_sales - total_expenses

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Total Sales",
                f"{total_sales:,.2f}"
            )

        with col2:
            st.metric(
                "💳 Total Expenses",
                f"{total_expenses:,.2f}"
            )

        with col3:
            st.metric(
              "📈 Net Profit",
             f"{profit:,.2f}"
            )

        st.markdown("---")

        if profit > 0:
            st.success(
                "📈 Your farm is currently profitable."
            )

        elif profit < 0:
            st.error(
                "📉 Your farm currently has a loss."
            )

        else:
            st.info(
                "Farm sales and expenses are currently balanced."
            )