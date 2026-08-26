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

        st.subheader("📊 Farm Productivity Dashboard")

        if "sales" not in data:
            data["sales"] = []

        if "expenses" not in data:
            data["expenses"] = []

        if "crop_records" not in data:
            data["crop_records"] = []

        if "yield_records" not in data:
            data["yield_records"] = []

        total_sales = sum(
            float(sale.get("total", 0))
            for sale in data["sales"]
        )

        total_expenses = sum(
            float(expense.get("amount", 0))
            for expense in data["expenses"]
        )

        net_profit = total_sales - total_expenses

        total_crop_records = len(
            data["crop_records"]
        )

        total_yield_records = len(
            data["yield_records"]
        )

        total_sales_records = len(
            data["sales"]
        )

        total_expense_records = len(
            data["expenses"]
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Total Sales",
                f"{total_sales:,.2f}"
            )

        with col2:
            st.metric(
                "💸 Total Expenses",
                f"{total_expenses:,.2f}"
            )

        with col3:
            st.metric(
                "📈 Net Profit",
                f"{net_profit:,.2f}"
            )

        st.markdown("---")

        col4, col5, col6, col7 = st.columns(4)

        with col4:
            st.metric(
                "🌾 Crop Records",
                total_crop_records
            )

        with col5:
            st.metric(
                "📈 Yield Records",
                total_yield_records
            )

        with col6:
            st.metric(
                "💰 Sales Records",
                total_sales_records
            )

        with col7:
            st.metric(
                "💸 Expense Records",
                total_expense_records
            )

        st.markdown("---")

        st.subheader("📋 Productivity Overview")

        if net_profit > 0:

            st.success(
                "📈 Your farm is currently profitable."
            )

        elif net_profit < 0:

            st.error(
                "📉 Your farm is currently operating at a loss."
            )

        else:

            st.info(
                "ℹ️ Your farm currently has no recorded profit or loss."
            )

        st.write(
            "Use your Crop Production, Yield, Sales, and Expense "
            "Records to maintain an accurate view of farm performance."
        )
    


    elif productivity_option == "🌾 Crop Production Records":

        st.subheader("🌾 Crop Production Records")

        if "crop_records" not in data:
            data["crop_records"] = []

        st.write(
            f"📋 Total Crop Production Records: "
            f"{len(data['crop_records'])}"
        )

        st.markdown("---")

        st.write("### ➕ Add Crop Production Record")

        crop_name = st.text_input(
            "🌱 Crop Name",
            key="crop_production_name"
        )

        area = st.number_input(
            "📐 Farm Area",
            min_value=0.0,
            step=0.1,
            key="crop_production_area"
        )

        area_unit = st.selectbox(
            "Area Unit",
            ["hectares", "acres"],
            key="crop_production_area_unit"
        )

        quantity = st.number_input(
            "🌾 Production Quantity",
            min_value=0.0,
            step=0.1,
            key="crop_production_quantity"
        )

        production_unit = st.selectbox(
            "Production Unit",
            ["kg", "tons", "bags", "crates", "other"],
            key="crop_production_unit"
        )

        production_date = st.date_input(
            "📅 Production Date",
            key="crop_production_date"
        )

        notes = st.text_area(
            "📝 Notes",
            key="crop_production_notes"
        )

        if st.button(
            "💾 Save Crop Production Record",
            key="save_crop_production"
        ):

            if not crop_name.strip():
                st.warning("Please enter a crop name.")

            else:

                record = {
                    "crop_name": crop_name,
                    "area": area,
                    "area_unit": area_unit,
                    "quantity": quantity,
                    "production_unit": production_unit,
                    "date": str(production_date),
                    "notes": notes
                }

                data["crop_records"].append(record)

                st.success(
                    "✅ Crop production record saved successfully."
                )

                st.rerun()

        st.markdown("---")

        if data["crop_records"]:

            st.write("### 📋 Crop Production History")

            for record in reversed(data["crop_records"]):

                st.write(
                    f"🌱 {record['crop_name']} | "
                    f"{record['quantity']} "
                    f"{record['production_unit']} | "
                    f"{record['area']} "
                    f"{record['area_unit']} | "
                    f"{record['date']}"
                )

                if record["notes"]:
                    st.caption(record["notes"])

        else:

            st.info(
                "No crop production records available yet."
            )


    elif productivity_option == "📈 Yield Records":

        st.subheader("📈 Yield Records")

        if "yield_records" not in data:
            data["yield_records"] = []

        st.write(
            f"📋 Total Yield Records: "
            f"{len(data['yield_records'])}"
        )

        st.markdown("---")

        st.write("### ➕ Add Yield Record")

        crop_name = st.text_input(
            "🌱 Crop Name",
            key="yield_crop_name"
        )

        expected_yield = st.number_input(
            "🎯 Expected Yield",
            min_value=0.0,
            step=0.1,
            key="expected_yield"
        )

        actual_yield = st.number_input(
            "🌾 Actual Yield",
            min_value=0.0,
            step=0.1,
            key="actual_yield"
        )

        yield_unit = st.selectbox(
            "Yield Unit",
            ["kg", "tons", "bags", "crates", "other"],
            key="yield_unit"
        )

        harvest_date = st.date_input(
            "📅 Harvest Date",
            key="yield_harvest_date"
        )

        notes = st.text_area(
            "📝 Notes",
            key="yield_notes"
        )

        if st.button(
            "💾 Save Yield Record",
            key="save_yield_record"
        ):

            if not crop_name.strip():

                st.warning(
                    "Please enter a crop name."
                )

            else:

                record = {
                    "crop_name": crop_name,
                    "expected_yield": expected_yield,
                    "actual_yield": actual_yield,
                    "unit": yield_unit,
                    "date": str(harvest_date),
                    "notes": notes
                }

                data["yield_records"].append(record)

                st.success(
                    "✅ Yield record saved successfully."
                )

                st.rerun()

        st.markdown("---")

        if data["yield_records"]:

            st.write("### 📋 Yield History")

            for record in reversed(data["yield_records"]):

                st.write(
                    f"🌱 {record['crop_name']} | "
                    f"Expected: {record['expected_yield']} "
                    f"{record['unit']} | "
                    f"Actual: {record['actual_yield']} "
                    f"{record['unit']} | "
                    f"{record['date']}"
                )

                if record["notes"]:
                    st.caption(
                        f"📝 {record['notes']}"
                    )

        else:

            st.info(  
                  "No yield records available yet."
            )
            
    elif productivity_option == "💰 Sales Records":

        st.subheader("💰 Sales Records")

        if "sales" not in data:
            data["sales"] = []

        st.write(
            f"📋 Total Sales Records: {len(data['sales'])}"
        )

        st.markdown("---")

        st.write("### ➕ Add Sales Record")

        product_name = st.text_input(
            "🌾 Product / Crop Name",
            key="sales_product_name"
        )

        quantity = st.number_input(
            "📦 Quantity",
            min_value=0.0,
            step=0.1,
            key="sales_quantity"
        )

        price = st.number_input(
            "💰 Price per Unit",
            min_value=0.0,
            step=0.01,
            key="sales_price"
        )

        total = quantity * price

        st.metric(
            "💵 Total Sale Value",
            f"{total:,.2f}"
        )

        customer = st.text_input(
            "👤 Customer",
            key="sales_customer"
        )

        sale_date = st.date_input(
            "📅 Sale Date",
            key="sales_date"
        )

        notes = st.text_area(
            "📝 Notes",
            key="sales_notes"
        )

        if st.button(
            "💾 Save Sales Record",
            key="save_sales_record"
        ):

            if not product_name.strip():

                st.warning(
                    "Please enter a product or crop name."
                )

            elif quantity <= 0:

                st.warning(
                    "Quantity must be greater than zero."
                )

            elif price <= 0:

                st.warning(
                    "Price must be greater than zero."
                )

            else:

                record = {
                    "product": product_name,
                    "quantity": quantity,
                    "price": price,
                    "total": total,
                    "customer": customer,
                    "date": str(sale_date),
                    "notes": notes
                }

                data["sales"].append(record)

                st.success(
                    "✅ Sales record saved successfully."
                )

                st.rerun()

        st.markdown("---")

        if data["sales"]:

            st.write("### 📋 Sales History")

            for sale in reversed(data["sales"]):

                st.write(
                    f"🌾 {sale.get('product', 'Unknown')} | "
                    f"Quantity: {sale.get('quantity', 0)} | "
                    f"Price: {sale.get('price', 0):,.2f} | "
                    f"Total: {sale.get('total', 0):,.2f} | "
                    f"Date: {sale.get('date', '')}"
                )

                if sale.get("customer"):
                    st.caption(
                        f"👤 Customer: {sale['customer']}"
                    )

                if sale.get("notes"):
                    st.caption(
                        f"📝 {sale['notes']}"
                    )

        else:

            st.info(
                "No sales records available yet."
                       "No yield records available yet."
            )
    elif productivity_option == "💸 Expense Records":

        st.subheader("💸 Expense Records")

        if "expenses" not in data:
            data["expenses"] = []

        st.write(
            f"📋 Total Expense Records: {len(data['expenses'])}"
        )

        st.markdown("---")

        st.write("### ➕ Add Expense Record")

        expense_category = st.selectbox(
            "📂 Expense Category",
            [
                "🌱 Seeds",
                "🧪 Fertilizer",
                "💊 Pesticides",
                "💧 Irrigation",
                "🚜 Equipment",
                "👷 Labor",
                "🐄 Livestock",
                "🚚 Transportation",
                "⚡ Utilities",
                "🏠 Land / Rent",
                "📦 Other"
            ],
            key="expense_category"
        )

        description = st.text_input(
            "📝 Expense Description",
            key="expense_description"
        )

        amount = st.number_input(
            "💰 Expense Amount",
            min_value=0.0,
            step=0.01,
            key="expense_amount"
        )

        expense_date = st.date_input(
            "📅 Expense Date",
            key="expense_date"
        )

        notes = st.text_area(
            "📋 Notes",
            key="expense_notes"
        )

        if st.button(
            "💾 Save Expense Record",
            key="save_expense_record"
        ):

            if amount <= 0:

                st.warning(
                    "Expense amount must be greater than zero."
                )

            else:

                record = {
                    "category": expense_category,
                    "description": description,
                    "amount": amount,
                    "date": str(expense_date),
                    "notes": notes
                }

                data["expenses"].append(record)

                st.success(
                    "✅ Expense record saved successfully."
                )

                st.rerun()

        st.markdown("---")

        if data["expenses"]:

            st.write("### 📋 Expense History")

            total_expenses = sum(
                float(expense.get("amount", 0))
                for expense in data["expenses"]
            )

            st.metric(
                "💸 Total Expenses",
                f"{total_expenses:,.2f}"
            )

            for expense in reversed(data["expenses"]):

                st.write(
                    f"📂 {expense.get('category', 'Other')} | "
                    f"{expense.get('description', '')} | "
                    f"Amount: "
                    f"{float(expense.get('amount', 0)):,.2f} | "
                    f"Date: {expense.get('date', '')}"
                )

                if expense.get("notes"):
                    st.caption(
                        f"📝 {expense['notes']}"
                    )

        else:

            st.info(
                "No expense records available yet."
            )

    
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