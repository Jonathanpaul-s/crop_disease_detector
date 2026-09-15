
import streamlit as st
from pathlib import Path
import base64

BACKGROUND = Path("assets/farm_logo.png")

if BACKGROUND.exists():
    with open(BACKGROUND, "rb") as f:
        bg = base64.b64encode(f.read()).decode()

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image:
            linear-gradient(rgba(255,255,255,0.55), rgba(255,255,255,0.55)),
            url("data:image/png;base64,{bg}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Make the main content easier to read */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.78);
        border-radius: 15px;
        padding: 2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 💾 ACCOUNT DATA STORAGE
# ============================================================

import json
import os


def _load(filename, default):
    """Load JSON data safely from a local file."""
    try:
        if not os.path.exists(filename):
            return default

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data

    except (json.JSONDecodeError, OSError):
        return default


def _save(filename, data):
    """Save JSON data safely to a local file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except OSError as e:
        st.error(f"Unable to save account data: {e}")


# ============================================================
# 🔐 PASSWORD HASHING
# ============================================================

import hashlib

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# 🎯 APPLY FARMER PERSONALIZATION
# ============================================================

if st.session_state.get("logged_in", False):

    farmer_profile = st.session_state.get(
        "farmer_profile",
        {}
    )



# ============================================================
# 🧠 PERSONALIZATION ENGINE
# ============================================================

def build_farmer_context(profile):
    """Build a safe context used by the personalization engine."""
    
    if not isinstance(profile, dict):
        profile = {}

    return {
        "country": str(profile.get("country", "")).strip().lower(),
        "location": str(profile.get("location", "")).strip().lower(),
        "farm_type": str(profile.get("farm_type", "")).strip().lower(),
        "experience": str(profile.get("experience", "")).strip().lower(),
        "farm_size": str(profile.get("farm_size", "")).strip().lower(),
        "crops": profile.get("crops", []),
    }


def personalize_features(features, context):
    """
    Personalize the existing feature list according to farmer context.
    Does not delete the original features.
    """

    if not isinstance(features, list):
        return features

    context = context or {}

    country = context.get("country", "")
    farm_type = context.get("farm_type", "")
    experience = context.get("experience", "")

    personalized = []

    for feature in features:
        if isinstance(feature, dict):
            item = feature.copy()
            name = str(item.get("name", item.get("Name", ""))).lower()

            score = item.get("Score", 0)

            # Country relevance
            if country:
                if country in name:
                    score += 10

            # Farm-type relevance
            if farm_type:
                if farm_type in name:
                    score += 10

            # Experience relevance
            if experience:
                if experience in name:
                    score += 5

            item["Score"] = score
            personalized.append(item)

        else:
            personalized.append(feature)

    # Keep highest-priority features first
    try:
        personalized = sorted(
            personalized,
            key=lambda x: x.get("Score", 0)
            if isinstance(x, dict) else 0,
            reverse=True
        )
    except Exception:
        pass

    return personalized



# ============================================================
# 🌱 CROP-SPECIFIC PERSONALIZATION RULES
# ============================================================

CROP_FEATURE_RULES = {

    "cassava": [
        "Soil Health Record",
        "Farm Productivity",
        "Yield Estimator",
        "AI Crop Calendar",
        "Crop Disease Detection",
        "Smart Fertilizer & Pesticide Stock Manager",
        "Farm Equipment Tracker",
        "Irrigation Schedule",
        "Harvest Time Estimator",
        "View Sales Record",
        "Calculate Profit",
    ],

    "maize": [
        "Soil Health Record",
        "Irrigation Schedule",
        "AI Crop Calendar",
        "Crop Disease Detection",
        "Yield Estimator",
        "Farm Productivity",
        "Smart Fertilizer & Pesticide Stock Manager",
        "Harvest Time Estimator",
        "Farm Performance Indicators",
        "View Sales Record",
        "Price Trend Checker",
    ],

    "corn": [
        "Soil Health Record",
        "Irrigation Schedule",
        "AI Crop Calendar",
        "Crop Disease Detection",
        "Yield Estimator",
        "Farm Productivity",
        "Smart Fertilizer & Pesticide Stock Manager",
        "Harvest Time Estimator",
        "View Sales Record",
        "Price Trend Checker",
        "Calculate Profit",
    ],

    "rice": [
        "Irrigation Schedule",
        "Soil Health Record",
        "AI Crop Calendar",
        "Crop Disease Detection",
        "Yield Estimator",
        "Farm Productivity",
        "Harvest Time Estimator",
        "Farm Plot Mapping",
        "Weather",
        "View Sales Record",
        "Price Trend Checker",
    ],

    "tomato": [
        "Irrigation Schedule",
        "Crop Disease Detection",
        "Soil Health Record",
        "Smart Fertilizer & Pesticide Stock Manager",
        "AI Crop Calendar",
        "Yield Estimator",
        "Farm Productivity",
        "Harvest Time Estimator",
        "Farm Plot Mapping",
        "View Sales Record",
        "Price Trend Checker",
    ],

    "yam": [
        "Soil Health Record",
        "AI rop Calendar",
        "Crop Disease Detection",
        "Farm Productivity",
        "Yield Estimator",
        "Harvest Time Estimator",
        "Smart Fertilizer & Pesticide Stock Manager",
        "Irrigation Schedule",
        "Farm Plot Mapping",
        "View Sales Record",
        "Calculate Profit",
    ],
}


# ============================================================
# 🎯 PERSONALIZED FEATURE RECOMMENDATION ENGINE
# ============================================================

def recommend_features(features, profile):

    if not isinstance(features, list):
        return []

    if not isinstance(profile, dict):
        profile = {}

    crop_type = str(
        profile.get("crop_type", "")
    ).lower().strip()

    location = str(
        profile.get("location", "")
    ).lower().strip()

    country = str(
        profile.get("country", "")
    ).lower().strip()

    farm_type = str(
        profile.get("farm_type", "")
    ).lower().strip()

    experience = str(
        profile.get("experience", "")
    ).lower().strip()

    # --------------------------------------------------------
    # 🌱 Get crop-specific features
    # --------------------------------------------------------

    crop_rules = CROP_FEATURE_RULES.get(
        crop_type,
        []
    )

    crop_rules = [
        str(x).lower().strip()
        for x in crop_rules
    ]

    scored_features = []

    # --------------------------------------------------------
    # ⭐ Score every existing feature
    # --------------------------------------------------------

    for feature in features:

        if isinstance(feature, dict):

            item = feature.copy()

            feature_name = str(
                item.get(
                    "name",
                    item.get("Name", "")
                )
            ).strip()

        else:

            feature_name = str(feature).strip()

            item = {
                "name": feature_name
            }

        name_lower = feature_name.lower().strip()

        score = 0

        # ====================================================
        # 🌱 EXACT CROP RELEVANCE
        # ====================================================

        if name_lower in crop_rules:
            score += 100

        # Partial crop-rule matching
        for rule in crop_rules:

            if rule and (
                rule in name_lower
                or name_lower in rule
            ):
                score += 80
                break

        # ====================================================
        # 🌾 FARM TYPE
        # ====================================================

        if farm_type in [
            "crop farming",
            "mixed farming"
        ]:

            if any(word in name_lower for word in [
                "crop",
                "soil",
                "irrigation",
                "yield",
                "disease",
                "fertilizer",
                "pesticide",
                "calendar",
                "harvest"
            ]):
                score += 30

        elif farm_type == "livestock farming":

            if any(word in name_lower for word in [
                "livestock",
                "animal",
                "feed",
                "health",
                "farm management"
            ]):
                score += 30

        elif farm_type == "aquaculture":

            if any(word in name_lower for word in [
                "water",
                "soil",
                "health",
                "productivity",
                "market"
            ]):
                score += 30

        elif farm_type == "urban farming":

            if any(word in name_lower for word in [
                "crop",
                "irrigation",
                "soil",
                "calendar",
                "disease"
            ]):
                score += 30

        # ====================================================
        # 📍 LOCATION CONTEXT
        # ====================================================

        if location:

            if any(word in name_lower for word in [
                "irrigation",
                "soil",
                "weather",
                "climate",
                "crop",
                "disease",
                "calendar"
            ]):
             score += 10

        # ====================================================
        # 🌍 COUNTRY CONTEXT
        # ====================================================

        if country:

            if any(word in name_lower for word in [
                "market",
                "price",
                "sales",
                "sale",
                "order",
                "loan",
                "profit",
                "expense"
            ]):
                score += 10

        # ====================================================
        # 👨‍🌾 EXPERIENCE
        # ====================================================

        if experience == "beginner":

            if any(word in name_lower for word in [
                "tips",
                "tutor",
                "calendar",
                "disease",
                "soil"
            ]):
                score += 15

        elif experience in [
            "experienced",
            "professional"
        ]:

            if any(word in name_lower for word in [
                "yield",
                "productivity",
                "drone",
                "mapping",
                "roi",
                "market"
            ]):
                score += 15

        # ----------------------------------------------------
        # Store score internally
        # ----------------------------------------------------

        item["_personalization_score"] = score

        scored_features.append(item)

    # ========================================================
    # ⭐ SORT BY RELEVANCE
    # ========================================================

    scored_features.sort(
        key=lambda x: x.get(
            "_personalization_score",
            0
        ),
        reverse=True
    )

    # ========================================================
    # 🎯 RETURN ONLY TOP 20
    # ========================================================

    return scored_features[:20]

# ============================================================
# 🌾 SMART FARM AI FEATURE CATALOG
# ============================================================

SMART_FARM_FEATURES = [
    "View Sales Record",
    "View Expense",
    "Calculate Profit",
    "View Farmer Record",
    "Farm Productivity",
    "Yield Estimator",
    "Farm Loan Recorder",
    "Add Loan Record",

    "Irrigation Schedule",
    "Soil Health Record",

    "Farm Plot Mapping",

    "Smart Fertilizer & Pesticide Stock Manager",
    "AI Crop Calendar",
    "Drone Flight Scheduler",
    "Voice Command Interface",
    "Smart Tutor Multilanguage",

    "Crop Disease Detection",
    "AI Farm Tips",
    "Market Tools",
    "Price Trend Checker",
    "ROI Calculator"
]

# ============================================================
# 🔐 LOGIN STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "farmer_profile" not in st.session_state:
    st.session_state.farmer_profile = {}


# ============================================================
# 🔐 ACCOUNT MANAGEMENT
# ============================================================

if not st.session_state.logged_in:

    st.subheader("🔐 User Account Management")

    account_action = st.radio(
        "Choose an action",
        ["Login", "Create Account"],
        key="account_action_unique_001"
    )

    if account_action == "Login":

        username = st.text_input(
            "Username",
            key="login_username_unique_001"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password_unique_001"
        )

        if st.button(
            "🔓 Login",
            key="login_button_unique_001"
        ):

            # Load saved accounts from disk
            users = _load("accounts.json", [])

            if not isinstance(users, list):
                users = []

            user_found = None

            for user in users:
                if (
                    isinstance(user, dict)
                    and user.get("username") == username
                    and user.get("password") == hash_password(password)
                ):
                    user_found = user
                    break

            if user_found:

                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.session_state.farmer_profile = user_found.get(
                    "profile",
                    {}
                )

                st.success("Login successful!")
                st.rerun()

            else:
                st.error("Invalid username or password.")

    else:

        new_username = st.text_input(
            "Create Username",
            key="register_username_unique_001"
        )

        new_email = st.text_input(
            "Email",
            key="register_email_unique_001"
        )

        new_password = st.text_input(
            "Create Password",
            type="password",
            key="register_password_unique_001"
        )

        country = st.text_input(
            "Country",
            key="register_country_unique_001"
        )

        location = st.text_input(
            "Location",
            key="register_location_unique_001"
        )

        crop_type = st.text_input(
            "Main Crop Type",
            key="register_crop_type_unique_001"
        )

        farm_type = st.selectbox(
            "Farm Type",
            [
                "Crop Farming",
                "Livestock Farming",
                "Mixed Farming",
                "Aquaculture",
                "Urban Farming"
            ],
            key="register_farm_type_unique_001"
        )

        experience = st.selectbox(
            "Farming Experience",
            [
                "Beginner",
                "Intermediate",
                "Experienced",
                "Professional"
            ],
            key="register_experience_unique_001"
        )

        if st.button(
            "📝 Create Account",
            key="create_account_button_unique_001"
        ):

            if not new_username or not new_password:
                st.warning("Please enter a username and password.")

            else:

                # Load existing accounts from disk
                users = _load("accounts.json", [])

                if not isinstance(users, list):
                    users = []

                if any(
                    isinstance(user, dict)
                    and user.get("username") == new_username
                    for user in users
                ):
                    st.error("Username already exists.")

                else:

                    profile = {
                        "country": country,
                        "location": location,
                        "crop_type": crop_type,
                        "farm_type": farm_type,
                        "experience": experience
                    }
                    users.append({
                        "username": new_username,
                        "email": new_email,
                        "password": hash_password(new_password),
                        "profile": profile
                    })

                    # Permanently save account
                    _save("accounts.json", users)
                    st.success(
                        "Account created successfully. You can now login."
                    )

 # ============================================================
# 🔒 STOP APP UNTIL USER IS LOGGED IN
# ============================================================

if not st.session_state.logged_in:
    st.stop() 


# ============================================================
# SMART FARM AI — UNIFIED FARM CONTEXT & PERSONALIZATION
# ============================================================

farmer_profile = st.session_state.get("farmer_profile", {})

if not isinstance(farmer_profile, dict):
    farmer_profile = {}

# ------------------------------------------------------------
# 1. Load farmer farms
# ------------------------------------------------------------

farms = farmer_profile.get("farms", [])

if not isinstance(farms, list):
    farms = []

# Create a default farm if the farmer has none
if not farms:
    default_farm = {
        "farm_id": "main_farm",
        "farm_name": "Main Farm",
        "crop_type": farmer_profile.get("crop_type", "Not specified"),
        "location": farmer_profile.get("location", "Not specified"),
        "farm_type": farmer_profile.get("farm_type", "Not specified"),
        "farm_size": farmer_profile.get("farm_size", "Not specified"),
        "status": "active",
    }

    farms.append(default_farm)
    farmer_profile["farms"] = farms
    st.session_state.farmer_profile = farmer_profile


# ------------------------------------------------------------
# 2. Only active farms appear as current farm choices
# ------------------------------------------------------------

active_farms = [
    farm for farm in farms
    if str(farm.get("status", "active")).lower() == "active"
]

if not active_farms:
    active_farms = farms


# ------------------------------------------------------------
# 3. Restore previously selected farm
# ------------------------------------------------------------

saved_farm_id = st.session_state.get("current_farm_id")

current_farm = None

if saved_farm_id:
    current_farm = next(
        (
            farm for farm in active_farms
            if str(farm.get("farm_id")) == str(saved_farm_id)
        ),
        None
    )

# If no valid farm was selected, use the first active farm
if current_farm is None and active_farms:
    current_farm = active_farms[0]
    st.session_state.current_farm_id = current_farm.get("farm_id")


# ------------------------------------------------------------
# 4. Keep current farm available globally through session state
# ------------------------------------------------------------

st.session_state.current_farm = current_farm


# ------------------------------------------------------------
# 5. Build a unified personalization profile
# ------------------------------------------------------------

personalized_profile = dict(farmer_profile)

if current_farm:

    personalized_profile.update({
        "current_farm_id": current_farm.get("farm_id"),
        "current_farm_name": current_farm.get("farm_name"),
        "current_crop": current_farm.get("crop_type"),
        "current_location": current_farm.get("location"),
        "current_farm_type": current_farm.get("farm_type"),
        "current_farm_size": current_farm.get("farm_size"),
    })

    # Current farm becomes the main context
    if current_farm.get("crop_type"):
        personalized_profile["crop_type"] = current_farm.get("crop_type")

    if current_farm.get("location"):
        personalized_profile["location"] = current_farm.get("location")

    if current_farm.get("farm_type"):
        personalized_profile["farm_type"] = current_farm.get("farm_type")

    if current_farm.get("farm_size"):
        personalized_profile["farm_size"] = current_farm.get("farm_size")


st.session_state.personalized_profile = personalized_profile


# ------------------------------------------------------------
# 6. Generate personalized recommendations
# ------------------------------------------------------------

recommended_features = recommend_features(
    SMART_FARM_FEATURES,
    personalized_profile
)


# ------------------------------------------------------------
# 7. Current Farm Context Bar
# ------------------------------------------------------------

if current_farm:

    farm_name = current_farm.get("farm_name", "Current Farm")
    crop_name = current_farm.get("crop_type", "Not specified")
    farm_location = current_farm.get("location", "Not specified")

    st.markdown(
        f"""
        <div style="
            background: rgba(255,255,255,0.90);
            padding: 14px 18px;
            border-radius: 14px;
            margin-bottom: 18px;
            border-left: 5px solid #2e7d32;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        ">
            <div style="font-size: 13px; color: #666;">
                CURRENT FARM
            </div>

            <div style="
                font-size: 22px;
                font-weight: 700;
                margin-top: 3px;
            ">
                🌱 {farm_name}
            </div>

            <div style="
                font-size: 14px;
                margin-top: 6px;
                color: #555;
            ">
                🌾 Crop: {crop_name}
                &nbsp;&nbsp;|&nbsp;&nbsp;
                📍 Location: {farm_location}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# 8. Personalization summary
# ------------------------------------------------------------

with st.expander("⭐ My Personalized Farm Recommendations", expanded=False):

    if recommended_features:

        st.write(
            "Smart Farm AI has selected the tools most relevant to your "
            "current farm and farming situation."
        )

        for feature in recommended_features[:20]:

            if isinstance(feature, dict):
                feature_name = feature.get(
                    "name",
                    feature.get("Name", "Feature")
                )
            else:
                feature_name = str(feature)

            st.markdown(f"⭐ {feature_name}")

    else:
        st.info(
            "Complete your farmer profile and current farm information "
            "to receive personalized recommendations."
        )


    # ============================================================
# SMART FARM AI — CURRENT FARM SELECTOR
# ============================================================

if active_farms:

    farm_options = {
        farm.get("farm_name", f"Farm {i + 1}"): farm
        for i, farm in enumerate(active_farms)
    }

    selected_farm_name = st.selectbox(
        "🌱 Select Current Farm",
        list(farm_options.keys()),
        index=list(farm_options.keys()).index(
            current_farm.get("farm_name")
        ) if current_farm and current_farm.get("farm_name") in farm_options else 0,
        key="current_farm_selector"
    )

    selected_farm = farm_options[selected_farm_name]

    if (
        st.session_state.get("current_farm_id")
        != selected_farm.get("farm_id")
    ):
        st.session_state.current_farm_id = selected_farm.get("farm_id")
        st.session_state.current_farm = selected_farm

        # Rebuild personalization immediately
        personalized_profile = dict(farmer_profile)
        personalized_profile.update({
            "current_farm_id": selected_farm.get("farm_id"),
            "current_farm_name": selected_farm.get("farm_name"),
            "current_crop": selected_farm.get("crop_type"),
            "current_location": selected_farm.get("location"),
            "current_farm_type": selected_farm.get("farm_type"),
            "current_farm_size": selected_farm.get("farm_size"),
            "crop_type": selected_farm.get("crop_type"),
            "location": selected_farm.get("location"),
            "farm_type": selected_farm.get("farm_type"),
            "farm_size": selected_farm.get("farm_size"),
        })

        st.session_state.personalized_profile = personalized_profile

        recommended_features = recommend_features(
            SMART_FARM_FEATURES,
            personalized_profile
        )

        st.rerun()    



# ============================================================
# SMART FARM AI — PRECISION AGRICULTURE ENGINE
# ============================================================

def precision_agriculture_analysis(farm, farmer_profile):
    """
    Precision Agriculture (PA) engine.

    Uses the selected/current farm and farmer profile to generate
    farm-specific recommendations, priorities, and alerts.
    """

    farm = farm if isinstance(farm, dict) else {}
    farmer_profile = farmer_profile if isinstance(farmer_profile, dict) else {}

    crop = str(
        farm.get("crop_type")
        or farmer_profile.get("crop_type")
        or "Not specified"
    ).strip()

    location = str(
        farm.get("location")
        or farmer_profile.get("location")
        or "Not specified"
    ).strip()

    farm_type = str(
        farm.get("farm_type")
        or farmer_profile.get("farm_type")
        or "Not specified"
    ).strip()

    farm_size = str(
        farm.get("farm_size")
        or farmer_profile.get("farm_size")
        or "Not specified"
    ).strip()

    experience = str(
        farmer_profile.get("experience")
        or "Not specified"
    ).strip()

    crop_lower = crop.lower()
    farm_type_lower = farm_type.lower()

    recommendations = []
    alerts = []

    # --------------------------------------------------------
    # CORE PRECISION AGRICULTURE RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations.append(
        f"Monitor {crop} field conditions regularly and make decisions "
        "based on the actual condition of the farm."
    )

    recommendations.append(
        "Use soil moisture information to improve irrigation timing "
        "and reduce unnecessary water use."
    )

    recommendations.append(
        "Apply fertilizer according to crop needs and soil conditions "
        "rather than using the same rate across the entire farm."
    )

    recommendations.append(
        "Monitor crop health early so disease, pest, or nutrient problems "
        "can be detected before they spread."
    )

    recommendations.append(
        "Use weather and climate information when planning irrigation, "
        "fertilizer application, spraying, and other farm activities."
    )

    recommendations.append(
        "Record farm observations and yield results so future decisions "
        "can become more accurate and data-driven."
    )

    # --------------------------------------------------------
    # CROP-SPECIFIC GUIDANCE
    # --------------------------------------------------------

    crop_rules = {
        "maize": [
            "Monitor maize for nutrient deficiency, especially nitrogen deficiency.",
            "Track soil moisture carefully during establishment and grain development.",
            "Monitor for fall armyworm and other major maize pests."
        ],
        "corn": [
            "Monitor corn for nutrient deficiency, especially nitrogen deficiency.",
            "Track soil moisture during establishment and grain development.",
            "Inspect plants regularly for pest and disease pressure."
        ],
        "cassava": [
            "Monitor cassava for mosaic disease, bacterial blight, and pest damage.",
            "Inspect leaves and stems regularly for abnormal symptoms.",
            "Monitor soil moisture during establishment and periods of water stress."
        ],
        "rice": [
            "Monitor field water conditions carefully and avoid unnecessary irrigation.",
            "Watch for rice diseases and pest pressure during critical growth stages.",
            "Use weather information when planning fertilizer and crop protection activities."
        ],
        "tomato": [
            "Monitor tomato leaves and fruits frequently for disease and pest symptoms.",
            "Avoid excessive irrigation and monitor soil moisture.",
            "Use weather information to reduce disease risk during wet periods."
        ],
        "yam": [
            "Monitor yam vines and leaves for disease and pest symptoms.",
            "Maintain appropriate soil moisture without prolonged waterlogging.",
            "Monitor nutrient conditions during important growth stages."
        ]
    }

    for key, rules in crop_rules.items():
        if key in crop_lower:
            recommendations.extend(rules)
            break

    # --------------------------------------------------------
    # FARM-TYPE GUIDANCE
    # --------------------------------------------------------

    if "crop" in farm_type_lower:
        recommendations.append(
            "Prioritize field-level monitoring of soil, crop health, "
            "water, weather, pests, and yield."
        )

    elif "mixed" in farm_type_lower:
        recommendations.append(
            "Consider interactions between crop production, livestock "
            "resources, soil fertility, water, and farm economics."
        )

    elif "livestock" in farm_type_lower:
        recommendations.append(
            "Use environmental monitoring to support animal comfort, "
            "water availability, feed planning, and farm productivity."
        )

    # --------------------------------------------------------
    # EXPERIENCE-BASED GUIDANCE
    # --------------------------------------------------------

    if experience.lower() == "beginner":
        recommendations.append(
            "Start with simple measurements such as soil moisture, "
            "weather conditions, crop health, and farm records."
        )

    elif experience.lower() in ["experienced", "professional"]:
        recommendations.append(
            "Use historical farm records and sensor data to identify "
            "patterns and improve field-level decision making."
        )

    # --------------------------------------------------------
    # PRECISION AGRICULTURE ALERTS
    # --------------------------------------------------------

    if crop == "Not specified":
        alerts.append(
            "Crop information is missing. Add the crop for more precise "
            "agricultural recommendations."
        )

    if location == "Not specified":
        alerts.append(
            "Farm location is missing. Add the location to improve "
            "weather, climate, and regional recommendations."
        )

    if farm_size == "Not specified":
        alerts.append(
            "Farm size is missing. Add farm size to improve resource "
            "and productivity calculations."
        )

    # --------------------------------------------------------
    # PRIORITY ACTIONS
    # --------------------------------------------------------

    priority_actions = [
        "Monitor soil moisture",
        "Monitor crop health",
        "Check weather conditions",
        "Review irrigation needs",
        "Review fertilizer needs",
        "Record farm observations",
        "Monitor pests and diseases"
    ]

    return {
        "farm": farm,
        "crop": crop,
        "location": location,
        "farm_type": farm_type,
        "farm_size": farm_size,
        "experience": experience,
        "recommendations": recommendations,
        "alerts": alerts,
        "priority_actions": priority_actions
    }


# ------------------------------------------------------------
# RUN PRECISION AGRICULTURE FOR THE CURRENT FARM
# ------------------------------------------------------------

current_farm = st.session_state.get("current_farm", {})
personalized_profile = st.session_state.get(
    "personalized_profile",
    farmer_profile
)

pa_analysis = precision_agriculture_analysis(
    current_farm,
    personalized_profile
)

st.session_state.pa_analysis = pa_analysis


# ============================================================
# SMART FARM AI — GREEN CHLOROPHYLL INDEX (CIG) ENGINE
# ============================================================

def calculate_cig(near_infrared, green):
    """
    Green Chlorophyll Index (CIG).

    CIG = (NIR / Green) - 1

    Used with suitable multispectral/remote-sensing data
    to estimate relative vegetation chlorophyll condition.
    """

    try:
        nir = float(near_infrared)
        green_band = float(green)

        if green_band <= 0:
            return None

        return (nir / green_band) - 1

    except (TypeError, ValueError):
        return None


def chlorophyll_status(cig_value):
    """Convert CIG into a simple farm interpretation."""

    if cig_value is None:
        return "Data unavailable"

    if cig_value < 1:
        return "Low chlorophyll signal"

    if cig_value < 2:
        return "Moderate chlorophyll signal"

    return "Healthy chlorophyll signal"


def green_chlorophyll_analysis(farm, farmer_profile):
    """
    CIG intelligence layer.

    Uses the current farm context and prepares the platform
    for future drone/satellite/multispectral measurements.
    """

    farm = farm if isinstance(farm, dict) else {}
    farmer_profile = (
        farmer_profile
        if isinstance(farmer_profile, dict)
        else {}
    )

    crop = str(
        farm.get("crop_type")
        or farmer_profile.get("crop_type")
        or "Not specified"
    )

    location = str(
        farm.get("location")
        or farmer_profile.get("location")
        or "Not specified"
    )

    recommendations = [
        "Monitor vegetation colour and crop vigour regularly.",
        "Investigate areas showing weaker crop growth or unusual colour.",
        "Compare crop condition across different areas of the farm.",
        "Use multispectral drone or satellite data when available "
        "to improve chlorophyll assessment.",
        "Combine chlorophyll information with soil, weather, irrigation, "
        "and crop-health data before making management decisions."
    ]

    alerts = []

    if crop == "Not specified":
        alerts.append(
            "Crop information is required for more meaningful "
            "chlorophyll interpretation."
        )

    return {
        "crop": crop,
        "location": location,
        "cig": None,
        "status": "Waiting for multispectral data",
        "recommendations": recommendations,
        "alerts": alerts
    }


# ------------------------------------------------------------
# RUN CIG FOR THE CURRENT FARM
# ------------------------------------------------------------

current_farm = st.session_state.get("current_farm", {})
personalized_profile = st.session_state.get(
    "personalized_profile",
    farmer_profile
)

cig_analysis = green_chlorophyll_analysis(
    current_farm,
    personalized_profile
)

st.session_state.cig_analysis = cig_analysis


# ============================================================
# SMART FARM AI — CLIMATE-SMART AGRICULTURE (CSA) ENGINE
# ============================================================

def climate_smart_agriculture_analysis(farm, farmer_profile):
    """
    Climate-Smart Agriculture engine.

    Connects farm context with climate-aware recommendations,
    risk management, productivity, and resource efficiency.
    """

    farm = farm if isinstance(farm, dict) else {}

    farmer_profile = (
        farmer_profile
        if isinstance(farmer_profile, dict)
        else {}
    )

    crop = str(
        farm.get("crop_type")
        or farmer_profile.get("crop_type")
        or "Not specified"
    ).strip()

    location = str(
        farm.get("location")
        or farmer_profile.get("location")
        or "Not specified"
    ).strip()

    farm_type = str(
        farm.get("farm_type")
        or farmer_profile.get("farm_type")
        or "Not specified"
    ).strip()

    recommendations = [
        "Use weather and seasonal information when planning farm activities.",
        "Improve water efficiency by matching irrigation with crop needs "
        "and soil moisture.",
        "Protect soil through appropriate soil-management and erosion-control practices.",
        "Adjust planting and farm operations when climate conditions create increased risk.",
        "Monitor crop health early so climate-related stress can be detected quickly.",
        "Use farm records to compare productivity, resource use, and climate conditions over time.",
        "Combine weather, soil, crop, irrigation, disease, and yield information "
        "for better climate-aware decisions."
    ]

    climate_risks = [
        "Drought and water stress",
        "Excess rainfall and flooding",
        "Heat stress",
        "Changing pest and disease pressure",
        "Soil degradation and erosion"
    ]

    adaptation_actions = [
        "Improve irrigation efficiency",
        "Protect soil moisture",
        "Monitor weather before major farm operations",
        "Strengthen crop-health monitoring",
        "Use farm records to identify climate-related production changes"
    ]

    alerts = []

    if crop == "Not specified":
        alerts.append(
            "Add a crop to receive more specific climate-smart recommendations."
        )

    if location == "Not specified":
        alerts.append(
            "Add the farm location to improve climate and seasonal guidance."
        )

    return {
        "crop": crop,
        "location": location,
        "farm_type": farm_type,
        "recommendations": recommendations,
        "climate_risks": climate_risks,
        "adaptation_actions": adaptation_actions,
        "alerts": alerts
    }


# ------------------------------------------------------------
# RUN CSA FOR THE CURRENT FARM
# ------------------------------------------------------------

current_farm = st.session_state.get("current_farm", {})

personalized_profile = st.session_state.get(
    "personalized_profile",
    farmer_profile
)

csa_analysis = climate_smart_agriculture_analysis(
    current_farm,
    personalized_profile
)

st.session_state.csa_analysis = csa_analysis

# ============================================================
# 🌾 FARM SELECTION & MULTI-FARM MANAGEMENT
# ============================================================

if st.session_state.get("logged_in", False):

    st.subheader("🌾 My Farms")

    current_username = st.session_state.get(
        "current_user",
        ""
    )

    # ========================================================
    # 💾 LOAD CURRENT USER PROFILE FROM ACCOUNT
    # ========================================================

    users = _load(
        "accounts.json",
        []
    )

    if not isinstance(users, list):
        users = []

    current_user_data = None

    for user in users:
        if (
            isinstance(user, dict)
            and user.get("username") == current_username
        ):
            current_user_data = user
            break

    if current_user_data is not None:

        farmer_profile = current_user_data.get(
            "profile",
            {}
        )

        if not isinstance(farmer_profile, dict):
            farmer_profile = {}

        # Keep session profile synchronized
        st.session_state.farmer_profile = farmer_profile

    else:

        farmer_profile = st.session_state.get(
            "farmer_profile",
            {}
        )

        if not isinstance(farmer_profile, dict):
            farmer_profile = {}

    # ========================================================
    # 🌾 GET ALL FARMS
    # ========================================================

    farms = farmer_profile.get(
        "farms",
        []
    )

    if not isinstance(farms, list):
        farms = []

    # ========================================================
    # 🏡 CREATE MAIN FARM FROM REGISTRATION
    # ========================================================

    if not farms:

        registered_crop = str(
            farmer_profile.get(
                "crop_type",
                ""
            )
        ).strip()

        registered_location = str(
            farmer_profile.get(
                "location",
                ""
            )
        ).strip()

        if registered_crop or registered_location:

            main_farm = {
                "farm_name": "Main Farm",
                "location": registered_location,
                "crop_type": registered_crop,
                "farm_type": farmer_profile.get(
                    "farm_type",
                    ""
                ),
                "status": "active"
            }

            farms.append(main_farm)

            farmer_profile["farms"] = farms

            st.session_state.farmer_profile = (
                farmer_profile
            )

            # Save Main Farm
            if current_user_data is not None:

                current_user_data["profile"] = (
                    farmer_profile
                )

                _save(
                    "accounts.json",
                    users
                )

    # ========================================================
    # 🟢 NORMALIZE FARM STATUS
    # ========================================================

    for farm in farms:

        if not isinstance(farm, dict):
            continue

        if farm.get("status") not in [
            "active",
            "archived"
        ]:
            farm["status"] = "active"

    farmer_profile["farms"] = farms

    st.session_state.farmer_profile = (
        farmer_profile
    )

    # ========================================================
    # 🟢 ACTIVE FARM
    # ========================================================

    active_farms = [
        farm
        for farm in farms
        if isinstance(farm, dict)
        and farm.get("status", "active") == "active"
    ]

    # ========================================================
    # 📦 ARCHIVED FARMS
    # ========================================================

    archived_farms = [
        farm
        for farm in farms
        if isinstance(farm, dict)
        and farm.get("status") == "archived"
    ]

    # ========================================================
    # 🟢 ACTIVE FARM NAVIGATION
    # ========================================================

    st.subheader("⛔️ Active Farms")

    if active_farms:

        active_farm_names = [
            farm.get(
                "farm_name",
                f"Farm {i + 1}"
            )
            for i, farm in enumerate(active_farms)
        ]

        selected_farm_name = st.selectbox(
            "📍 Select Farm to Manage",
            active_farm_names,
            key="selected_active_farm_unique_005"
        )

        selected_farm = next(
            (
                farm
                for farm in active_farms
                if farm.get("farm_name")
                == selected_farm_name
            ),
            None
        )

        if selected_farm:

            # =================================================
            # 🌾 CURRENT FARM
            # =================================================

            st.session_state.current_farm = (
                selected_farm
            )

            st.success(
                f"🌾 Currently managing: "
                f"{selected_farm.get('farm_name', 'Farm')}"
            )

            st.write(
                f"🌱 Crop: "
                f"{selected_farm.get('crop_type', 'Not specified')}"
            )

            st.write(
                f"📍 Location: "
                f"{selected_farm.get('location', 'Not specified')}"
            )

            st.write(
                f"🌾 Farm Type: "
                f"{selected_farm.get('farm_type', 'Not specified')}"
            )

            # =================================================
            # 🧠 FARM-SPECIFIC PERSONALIZATION
            # =================================================

            personalization_profile = (
                farmer_profile.copy()
            )

            personalization_profile["crop_type"] = str(
                selected_farm.get(
                    "crop_type",
                    ""
                )
            ).lower().strip()

            personalization_profile["location"] = str(
                selected_farm.get(
                    "location",
                    ""
                )
            ).lower().strip()

            personalization_profile["farm_type"] = str(
                selected_farm.get(
                    "farm_type",
                    farmer_profile.get(
                        "farm_type",
                        ""
                    )
                )
            ).lower().strip()

            recommended_features = recommend_features(
                SMART_FARM_FEATURES,
                personalization_profile
            )

            st.session_state.recommended_features = (
                recommended_features
            )

            # =================================================
            # 📦 ARCHIVE CURRENT FARM
            # =================================================

            if st.button(
                "📦 Archive This Farm",
                key="archive_farm_unique_005",
                use_container_width=True
            ):

                selected_farm["status"] = "archived"

                farmer_profile["farms"] = farms

                st.session_state.farmer_profile = (
                    farmer_profile
                )

                # Save to account
                if current_user_data is not None:

                    current_user_data["profile"] = (
                        farmer_profile
                    )

                    _save(
                        "accounts.json",
                        users
                    )

                st.session_state.current_farm = None

                st.success(
                    f"📦 {selected_farm_name} "
                    "has been archived."
                )

                st.rerun()

    else:

        st.info(
            "No active farms yet. Add a farm below."
        )

        # ========================================================
    # ➕ ADD ANOTHER FARM
    # ========================================================

    st.subheader("➕ Add Another Farm")

    with st.expander(
        "➕ Add New Farm",
        expanded=True
    ):

        new_farm_name = st.text_input(
            "Farm Name",
            key="new_farm_name_unique_005"
        )

        new_farm_location = st.text_input(
            "Farm Location",
            key="new_farm_location_unique_005"
        )

        new_farm_crop = st.text_input(
            "Crop Type",
            key="new_farm_crop_unique_005"
        )

        new_farm_type = st.selectbox(
            "Farm Type",
            [
                "Crop Farming",
                "Livestock Farming",
                "Mixed Farming",
                "Aquaculture",
                "Urban Farming"
            ],
            key="new_farm_type_unique_005"
        )

        if st.button(
            "➕ Add Farm",
            key="add_farm_button_unique_005",
            use_container_width=True
        ):

            if not new_farm_name.strip():

                st.warning(
                    "Please enter a farm name."
                )

            elif not new_farm_crop.strip():

                st.warning(
                    "Please enter the crop type."
                )

            else:

                existing_names = [
                    str(
                        farm.get(
                            "farm_name",
                            ""
                        )
                    ).lower().strip()
                    for farm in farms
                    if isinstance(farm, dict)
                ]

                if (
                    new_farm_name.lower().strip()
                    in existing_names
                ):

                    st.error(
                        "A farm with this name already exists."
                    )

                else:

                    new_farm = {
                        "farm_name": new_farm_name.strip(),
                        "location": new_farm_location.strip(),
                        "crop_type": new_farm_crop.strip(),
                        "farm_type": new_farm_type,
                        "status": "active"
                    }

                    # Add to farm list
                    farms.append(new_farm)

                    farmer_profile["farms"] = farms

                    st.session_state.farmer_profile = (
                        farmer_profile
                    )

                    st.session_state.current_farm = (
                        new_farm
                    )

                    # =========================================
                    # 💾 SAVE FARM TO CURRENT ACCOUNT
                    # =========================================

                    if current_user_data is not None:

                        current_user_data["profile"] = (
                            farmer_profile
                        )

                        _save(
                            "accounts.json",
                            users
                        )

                    # =========================================
                    # 🧠 CALCULATE RECOMMENDATION
                    # FOR THE NEW FARM
                    # =========================================

                    new_personalization_profile = (
                        farmer_profile.copy()
                    )

                    new_personalization_profile[
                        "crop_type"
                    ] = new_farm["crop_type"].lower().strip()

                    new_personalization_profile[
                        "location"
                    ] = new_farm["location"].lower().strip()

                    new_personalization_profile[
                        "farm_type"
                    ] = new_farm["farm_type"].lower().strip()

                    recommended_features = (
                        recommend_features(
                            SMART_FARM_FEATURES,
                            new_personalization_profile
                        )
                    )

                    st.session_state.recommended_features = (
                        recommended_features
                    )

                    st.success(
                        f"✅ {new_farm['farm_name']} "
                        "added successfully!"
                    )

                    st.rerun()

    # ========================================================
    # 📋 SHOW ACTIVE FARM LIST
    # ========================================================

    if active_farms:

        st.subheader("📋 Your Active Farms")

        for i, farm in enumerate(active_farms):

            st.write(
                f"🟢 {farm.get('farm_name', f'Farm {i + 1}')} "
                f"— 🌱 {farm.get('crop_type', 'Unknown crop')} "
                f"— 📍 {farm.get('location', 'Unknown location')}"
            )

    # ========================================================
    # 📦 ARCHIVED FARMS
    # ========================================================

    st.subheader("📦 Archived Farms")

    if archived_farms:

        archived_names = [
            farm.get(
                "farm_name",
                f"Archived Farm {i + 1}"
            )
            for i, farm in enumerate(archived_farms)
        ]

        archived_selected_name = st.selectbox(
            "Select Archived Farm",
            archived_names,
            key="archived_farm_unique_005"
        )

        archived_farm = next(
            (
                farm
                for farm in archived_farms
                if farm.get("farm_name")
                == archived_selected_name
            ),
            None
        )

        if archived_farm:

            st.write(
                f"🌱 Crop: "
                f"{archived_farm.get('crop_type', 'Not specified')}"
            )

            st.write(
                f"📍 Location: "
                f"{archived_farm.get('location', 'Not specified')}"
            )

            # =================================================
            # 🔄 RESTORE
            # =================================================

            if st.button(
                "🔄 Restore Farm",
                key="restore_farm_unique_005",
                use_container_width=True
            ):

                archived_farm["status"] = "active"

                farmer_profile["farms"] = farms

                st.session_state.farmer_profile = (
                    farmer_profile
                )

                if current_user_data is not None:

                    current_user_data["profile"] = (
                        farmer_profile
                    )

                    _save(
                        "accounts.json",
                        users
                    )

                st.success(
                    f"🟢 {archived_selected_name} "
                    "restored successfully!"
                )

                st.rerun()

            # =================================================
            # 🗑 PERMANENT DELETE
            # =================================================

            if st.button(
                "🗑 Permanently Delete Farm",
                key="delete_farm_unique_005",
                use_container_width=True
            ):

                farms = [
                    farm
                    for farm in farms
                    if farm.get("farm_name")
                    != archived_selected_name
                ]

                farmer_profile["farms"] = farms

                st.session_state.farmer_profile = (
                    farmer_profile
                )

                if current_user_data is not None:

                    current_user_data["profile"] = (
                        farmer_profile
                    )

                    _save(
                        "accounts.json",
                        users
                    )

                st.session_state.current_farm = None

                st.success(
                    f"🗑 {archived_selected_name} "
                    "deleted permanently."
                )

                st.rerun()

    else:

        st.info(
            "📦 No archived farms."
        )
     

# ============================================================
# ⭐ RECOMMENDED FEATURES
# ============================================================

if st.session_state.get("logged_in", False):

    st.subheader("⭐ Recommended for You")

    for feature in recommended_features:

        if isinstance(feature, dict):

            feature_name = feature.get(
                "name",
                feature.get("Name", "Feature")
            )

        else:

            feature_name = str(feature)

        st.write(f"⭐ {feature_name}")



import streamlit as st

import json

import hashlib

import pandas as pd

import random

import datetime

from pathlib import Path

from datetime import date, datetime, timedelta





# =========================

# Helpers

# =========================

def _load(path, default):

    p = Path(path)

    if not p.exists():

        return default

    try:

        return json.loads(p.read_text(encoding="utf-8"))

    except Exception:

        return default



def _save(path, data):

    Path(path).write_text(json.dumps(data, indent=4), encoding="utf-8")



# =========================

# Optional Auth Utilities (unused UI in this file but kept for future)

# =========================

def hash_password(password: str) -> str:

    return hashlib.sha256(password.encode()).hexdigest()



# =========================

# FARM MANAGEMENT FEATURES

# =========================

def user_account_management_ui():
    st.subheader("👤 User Account Management")

    action = st.radio("Choose Action", ["Register", "Login"], key="acc_action")

    if action == "Register":
        username = st.text_input("Username", key="reg_username")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_password")

        if st.button("Register", key="reg_btn"):
            users = _load("accounts.json", [])
            if any(u["username"] == username for u in users):
                st.error("❌ Username already exists.")
            else:
                users.append({
                    "username": username,
                    "email": email,
                    "password": hash_password(password)
                })
                _save("accounts.json", users)
                st.success("✅ Registration successful!")

    elif action == "Login":
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        if st.button("Login", key="login_btn"):
            users = _load("accounts.json", [])
            user = next((u for u in users if u["username"] == username), None)
            if user and user["password"] == hash_password(password):
                st.success(f"✅ Welcome back, {username}!")
                st.session_state["logged_in"] = True
            else:
                st.error("❌ Invalid username or password.")


# Optional: a simple v2 UI for the "upgrade" router with unique keys
def user_account_management_ui_v2():
    st.subheader("👤 User Account Management (v2)")
    username = st.text_input("Username", key=k2("acc_username"))
    email = st.text_input("Email", key=k2("acc_email"))
    if st.button("Save Account", key=k2("acc_save_btn")):
        _save("account.json", {"username": username, "email": email})
        st.success("✅ Account saved.")

 # ============================================================
# SMART FARM AI — FARM MANAGEMENT
# ============================================================

def farm_management_ui():

    st.subheader("🌿 Farm Management")

    farmer_profile = st.session_state.get(
        "farmer_profile",
        {}
    )

    if not isinstance(farmer_profile, dict):
        farmer_profile = {}

    farms = farmer_profile.get("farms", [])

    if not isinstance(farms, list):
        farms = []

    # ========================================================
    # ADD NEW FARM
    # ========================================================

    st.markdown("### ➕ Add New Farm")

    with st.form("add_farm_form"):

        farm_name = st.text_input(
            "🌱 Farm Name",
            placeholder="e.g. Main Farm"
        )

        crop_type = st.text_input(
            "🌾 Main Crop",
            placeholder="e.g. Maize"
        )

        location = st.text_input(
            "📍 Farm Location",
            placeholder="e.g. Anambra, Nigeria"
        )

        farm_type = st.selectbox(
            "🚜 Farm Type",
            [
                "Crop Farming",
                "Livestock Farming",
                "Mixed Farming",
                "Aquaculture",
                "Urban Farming"
            ]
        )

        farm_size = st.text_input(
            "📊 Farm Size",
            placeholder="e.g. 5 hectares"
        )

        add_farm = st.form_submit_button(
            "➕ Add Farm"
        )

    if add_farm:

        if not farm_name.strip():

            st.error("Please enter a farm name.")

        else:

            farm_id = (
                "farm_"
                + str(len(farms) + 1)
                + "_"
                + str(abs(hash(farm_name)))
            )

            new_farm = {
                "farm_id": farm_id,
                "farm_name": farm_name.strip(),
                "crop_type": crop_type.strip(),
                "location": location.strip(),
                "farm_type": farm_type,
                "farm_size": farm_size.strip(),
                "status": "active"
            }

            farms.append(new_farm)

            farmer_profile["farms"] = farms

            st.session_state.farmer_profile = farmer_profile

            # Automatically make the new farm current
            st.session_state.current_farm_id = farm_id
            st.session_state.current_farm = new_farm

            personalized_profile = dict(farmer_profile)

            personalized_profile.update({
                "current_farm_id": farm_id,
                "current_farm_name": farm_name.strip(),
                "current_crop": crop_type.strip(),
                "current_location": location.strip(),
                "current_farm_type": farm_type,
                "current_farm_size": farm_size.strip(),
                "crop_type": crop_type.strip(),
                "location": location.strip(),
                "farm_type": farm_type,
                "farm_size": farm_size.strip()
            })

            st.session_state.personalized_profile = (
                personalized_profile
            )

            recommended_features = recommend_features(
                SMART_FARM_FEATURES,
                personalized_profile
            )

            st.session_state.recommended_features = (
                recommended_features
            )

            st.success(
                f"✅ {farm_name.strip()} has been added "
                "and selected as your current farm."
            )

            st.rerun()

    st.divider()

    # ========================================================
    # EXISTING FARMS
    # ========================================================

    st.markdown("### 🌾 My Farms")

    active_farms = [
        farm for farm in farms
        if str(
            farm.get("status", "active")
        ).lower() == "active"
    ]

    if not active_farms:

        st.info(
            "No farms have been added yet. "
            "Use the form above to add your first farm."
        )

    else:
        for farm in active_farms:

            farm_name_display = farm.get(
                "farm_name",
                "Unnamed Farm"
            )

            crop_display = farm.get(
                "crop_type",
                "Not specified"
            )

            location_display = farm.get(
                "location",
                "Not specified"
            )

            farm_type_display = farm.get(
                "farm_type",
                "Not specified"
            )

            farm_size_display = farm.get(
                "farm_size",
                "Not specified"
            )

            farm_id = farm.get(
                "farm_id"
            )

            st.markdown(
                f"### 🌱 {farm_name_display}"
            )

            f1, f2, f3, f4 = st.columns(4)

            with f1:
                st.write(
                    f"🌾 Crop: {crop_display}"
                )

            with f2:
                st.write(
                    f"📍 Location: {location_display}"
                )

            with f3:
                st.write(
                    f"🚜 Type: {farm_type_display}"
                )

            with f4:
                st.write(
                    f"📊 Size: {farm_size_display}"
                )

            if (
                st.session_state.get(
                    "current_farm_id"
                ) == farm_id
            ):

                st.success(
                    "🟢 Current Farm"
                )

            else:

                if st.button(
                    "🌱 Select This Farm",
                    key=f"select_farm_{farm_id}"
                ):

                    st.session_state.current_farm_id = farm_id
                    st.session_state.current_farm = farm

                    personalized_profile = dict(
                        farmer_profile
                    )

                    personalized_profile.update({
                        "current_farm_id": farm_id,
                        "current_farm_name": farm.get(
                            "farm_name"
                        ),
                        "current_crop": farm.get(
                            "crop_type"
                        ),
                        "current_location": farm.get(
                            "location"
                        ),
                        "current_farm_type": farm.get(
                            "farm_type"
                        ),
                        "current_farm_size": farm.get(
                            "farm_size"
                        ),
                        "crop_type": farm.get(
                            "crop_type"
                        ),
                        "location": farm.get(
                            "location"
                        ),
                        "farm_type": farm.get(
                            "farm_type"
                        ),
                        "farm_size": farm.get(
                            "farm_size"
                        )
                    })

                    st.session_state.personalized_profile = (
                        personalized_profile
                    )

                    st.session_state.recommended_features = (
                        recommend_features(
                            SMART_FARM_FEATURES,
                            personalized_profile
                        )
                    )

                    st.success(
                        f"✅ {farm_name_display} "
                        "is now your current farm."
                    )

                    st.rerun()


# =========================================================
# FARM PLOT MAPPING — CONSOLIDATED
# =========================================================

def farm_plot_mapping_ui():

    st.header("🌍 Farm Plot Mapping")

    # ---------------------------------------------------------
    # CURRENT FARM CONTEXT
    # ---------------------------------------------------------

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(current_farm, dict):
        current_farm = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_farm_id = current_farm.get(
        "farm_id",
        "main_farm"
    )

    current_farm_name = current_farm.get(
        "farm_name",
        personalized_profile.get(
            "current_farm_name",
            "Main Farm"
        )
    )

    current_crop = current_farm.get(
        "crop_type",
        personalized_profile.get(
            "crop_type",
            "Not specified"
        )
    )

    current_location = current_farm.get(
        "location",
        personalized_profile.get(
            "location",
            "Not specified"
        )
    )

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # =========================================================
    # FARM PLOT MAPPING
    # =========================================================

    plot_option = st.sidebar.selectbox(
        "🌍 Select a Farm Plot Feature",
        [
            "➕ Add New Farm Plot",
            "📋 View Mapped Plots",
            "🗑 Manage Plots",
            "⬇️ Download Plots CSV"
        ],
        key="farm_plot_feature"
    )

    # =========================================================
    # LOAD PLOTS
    # =========================================================

    plots = _load(
        "plots.json",
        []
    )

    if not isinstance(
        plots,
        list
    ):
        plots = []

    # Keep only plots belonging to the current farm.
    # Older plots without farm_id remain available to Main Farm.
    farm_plots = [
        plot
        for plot in plots
        if str(
            plot.get(
                "farm_id",
                "main_farm"
            )
        ) == str(current_farm_id)
    ]

    # =========================================================
    # 1. ADD NEW FARM PLOT
    # =========================================================

    if plot_option == "➕ Add New Farm Plot":

        st.subheader("➕ Add New Farm Plot")

        with st.form(
            "farm_plot_add_form",
            clear_on_submit=True
        ):

            plot_name = st.text_input(
                "Plot Name",
                key="farm_plot_name"
            )

            plot_size = st.number_input(
                "Plot Size (hectares)",
                min_value=0.1,
                step=0.1,
                key="farm_plot_size"
            )

            plot_location = st.text_input(
                "Location Description",
                value=current_location
                if current_location != "Not specified"
                else "",
                key="farm_plot_location"
            )

            plot_crop = st.selectbox(
                "Crop Planted",
                [
                    "Maize",
                    "Cassava",
                    "Tomato",
                    "Rice",
                    "Yam",
                    "Other"
                ],
                index=(
                    [
                        "Maize",
                        "Cassava",
                        "Tomato",
                        "Rice",
                        "Yam",
                        "Other"
                    ].index(current_crop)
                    if current_crop in [
                        "Maize",
                        "Cassava",
                        "Tomato",
                        "Rice",
                        "Yam",
                        "Other"
                    ]
                    else 0
                ),
                key="farm_plot_crop"
            )

            submitted = st.form_submit_button(
                "💾 Save Plot",
                use_container_width=True
            )

        if submitted:

            if not plot_name.strip():

                st.warning(
                    "Please enter a plot name."
                )

            else:

                new_plot = {
                    "farm_id": current_farm_id,
                    "farm_name": current_farm_name,
                    "crop_type": current_crop,
                    "location": current_location,
                    "name": plot_name.strip(),
                    "size": float(plot_size),
                    "plot_location": plot_location.strip(),
                    "crop": plot_crop
                }

                plots.append(
                    new_plot
                )

                _save(
                    "plots.json",
                    plots
                )

                st.success(
                    f"✅ Plot '{plot_name.strip()}' "
                    f"saved successfully for "
                    f"{current_farm_name}."
                )

    # =========================================================
    # 2. VIEW MAPPED PLOTS
    # =========================================================

    elif plot_option == "📋 View Mapped Plots":

        st.subheader(
            f"📋 Mapped Plots — {current_farm_name}"
        )

        if farm_plots:

            for index, plot in enumerate(
                farm_plots,
                1
            ):

                plot_name = plot.get(
                    "name",
                    plot.get(
                        "Name",
                        f"Plot {index}"
                    )
                )

                plot_size = plot.get(
                    "size",
                    plot.get(
                        "Size (ha)",
                        0
                    )
                )

                plot_location = plot.get(
                    "plot_location",
                    plot.get(
                        "Location",
                        ""
                    )
                )

                plot_crop = plot.get(
                    "crop",
                    plot.get(
                        "Crop",
                        current_crop
                    )
                )

                st.markdown(
                    f"""
### 📍 Plot {index}: {plot_name}

- 🌱 Farm: {current_farm_name}
- 🌾 Crop: {plot_crop}
- 📐 Size: {float(plot_size):,.2f} hectares
- 📍 Location: {plot_location or "Not specified"}

---
"""
                )

        else:

            st.info(
                f"No farm plots mapped for "
                f"{current_farm_name} yet."
            )

    # =========================================================
    # 3. MANAGE PLOTS
    # =========================================================

    elif plot_option == "🗑 Manage Plots":

        st.subheader(
            f"🗑 Manage Plots — {current_farm_name}"
        )

        if farm_plots:

            for index, plot in enumerate(
                farm_plots
            ):

                plot_name = plot.get(
                    "name",
                    plot.get(
                        "Name",
                        f"Plot {index + 1}"
                    )
                )

                plot_size = plot.get(
                    "size",
                    plot.get(
                        "Size (ha)",
                        0
                    )
                )

                plot_crop = plot.get(
                    "crop",
                    plot.get(
                        "Crop",
                        current_crop
                    )
                )
                with st.expander(
                    f"📌 {plot_name} • "
                    f"{plot_crop} • "
                    f"{float(plot_size):,.2f} ha"
                ):

                    plot_location = plot.get(
                        "plot_location",
                        plot.get(
                            "Location",
                            ""
                        )
                    )

                    st.write(
                        f"📍 Location: "
                        f"{plot_location or 'Not specified'}"
                    )

                    if st.button(
                        "🗑 Delete this plot",
                        key=f"farm_plot_delete_{index}"
                    ):

                        # Find the exact plot in the original
                        # plots list before deleting it.
                        target_index = None

                        for original_index, original_plot in enumerate(
                            plots
                        ):

                            if original_plot is plot:

                                target_index = original_index
                                break

                        if target_index is not None:

                            plots.pop(
                                target_index
                            )

                            _save(
                                "plots.json",
                                plots
                            )

                            st.success(
                                f"✅ Plot '{plot_name}' "
                                f"deleted."
                            )

                            st.rerun()

        else:

            st.info(
                f"No plots available to manage for "
                f"{current_farm_name}."
            )

    # =========================================================
    # 4. DOWNLOAD PLOTS CSV
    # =========================================================

    elif plot_option == "⬇️ Download Plots CSV":

        st.subheader(
            f"⬇️ Download Farm Plots — {current_farm_name}"
        )

        if farm_plots:

            import pandas as pd

            csv_data = []

            for plot in farm_plots:

                csv_data.append(
                    {
                        "Farm ID": plot.get(
                            "farm_id",
                            current_farm_id
                        ),
                        "Farm Name": plot.get(
                            "farm_name",
                            current_farm_name
                        ),
                        "Crop": plot.get(
                            "crop",
                            plot.get(
                                "Crop",
                                current_crop
                            )
                        ),
                        "Plot Name": plot.get(
                            "name",
                            plot.get(
                                "Name",
                                ""
                            )
                        ),
                        "Size (hectares)": plot.get(
                            "size",
                            plot.get(
                                "Size (ha)",
                                0
                            )
                        ),
                        "Location": plot.get(
                            "plot_location",
                            plot.get(
                                "Location",
                                ""
                            )
                        )
                    }
                )

            csv = pd.DataFrame(
                csv_data
            ).to_csv(
                index=False
            ).encode(
                "utf-8"
            )

            st.download_button(
                "⬇️ Download Plots CSV",
                csv,
                file_name="farm_plots.csv",
                mime="text/csv",
                key="farm_plot_download_csv"
            )

            st.success(
                f"✅ {len(farm_plots)} plot(s) ready "
                f"for download."
            )

        else:

            st.info(
                f"No plots available for "
                f"{current_farm_name}."
            )



def smart_fert_pest_ui():
    import streamlit as st
    import datetime

    st.subheader("🌾 Smart Fertilizer & Pesticide Stock Manager")

    # safe load/save wrappers if you have _load/_save helpers
    def _safe_load(path, default):
        try:
            return _load(path, default)
        except Exception as e:
            st.warning(f"Could not load {path}: {e}")
            return default

    def _safe_save(path, data):
        try:
            _save(path, data)
            return True
        except Exception as e:
            st.error(f"Save failed: {e}")
            return False

    inv = _safe_load("chem_inventory.json", [])

    base = "smart_fert_pest"
    form_key = f"{base}_form"
    item_key = f"{base}_item"
    qty_key = f"{base}_qty"
    submit_key = f"{base}_submit"

    with st.form(form_key):
        item = st.text_input("Item (Fertilizer/Pesticide)", key=item_key)
        qty = st.number_input("Quantity", min_value=0, step=1, key=qty_key)
        # compatibility: some Streamlit versions don't accept key= on form_submit_button
        try:
            submitted = st.form_submit_button("Save Stock", key=submit_key)
        except TypeError:
            submitted = st.form_submit_button("Save Stock")

    if submitted:
        if not (item or "").strip():
            st.warning("Enter an item name before saving.")
        else:
            inv.append({"item": item.strip(), "qty": int(qty), "date": str(datetime.date.today())})
            _safe_save("chem_inventory.json", inv)
            st.success(f"✅ {qty} units of {item} saved.")

    if inv:
        st.markdown("### 📦 Current Stock")
        for it in inv:
            i = it.get("item") if isinstance(it, dict) else str(it)
            q = it.get("qty") if isinstance(it, dict) else ""
            d = it.get("date") if isinstance(it, dict) else ""
            st.write(f"- {i}: {q} (as of {d})")
    else:
        st.info("No fertilizer/pesticide stock records yet.")


def smart_tutor_voice():
    import streamlit as st
    import os
    from datetime import datetime

    # Optional deps (gracefully handled)
    try:
        import speech_recognition as sr
    except Exception:
        sr = None
    try:
        import pyttsx3
    except Exception:
        pyttsx3 = None
    try:
        from gtts import gTTS
    except Exception:
        gTTS = None

    st.subheader("🧑‍🏫 Smart Tutor Multilanguage")
    st.info("🌍 Learn agriculture tips in multiple African languages (via text or voice).")

    # Available languages
    languages = [
        "English", "Yoruba", "Igbo", "Hausa", "Urhobo",
        "Ijaw", "Efik", "Ibibio", "Tiv", "Kanuri"
    ]
    lang_choice = st.selectbox("Select a language", languages, key="tutor_lang")

    # --- Input options ---
    st.markdown("**🎤 Speak or ✍️ Type your agriculture question**")

    # 1. Voice input
    voice_question = None
    if sr and st.button("🎙 Record Question", key="tutor_record"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... please speak now.")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        try:
            voice_question = recognizer.recognize_google(audio)
            st.success(f"✅ You said: {voice_question}")
        except Exception as e:
            st.error(f"Voice recognition failed: {e}")

    # 2. Text input
    text_question = st.text_input("Or type your question here:", key="tutor_text")

    # Use whichever question is available
    final_question = voice_question if voice_question else text_question

    # --- Answer button ---
    if st.button("Get Answer", key="tutor_btn"):
        if final_question and final_question.strip():
            # Simulated agricultural responses (you can expand this later with AI)
            if "fertilizer" in final_question.lower():
                answer = "Use organic compost or NPK fertilizer depending on soil needs."
            elif "water" in final_question.lower() or "irrigation" in final_question.lower():
                answer = "Irrigate crops early in the morning or late evening to reduce evaporation."
            else:
                answer = "Practice crop rotation, weed control, and proper spacing for better yields."

            # Add a language flavor
            if lang_choice == "Yoruba":
                answer = "Agbẹ́! " + answer
            elif lang_choice == "Igbo":
                answer = "Ndi ugbo! " + answer
            elif lang_choice == "Hausa":
                answer = "Manomi! " + answer

            st.success(f"({lang_choice}) {answer}")

            # Voice playback if possible
            if pyttsx3:
                engine = pyttsx3.init()
                engine.say(answer)
                engine.runAndWait()
            elif gTTS:
                try:
                    tts = gTTS(answer)
                    filename = "tutor_voice.mp3"
                    tts.save(filename)
                    audio_file = open(filename, "rb")
                    st.audio(audio_file.read(), format="audio/mp3")
                except Exception as e:
                    st.warning(f"Text-to-speech failed: {e}")
        else:
            st.warning("❌ Please ask a question by typing or speaking.")

#Ai crop calendar
def ai_crop_calendar_ui():
    st.header("🤖 AI Crop Calendar")

    # ==========================================================
    # CURRENT FARM CONTEXT
    # ==========================================================
    current_farm = st.session_state.get("current_farm", {})

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "")
    current_location = current_farm.get("location", "")

    # Try to get country from personalization/profile
    personalized_profile = st.session_state.get("personalized_profile", {})

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    farmer_profile = st.session_state.get("farmer_profile", {})

    if not isinstance(farmer_profile, dict):
        farmer_profile = {}

    current_country = (
        personalized_profile.get("country")
        or farmer_profile.get("country")
        or current_farm.get("country")
        or "Not specified"
    )

    st.info(
        f"🌿 Current Farm: {current_farm_name} | "
        f"Crop: {current_crop or 'Not specified'} | "
        f"Location: {current_location or 'Not specified'} | "
        f"Country: {current_country}"
    )

    st.write(
        "Generate planting and harvesting guidance using the selected crop, "
        "farm location and agro-ecological conditions."
    )

    # ==========================================================
    # CROP OPTIONS
    # ==========================================================
    crops = [
        "Maize",
        "Rice",
        "Cassava",
        "Yam",
        "Tomato",
    ]

    default_crop_index = 0

    if current_crop:
        for i, crop_name in enumerate(crops):
            if crop_name.lower() == str(current_crop).lower():
                default_crop_index = i
                break

    # ==========================================================
    # INPUTS
    # ==========================================================
    col1, col2 = st.columns(2)

    with col1:
        crop = st.selectbox(
            "🌾 Select Crop",
            crops,
            index=default_crop_index,
            key=f"ai_calendar_crop_{current_farm_id}",
        )

    with col2:
        location = st.text_input(
            "📍 Farm Location",
            value=current_location or "",
            key=f"ai_calendar_location_{current_farm_id}",
        )

    zone_options = [
        "South-South",
        "South-West",
        "South-East",
        "Middle Belt",
        "North",
        "Other / International",
    ]

    zone = st.selectbox(
        "🌍 Agro-Ecological Zone",
        zone_options,
        key=f"ai_calendar_zone_{current_farm_id}",
    )

    farming_method = st.selectbox(
        "💧 Farming Method",
        [
            "Rain-fed",
            "Irrigated",
        ],
        key=f"ai_calendar_method_{current_farm_id}",
    )

    # ==========================================================
    # CONSOLIDATED CALENDAR KNOWLEDGE
    # ==========================================================
    rainfed_calendar = {
        "Maize": {
            "planting": "April – June",
            "harvest": "About 3–4 months after planting",
            "note": "Plant near the beginning of reliable rainfall.",
        },

        "Rice": {
            "planting": "May – July",
            "harvest": "About 3–5 months after planting",
            "note": "Water availability and rice variety strongly affect timing.",
        },

        "Cassava": {
            "planting": "At the onset of reliable rains",
            "harvest": "About 8–18 months after planting",
            "note": "Adequate soil moisture is important during establishment.",
        },

        "Yam": {
            "planting": "December – April depending on rainfall pattern",
            "harvest": "About 6–10 months after planting",
            "note": "Planting timing varies significantly by region and variety.",
        },

        "Tomato": {
            "planting": "February – April or suitable local wet-season window",
            "harvest": "About 2–4 months after transplanting",
            "note": "Avoid periods of excessive rainfall and disease pressure where possible.",
        },
    }

    irrigated_calendar = {
        "Maize": {
            "planting": "Can be planted outside the normal rainy-season window",
            "harvest": "About 3–4 months after planting",
            "note": "Maintain adequate irrigation according to crop stage.",
        },

        "Rice": {
            "planting": "Dry-season production is possible with reliable irrigation",
            "harvest": "About 3–5 months after planting",
            "note": "Ensure sufficient and controlled water supply.",
        },

        "Cassava": {
            "planting": "Most months where sufficient moisture can be maintained",
            "harvest": "About 8–18 months after planting",
            "note": "Avoid severe moisture stress during establishment.",
        },

        "Yam": {
            "planting": "Timing can be adjusted where reliable water is available",
            "harvest": "About 6–10 months after planting",
            "note": "Variety, seed material and local climate remain important.",
        },

        "Tomato": {
            "planting": "Often suitable for dry-season irrigated production",
            "harvest": "About 2–4 months after transplanting",
            "note": "Monitor heat, humidity, irrigation and disease pressure.",
        },
    }

    # ==========================================================
    # GENERATE CALENDAR
    # ==========================================================
    if st.button(
        "📅 Generate AI Crop Calendar",
        key=f"ai_calendar_generate_{current_farm_id}",
        use_container_width=True,
    ):
        if farming_method == "Rain-fed":
            calendar_data = rainfed_calendar.get(crop)
        else:
            calendar_data = irrigated_calendar.get(crop)

        if calendar_data:
            planting_window = calendar_data["planting"]
            harvest_window = calendar_data["harvest"]
            calendar_note = calendar_data["note"]

            st.success(
                f"🌱 Recommended planting window for {crop}: "
                f"{planting_window}"
            )

            st.success(
                f"🌾 Estimated harvest timing: {harvest_window}"
            )

            st.write("### 🧠 Calendar Context")

            st.write(f"Farm: {current_farm_name}")
            st.write(f"Crop: {crop}")
            st.write(f"Location: {location or 'Not specified'}")
            st.write(f"Country: {current_country}")
            st.write(f"Agro-Ecological Zone: {zone}")
            st.write(f"Production Method: {farming_method}")

            st.info(calendar_note)

            # ==================================================
            # SAVE SCHEDULE
            # ==================================================
            rows_key = f"ai_calendar_rows_{current_farm_id}"

            if rows_key not in st.session_state:
                st.session_state[rows_key] = []

            schedule = {
                "Farm ID": current_farm_id,
                "Farm": current_farm_name,
                "Crop": crop,
                "Country": current_country,
                "Location": location,
                "Zone": zone,
                "Method": farming_method,
                "Planting Window": planting_window,
                "Harvest Timing": harvest_window,
                "Added On": date.today().isoformat(),
            }

            st.session_state[rows_key].append(schedule)
            st.warning(
                "🟡 This calendar currently uses consolidated seasonal "
                "agronomic rules. Final intelligence will combine local "
                "weather, rainfall forecasts, soil conditions, crop variety, "
                "PA and CSA information."
            )

    # ==========================================================
    # SAVED FARM CALENDARS
    # ==========================================================
    rows_key = f"ai_calendar_rows_{current_farm_id}"
    rows = st.session_state.get(rows_key, [])

    if rows:
        st.divider()

        st.subheader(
            f"🧾 Saved Schedules — {current_farm_name}"
        )

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "⬇️ Download Calendar CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"{current_farm_name}_crop_calendar.csv",
                mime="text/csv",
                key=f"ai_calendar_download_{current_farm_id}",
                use_container_width=True,
            )

        with col2:
            if st.button(
                "🧹 Clear Farm Schedules",
                key=f"ai_calendar_clear_{current_farm_id}",
                use_container_width=True,
            ):
                st.session_state[rows_key] = []

                st.success(
                    "✅ Calendar schedules cleared."
                )

                st.rerun()
def drone_irrigation_assistant_ui():
    import streamlit as st
    import re
    import time
    from datetime import datetime

    # =========================================================
    # CURRENT FARM CONTEXT
    # =========================================================
    current_farm = st.session_state.get("current_farm", {}) or {}
    personalized_profile = st.session_state.get("personalized_profile", {}) or {}
    farmer_profile = st.session_state.get("farmer_profile", {}) or {}

    farm_id = str(
        st.session_state.get("current_farm_id")
        or current_farm.get("farm_id")
        or "main_farm"
    )

    farm_name = (
        current_farm.get("farm_name")
        or current_farm.get("name")
        or "Main Farm"
    )

    crop = (
        current_farm.get("crop_type")
        or current_farm.get("crop")
        or "Not selected"
    )

    location = (
        current_farm.get("location")
        or personalized_profile.get("location")
        or farmer_profile.get("location")
        or "Not selected"
    )

    country = (
        current_farm.get("country")
        or personalized_profile.get("country")
        or farmer_profile.get("country")
        or "Not selected"
    )

    st.header("🚁 Voice-Controlled Drone Irrigation Assistant")

    st.info(
        f"🌾 Current Farm: {farm_name} | "
        f"Crop: {crop} | "
        f"Location: {location} | "
        f"Country: {country}"
    )

    st.caption(
        "Smart Farm AI drone irrigation control with field-condition "
        "monitoring, irrigation guidance and mission management."
    )

    # =========================================================
    # FARM-SPECIFIC SESSION KEYS
    # =========================================================
    def dk(name):
        return f"drone_irrigation_{farm_id}_{name}"

    armed_key = dk("armed")
    flying_key = dk("flying")
    battery_key = dk("battery")
    mission_key = dk("mission")
    log_key = dk("log")
    last_tick_key = dk("last_tick")

    if armed_key not in st.session_state:
        st.session_state[armed_key] = False

    if flying_key not in st.session_state:
        st.session_state[flying_key] = False

    if battery_key not in st.session_state:
        st.session_state[battery_key] = 100.0

    if mission_key not in st.session_state:
        st.session_state[mission_key] = None

    if log_key not in st.session_state:
        st.session_state[log_key] = []

    if last_tick_key not in st.session_state:
        st.session_state[last_tick_key] = time.time()

    # =========================================================
    # EVENT LOGGER
    # =========================================================
    def add_log(message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state[log_key].append(
            f"{timestamp} — {message}"
        )

    # =========================================================
    # BATTERY / MISSION UPDATE
    # =========================================================
    now = time.time()

    elapsed_seconds = max(
        0,
        now - st.session_state[last_tick_key]
    )

    st.session_state[last_tick_key] = now

    if st.session_state[flying_key]:
        battery_drain = elapsed_seconds / 120.0

        st.session_state[battery_key] = max(
            0.0,
            st.session_state[battery_key] - battery_drain
        )

    active_mission = st.session_state[mission_key]

    if active_mission:
        elapsed_mission = max(
            0,
            now - active_mission.get("started_at", now)
        )

        remaining_seconds = max(
            0,
            active_mission.get("duration_seconds", 0)
            - elapsed_mission
        )

        active_mission["remaining_seconds"] = remaining_seconds

        if remaining_seconds <= 0:
            zone_finished = active_mission.get(
                "zone",
                "selected zone"
            )
            st.session_state[mission_key] = None

            add_log(
                f"Irrigation mission completed in {zone_finished}"
            )

    # =========================================================
    # LOW BATTERY SAFETY
    # =========================================================
    if (
        st.session_state[flying_key]
        and st.session_state[battery_key] <= 10
    ):
        st.session_state[mission_key] = None
        st.session_state[flying_key] = False

        add_log(
            "Emergency return/landing triggered because battery reached 10%"
        )

        st.error(
            "🔋 Critical battery level. Active mission stopped and "
            "the simulated drone was returned to safety."
        )

    # =========================================================
    # DRONE STATUS
    # =========================================================
    st.subheader("📡 Drone Status")

    status1, status2, status3, status4 = st.columns(4)

    status1.metric(
        "Drone",
        "Armed"
        if st.session_state[armed_key]
        else "Disarmed"
    )

    status2.metric(
        "Flight",
        "In Air"
        if st.session_state[flying_key]
        else "Landed"
    )

    status3.metric(
        "Battery",
        f"{st.session_state[battery_key]:.0f}%"
    )

    status4.metric(
        "Mission",
        "Active"
        if st.session_state[mission_key]
        else "Standby"
    )

    if st.session_state[battery_key] <= 20:
        st.warning(
            "🔋 Battery is low. Replace or recharge it before "
            "starting another major mission."
        )

    # =========================================================
    # FIELD / IRRIGATION INTELLIGENCE
    # =========================================================
    st.subheader("🌱 Field Irrigation Intelligence")

    st.caption(
        "These values currently simulate field/sensor conditions. "
        "Real IoT sensor data can replace them later."
    )

    sensor1, sensor2, sensor3 = st.columns(3)

    with sensor1:
        zone_a = st.slider(
            "Zone A Soil Moisture (%)",
            min_value=0,
            max_value=100,
            value=35,
            key=dk("zone_a")
        )

    with sensor2:
        zone_b = st.slider(
            "Zone B Soil Moisture (%)",
            min_value=0,
            max_value=100,
            value=50,
            key=dk("zone_b")
        )

    with sensor3:
        zone_c = st.slider(
            "Zone C Soil Moisture (%)",
            min_value=0,
            max_value=100,
            value=65,
            key=dk("zone_c")
        )

    weather1, weather2 = st.columns(2)

    with weather1:
        temperature = st.number_input(
            "Ambient Temperature (°C)",
            min_value=-20.0,
            max_value=60.0,
            value=30.0,
            step=0.5,
            key=dk("temperature")
        )

    with weather2:
        rainfall_expected = st.selectbox(
            "Rainfall Expected",
            ["No", "Yes"],
            key=dk("rainfall")
        )

    zones = {
        "Zone A": zone_a,
        "Zone B": zone_b,
        "Zone C": zone_c
    }

    driest_zone = min(
        zones,
        key=zones.get
    )

    driest_value = zones[driest_zone]

    intel1, intel2 = st.columns(2)

    intel1.metric(
        "Highest Irrigation Priority",
        driest_zone
    )

    intel2.metric(
        "Priority Zone Moisture",
        f"{driest_value}%"
    )

    # =========================================================
    # SMART FARM AI GUIDANCE
    # =========================================================
    st.markdown("### 🧠 Smart Farm AI Guidance")

    if rainfall_expected == "Yes":
        st.warning(
            "🌧 Rainfall is expected. Irrigation should be reviewed "
            "before deployment to reduce unnecessary water use."
        )

    elif driest_value < 30:
        st.error(
            f"💧 High irrigation demand detected in {driest_zone}. "
            f"Soil moisture is only {driest_value}%."
        )

    elif driest_value < 45:
        st.warning(
            f"💧 Moderate water demand detected in {driest_zone}. "
            "Irrigation may be appropriate."
        )

    elif driest_value <= 70:
        st.success(
            "🌱 Current soil moisture is generally within an "
            "acceptable operating range."
        )

    else:
        st.info(
            "💦 Soil moisture is already relatively high. "
            "Avoid unnecessary irrigation."
        )

    if temperature >= 35:
        st.info(
            "🌡 High temperature detected. Early-morning or "
            "evening irrigation may reduce evaporation losses."
        )

    elif temperature <= 5:
        st.info(
            "❄️ Low temperature detected. Irrigation should be "
            "reviewed carefully for the local crop and conditions."
        )

    # =========================================================
    # DRONE CONTROLS
    # =========================================================
    st.subheader("🎮 Drone Controls")

    control1, control2, control3 = st.columns(3)

    if control1.button(
        "🔓 Arm",
        key=dk("arm_button"),
        use_container_width=True
    ):
        if st.session_state[armed_key]:
            st.info("Drone is already armed.")
        else:
            st.session_state[armed_key] = True
            add_log("Drone armed")
            st.success("Drone armed successfully.")
            st.rerun()

    if control2.button(
        "🚀 Takeoff",
        key=dk("takeoff_button"),
        use_container_width=True
    ):
        if not st.session_state[armed_key]:
            st.warning(
                "Arm the drone before takeoff."
            )

        elif st.session_state[flying_key]:
            st.info(
                "Drone is already in the air."
            )

        elif st.session_state[battery_key] < 20:
            st.error(
                "Battery is below the safe takeoff threshold."
            )

        else:
            st.session_state[flying_key] = True
            add_log("Drone takeoff")
            st.success("Drone takeoff successful.")
            st.rerun()

    if control3.button(
        "🛬 Land",
        key=dk("land_button"),
        use_container_width=True
    ):
        if not st.session_state[flying_key]:
            st.info("Drone is already landed.")

        else:
            st.session_state[flying_key] = False
            st.session_state[mission_key] = None

            add_log(
                "Drone landed and active mission stopped"
            )

            st.success("Drone landed.")
            st.rerun()

    control4, control5, control6 = st.columns(3)

    if control4.button(
        "🏠 Return Home",
        key=dk("return_home_button"),
        use_container_width=True
    ):
        st.session_state[mission_key] = None
        st.session_state[flying_key] = False

        add_log(
            "Return-to-home completed"
        )

        st.success(
            "Drone returned home."
        )

        st.rerun()

    if control5.button(
        "🔋 Swap Battery",
        key=dk("swap_battery_button"),
        use_container_width=True
    ):
        if st.session_state[flying_key]:
            st.warning(
                "Land the drone before replacing the battery."
            )

        else:
            st.session_state[battery_key] = 100.0

            add_log(
                "Battery replaced — charge restored to 100%"
            )

            st.success(
                "Battery restored to 100%."
            )

            st.rerun()

    if control6.button(
        "🔒 Disarm",
        key=dk("disarm_button"),
        use_container_width=True
    ):
        if st.session_state[flying_key]:
            st.warning(
                "Land the drone before disarming."
            )

        else:
            st.session_state[armed_key] = False

            add_log(
                "Drone disarmed"
            )

            st.success(
                "Drone disarmed."
            )

            st.rerun()

    # =========================================================
    # IRRIGATION MISSION
    # =========================================================
    st.subheader("💦 Irrigation Mission")

    mission1, mission2, mission3 = st.columns(3)

    with mission1:
        target_zone = st.selectbox(
            "Target Zone",
            ["Zone A", "Zone B", "Zone C"],
            index=["Zone A", "Zone B", "Zone C"].index(
                driest_zone
            ),
            key=dk("target_zone")
        )

    with mission2:
        duration = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=120,
            value=10,
            step=1,
            key=dk("duration")
        )

    with mission3:
        flow_rate = st.number_input(
            "Flow Rate (L/min)",
            min_value=0.1,
            max_value=100.0,
            value=5.0,
            step=0.5,
            key=dk("flow_rate")
        )

    estimated_water = float(duration) * float(flow_rate)

    st.metric(
        "Estimated Water Application",
        f"{estimated_water:.1f} L"
    )

    target_moisture = zones[target_zone]

    if st.button(
        "▶️ Start Irrigation Mission",
        key=dk("start_mission_button"),
        use_container_width=True
    ):
        if not st.session_state[armed_key]:
            st.error(
                "Arm the drone before starting the mission."
            )

        elif not st.session_state[flying_key]:
            st.error(
                "Take off before starting irrigation."
            )

        elif st.session_state[battery_key] < 20:
            st.error(
                "Battery is too low to safely start the mission."
            )

        elif rainfall_expected == "Yes":
            st.warning(
                "Mission blocked because rainfall is expected. "
                "Review weather conditions before irrigating."
            )

        elif target_moisture >= 70:
            st.warning(
                f"{target_zone} already has {target_moisture}% "
                "soil moisture. Irrigation is not currently recommended."
            )

        else:
            duration_seconds = int(duration) * 60

            st.session_state[mission_key] = {
                "farm_id": farm_id,
                "farm_name": farm_name,
                "crop": crop,
                "zone": target_zone,
                "duration_minutes": int(duration),
                "duration_seconds": duration_seconds,
                "flow_rate": float(flow_rate),
                "estimated_water": estimated_water,
                "started_at": time.time(),
                "remaining_seconds": duration_seconds
            }

            st.session_state[battery_key] = max(
                0.0,
                st.session_state[battery_key] - 2.0
            )

            add_log(
                f"Irrigation started in {target_zone} "
                f"for {duration} minutes at {flow_rate:.1f} L/min"
            )

            st.success(
                f"💦 Irrigation mission started in {target_zone}."
            )

            st.rerun()

    # =========================================================
    # ACTIVE MISSION
    # =========================================================
    active_mission = st.session_state[mission_key]

    if active_mission:
        st.markdown("### 🚁 Active Mission")

        remaining_seconds = active_mission.get(
            "remaining_seconds",
            0
        )

        remaining_minutes = remaining_seconds / 60.0

        active1, active2, active3 = st.columns(3)

        active1.metric(
            "Zone",
            active_mission.get("zone", "Unknown")
        )

        active2.metric(
            "Remaining",
            f"{remaining_minutes:.1f} min"
        )
        active3.metric(
            "Water Estimate",
            f"{active_mission.get('estimated_water', 0):.1f} L"
        )

        if st.button(
            "⛔ Stop Irrigation Mission",
            key=dk("stop_mission_button"),
            use_container_width=True
        ):
            stopped_zone = active_mission.get(
                "zone",
                "selected zone"
            )

            st.session_state[mission_key] = None

            add_log(
                f"Irrigation mission manually stopped in {stopped_zone}"
            )

            st.success(
                "Irrigation mission stopped."
            )

            st.rerun()

    # =========================================================
    # COMMAND HANDLER
    # =========================================================
    def handle_command(command_text):
        cmd = (
            command_text
            or ""
        ).strip().lower()

        if not cmd:
            st.warning(
                "Enter a command first."
            )
            return

        if cmd in [
            "arm",
            "arm drone",
            "arm the drone"
        ]:
            if st.session_state[armed_key]:
                st.info(
                    "Drone is already armed."
                )
            else:
                st.session_state[armed_key] = True
                add_log(
                    "Drone armed through command assistant"
                )
                st.success(
                    "🔓 Drone armed."
                )

        elif (
            "takeoff" in cmd
            or "take off" in cmd
        ):
            if not st.session_state[armed_key]:
                st.warning(
                    "Arm the drone first."
                )

            elif st.session_state[battery_key] < 20:
                st.error(
                    "Battery is too low for safe takeoff."
                )

            else:
                st.session_state[flying_key] = True

                add_log(
                    "Takeoff command accepted"
                )

                st.success(
                    "🚀 Drone takeoff command accepted."
                )

        elif "land" in cmd:
            st.session_state[flying_key] = False
            st.session_state[mission_key] = None

            add_log(
                "Landing command accepted"
            )

            st.success(
                "🛬 Drone landed."
            )

        elif (
            "return home" in cmd
            or "return to home" in cmd
            or cmd == "home"
            or "rth" in cmd
        ):
            st.session_state[mission_key] = None
            st.session_state[flying_key] = False

            add_log(
                "Return-to-home command accepted"
            )

            st.success(
                "🏠 Drone returned home."
            )

        elif (
            "stop" in cmd
            or "abort" in cmd
            or "cancel" in cmd
        ):
            if st.session_state[mission_key]:
                stopped_zone = st.session_state[
                    mission_key
                ].get(
                    "zone",
                    "selected zone"
                )

                st.session_state[mission_key] = None

                add_log(
                    f"Mission stopped through command assistant "
                    f"in {stopped_zone}"
                )

                st.success(
                    "⛔ Irrigation mission stopped."
                )

            else:
                st.info(
                    "There is no active irrigation mission."
                )

        elif "status" in cmd:
            mission_status = (
                "Active"
                if st.session_state[mission_key]
                else "Standby"
            )

            st.info(
                f"Battery: {st.session_state[battery_key]:.0f}% | "
                f"Armed: {st.session_state[armed_key]} | "
                f"In Air: {st.session_state[flying_key]} | "
                f"Mission: {mission_status}"
            )

        elif (
            "moisture" in cmd
            or "field status" in cmd
        ):
            st.info(
                f"Zone A: {zone_a}% | "
                f"Zone B: {zone_b}% | "
                f"Zone C: {zone_c}% | "
                f"Highest priority: {driest_zone}"
            )

        else:
            zone_match = re.search(
                r"(?:irrigate|water|start)"
                r".*?(?:zone\s*)?([abc])\b",
                cmd
            )

            if zone_match:
                selected_letter = (
                    zone_match.group(1).upper()
                )

                selected_zone = (
                    f"Zone {selected_letter}"
                )

                selected_moisture = zones[
                    selected_zone
                ]

                if not st.session_state[armed_key]:
                    st.warning(
                        "Arm the drone first."
                    )

                elif not st.session_state[flying_key]:
                    st.warning(
                        "Take off before starting irrigation."
                    )

                elif rainfall_expected == "Yes":
                    st.warning(
                        "Irrigation command blocked because "
                        "rainfall is expected."
                    )

                elif selected_moisture >= 70:
                    st.warning(
                        f"{selected_zone} already has "
                        f"{selected_moisture}% soil moisture."
                    )

                else:
                    duration_seconds = (
                        int(duration) * 60
                    )

                    st.session_state[
                        mission_key
                    ] = {
                        "farm_id": farm_id,
                        "farm_name": farm_name,
                        "crop": crop,
                        "zone": selected_zone,
                        "duration_minutes": int(
                            duration
                        ),
                        "duration_seconds": duration_seconds,
                        "flow_rate": float(
                            flow_rate
                        ),
                        "estimated_water": (
                            estimated_water
                        ),
                        "started_at": time.time(),
                        "remaining_seconds": (
                            duration_seconds
                        )
                    }

                    st.session_state[
                        battery_key
                    ] = max(
                        0.0,
                        st.session_state[
                            battery_key
                        ] - 2.0
                    )

                    add_log(
                        f"Command irrigation started in "
                        f"{selected_zone}"
                    )

                    st.success(
                        f"💦 Irrigation started in "
                        f"{selected_zone}."
                    )

            else:
                st.warning(
                    "Command not recognized. Try: arm, takeoff, "
                    "irrigate zone A, irrigate zone B, "
                    "irrigate zone C, stop irrigation, "
                    "return home, land, moisture or status."
                )

    # =========================================================
    # COMMAND ASSISTANT
    # =========================================================
    st.subheader("🎙️ Voice / Typed Command Assistant")

    st.caption(
        "Typed commands are available now. A real microphone/voice "
        "input layer can use the same command handler."
    )

    command = st.text_input(
        "Command",
        placeholder=(
            "Example: arm, takeoff, irrigate zone A, "
            "stop irrigation, return home, status"
        ),
        key=dk("command_input")
    )

    if st.button(
        "▶ Run Command",
        key=dk("run_command_button"),
        use_container_width=True
    ):
        handle_command(command)

    # =========================================================
    # EVENT LOG
    # =========================================================
    st.subheader("📋 Drone Event Log")

    events = st.session_state[log_key]

    if events:
        for event in reversed(
            events[-20:]
        ):
            st.write(
                f"• {event}"
            )

        if st.button(
            "🗑 Clear Event Log",
            key=dk("clear_log_button")
        ):
            st.session_state[log_key] = []
            st.rerun()

    else:
        st.caption(
            "No drone events recorded for this farm yet."
        )

    # =========================================================
    # IMPLEMENTATION STATUS
    # =========================================================
    st.caption(
        "🟡 Current implementation uses simulated drone and field "
        "conditions. Real drone hardware, IoT soil sensors, weather, "
        "PA and CSA intelligence can replace the simulated inputs "
        "during final integration."
    )

# ==========================================
# 💦 IRRIGATION SCHEDULER
# ==========================================

def irrigation_scheduler_ui():
    st.header("💦 Irrigation Scheduler")
    st.write(
        "Plan and manage irrigation sessions using the Current Farm, crop, "
        "field conditions, timing, irrigation purpose, and water requirements."
    )

    # ==========================================
    # CURRENT FARM CONTEXT
    # ==========================================
    current_farm = st.session_state.get("current_farm", {})

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "")
    current_location = current_farm.get("location", "")
    current_farm_type = current_farm.get("farm_type", "")
    current_farm_size = current_farm.get("farm_size", 0)

    farmer_profile = st.session_state.get("farmer_profile", {})

    if not isinstance(farmer_profile, dict):
        farmer_profile = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_country = (
        current_farm.get("country")
        or personalized_profile.get("country")
        or farmer_profile.get("country")
        or "Not specified"
    )

    st.info(
        f"🌿 Current Farm: {current_farm_name} | "
        f"Crop: {current_crop or 'Not specified'} | "
        f"Location: {current_location or 'Not specified'} | "
        f"Country: {current_country}"
    )

    # ==========================================
    # FARM-SPECIFIC KEYS
    # ==========================================
    def irrigation_key(name):
        return f"irrigation_scheduler_{current_farm_id}_{name}"

    schedule_key = irrigation_key("schedule")
    view_key = irrigation_key("view")

    if schedule_key not in st.session_state:
        st.session_state[schedule_key] = []

    if view_key not in st.session_state:
        st.session_state[view_key] = None

    # ==========================================
    # MAIN BUTTONS
    # ==========================================
    c1, c2, c3 = st.columns([1.4, 1.4, 0.8])

    with c1:
        if st.button(
            "📤 Schedule Irrigation",
            key=irrigation_key("btn_schedule"),
            use_container_width=True
        ):
            st.session_state[view_key] = "add"

    with c2:
        if st.button(
            "📋 View Schedule",
            key=irrigation_key("btn_list"),
            use_container_width=True
        ):
            st.session_state[view_key] = "list"

    with c3:
        if st.button(
            "🔄 Reset View",
            key=irrigation_key("btn_reset"),
            use_container_width=True
        ):
            st.session_state[view_key] = None
            st.rerun()

    view = st.session_state.get(view_key)

    # ==========================================
    # SCHEDULE IRRIGATION
    # ==========================================
    if view == "add":
        st.subheader("📤 Schedule New Irrigation")

        with st.form(
            irrigation_key("schedule_form"),
            clear_on_submit=True
        ):
            c1, c2 = st.columns(2)

            with c1:
                irrigation_date = st.date_input(
                    "📅 Irrigation Date",
                    value=datetime.now().date(),
                    key=irrigation_key("date")
                )

            with c2:
                irrigation_time = st.time_input(
                    "⏰ Irrigation Time",
                    value=datetime.now().replace(
                        second=0,
                        microsecond=0
                    ).time(),
                    key=irrigation_key("time")
                )

            c3, c4 = st.columns(2)

            with c3:
                purpose = st.selectbox(
                    "🎯 Purpose",
                    [
                        "General Irrigation",
                        "Spot Watering",
                        "Fertigation",
                        "Crop Treatment Support"
                    ],
                    key=irrigation_key("purpose")
                )

            with c4:
                irrigation_method = st.selectbox(
                    "💧 Irrigation Method",
                    [
                        "Drip",
                        "Sprinkler",
                        "Surface",
                        "Manual",
                        "Drone",
                        "Other"
                    ],
                    key=irrigation_key("method")
                )

            default_plot = (
                current_farm.get("plot_name")
                or current_farm.get("farm_plot")
                or ""
            )

            plot = st.text_input(
                "📍 Farm Plot / Block",
                value=default_plot,
                key=irrigation_key("plot")
            )

            c5, c6 = st.columns(2)

            with c5:
                duration_min = st.number_input(
                    "⏱ Duration (minutes)",
                    min_value=1,
                    max_value=1440,
                    value=30,
                    step=5,
                    key=irrigation_key("duration")
                )

            with c6:
                soil_moisture = st.number_input(
                    "🌱 Current Soil Moisture (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=50.0,
                    step=1.0,
                    key=irrigation_key("soil_moisture")
                )

            c7, c8 = st.columns(2)

            with c7:
                temperature = st.number_input(
                    "🌡 Temperature (°C)",
                    min_value=-20.0,
                    max_value=60.0,
                    value=30.0,
                    step=0.5,
                    key=irrigation_key("temperature")
                )

            with c8:
                rainfall_expected = st.selectbox(
                    "🌧 Rainfall Expected?",
                    [
                        "Unknown",
                        "Yes",
                        "No"
                    ],
                    key=irrigation_key("rainfall")
                )

            submit = st.form_submit_button(
                "💾 Save Irrigation Schedule",
                use_container_width=True
            )

        if submit:
            irrigation_status = "Scheduled"
            intelligence_note = ""

            if soil_moisture >= 70:
                irrigation_status = "Review Before Irrigating"
                intelligence_note = (
                    "Soil moisture is already relatively high. "
                    "Check field conditions before irrigation to reduce "
                    "overwatering and waterlogging risk."
                )

            elif soil_moisture < 30:
                intelligence_note = (
                    "Soil moisture is low, so irrigation demand may be high."
                )

            else:
                intelligence_note = (
                    "Soil moisture is moderate. Continue monitoring conditions "
                    "before and after irrigation."
                )

            if rainfall_expected == "Yes":
                irrigation_status = "Weather Review Required"
                intelligence_note += (
                    " Rainfall is expected, so irrigation may need to be "
                    "reduced, delayed, or cancelled."
                )

            if temperature >= 35:
                intelligence_note += (
                    " High temperature may increase crop water demand. "
                    "Early-morning or evening irrigation may reduce evaporation."
                )

            item = {
                "Farm ID": current_farm_id,
                "Farm": current_farm_name,
                "Crop": current_crop or "Not specified",
                "Location": current_location or "Not specified",
                "Date": irrigation_date.strftime("%Y-%m-%d"),
                "Time": irrigation_time.strftime("%H:%M"),
                "Purpose": purpose,
                "Method": irrigation_method,
                "Farm Plot": plot or "Not specified",
                "Duration (min)": int(duration_min),
                "Soil Moisture (%)": float(soil_moisture),
                "Temperature (°C)": float(temperature),
                "Rainfall Expected": rainfall_expected,
                "Status": irrigation_status,
                "Smart Farm AI Note": intelligence_note,
                "Created": datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            }

            st.session_state[schedule_key].append(item)

            st.success(
                f"✅ Irrigation scheduled for "
                f"{item['Date']} at {item['Time']}."
            )

            if irrigation_status == "Scheduled":
                st.info(
                    f"💧 {intelligence_note}"
                )
            else:
                st.warning(
                    f"⚠️ {irrigation_status}: {intelligence_note}"
                )

    # ==========================================
    # VIEW SCHEDULE
    # ==========================================
    elif view == "list":
        st.subheader("📋 Irrigation Schedule")

        items = st.session_state.get(
            schedule_key,
            []
        )

        if items:
            df = pd.DataFrame(items)

            st.dataframe(
                df,
                use_container_width=True
            )

            total_sessions = len(items)

            total_minutes = sum(
                int(item.get("Duration (min)", 0))
                for item in items
            )

            review_count = sum(
                1
                for item in items
                if item.get("Status") != "Scheduled"
            )

            m1, m2, m3 = st.columns(3)

            with m1:
                st.metric(
                    "Scheduled Sessions",
                    total_sessions
                )

            with m2:
                st.metric(
                    "Total Irrigation Time",
                    f"{total_minutes} min"
                )

            with m3:
                st.metric(
                    "Sessions Requiring Review",
                    review_count
                )

            c1, c2 = st.columns(2)

            with c1:
                st.download_button(
                    "⬇️ Download Schedule",
                    data=df.to_csv(
                        index=False
                    ).encode("utf-8"),
                    file_name=(
                        f"{current_farm_id}_"
                        f"irrigation_schedule.csv"
                    ),
                    mime="text/csv",
                    key=irrigation_key("download")
                )

            with c2:
                if st.button(
                    "🧹 Clear All",
                    key=irrigation_key("clear_all")
                ):
                    st.session_state[schedule_key] = []
                    st.rerun()

            st.divider()

            st.subheader(
                "🗑 Manage Scheduled Sessions"
            )

            for index, item in enumerate(
                list(items)
            ):
                title = (
                    f"📌 {item.get('Date', '')} "
                    f"{item.get('Time', '')} — "
                    f"{item.get('Purpose', '')} @ "
                    f"{item.get('Farm Plot', 'Not specified')}"
                )

                with st.expander(title):
                    st.write(
                        f"Crop: "
                        f"{item.get('Crop', 'Not specified')}"
                    )

                    st.write(
                        f"Method: "
                        f"{item.get('Method', 'Not specified')}"
                    )
                    st.write(
                        f"Duration: "
                        f"{item.get('Duration (min)', 0)} minutes"
                    )

                    st.write(
                        f"Status: "
                        f"{item.get('Status', 'Scheduled')}"
                    )

                    note = item.get(
                        "Smart Farm AI Note",
                        ""
                    )

                    if note:
                        st.info(note)

                    if st.button(
                        "Delete this entry",
                        key=irrigation_key(
                            f"delete_{index}"
                        )
                    ):
                        st.session_state[
                            schedule_key
                        ].pop(index)

                        st.rerun()

        else:
            st.info(
                f"No irrigation sessions have been scheduled "
                f"for {current_farm_name}."
            )

    # ==========================================
    # DEFAULT VIEW
    # ==========================================
    else:
        st.info(
            "Choose Schedule Irrigation or View Schedule above."
        )

# ==========================================
# 📈 DECISION-MAKING MODELS
# ==========================================

def decision_making_models_ui():
    st.header("📈 Decision-Making Models")

    st.write(
        "Smart Farm AI uses current farm conditions and farmer inputs "
        "to support irrigation, fertilizer, and crop-rotation decisions."
    )

    # ------------------------------------------
    # CURRENT FARM
    # ------------------------------------------
    current_farm = st.session_state.get("current_farm", {})

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "")
    current_location = current_farm.get("location", "")
    current_farm_type = current_farm.get("farm_type", "")
    current_farm_size = current_farm.get("farm_size", 0)

    farmer_profile = st.session_state.get("farmer_profile", {})

    if not isinstance(farmer_profile, dict):
        farmer_profile = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_country = (
        current_farm.get("country")
        or personalized_profile.get("country")
        or farmer_profile.get("country")
        or "Not specified"
    )

    st.info(
        f"🌿 Current Farm: {current_farm_name} | "
        f"Crop: {current_crop or 'Not specified'} | "
        f"Location: {current_location or 'Not specified'} | "
        f"Country: {current_country}"
    )

    # ------------------------------------------
    # UNIQUE KEYS
    # ------------------------------------------
    def dm_key(name):
        return f"decision_model_{current_farm_id}_{name}"

    active_key = dm_key("active_tool")

    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # ------------------------------------------
    # TOOL BUTTONS
    # ------------------------------------------
    c1, c2, c3, c4 = st.columns([1.4, 1.4, 1.6, 0.8])

    with c1:
        if st.button(
            "💧 Irrigation",
            key=dm_key("btn_irrigation")
        ):
            st.session_state[active_key] = "irrigation"

    with c2:
        if st.button(
            "🌿 Fertilizer",
            key=dm_key("btn_fertilizer")
        ):
            st.session_state[active_key] = "fertilizer"

    with c3:
        if st.button(
            "🔄 Crop Rotation",
            key=dm_key("btn_rotation")
        ):
            st.session_state[active_key] = "rotation"

    with c4:
        if st.button(
            "🔄 Reset",
            key=dm_key("btn_reset")
        ):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state.get(active_key)

    # ==========================================
    # 💧 IRRIGATION DECISION
    # ==========================================
    if tool == "irrigation":
        st.subheader("💧 Irrigation Decision")

        col1, col2 = st.columns(2)

        with col1:
            soil_moisture = st.slider(
                "Soil Moisture (%)",
                0,
                100,
                50,
                key=dm_key("soil_moisture")
            )

        with col2:
            temperature = st.slider(
                "Temperature (°C)",
                -10,
                50,
                30,
                key=dm_key("temperature")
            )

        col3, col4 = st.columns(2)

        with col3:
            rainfall = st.selectbox(
                "Rainfall Expected Soon?",
                [
                    "Unknown",
                    "Yes",
                    "No"
                ],
                key=dm_key("rainfall")
            )

        with col4:
            growth_stage = st.selectbox(
                "Crop Growth Stage",
                [
                    "Not specified",
                    "Establishment",
                    "Vegetative",
                    "Flowering",
                    "Fruiting",
                    "Maturity"
                ],
                key=dm_key("growth_stage")
            )

        irrigation_score = 0
        reasons = []

        if soil_moisture < 25:
            irrigation_score += 4
            reasons.append(
                "Soil moisture is critically low."
            )

        elif soil_moisture < 40:
            irrigation_score += 3
            reasons.append(
                "Soil moisture is below the preferred range."
            )

        elif soil_moisture < 60:
            irrigation_score += 1
            reasons.append(
                "Soil moisture is moderate."
            )

        else:
            irrigation_score -= 2
            reasons.append(
                "Soil moisture is currently adequate."
            )

        if temperature >= 35:
            irrigation_score += 2
            reasons.append(
                "High temperature increases crop water demand."
            )

        elif temperature >= 30:
            irrigation_score += 1
            reasons.append(
                "Temperature may increase water demand."
            )

        if rainfall == "Yes":
            irrigation_score -= 3
            reasons.append(
                "Rainfall is expected soon."
            )

        elif rainfall == "No":
            irrigation_score += 1
            reasons.append(
                "No rainfall is expected soon."
            )

        if growth_stage in [
            "Flowering",
            "Fruiting"
        ]:
            irrigation_score += 1
            reasons.append(
                f"{growth_stage} can be sensitive to water stress."
            )

        if irrigation_score >= 5:
            decision = "Irrigation strongly recommended"

            recommendation = (
                "Apply irrigation according to crop root depth, "
                "soil type, and field conditions. Prefer early "
                "morning or evening irrigation where practical."
            )

            risk = "High water-stress risk"

        elif irrigation_score >= 2:
            decision = "Moderate irrigation recommended"

            recommendation = (
                "Apply controlled irrigation and monitor soil "
                "moisture before the next irrigation cycle."
            )

            risk = "Moderate water-stress risk"

        elif irrigation_score >= 0:
            decision = "Monitor before irrigating"

            recommendation = (
                "Water stress is not severe. Check soil moisture "
                "and local weather again before irrigation."
            )

            risk = "Low to moderate water-stress risk"

        else:
            decision = "Irrigation not required now"

            recommendation = (
                "Avoid unnecessary irrigation. Continue monitoring "
                "soil moisture to reduce water waste and waterlogging."
            )

            risk = "Low water-stress risk"

        st.success(
            f"✅ Decision: {decision}"
        )

        st.write(
            f"Risk Level: {risk}"
        )

        st.write(
            f"Recommended Action: {recommendation}"
        )

        st.write(
            "Decision Factors:"
        )

        for reason in reasons:
            st.write(
                f"• {reason}"
            )

        st.caption(
            f"Farm: {current_farm_name} | "
            f"Crop: {current_crop or 'Not specified'} | "
            f"Location: {current_location or 'Not specified'}"
        )

    # ==========================================
    # 🌿 FERTILIZER DECISION
    # ==========================================
    elif tool == "fertilizer":
        st.subheader("🌿 Fertilizer Decision")

        crop_options = [
            "Maize",
            "Rice",
            "Cassava",
            "Yam",
            "Tomato",
            "Soybean",
            "Cowpea",
            "Other"
        ]
        crop_index = 0

        if current_crop in crop_options:
            crop_index = crop_options.index(
                current_crop
            )

        crop_type = st.selectbox(
            "Crop Type",
            crop_options,
            index=crop_index,
            key=dm_key("fert_crop")
        )

        growth_stage = st.selectbox(
            "Growth Stage",
            [
                "Establishment",
                "Vegetative",
                "Flowering",
                "Fruiting",
                "Maturity"
            ],
            key=dm_key("fert_growth_stage")
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            nitrogen = st.selectbox(
                "Nitrogen Status",
                [
                    "Unknown",
                    "Low",
                    "Adequate",
                    "High"
                ],
                key=dm_key("nitrogen")
            )

        with c2:
            phosphorus = st.selectbox(
                "Phosphorus Status",
                [
                    "Unknown",
                    "Low",
                    "Adequate",
                    "High"
                ],
                key=dm_key("phosphorus")
            )

        with c3:
            potassium = st.selectbox(
                "Potassium Status",
                [
                    "Unknown",
                    "Low",
                    "Adequate",
                    "High"
                ],
                key=dm_key("potassium")
            )

        soil_ph = st.number_input(
            "Soil pH",
            min_value=3.0,
            max_value=10.0,
            value=6.5,
            step=0.1,
            key=dm_key("soil_ph")
        )

        recommendations = []
        warnings = []

        if nitrogen == "Low":
            recommendations.append(
                "Nitrogen appears low. Consider an appropriate "
                "nitrogen source based on crop requirement and "
                "local agronomic guidance."
            )

        elif nitrogen == "High":
            warnings.append(
                "Nitrogen is already high. Avoid unnecessary "
                "additional nitrogen."
            )

        elif nitrogen == "Adequate":
            recommendations.append(
                "Nitrogen level appears adequate."
            )

        if phosphorus == "Low":
            recommendations.append(
                "Phosphorus appears low. Correcting deficiency "
                "may support root development and crop establishment."
            )

        elif phosphorus == "High":
            warnings.append(
                "Phosphorus is already high. Additional application "
                "may not be necessary."
            )

        elif phosphorus == "Adequate":
            recommendations.append(
                "Phosphorus level appears adequate."
            )

        if potassium == "Low":
            recommendations.append(
                "Potassium appears low. Potassium management may "
                "be important for crop strength and yield formation."
            )

        elif potassium == "High":
            warnings.append(
                "Potassium is already high. Avoid excessive application."
            )

        elif potassium == "Adequate":
            recommendations.append(
                "Potassium level appears adequate."
            )

        if soil_ph < 5.5:
            warnings.append(
                "Soil is strongly acidic for many crops. "
                "Consider proper soil testing before applying amendments."
            )

        elif soil_ph > 8.0:
            warnings.append(
                "Soil is alkaline. Some nutrients may become less available."
            )

        else:
            recommendations.append(
                "Soil pH is within a generally workable range "
                "for many crops."
            )

        if growth_stage == "Establishment":
            recommendations.append(
                "Prioritize healthy root establishment and avoid "
                "excessive fertilizer concentration near young roots."
            )

        elif growth_stage == "Vegetative":
            recommendations.append(
                "Vegetative growth can increase nutrient demand. "
                "Correct confirmed deficiencies appropriately."
            )

        elif growth_stage == "Flowering":
            recommendations.append(
                "Maintain balanced nutrition during flowering "
                "and avoid excessive nitrogen."
            )

        elif growth_stage == "Fruiting":
            recommendations.append(
                "Balanced nutrition is important during fruit "
                "and yield development."
            )

        elif growth_stage == "Maturity":
            recommendations.append(
                "Avoid unnecessary late fertilizer applications "
                "unless a diagnosed deficiency requires correction."
            )

        st.success(
            f"✅ Fertilizer assessment prepared for "
            f"{crop_type} at the {growth_stage.lower()} stage."
        )

        if recommendations:
            st.write(
                "Recommended Actions:"
            )

            for item in recommendations:
                st.write(
                    f"• {item}"
                )

        if warnings:
            st.warning(
                "⚠️ Important Considerations"
            )

            for item in warnings:
                st.write(
                    f"• {item}"
                )

        if (
            nitrogen == "Unknown"
            or phosphorus == "Unknown"
            or potassium == "Unknown"
        ):
            st.info(
                "Connect soil-test or sensor data for nitrogen, "
                "phosphorus, and potassium to improve this decision."
            )

        st.caption(
            f"Farm: {current_farm_name} | "
            f"Crop: {crop_type} | "
            f"Location: {current_location or 'Not specified'}"
        )

    # ==========================================
    # 🔄 CROP ROTATION DECISION
    # ==========================================
    elif tool == "rotation":
        st.subheader("🔄 Crop Rotation Decision")

        crop_options = [
            "Maize",
            "Cassava",
            "Tomato",
            "Yam",
            "Rice",
            "Soybean",
            "Cowpea"
        ]

        crop_index = 0

        if current_crop in crop_options:
            crop_index = crop_options.index(
                current_crop
            )

        previous_crop = st.selectbox(
            "Previous Crop",
            crop_options,
            index=crop_index,
            key=dm_key("previous_crop")
        )

        rotation_goal = st.selectbox(
            "Main Rotation Goal",
            [
                "Improve Soil Fertility",
                "Reduce Pest and Disease Pressure",
                "Improve Soil Structure",
                "Diversify Production"
            ],
            key=dm_key("rotation_goal")
        )

        rotation_options = {
            "Maize": {
                "Improve Soil Fertility": "Soybean or Cowpea",
                "Reduce Pest and Disease Pressure": "Soybean, Cowpea, or another non-cereal crop",
                "Improve Soil Structure": "Legume or suitable cover crop",
                "Diversify Production": "Cassava, vegetables, or legumes"
            },
            "Cassava": {
                "Improve Soil Fertility": "Cowpea or Soybean",
                "Reduce Pest and Disease Pressure": "Maize, Sorghum, or legumes",
                "Improve Soil Structure": "Legume or suitable cover crop",
                "Diversify Production": "Maize, vegetables, or legumes"
            },
            "Tomato": {
                "Improve Soil Fertility": "Cowpea or Soybean",
                "Reduce Pest and Disease Pressure": "Maize, Sorghum, or another non-solanaceous crop",
                "Improve Soil Structure": "Legume or suitable cover crop",
                "Diversify Production": "Cereal or legume crop"
            },
            "Yam": {
                "Improve Soil Fertility": "Cowpea or Soybean",
                "Reduce Pest and Disease Pressure": "Maize, vegetables, or legumes",
                "Improve Soil Structure": "Legume or suitable cover crop",
                "Diversify Production": "Vegetables, maize, or legumes"
            },
            "Rice": {
                "Improve Soil Fertility": "Cowpea or Soybean",
                "Reduce Pest and Disease Pressure": "Legume or suitable upland crop",
                "Improve Soil Structure": "Legume or cover crop where suitable",
                "Diversify Production": "Legume or vegetable crop"
            },
            "Soybean": {
                "Improve Soil Fertility": "Maize",
                "Reduce Pest and Disease Pressure": "Maize, Sorghum, or another cereal",
                "Improve Soil Structure": "Maize or suitable cover crop",
                "Diversify Production": "Maize, vegetables, or root crops"
            },
            "Cowpea": {
                "Improve Soil Fertility": "Maize",
                "Reduce Pest and Disease Pressure": "Maize, Sorghum, or another cereal",
                "Improve Soil Structure": "Maize or suitable cover crop",
                "Diversify Production": "Maize, vegetables, or root crops"
            }
        }

        suggestion = rotation_options.get(
            previous_crop,
            {}
        ).get(
            rotation_goal,
            "Consider rotating with a crop from a different botanical family."
        )

        st.success(
            f"✅ Suggested Next Crop: {suggestion}"
        )

        st.write(
            f"Reason: The recommendation considers the previous "
            f"crop ({previous_crop}) and your goal "
            f"({rotation_goal.lower()})."
        )

        st.info(
            "Final rotation decisions should also consider local climate, "
            "soil condition, water availability, planting season, "
            "previous disease history, and market conditions."
        )

        st.caption(
            f"Farm: {current_farm_name} | "
            f"Location: {current_location or 'Not specified'}"
        )

    # ==========================================
    # DEFAULT VIEW
    # ==========================================
    else:
        st.info(
            "Choose Irrigation, Fertilizer, or Crop Rotation above."
        )


# ================================
# 💾 Data Backup & Recovery (drop-in)
# ================================
def data_backup_recovery_ui_impl():
    import os, shutil, io
    from datetime import datetime
    import streamlit as st

    # --- key helper fallback (uses your existing kbak if present) ---
    try:
        kbak  # type: ignore[name-defined]
    except NameError:
        def kbak(name: str) -> str:
            return f"bk_{name}"

    st.header("💾 Data Backup & Recovery")
    st.caption("Create a .zip backup of your farm data, restore a previous backup, or manage backup files.")

    # --- folders ---
    data_dir = "farm_data"
    backup_dir = "backups"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    # --- active tool in session ---
    active_key = kbak("active_tool")
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # --- triggers row ---
    c1, c2, c3, c4 = st.columns([1.6, 1.6, 1.6, 0.8])
    with c1:
        if st.button("💾 Create Backup (.zip)", key=kbak("btn_backup")):
            st.session_state[active_key] = "backup"
    with c2:
        if st.button("♻️ Restore Backup", key=kbak("btn_restore")):
            st.session_state[active_key] = "restore"
    with c3:
        if st.button("🗑 Manage Backups", key=kbak("btn_manage")):
            st.session_state[active_key] = "manage"
    with c4:
        if st.button("🔄 Reset", key=kbak("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # Helper: list .zip backups
    def _list_zips():
        return sorted(
            [f for f in os.listdir(backup_dir) if f.lower().endswith(".zip")]
        )

    # ======================
    # Tool: Create Backup
    # ======================
    if tool == "backup":
        st.subheader("💾 Create Backup")
        st.write(f"Source: `{data_dir}`  →  Backups go to `{backup_dir}` as .zip files")

        if st.button("📂 Backup Now", key=kbak("do_backup"), use_container_width=True):
            try:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                base = os.path.join(backup_dir, backup_name)
                # Make a .zip of *contents* of data_dir
                zip_path = shutil.make_archive(base_name=base, format="zip", root_dir=data_dir)
                st.success(f"✅ Backup created: {os.path.basename(zip_path)}")

                # Offer immediate download
                with open(zip_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Backup",
                        f.read(),
                        file_name=os.path.basename(zip_path),
                        mime="application/zip",
                        key=kbak("dl_new_backup")
                    )
            except Exception as e:
                st.error(f"❌ Error creating backup: {e}")

    # ======================
    # Tool: Restore Backup
    # ======================
    elif tool == "restore":
        st.subheader("♻️ Restore Backup")
        zips = _list_zips()
        if not zips:
            st.info("ℹ️ No backups found yet. Create one first.")
        else:
            selected = st.selectbox("Select a backup (.zip) to restore", zips, key=kbak("sel_restore"))
            st.warning(
                "Restoring will replace the current contents of `farm_data/` "
                "with the files from this backup."
            )
            if st.button("🔄 Restore", key=kbak("do_restore"), use_container_width=True):
                try:
                    # Remove current data_dir and recreate empty
                    if os.path.exists(data_dir):
                        shutil.rmtree(data_dir)
                    os.makedirs(data_dir, exist_ok=True)

                    # Extract zip *into* data_dir
                    zip_path = os.path.join(backup_dir, selected)
                    shutil.unpack_archive(zip_path, extract_dir=data_dir, format="zip")
                    st.success(f"✅ Restored from '{selected}'.")
                except Exception as e:
                    st.error(f"❌ Error restoring backup: {e}")

    # ======================
    # Tool: Manage Backups
    # ======================
    elif tool == "manage":
        st.subheader("🗑 Manage Backups")
        zips = _list_zips()
        if not zips:
            st.info("No backups to manage yet.")
        else:
            selected = st.selectbox("Select a backup (.zip)", zips, key=kbak("sel_manage"))
            cA, cB, cC = st.columns([1, 1, 1])
            with cA:
                # Download
                zip_path = os.path.join(backup_dir, selected)
                with open(zip_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download Selected",
                        f.read(),
                        file_name=selected,
                        mime="application/zip",
                        key=kbak("dl_sel")
                    )
            with cB:
                # Delete
                if st.button("🗑 Delete Selected", key=kbak("del_sel")):
                    try:
                        os.remove(zip_path)
                        st.success(f"Deleted backup '{selected}'.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting backup: {e}")
            with cC:
                if st.button("📁 Refresh List", key=kbak("refresh")):
                    st.rerun()

    else:
        st.info("Choose an action above to create, restore, or manage backups.")

# ---- aliases so any of these names work in your router ----
data_backup_recovery_ui = data_backup_recovery_ui_impl
backup_recovery_ui      = data_backup_recovery_ui_impl
data_backup_ui          = data_backup_recovery_ui_impl
backup_ui               = data_backup_recovery_ui_impl
_data_backup_recovery_ui= data_backup_recovery_ui_impl




def data_backup_recovery_ui():
    import streamlit as st

    candidates = [
        "data_backup_recovery_ui_impl",
        "backup_recovery_ui",
        "data_backup_ui",
        "backup_ui",
        "_data_backup_recovery_ui",
    ]
    for name in candidates:
        impl = globals().get(name)
        if callable(impl):
            return impl()

    st.header("💾 Data Backup & Recovery")
    st.info(
        "The Backup & Recovery implementation isn’t loaded in this file. "
        "Define one of these functions and I’ll call it automatically:\n\n"
        f"- {', '.join(candidates)}"
    )



def drone_irrigation_assistant_ui():
    # Keep it self-contained so it never NameErrors
    import streamlit as st

    # Try to find your real implementation if it lives elsewhere
    candidates = [
        "drone_irrigation_assistant_ui_impl",
        "irrigation_voice_assistant_ui",
        "voice_irrigation_assistant_ui",
        "drone_irrigation_assistant",   # common alt name
        "_drone_irrigation_assistant_ui",
    ]
    for name in candidates:
        impl = globals().get(name)
        if callable(impl):
            return impl()  # delegate to your actual function

    # Fallback if nothing found (prevents NameError and explains what to do)
    st.subheader("🚁 Voice-Controlled Drone Irrigation Assistant")
    st.info(
        "The voice irrigation assistant implementation isn’t loaded in this file. "
        "Define one of these functions anywhere before runtime and I’ll call it automatically:\n\n"
        f"- {', '.join(candidates)}"
    )



def drone_flight_scheduler_ui():

    st.subheader("🚁 Drone Flight Scheduler")

    flights = _load("drone_flights.json", [])

    with st.form("drone_form"):

        date = st.date_input("📅 Flight Date", key="dr_date")

        time = st.time_input("⏰ Flight Time", key="dr_time")

        purpose = st.selectbox("🎯 Purpose", ["Crop Monitoring", "Pesticide Spraying", "Fertilizer Spraying", "Aerial Mapping", "Livestock Surveillance"], key="d_purpose")

        plot = st.text_input("📍 Plot ID/Name",  key="dr_plot")

        submitted = st.form_submit_button("📤 Schedule Flight")

    if submitted:

        flights.append({"date": str(date), "time": str(time), "purpose": purpose, "plot": plot})

        _save("drone_flights.json", flights)

        st.success("✅ Flight scheduled.")

    if flights:

        st.markdown("### 🗓 Scheduled Flights")

        for f in flights:

            st.write(f"- {f['date']} {f['time']} — {f['purpose']} @ {f['plot']}")



def voice_command_ui():
    import streamlit as st
    import re

    # Optional voice deps — UI still works without them
    try:
        import speech_recognition as sr
    except Exception:
        sr = None

    st.subheader("🎙 Voice Command Interface")
    st.caption("Say or type a command to jump to a page (e.g., “open live sensor dashboard”, “go to predictions”).")

    # --- helpers -------------------------------------------------------------
    def _v2_key():
        # Use your existing k2() helper if present; otherwise fallback to a safe string
        try:
            return k2("main_menu_option")
        except Exception:
            return "v2_main_menu_option"

    def _try_rerun():
        """Call Streamlit rerun with compatibility across versions."""
        try:
            if hasattr(st, "rerun"):
                st.rerun()
            elif hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
        except Exception:
            # If rerun fails just continue — UI will update on next interaction
            pass

    def _go(label: str):
        """Attempt to navigate by setting the v2 menu key."""
        # This assignment is safe when done from callbacks (on_change) or
        # before the menu widget is created. We use it from the typed-command
        # callback which runs in a safe update context.
        st.session_state[_v2_key()] = label

    def _route(cmd: str) -> bool:
        """Map free-text commands to pages. Return True if a route was matched."""
        c = (cmd or "").strip().lower()
        if not c:
            return False

        # normalize common words
        c = c.replace("open ", "").replace("go to ", "").replace("goto ", "")

        # high-confidence matches first
        if re.search(r"\blive\b.*\bsensor\b|\bsensor\b.*\bdashboard\b", c):
            _go("📡 Live Sensor Dashboard"); return True
        if "drone" in c and ("schedule" in c or "scheduler" in c or "flight" in c):
            _go("🚁 Drone Flight Scheduler"); return True
        if ("voice" in c and ("irrig" in c or "drone" in c)) or "voice assistant" in c:
            _go("🚁 Voice-Controlled Drone Irrigation Assistant"); return True
        if "prediction" in c:
            _go("🧪 AI Predictions"); return True
        if "tip" in c or "tips" in c:
            _go("📚 AI Farm Tips"); return True
        if "profit" in c or "loss" in c or "statement" in c:
            _go("📊 Farm Profit & Loss Statement"); return True
        if "plot" in c or "mapping" in c or "map" in c:
            _go("🌍 Farm Plot Mapping"); return True
        if "irrigation" in c and "soil" in c:
            _go("💧 Irrigation & Soil"); return True
        if "expanded" in c and "calendar" in c:
            _go("📅 Expanded AI Crop Calendar"); return True
        if "crop calendar" in c:
            _go("🤖 AI Crop Calendar"); return True
        if "performance" in c and "indicator" in c:
            _go("📍 Farm Performance Indicators"); return True
        if "market" in c or "economic" in c or "price" in c:
            _go("📈 Market & Economic Tools"); return True
        if "backup" in c or "restore" in c or "recovery" in c:
            _go("💾 Data Backup & Recovery"); return True
        if "home" in c:
            _go("🏡 Home"); return True

        # fallback: try fuzzy contains for any top-level label keywords
        for label in [
            "🏡 Home",
            "🌿 Farm Management",
            "📊 Productivity & Records",
            "💧 Irrigation & Soil",
            "📅 Calendar & Seasons",
            "🧪 AI Predictions",
            "📈 Market & Economic Tools",
            "📚 AI Farm Tips",
            "📊 Farm Profit & Loss Statement",
            "🌍 Farm Plot Mapping",
            "🌐 Farmer Community Forum",
            "📡 Live Sensor Dashboard",
            "🚨 Smart Farm Alerts",
            "🎙️ Voice Command Interface",
            "🚁 Drone Flight Scheduler",
            "🧑‍🏫 Smart Tutor (Voice)",
            "💾 Data Backup & Recovery",
            "📍 Farm Lot Management",
            "📅 Expanded AI Crop Calendar",
            "🤖 AI Crop Calendar",
            "📈 Decision-Making Models",
            "📍 Farm Performance Indicators",
            "🔒 User Account Management",
        ]:
            words = re.findall(r"\w+", label.lower())
            if any(w in c for w in words if len(w) > 2):
                _go(label)
                return True

        return False

    # --- typed-command callback (safe) --------------------------------------
    def _apply_typed_command():
        """This runs as the text_input on_change callback — safe to mutate widget-backed keys."""
        cmd = st.session_state.get("vc_text", "").strip()
        if not cmd:
            return
        matched = False
        try:
            matched = _route(cmd)
        except Exception as e:
            # If setting the menu key fails for any reason, show an info message
            st.warning(f"Could not apply navigation: {e}")
            matched = False

        # clear command input after applying (so user sees it reset)
        st.session_state["vc_text"] = ""
        if matched:
            _try_rerun()
        else:
            st.info("No route matched. Try keywords: sensor, predictions, calendar, drone, backup, home.")

    # --- UI ------------------------------------------------------------------
    col_mic, col_cmd = st.columns([1, 3])

    # 1) Voice (only if SpeechRecognition is available)
    if sr is not None:
        if col_mic.button("🎤 Speak"):
            try:
                recog = sr.Recognizer()
                with sr.Microphone() as source:
                    st.info("Listening…")
                    try:
                        recog.adjust_for_ambient_noise(source, duration=0.6)
                    except Exception:
                        pass
                    audio = recog.listen(source, timeout=4, phrase_time_limit=6)
                cmd = recog.recognize_google(audio)
                st.success(f"🗣 {cmd}")
                # voice path: route immediately (mic path has historically run before menu widget is created,
                # which is why it likely worked for you already)
                try:
                    if _route(cmd):
                        _try_rerun()
                    else:
                        st.info("No route matched. Try: live sensor, predictions, calendar, drone scheduler, backup.")
                except Exception as e:
                    st.error(f"Navigation error: {e}")
            except sr.WaitTimeoutError:
                st.error("Timed out. Try again.")
            except sr.UnknownValueError:
                st.error("I couldn't understand that. Try again.")
            except sr.RequestError:
                st.error("Speech service unavailable. Type your command instead.")
            except Exception as e:
                st.error(f"Mic error: {e}")
    else:
        col_mic.caption("Install voice deps to enable mic: `pip install SpeechRecognition pyaudio`")

    # 2) Typed command (always available) — uses on_change callback to safely mutate menu key
    cmd_text = col_cmd.text_input(
        "Type a command",
        placeholder="e.g., open live sensor dashboard, go to predictions, open backup",
        key="vc_text",
        on_change=_apply_typed_command,
    )
    # Note: we've removed the separate "Go" button handler to avoid mutation-after-widget errors.


# farm performance indicators
def farm_performance_indicators_ui():
    import pandas as pd
    from datetime import datetime

    st.header("📍 Farm Performance Indicators")

    current_farm = st.session_state.get("current_farm", {})
    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "")
    current_location = current_farm.get("location", "")
    current_farm_size = current_farm.get("farm_size", 0)

    farmer_profile = st.session_state.get("farmer_profile", {})
    if not isinstance(farmer_profile, dict):
        farmer_profile = {}

    personalized_profile = st.session_state.get("personalized_profile", {})
    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_country = (
        current_farm.get("country")
        or personalized_profile.get("country")
        or farmer_profile.get("country")
        or "Nigeria"
    )

    currency_map = {
        "Nigeria": ("₦", "NGN"),
        "Canada": ("C$", "CAD"),
        "Iran": ("﷼", "IRR"),
        "Cyprus": ("€", "EUR"),
        "United States": ("$", "USD"),
        "USA": ("$", "USD"),
        "United Kingdom": ("£", "GBP"),
    }

    currency_symbol, currency_code = currency_map.get(
        current_country,
        ("$", "USD")
    )

    st.info(
        f"🌿 Current Farm: {current_farm_name} | "
        f"Crop: {current_crop or 'Not specified'} | "
        f"Location: {current_location or 'Not specified'} | "
        f"Country: {current_country}"
    )

    st.write(
        "Evaluate field health, crop water stress and market readiness "
        "for the Current Farm."
    )

    def fpi_key(name):
        return f"fpi_{current_farm_id}_{name}"

    c1, c2, c3 = st.columns(3)

    with c1:
        pest = st.number_input(
            "🐛 Pest incidence (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=1.0,
            key=fpi_key("pest")
        )

        disease = st.number_input(
            "🦠 Disease incidence (%)",
            min_value=0.0,
            max_value=100.0,
            value=8.0,
            step=1.0,
            key=fpi_key("disease")
        )

        soil_moist = st.number_input(
            "💧 Soil moisture (%)",
            min_value=0.0,
            max_value=100.0,
            value=55.0,
            step=1.0,
            key=fpi_key("soil_moisture")
        )

    with c2:
        ndvi = st.number_input(
            "🌿 Vegetation Index / NDVI (0–1)",
            min_value=0.0,
            max_value=1.0,
            value=0.65,
            step=0.01,
            key=fpi_key("ndvi")
        )

        temp = st.number_input(
            "🌡️ Temperature (°C)",
            min_value=-20.0,
            max_value=60.0,
            value=30.0,
            step=0.5,
            key=fpi_key("temperature")
        )

        et0 = st.number_input(
            "☀️ ET₀ (mm/day)",
            min_value=0.0,
            max_value=20.0,
            value=4.5,
            step=0.1,
            key=fpi_key("et0")
        )

    with c3:
        expected_yield = st.number_input(
            "🌾 Expected yield (tons)",
            min_value=0.0,
            value=5.0,
            step=0.1,
            key=fpi_key("yield")
        )

        price = st.number_input(
            f"💰 Current price ({currency_symbol}/ton)",
            min_value=0.0,
            value=250000.0 if current_country == "Nigeria" else 1000.0,
            step=100.0,
            key=fpi_key("price")
        )

        cost = st.number_input(
            f"📉 Production cost ({currency_symbol}/ton)",
            min_value=0.0,
            value=180000.0 if current_country == "Nigeria" else 700.0,
            step=100.0,
            key=fpi_key("cost")
        )

        storage_days = st.number_input(
            "📦 Storage days if sale is delayed",
            min_value=0,
            value=7,
            step=1,
            key=fpi_key("storage_days")
        )

        storage_cost_day = st.number_input(
            f"🏪 Storage cost ({currency_symbol}/ton/day)",
            min_value=0.0,
            value=200.0 if current_country == "Nigeria" else 5.0,
            step=10.0 if current_country == "Nigeria" else 1.0,
            key=fpi_key("storage_cost")
        )

    if st.button(
        "📊 Calculate Farm Indicators",
        key=fpi_key("calculate"),
        use_container_width=True
    ):
        score = 100.0
        score -= 0.45 * pest
        score -= 0.45 * disease

        if 45 <= soil_moist <= 70:
            score += 5
        elif soil_moist < 30 or soil_moist > 85:
            score -= 10

        if ndvi >= 0.70:
            score += 8
        elif ndvi >= 0.50:
            score += 4
        elif ndvi < 0.30:
            score -= 12

        score = max(0.0, min(100.0, score))

        if score >= 80:
            health_status = "Excellent"
        elif score >= 65:
            health_status = "Good"
        elif score >= 45:
            health_status = "Moderate"
        else:
            health_status = "Needs Attention"

        stress_points = 0

        if soil_moist < 30:
            stress_points += 2
        elif soil_moist < 45:
            stress_points += 1

        if temp > 35:
            stress_points += 2
        elif temp > 30:
            stress_points += 1

        if et0 > 6:
            stress_points += 2
        elif et0 > 4:
            stress_points += 1

        if stress_points >= 4:
            water_level = "High"
            water_rec = "Irrigation should be prioritised."

        elif stress_points >= 2:
            water_level = "Moderate"
            water_rec = "Monitor soil moisture closely."

        else:
            water_level = "Low"
            water_rec = "Current indicators do not suggest significant water stress."

        margin_per_ton = price - cost
        gross_margin = margin_per_ton * expected_yield
        delay_cost = storage_days * storage_cost_day * expected_yield
        adjusted_margin = gross_margin - delay_cost

        if margin_per_ton <= 0:
            market_status = "Needs Attention"
            market_note = "Current selling price does not cover estimated production cost."

        elif adjusted_margin <= 0:
            market_status = "High Storage Risk"
            market_note = "Storage costs could remove the expected profit."

        elif delay_cost > gross_margin * 0.10:
            market_status = "Moderate"
            market_note = "Storage costs are reducing the expected margin."

        else:
            market_status = "Ready"
            market_note = "Current price and estimated costs indicate a positive selling margin."

        st.divider()

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric(
                "🌿 Field Health Score",
                f"{score:.1f}/100",
                health_status
            )

        with r2:
            st.metric(
                "💧 Water Stress",
                water_level
            )

        with r3:
            st.metric(
                "💹 Market Readiness",
                market_status
            )

        st.write("### 🌱 Field Assessment")
        st.write(f"Health Status: {health_status}")
        st.write(f"Water Recommendation: {water_rec}")

        st.write("### 💰 Farm Economics")

        e1, e2, e3 = st.columns(3)

        with e1:
            st.metric(
                "Margin / Ton",
                f"{currency_symbol}{margin_per_ton:,.2f}"
            )

        with e2:
            st.metric(
                "Gross Margin",
                f"{currency_symbol}{gross_margin:,.2f}"
            )

        with e3:
            st.metric(
                "Adjusted Margin",
                f"{currency_symbol}{adjusted_margin:,.2f}"
            )

        st.info(market_note)

        rows_key = fpi_key("rows")

        if rows_key not in st.session_state:
            st.session_state[rows_key] = []
            st.session_state[rows_key].append({
            "Timestamp": datetime.now().isoformat(timespec="seconds"),
            "Farm ID": current_farm_id,
            "Farm": current_farm_name,
            "Crop": current_crop,
            "Location": current_location,
            "Country": current_country,
            "Farm Size": current_farm_size,
            "Pest %": pest,
            "Disease %": disease,
            "Soil Moisture %": soil_moist,
            "NDVI": ndvi,
            "Temperature °C": temp,
            "ET0 mm/day": et0,
            "Expected Yield Tons": expected_yield,
            f"Price {currency_code}/Ton": price,
            f"Cost {currency_code}/Ton": cost,
            "Storage Days": storage_days,
            f"Storage Cost {currency_code}/Ton/Day": storage_cost_day,
            "Field Health Score": round(score, 1),
            "Health Status": health_status,
            "Water Stress": water_level,
            f"Margin/Ton {currency_code}": round(margin_per_ton, 2),
            f"Gross Margin {currency_code}": round(gross_margin, 2),
            f"Adjusted Margin {currency_code}": round(adjusted_margin, 2),
            "Market Status": market_status,
            "Recommendation": market_note,
        })

        st.success(
            f"✅ Performance snapshot saved for {current_farm_name}."
        )

    rows_key = fpi_key("rows")
    rows = st.session_state.get(rows_key, [])

    if rows:
        st.divider()

        st.subheader(
            f"🧾 Performance History — {current_farm_name}"
        )

        df = pd.DataFrame(rows)

        st.dataframe(
            df,
            use_container_width=True
        )

        col_a, col_b = st.columns(2)

        with col_a:
            st.download_button(
                "⬇️ Download CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"{current_farm_name}_farm_performance_indicators.csv",
                mime="text/csv",
                key=fpi_key("download"),
                use_container_width=True
            )

        with col_b:
            if st.button(
                "🧹 Clear Snapshots",
                key=fpi_key("clear"),
                use_container_width=True
            ):
                st.session_state[rows_key] = []
                st.rerun()

    else:
        st.info(
            "No performance snapshots saved for this farm yet."
        )

# ============================================================
# AI PREDICTIONS — UNIFIED FARM-AWARE PLATFORM
# ============================================================

def ai_predictions_ui():
    st.header("🧪 AI-Powered Farm Predictions")

    # -------------------------------------------------
    # CURRENT FARM CONTEXT
    # -------------------------------------------------
    current_farm = st.session_state.get("current_farm", {})

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "")
    current_location = current_farm.get("location", "")
    current_farm_size = current_farm.get("farm_size", 1.0)

    try:
        current_farm_size = float(current_farm_size)
    except (TypeError, ValueError):
        current_farm_size = 1.0

    if current_farm_size <= 0:
        current_farm_size = 1.0

    st.info(
        f"🌿 Current Farm: {current_farm_name} | "
        f"Crop: {current_crop or 'Not specified'} | "
        f"Location: {current_location or 'Not specified'}"
    )

    # -------------------------------------------------
    # ACTIVE AI TOOL
    # -------------------------------------------------
    active_key = "ai_predictions_active_tool"

    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # Support older voice/navigation state if available
    if (
        "ai_prediction_tool" in st.session_state
        and st.session_state[active_key] is None
    ):
        old_tool = st.session_state.get("ai_prediction_tool")

        tool_map = {
            "Crop Disease Detection": "disease",
            "Yield Prediction": "yield",
            "Soil Health Check": "soil",
            "Decision-Making Models": "decision",
        }

        st.session_state[active_key] = tool_map.get(old_tool)

    # -------------------------------------------------
    # AI TOOL BUTTONS
    # -------------------------------------------------
    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        if st.button(
            "🦠 Disease Detection",
            key=f"ai_pred_disease_button_{current_farm_id}",
            use_container_width=True,
        ):
            st.session_state[active_key] = "disease"

    with c2:
        if st.button(
            "📈 Yield Prediction",
            key=f"ai_pred_yield_button_{current_farm_id}",
            use_container_width=True,
        ):
            st.session_state[active_key] = "yield"

    with c3:
        if st.button(
            "🧪 Soil Health",
            key=f"ai_pred_soil_button_{current_farm_id}",
            use_container_width=True,
        ):
            st.session_state[active_key] = "soil"

    with c4:
        if st.button(
            "🤖 Decision Model",
            key=f"ai_pred_decision_button_{current_farm_id}",
            use_container_width=True,
        ):
            st.session_state[active_key] = "decision"

    with c5:
        if st.button(
            "🔄 Reset",
            key=f"ai_pred_reset_button_{current_farm_id}",
            use_container_width=True,
        ):
            st.session_state[active_key] = None

    st.divider()

    active_tool = st.session_state.get(active_key)

    # -------------------------------------------------
    # DEFAULT SCREEN
    # -------------------------------------------------
    if active_tool is None:
        st.subheader("🧠 Smart Farm AI Prediction Centre")

        st.write(
            "Select an AI prediction tool above to analyse the current farm."
        )

        st.caption(
            "Disease detection, yield prediction, soil health analysis and "
            "decision-support models are connected to the Current Farm context."
        )

    # -------------------------------------------------
    # CROP DISEASE DETECTION
    # -------------------------------------------------
    elif active_tool == "disease":
        st.subheader("🦠 Crop Disease Detection")

        crop_name = st.text_input(
            "Crop",
            value=current_crop,
            key=f"ai_pred_disease_crop_{current_farm_id}",
        )
        uploaded_image = st.file_uploader(
            "Upload a clear crop leaf or plant image",
            type=["jpg", "jpeg", "png"],
            key=f"ai_pred_disease_image_{current_farm_id}",
        )

        if uploaded_image is not None:
            st.image(
                uploaded_image,
                caption=f"{crop_name or 'Crop'} image",
                use_container_width=True,
            )

        if st.button(
            "🔍 Analyse Crop",
            key=f"ai_pred_analyse_disease_{current_farm_id}",
        ):
            if uploaded_image is None:
                st.warning("Please upload a crop image first.")

            else:
                # -----------------------------------------
                # TEMPORARY CONSOLIDATED PREDICTION LOGIC
                # Replace with trained disease model later.
                # -----------------------------------------
                predicted_disease = "Maize Leaf Blight"
                confidence = 82

                st.success("Analysis completed.")

                m1, m2 = st.columns(2)

                with m1:
                    st.metric(
                        "Predicted Condition",
                        predicted_disease,
                    )

                with m2:
                    st.metric(
                        "Confidence",
                        f"{confidence}%",
                    )

                st.write("### Recommended Action")

                st.write(
                    "Inspect affected leaves, remove badly infected plant "
                    "material where appropriate, monitor nearby plants and "
                    "follow crop-specific disease-management guidance."
                )

                st.warning(
                    "🟡 Consolidated prediction logic. "
                    "The production disease-recognition model will replace "
                    "this temporary result during the AI model upgrade."
                )

    # -------------------------------------------------
    # YIELD PREDICTION
    # -------------------------------------------------
    elif active_tool == "yield":
        st.subheader("📈 Yield Prediction")

        crop_name = st.text_input(
            "Crop",
            value=current_crop,
            key=f"ai_pred_yield_crop_{current_farm_id}",
        )

        area = st.number_input(
            "Farm Area (hectares)",
            min_value=0.01,
            value=float(current_farm_size),
            step=0.1,
            key=f"ai_pred_yield_area_{current_farm_id}",
        )

        rainfall = st.number_input(
            "Expected Rainfall (mm)",
            min_value=0.0,
            value=800.0,
            step=10.0,
            key=f"ai_pred_yield_rainfall_{current_farm_id}",
        )

        fertilizer = st.number_input(
            "Fertilizer Applied (kg)",
            min_value=0.0,
            value=100.0,
            step=10.0,
            key=f"ai_pred_yield_fertilizer_{current_farm_id}",
        )

        if st.button(
            "📊 Predict Yield",
            key=f"ai_pred_run_yield_{current_farm_id}",
        ):
            # -----------------------------------------
            # TEMPORARY CONSOLIDATED YIELD FORMULA
            # Replace with trained regional ML model.
            # -----------------------------------------
            estimated_yield = (
                (area * 2.5)
                + (fertilizer * 0.1)
                + (rainfall * 0.05)
            )

            st.success("Yield prediction completed.")

            st.metric(
                "Estimated Yield",
                f"{estimated_yield:.2f} tonnes",
            )

            yield_per_hectare = estimated_yield / area

            st.metric(
                "Estimated Yield / Hectare",
                f"{yield_per_hectare:.2f} t/ha",
            )

            st.write(
                f"Prediction context: {crop_name or 'Selected crop'} "
                f"on {current_farm_name}."
            )
            st.warning(
                "🟡 Consolidated prediction logic. "
                "Final yield prediction will use crop, country, region, "
                "weather, soil, farm history and other farm data."
            )

    # -------------------------------------------------
    # SOIL HEALTH CHECK
    # -------------------------------------------------
    elif active_tool == "soil":
        st.subheader("🧪 Soil Health Check")

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1,
            key=f"ai_pred_soil_ph_{current_farm_id}",
        )

        nitrogen = st.number_input(
            "Nitrogen Level",
            min_value=0.0,
            value=50.0,
            step=1.0,
            key=f"ai_pred_soil_n_{current_farm_id}",
        )

        phosphorus = st.number_input(
            "Phosphorus Level",
            min_value=0.0,
            value=40.0,
            step=1.0,
            key=f"ai_pred_soil_p_{current_farm_id}",
        )

        potassium = st.number_input(
            "Potassium Level",
            min_value=0.0,
            value=45.0,
            step=1.0,
            key=f"ai_pred_soil_k_{current_farm_id}",
        )

        if st.button(
            "🌱 Analyse Soil",
            key=f"ai_pred_run_soil_{current_farm_id}",
        ):
            soil_score = 0
            recommendations = []

            if 5.5 <= ph <= 7.5:
                soil_score += 25
            else:
                recommendations.append(
                    "Review soil pH and apply crop-appropriate correction."
                )

            if nitrogen >= 40:
                soil_score += 25
            else:
                recommendations.append(
                    "Nitrogen appears low. Review nitrogen requirements."
                )

            if phosphorus >= 30:
                soil_score += 25
            else:
                recommendations.append(
                    "Phosphorus appears low. Review phosphorus requirements."
                )

            if potassium >= 35:
                soil_score += 25
            else:
                recommendations.append(
                    "Potassium appears low. Review potassium requirements."
                )

            if soil_score >= 75:
                soil_status = "Good"
            elif soil_score >= 50:
                soil_status = "Moderate"
            else:
                soil_status = "Needs Attention"

            m1, m2 = st.columns(2)

            with m1:
                st.metric(
                    "Soil Health",
                    soil_status,
                )

            with m2:
                st.metric(
                    "Soil Score",
                    f"{soil_score}/100",
                )

            if recommendations:
                st.write("### Recommendations")

                for recommendation in recommendations:
                    st.write(f"• {recommendation}")

            else:
                st.success(
                    "The entered soil indicators are within the current "
                    "recommended ranges."
                )

            st.warning(
                "🟡 Current soil analysis uses rule-based thresholds. "
                "Final implementation will integrate crop-specific, "
                "regional and sensor/laboratory soil intelligence."
            )

    # -------------------------------------------------
    # DECISION-MAKING MODEL
    # -------------------------------------------------
    elif active_tool == "decision":
        st.subheader("🤖 Farm Decision-Making Model")

        crop_name = st.text_input(
            "Crop",
            value=current_crop,
            key=f"ai_pred_decision_crop_{current_farm_id}",
        )

        soil_moisture = st.slider(
            "Soil Moisture (%)",
            min_value=0,
            max_value=100,
            value=60,
            key=f"ai_pred_decision_moisture_{current_farm_id}",
        )
        pest_status = st.selectbox(
            "Pest Situation",
            [
                "No Pest Detected",
                "Low Pest Activity",
                "Moderate Pest Activity",
                "High Pest Activity",
            ],
            key=f"ai_pred_decision_pest_{current_farm_id}",
        )

        market_price = st.number_input(
            "Current Market Price",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key=f"ai_pred_decision_price_{current_farm_id}",
        )

        if st.button(
            "🧠 Generate Farm Decision",
            key=f"ai_pred_run_decision_{current_farm_id}",
        ):
            decisions = []

            if soil_moisture < 40:
                decisions.append(
                    "💧 Irrigation priority: Soil moisture is low. "
                    "Consider irrigating the crop."
                )

            elif soil_moisture > 80:
                decisions.append(
                    "💧 Water management: Soil moisture is high. "
                    "Reduce irrigation and check drainage."
                )

            else:
                decisions.append(
                    "💧 Soil moisture is currently within a reasonable range."
                )

            if pest_status == "High Pest Activity":
                decisions.append(
                    "🐛 High pest risk: Inspect the field immediately and "
                    "apply appropriate integrated pest-management measures."
                )

            elif pest_status == "Moderate Pest Activity":
                decisions.append(
                    "🐛 Moderate pest activity: Increase field monitoring "
                    "and prepare suitable control measures."
                )

            elif pest_status == "Low Pest Activity":
                decisions.append(
                    "🐛 Low pest activity: Continue monitoring the crop."
                )

            else:
                decisions.append(
                    "🐛 No significant pest activity reported."
                )

            if market_price > 0:
                decisions.append(
                    f"📈 Recorded market price: {market_price:,.2f}. "
                    "Compare this with production cost and recent market "
                    "trends before deciding when to sell."
                )

            if crop_name:
                decisions.append(
                    f"🌱 These recommendations are currently being evaluated "
                    f"for {crop_name} on {current_farm_name}."
                )

            st.success("Decision analysis completed.")

            st.write("### Recommended Actions")

            for decision in decisions:
                st.write(f"• {decision}")

            st.warning(
                "🟡 This Decision-Making Model is currently rule-based. "
                "It will later combine PA, CSA, CIG, weather, soil, crop, "
                "sensor, disease, yield and market intelligence."
            )


# ==========================================
# 📈 Market & Economic Tools
# ==========================================

def market_economic_tools_ui():
    st.header("📈 Market & Economic Tools")

    # ==========================================================
    # CURRENT FARM CONTEXT
    # ==========================================================
    current_farm = st.session_state.get("current_farm", {})

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "")
    current_location = current_farm.get("location", "")

    farmer_profile = st.session_state.get("farmer_profile", {})
    if not isinstance(farmer_profile, dict):
        farmer_profile = {}

    personalized_profile = st.session_state.get("personalized_profile", {})
    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_country = (
        current_farm.get("country")
        or personalized_profile.get("country")
        or farmer_profile.get("country")
        or "Nigeria"
    )

    # ==========================================================
    # CURRENCY CONTEXT
    # ==========================================================
    currency_map = {
        "Nigeria": ("₦", "NGN"),
        "Canada": ("C$", "CAD"),
        "Iran": ("﷼", "IRR"),
        "Cyprus": ("€", "EUR"),
        "United States": ("$", "USD"),
        "USA": ("$", "USD"),
        "United Kingdom": ("£", "GBP"),
    }

    currency_symbol, currency_code = currency_map.get(
        current_country,
        ("$", "USD")
    )

    st.info(
        f"🌿 Current Farm: {current_farm_name} | "
        f"Crop: {current_crop or 'Not specified'} | "
        f"Location: {current_location or 'Not specified'} | "
        f"Currency: {currency_code}"
    )

    # ==========================================================
    # UNIQUE FARM KEYS
    # ==========================================================
    def market_key(name):
        return f"market_{current_farm_id}_{name}"

    active_key = market_key("active_tool")

    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # ==========================================================
    # TOOL BUTTONS
    # ==========================================================
    c1, c2, c3, c4 = st.columns([1, 1, 1, 0.6])

    with c1:
        if st.button(
            "💰 ROI Calculator",
            key=market_key("btn_roi"),
            use_container_width=True
        ):
            st.session_state[active_key] = "roi"

    with c2:
        if st.button(
            "📈 Price Trend Checker",
            key=market_key("btn_trend"),
            use_container_width=True
        ):
            st.session_state[active_key] = "trend"

    with c3:
        if st.button(
            "⚖️ Break-even Calculator",
            key=market_key("btn_breakeven"),
            use_container_width=True
        ):
            st.session_state[active_key] = "breakeven"

    with c4:
        if st.button(
            "🔄 Reset",
            key=market_key("btn_reset"),
            use_container_width=True
        ):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state.get(active_key)

    # ==========================================================
    # ROI CALCULATOR
    # ==========================================================
    if tool == "roi":
        st.subheader("💰 ROI Calculator")

        st.write(
            f"Estimate the return on investment for {current_farm_name}."
        )

        col_a, col_b = st.columns(2)

        with col_a:
            investment = st.number_input(
                f"Investment amount ({currency_symbol})",
                min_value=0.0,
                step=1000.0,
                format="%.2f",
                key=market_key("roi_investment")
            )

        with col_b:
            return_value = st.number_input(
                f"Total return ({currency_symbol})",
                min_value=0.0,
                step=1000.0,
                format="%.2f",
                key=market_key("roi_return")
            )

        if st.button(
            "Calculate ROI",
            key=market_key("roi_calc"),
            use_container_width=True
        ):
            if investment <= 0:
                st.warning(
                    f"Enter an investment greater than {currency_symbol}0."
                )

            else:
                net_profit = return_value - investment
                roi = (net_profit / investment) * 100

                r1, r2 = st.columns(2)

                with r1:
                    st.metric(
                        "Net Profit",
                        f"{currency_symbol}{net_profit:,.2f}"
                    )

                with r2:
                    st.metric(
                        "ROI",
                        f"{roi:.2f}%"
                    )

                if roi > 0:
                    st.success(
                        "✅ The entered figures indicate a positive return."
                    )

                elif roi == 0:
                    st.info(
                        "The investment currently breaks even."
                    )

                else:
                    st.warning(
                        "The entered figures indicate a negative return."
                    )

    # ==========================================================
    # PRICE TREND CHECKER
    # ==========================================================
    elif tool == "trend":
        st.subheader("📈 Price Trend Checker")

        crop_name = st.text_input(
            "Crop name",
            value=current_crop or "Maize",
            key=market_key("trend_crop")
        )

        prices_csv = st.text_area(
            f"Enter recent prices in {currency_code}, separated by commas",
            value="120, 125, 130, 128, 135, 140",
            key=market_key("trend_prices"),
            help="Example: 120, 125, 130, 128, 135, 140"
        )

        if st.button(
            "Show Trend",
            key=market_key("trend_show"),
            use_container_width=True
        ):
            try:
                values = [
                    float(x.strip())
                    for x in prices_csv.split(",")
                    if x.strip()
                ]

                if len(values) < 2:
                    st.warning(
                        "Enter at least two price points."
                    )

                else:
                    df = pd.DataFrame(
                        {
                            "Period": list(
                                range(1, len(values) + 1)
                            ),
                            "Price": values
                        }
                    ).set_index("Period")

                    st.line_chart(df)

                    first_price = values[0]
                    last_price = values[-1]

                    change = last_price - first_price

                    if first_price != 0:
                        pct_change = (
                            change / first_price
                        ) * 100
                    else:
                        pct_change = 0.0

                    if change > 0:
                        direction = "increased"

                    elif change < 0:
                        direction = "decreased"

                    else:
                        direction = "not changed"

                    st.info(
                        f"{crop_name} price has {direction} by "
                        f"{currency_symbol}{abs(change):,.2f} "
                        f"(≈ {abs(pct_change):.2f}%) over the entered period."
                    )

            except ValueError:
                st.error(
                    "Invalid price input. Enter numbers separated by commas."
                )
                # ==========================================================
    # BREAK-EVEN CALCULATOR
    # ==========================================================
    elif tool == "breakeven":
        st.subheader("⚖️ Break-even Calculator")

        st.write(
            "Calculate how many units must be sold to cover farm costs."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            fixed_costs = st.number_input(
                f"Fixed costs ({currency_symbol})",
                min_value=0.0,
                step=1000.0,
                format="%.2f",
                key=market_key("be_fixed")
            )

        with c2:
            variable_cost = st.number_input(
                f"Variable cost per unit ({currency_symbol})",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                key=market_key("be_variable")
            )

        with c3:
            price_per_unit = st.number_input(
                f"Selling price per unit ({currency_symbol})",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                key=market_key("be_price")
            )

        if st.button(
            "Calculate Break-even",
            key=market_key("be_calc"),
            use_container_width=True
        ):
            contribution_margin = (
                price_per_unit - variable_cost
            )

            if contribution_margin <= 0:
                st.error(
                    "Selling price must be greater than "
                    "variable cost per unit."
                )

            elif fixed_costs <= 0:
                st.warning(
                    f"Enter fixed costs greater than {currency_symbol}0."
                )

            else:
                units = (
                    fixed_costs / contribution_margin
                )

                units_whole = int(units)

                if units > units_whole:
                    units_whole += 1

                break_even_revenue = (
                    units_whole * price_per_unit
                )

                b1, b2 = st.columns(2)

                with b1:
                    st.metric(
                        "Break-even Units",
                        f"{units_whole:,}"
                    )

                with b2:
                    st.metric(
                        "Break-even Revenue",
                        f"{currency_symbol}{break_even_revenue:,.2f}"
                    )

                st.success(
                    f"🎯 You need to sell approximately "
                    f"{units_whole:,} units to cover the entered costs."
                )

    # ==========================================================
    # DEFAULT VIEW
    # ==========================================================
    else:
        st.info(
            "Choose ROI Calculator, Price Trend Checker, "
            "or Break-even Calculator above."
        )

# ================================
# 📚 AI Farm Tips
# ================================

def ai_farm_tips_ui():
    st.header("📚 AI Farm Tips")

    current_farm = st.session_state.get("current_farm", {})

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "")
    current_location = current_farm.get("location", "")

    farmer_profile = st.session_state.get("farmer_profile", {})
    if not isinstance(farmer_profile, dict):
        farmer_profile = {}

    personalized_profile = st.session_state.get("personalized_profile", {})
    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_country = (
        current_farm.get("country")
        or personalized_profile.get("country")
        or farmer_profile.get("country")
        or "Not specified"
    )

    st.info(
        f"🌿 Current Farm: {current_farm_name} | "
        f"Crop: {current_crop or 'Not specified'} | "
        f"Location: {current_location or 'Not specified'} | "
        f"Country: {current_country}"
    )

    active_key = f"ai_farm_tips_{current_farm_id}_active_tool"

    if active_key not in st.session_state:
        st.session_state[active_key] = None

    c1, c2, c3 = st.columns([1.3, 1.3, 0.9])

    with c1:
        if st.button(
            "💡 Ask AI Tip",
            key=f"ai_farm_tips_{current_farm_id}_ask"
        ):
            st.session_state[active_key] = "ask"

    with c2:
        if st.button(
            "🌞 View Daily Tip",
            key=f"ai_farm_tips_{current_farm_id}_daily"
        ):
            st.session_state[active_key] = "daily"

    with c3:
        if st.button(
            "🔄 Reset",
            key=f"ai_farm_tips_{current_farm_id}_reset"
        ):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state.get(active_key)

    if tool == "ask":
        st.subheader("💡 Ask AI Farm Tip")

        user_q = st.text_input(
            "Ask your farming question:",
            key=f"ai_farm_tips_{current_farm_id}_question"
        )

        if st.button(
            "🧠 Get AI Tip",
            key=f"ai_farm_tips_{current_farm_id}_get_tip"
        ):
            if not user_q.strip():
                st.warning("Please enter a farming question first.")

            else:
                q = user_q.lower()

                crop_text = current_crop or "your crop"

                if any(word in q for word in ["fertilizer", "npk", "manure", "compost"]):
                    tip = (
                        f"For {crop_text}, base fertilizer decisions on soil "
                        f"condition and crop growth stage. Split nutrient "
                        f"applications where appropriate to reduce losses."
                    )

                elif any(word in q for word in ["irrigation", "water", "drip", "sprinkler", "moisture"]):
                    tip = (
                        f"Monitor soil moisture on {current_farm_name} before irrigation. "
                        f"Avoid both prolonged water stress and overwatering."
                    )

                elif any(word in q for word in ["pest", "insect", "worm", "aphid", "armyworm"]):
                    tip = (
                        f"Inspect {crop_text} regularly for pests. "
                        f"Use integrated pest management and identify the pest "
                        f"before applying treatment."
                    )

                elif any(word in q for word in ["disease", "blight", "fungus", "mildew", "virus"]):
                    tip = (
                        f"Inspect affected {crop_text} carefully, remove severely "
                        f"infected material where appropriate, and improve field hygiene."
                    )

                elif any(word in q for word in ["soil", "ph", "nutrient", "organic matter"]):
                    tip = (
                        f"Use soil-test information for {current_farm_name} whenever "
                        f"available. Nutrient and pH recommendations should depend "
                        f"on the crop and local soil conditions."
                    )

                elif any(word in q for word in ["harvest", "maturity", "storage"]):
                    tip = (
                        f"Harvest {crop_text} at the correct maturity stage and "
                        f"use suitable handling and storage conditions."
                    )

                elif any(word in q for word in ["market", "price", "sell", "profit"]):
                    tip = (
                        f"Compare market price with production, transport, and "
                        f"storage costs before selling {crop_text}."
                    )

                elif any(word in q for word in ["seed", "variety", "germination", "planting"]):
                    tip = (
                        f"Use healthy planting material for {crop_text} and select "
                        f"varieties suitable for {current_location or 'your location'}."
                    )

                elif any(word in q for word in ["weather", "rain", "rainfall", "climate"]):
                    tip = (
                        f"Check rainfall, temperature, and local weather conditions "
                        f"before making planting, spraying, irrigation, or harvesting decisions."
                    )

                else:
                    tip = (
                        f"For {current_farm_name}, consider crop condition, soil, "
                        f"weather, crop stage, and farm records before making decisions."
                    )

                st.success("✅ Smart Farm AI Recommendation")
                st.write(tip)

                st.caption(
                    f"Farm: {current_farm_name} | "
                    f"Crop: {current_crop or 'Not specified'} | "
                    f"Location: {current_location or 'Not specified'}"
                )

    elif tool == "daily":
        st.subheader("🌞 Daily Farm Tip")

        tips_pool = [
            "Scout crops regularly for pests and diseases.",
            "Check soil moisture before irrigating.",
            "Keep records of inputs, labour, yield, and sales.",
            "Clean farm tools to reduce disease spread.",
            "Use mulch where suitable to conserve soil moisture.",
            "Match fertilizer use to crop and soil requirements.",
            "Check weather conditions before spraying.",
            "Inspect irrigation systems for leaks and blockage.",
            "Harvest crops at the correct maturity stage.",
            "Compare market prices with production costs before selling."
        ]

        day_index = date.today().timetuple().tm_yday % len(tips_pool)

        st.info(f"🌿 {tips_pool[day_index]}")

        st.caption(
            f"Daily tip for {current_farm_name} | "
            f"{current_crop or 'Crop not specified'}"
        )

    else:
        st.info("Choose Ask AI Tip or View Daily Tip above.")


# =========================================================
# IRRIGATION & SOIL
# =========================================================

def irrigation_ui():

    # ---------------------------------------------------------
    # CURRENT FARM
    # ---------------------------------------------------------

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get(
        "farm_id",
        "main_farm"
    )

    current_farm_name = current_farm.get(
        "farm_name",
        "Main Farm"
    )

    current_crop = current_farm.get(
        "crop_type",
        "Not specified"
    )

    current_location = current_farm.get(
        "location",
        "Not specified"
    )

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------

    st.header("💧 Irrigation & Soil")

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # ---------------------------------------------------------
    # FIVE FEATURES
    # ---------------------------------------------------------

    irrigation_option = st.selectbox(
        "💧 Select an Irrigation & Soil Feature",
        [
            "💧 Irrigation Schedule",
            "🌱 Soil Health Record",
            "🌱 Soil Moisture Checker",
            "🚰 Water Usage Log",
            "💰 Irrigation Cost Estimator"
        ],
        key="irrigation_feature_v2"
    )

    # =========================================================
    # 1. IRRIGATION SCHEDULE
    # =========================================================

    if irrigation_option == "💧 Irrigation Schedule":

        st.subheader("💧 Irrigation Schedule")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        irrigation_date = st.date_input(
            "📅 Irrigation Date",
            key="irrigation_schedule_date_v2"
        )

        water_volume = st.number_input(
            "💧 Water Volume (liters)",
            min_value=0.0,
            step=1.0,
            key="irrigation_schedule_volume_v2"
        )

        if st.button(
            "💾 Save Irrigation Record",
            key="irrigation_schedule_save_v2"
        ):

            irrigation_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "date": str(irrigation_date),
                "water_volume": water_volume
            }

            try:
                with open(
                    "irrigation_schedule.json",
                    "r"
                ) as file:
                    irrigation_data = json.load(file)

                if not isinstance(irrigation_data, list):
                    irrigation_data = []

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):
                irrigation_data = []

            irrigation_data.append(irrigation_record)

            with open(
                "irrigation_schedule.json",
                "w"
            ) as file:
                json.dump(
                    irrigation_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Irrigation record saved for "
                f"{current_farm_name}."
            )

    # =========================================================
    # 2. SOIL HEALTH RECORD
    # =========================================================

    elif irrigation_option == "🌱 Soil Health Record":

        st.subheader("🌱 Soil Health Record")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")
        soil_ph = st.number_input(
            "🧪 Soil pH Level",
            min_value=0.0,
            max_value=14.0,
            step=0.1,
            key="irrigation_soil_ph_v2"
        )

        moisture_content = st.number_input(
            "💧 Moisture Content (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="irrigation_soil_moisture_v2"
        )

        nutrient_content = st.text_input(
            "🌿 Nutrient Content Summary",
            key="irrigation_soil_nutrients_v2"
        )

        test_date = st.date_input(
            "📅 Test Date",
            key="irrigation_soil_date_v2"
        )

        if st.button(
            "💾 Save Soil Health Record",
            key="irrigation_soil_save_v2"
        ):

            soil_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "soil_ph": soil_ph,
                "moisture_content": moisture_content,
                "nutrient_content": nutrient_content,
                "test_date": str(test_date)
            }

            try:
                with open(
                    "soil_health_records.json",
                    "r"
                ) as file:
                    soil_data = json.load(file)

                if not isinstance(soil_data, list):
                    soil_data = []

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):
                soil_data = []

            soil_data.append(soil_record)

            with open(
                "soil_health_records.json",
                "w"
            ) as file:
                json.dump(
                    soil_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Soil health record saved for "
                f"{current_farm_name}."
            )

        # -----------------------------------------------------
        # CURRENT FARM SOIL RECORDS
        # -----------------------------------------------------

        st.divider()

        st.subheader(
            f"📋 Soil Records — {current_farm_name}"
        )

        try:
            with open(
                "soil_health_records.json",
                "r"
            ) as file:
                soil_data = json.load(file)

            if not isinstance(soil_data, list):
                soil_data = []

            farm_soil = [
                entry
                for entry in soil_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

            if farm_soil:

                for entry in farm_soil:

                    st.markdown(
                        f"""
- 📅 Test Date: {entry.get('test_date', '')}
- 🧪 Soil pH: {entry.get('soil_ph', 0)}
- 💧 Moisture: {entry.get('moisture_content', 0)}%
- 🌿 Nutrients: {entry.get('nutrient_content', '')}
---
"""
                    )

            else:

                st.info(
                    f"No soil health records for "
                    f"{current_farm_name}."
                )

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            st.info(
                f"No soil health records for "
                f"{current_farm_name} yet."
            )

    # =========================================================
    # 3. SOIL MOISTURE CHECKER
    # =========================================================

    elif irrigation_option == "🌱 Soil Moisture Checker":

        st.subheader("🌱 Soil Moisture Checker")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        plot_id = st.text_input(
            "🆔 Plot ID",
            key="soil_moisture_plot_id_v2"
        )
        moisture_level = st.slider(
            "💦 Moisture Level (%)",
            min_value=0,
            max_value=100,
            value=50,
            key="soil_moisture_level_v2"
        )

        if st.button(
            "💾 Save Moisture Reading",
            key="soil_moisture_save_v2"
        ):

            moisture_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "plot_id": plot_id,
                "moisture_level": moisture_level
            }

            try:
                with open(
                    "soil_moisture_records.json",
                    "r"
                ) as file:
                    moisture_data = json.load(file)

                if not isinstance(moisture_data, list):
                    moisture_data = []

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):
                moisture_data = []

            moisture_data.append(moisture_record)

            with open(
                "soil_moisture_records.json",
                "w"
            ) as file:
                json.dump(
                    moisture_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Soil moisture for "
                f"{current_farm_name} recorded as "
                f"{moisture_level}%."
            )

    # =========================================================
    # 4. WATER USAGE LOG
    # =========================================================

    elif irrigation_option == "🚰 Water Usage Log":

        st.subheader("🚰 Water Usage Log")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        with st.form(
            "water_usage_log_form_v2"
        ):

            water_date = st.date_input(
                "📅 Date of Irrigation",
                key="water_usage_date_v2"
            )

            water_used = st.number_input(
                "💧 Water Used (liters)",
                min_value=0.0,
                step=1.0,
                key="water_usage_amount_v2"
            )

            submitted = st.form_submit_button(
                "💾 Log Water Usage"
            )

        if submitted:

            water_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "date": str(water_date),
                "water_used": water_used
            }

            try:
                with open(
                    "water_usage_records.json",
                    "r"
                ) as file:
                    water_data = json.load(file)

                if not isinstance(water_data, list):
                    water_data = []

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):
                water_data = []

            water_data.append(water_record)

            with open(
                "water_usage_records.json",
                "w"
            ) as file:
                json.dump(
                    water_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ {water_used:,.1f} liters recorded "
                f"for {current_farm_name}."
            )

    # =========================================================
    # 5. IRRIGATION COST ESTIMATOR
    # =========================================================

    elif irrigation_option == "💰 Irrigation Cost Estimator":

        st.subheader("💰 Irrigation Cost Estimator")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")
        water_volume = st.number_input(
            "🚿 Enter Water Usage (liters)",
            min_value=0.0,
            step=1.0,
            key="irrigation_cost_water_v2"
        )

        cost_per_liter = st.number_input(
            "💸 Cost per Liter (₦)",
            min_value=0.0,
            step=0.01,
            key="irrigation_cost_per_liter_v2"
        )

        if st.button(
            "💰 Estimate Cost",
            key="irrigation_cost_estimate_v2"
        ):

            total_cost = (
                water_volume *
                cost_per_liter
            )

            st.success(
                f"💰 Estimated irrigation cost for "
                f"{current_farm_name}: "
                f"₦{total_cost:,.2f}"
            )



# =========================

# MARKET & FINANCE

# =========================

def market_finance_ui():

    market_option = st.sidebar.selectbox("📈 Select a Market Feature", [

        "📊 Market Price Fetcher",

        "📋 Farm Budget Planner",

        "💵 Farm Loan Tracker"

    ], key="market_feature")



    if market_option == "📊 Market Price Fetcher":

        st.subheader("📊 Market Price Fetcher")

        crop = st.selectbox("🌾 Select Crop", ["Maize", "Rice", "Cassava", "Tomato", "Yam"])

        location = st.text_input("📍 Enter Location")

        if st.button("📥 Fetch Market Price"):

            prices = {

                "Maize": "₦42,000 per ton",

                "Rice": "₦55,000 per bag",

                "Cassava": "₦12,000 per ton",

                "Tomato": "₦10,000 per basket",

                "Yam": "₦300 per tuber"

            }

            st.success(f"🛒 Market price of {crop} in {location} is {prices.get(crop)}")



    elif market_option == "📋 Farm Budget Planner":

        st.subheader("📋 Farm Budget Planner")

        income = st.number_input("💰 Expected Income (₦)", min_value=0)

        expenses = st.number_input("💸 Estimated Expenses (₦)", min_value=0)

        if st.button("📊 Calculate Budget"):

            balance = income - expenses

            if balance > 0:

                st.success(f"✅ Profit Estimate: ₦{balance}")

            elif balance == 0:

                st.info("⚖️ Break-even: No profit or loss.")

            else:

                st.error(f"⚠️ Loss Estimate: ₦{abs(balance)}")



    elif market_option == "💵 Farm Loan Tracker":

        st.subheader("💵 Farm Loan Tracker")

        loan_amount = st.number_input("🏦 Loan Amount (₦)", min_value=0)

        interest_rate = st.number_input("📈 Interest Rate (%)", min_value=0.0)

        duration_months = st.number_input("📅 Duration (months)", min_value=1)

        if st.button("📉 Calculate Loan Repayment"):

            total_interest = (loan_amount * interest_rate * duration_months) / (100 * 12)

            total_payment = loan_amount + total_interest

            monthly_payment = total_payment / duration_months

            st.info(f"📌 Total Repayment: ₦{round(total_payment, 2)}")

            st.info(f"📅 Monthly Payment: ₦{round(monthly_payment, 2)}")



# =========================

# SENSORS & MONITORING

# =========================

def sensors_monitoring_ui():

    sensor_option = st.sidebar.selectbox("📡 Select a Monitoring Feature", [

        "📈 Live Sensor Dashboard",

        "🚨 Sensor Alerts",

        "🌦 Weather Forecast",

        "🧠 Smart Tutor Assistant",

    ], key="sensor_monitoring")



    if sensor_option == "📈 Live Sensor Dashboard":

        st.subheader("📈 Live Sensor Dashboard")

        st.info("This dashboard displays real-time data from your connected farm sensors.")

        temperature = 28.5  # °C

        humidity = 65       # %

        soil_moisture = 40  # %

        st.metric("🌡 Temperature", f"{temperature} °C")

        st.metric("💧 Humidity", f"{humidity} %")

        st.metric("🌱 Soil Moisture", f"{soil_moisture} %")



    elif sensor_option == "🚨 Sensor Alerts":

        st.subheader("🚨 Sensor Alerts")

        moisture_level = random.randint(20, 100)  # %

        temperature = random.randint(10, 40)      # °C

        st.info(f"💧 Soil Moisture: {moisture_level}%")

        st.info(f"🌡 Temperature: {temperature}°C")

        if moisture_level < 40:

            st.warning("⚠️ Low moisture detected. Consider irrigating the crops.")

        elif moisture_level > 80:

            st.warning("⚠️ Excessive moisture. Risk of root rot.")

        if temperature > 35:

            st.error("🔥 High temperature detected! Take cooling measures immediately.")

        elif temperature < 15:

            st.warning("❄️ Low temperature detected. Protect crops from cold stress.")

        st.success("✅ All other sensor readings are in safe limits.")



    elif sensor_option == "🌦 Weather Forecast":

        st.subheader("🌦 Weather Forecast")

        st.success("Here's your local 3-day forecast.")

        forecast = {

            "Today": {"condition": "Sunny", "temp": "31°C"},

            "Tomorrow": {"condition": "Partly Cloudy", "temp": "29°C"},

            "Next Day": {"condition": "Rainy", "temp": "25°C"},

        }

        for day, data in forecast.items():

            st.write(f"{day} — {data['condition']}, 🌡 {data['temp']}")



    elif sensor_option == "🧠 Smart Tutor Assistant":

        st.subheader("📚 Smart Tutor")

        tips = [

            "Rotate your crops each season to maintain soil fertility. 🌱",

            "Use organic compost to boost plant health naturally. ♻️",

            "Water early in the morning to reduce evaporation. 💧",

            "Monitor your plants weekly for early signs of pests. 🐛",

            "Test your soil every year to know the right fertilizer to use. 🧪",

            "Intercropping can help reduce pests and increase yield. 🌾",

            "Mulch your soil to retain moisture and control weeds. 🌿",

            "Choose disease-resistant seed varieties for better harvests. 🌻"

        ]

        if st.button("💡 Get Advice", key="smart_tutor_tip"):

            st.success(random.choice(tips))


# =========================================================
# SUPPORT & HELP — FINAL INTEGRATED VERSION
# =========================================================

def support_help_ui():

    import streamlit as st
    import json
    import random
    import os
    import tempfile
    from datetime import datetime

    st.header("🆘 Support & Help")

    # =====================================================
    # CURRENT FARM CONTEXT
    # =====================================================

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(current_farm, dict):
        current_farm = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_farm_id = current_farm.get(
        "farm_id",
        "main_farm"
    )

    current_farm_name = current_farm.get(
        "farm_name",
        personalized_profile.get(
            "current_farm_name",
            "Main Farm"
        )
    )

    current_crop = current_farm.get(
        "crop_type",
        personalized_profile.get(
            "crop_type",
            "Not specified"
        )
    )

    current_location = current_farm.get(
        "location",
        personalized_profile.get(
            "location",
            "Not specified"
        )
    )

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # =====================================================
    # SUPPORT MENU
    # =====================================================

    help_option = st.sidebar.selectbox(
    "🆘 Select a Help Feature",
    [
        "👨‍🌾 Farmers Community Forum",
        "💾 Data Backup & Recovery",
        "📘 Tutorial & Guide",
        "🧑‍🏫 Smart Tutor (Multi-Language)",
        "🤖 Chatbot Assistant"
    ],
    key="support_help"
)

    # =====================================================
    # 1. FARMERS COMMUNITY FORUM
    # =====================================================

    if help_option == "👨‍🌾 Farmers Community Forum":

        st.subheader(
            "👨‍🌾 Farmers Community Forum"
        )

        st.write(
            "Connect with other farmers, share experiences, "
            "and ask questions."
        )

        try:

            with open(
                "forum_posts.json",
                "r"
            ) as file:

                forum_posts = json.load(file)

            if not isinstance(
                forum_posts,
                list
            ):

                forum_posts = []

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            forum_posts = []

        new_post = st.text_area(
            "💬 Share your thoughts or ask a question:",
            key="forum_new_post"
        )

        if st.button(
            "📢 Post Message",
            key="forum_post_btn"
        ):

            if not new_post.strip():

                st.warning(
                    "⚠️ Please enter a message before posting."
                )

            else:

                new_forum_post = {
                    "farm_id": current_farm_id,
                    "farm_name": current_farm_name,
                    "crop_type": current_crop,
                    "location": current_location,
                    "message": new_post.strip(),
                    "date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M"
                    )
                }

                forum_posts.append(
                    new_forum_post
                )

                with open(
                    "forum_posts.json",
                    "w"
                ) as file:

                    json.dump(
                        forum_posts,
                        file,
                        indent=4
                    )
                    st.success(
                    "✅ Your message has been posted!"
                )

                st.rerun()

        st.write("### 📜 Forum Messages")

        farm_posts = [
            post
            for post in forum_posts
            if isinstance(post, dict)
            and str(
                post.get(
                    "farm_id",
                    "main_farm"
                )
            ) == str(current_farm_id)
        ]

        if farm_posts:

            for idx, post in enumerate(
                reversed(farm_posts),
                1
            ):

                st.markdown(
                    f"""
👨‍🌾 {post.get('farm_name', 'Farmer')}

💬 {post.get('message', '')}

🌾 Crop: {post.get('crop_type', 'Not specified')}  
📍 Location: {post.get('location', 'Not specified')}  
📅 {post.get('date', '')}

---
"""
                )

        else:

            st.info(
                "No messages yet for this farm. "
                "Be the first to post!"
            )

    # =====================================================
    # 2. DATA BACKUP & RECOVERY
    # =====================================================

    elif help_option == "💾 Data Backup & Recovery":

        st.subheader(
            "💾 Data Backup & Recovery"
        )

        st.write(
            f"Backup and restore data associated with "
            f"{current_farm_name}."
        )

        backup_files = [
            "accounts.json",
            "sales_records.json",
            "expenses.json",
            "inventory.json",
            "plots.json",
            "forum_posts.json",
            "chem_inventory.json"
        ]

        backup_data = {}

        for filename in backup_files:

            try:

                with open(
                    filename,
                    "r"
                ) as file:

                    backup_data[filename] = json.load(
                        file
                    )

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):

                backup_data[filename] = []

        backup_json = json.dumps(
            backup_data,
            indent=4
        ).encode("utf-8")

        st.download_button(
            "📤 Backup Farm Data",
            data=backup_json,
            file_name=f"{current_farm_id}_backup.json",
            mime="application/json",
            key="support_backup_download"
        )

        st.success(
            "✅ Your available Smart Farm AI data "
            "is ready for backup."
        )

        st.divider()

        st.write(
            "📥 Restore Data"
        )

        restore_file = st.file_uploader(
            "Upload a Smart Farm AI backup file",
            type=["json"],
            key="support_restore_file"
        )

        if restore_file is not None:

            if st.button(
                "Restore Backup",
                key="support_restore_btn"
            ):

                try:

                    restored_data = json.load(
                        restore_file
                    )

                    if not isinstance(
                        restored_data,
                        dict
                    ):

                        st.error(
                            "❌ Invalid backup format."
                        )

                    else:

                        restored_count = 0

                        for filename, data in restored_data.items():

                            if filename in backup_files:

                                with open(
                                    filename,
                                    "w"
                                ) as file:

                                    json.dump(
                                        data,
                                        file,
                                        indent=4
                                    )
                                    restored_count += 1

                        st.success(
                            f"✅ Backup restored successfully. "
                            f"{restored_count} data files restored."
                        )

                        st.rerun()

                except (
                    json.JSONDecodeError,
                    UnicodeDecodeError
                ):

                    st.error(
                        "❌ Could not read the backup file."
                    )

                except Exception as e:

                    st.error(
                        f"❌ Restore error: {e}"
                    )

    # =====================================================
    # 3. TUTORIAL & GUIDE
    # =====================================================

    elif help_option == "📘 Tutorial & Guide":

        st.subheader(
            "📘 Tutorial & Guide"
        )

        st.write(
            "Step-by-step guidance for using "
            "Smart Farm AI."
        )

        st.markdown(
            """
### 🌿 Farm Management
Manage your farm, plots, crops, fertilizer, pesticide stock,
calendar, drone scheduling, and voice commands.

### 📊 Productivity & Records
Track sales, expenses, profit, farmer records, productivity,
yield, loans, inventory, reports, and farm summaries.

### 🧠 AI Predictions
Use AI tools for crop disease detection, yield prediction,
soil health, and farm decision support.

### 💧 Irrigation & Soil
Manage irrigation and soil-related farm information.

### 💹 Market & Finance
Work with market and financial information relevant to the farm.

### 📡 Sensors & Monitoring
Monitor available farm sensor information and connected devices.

### 🆘 Support & Help
Use the Farmers Community Forum, Backup & Recovery,
Tutorial, Smart Tutor, and Chatbot Assistant.
"""
        )

        tips = [
            "Rotate your crops each season to maintain soil fertility. 🌱",
            "Use organic compost to improve soil health. ♻️",
            "Water early in the morning to reduce evaporation. 💧",
            "Monitor your plants regularly for early signs of pests. 🐛",
            "Test your soil regularly to guide fertilizer decisions. 🧪",
            "Intercropping can help manage pests and improve productivity. 🌾",
            "Mulch your soil to retain moisture and control weeds. 🌿",
            "Choose suitable seed varieties for your farming conditions. 🌻"
        ]

        if st.button(
            "💡 Get Advice",
            key="smart_tutor_tip"
        ):

            st.success(
                random.choice(tips)
            )

    # =====================================================
    # 4. SMART TUTOR — MULTI-LANGUAGE
    # =====================================================

    elif help_option == "🧑‍🏫 Smart Tutor (Multi-Language)":

        st.subheader(
            "🧑‍🏫 Smart Tutor (Multi-Language) + 🎙️ Voice"
        )

        st.caption(
            "Ask farming questions by voice or typing."
        )

        LANGS = [
            "Urhobo",
            "Yorùbá",
            "Hausa",
            "Ịjọ (Ijaw)",
            "Efik (Calabar)",
            "Ịgbò (Igbo)",
            "Edo (Bini)",
            "Tiv",
            "Ibibio",
            "Kanuri",
            "Nupe",
            "Fulfulde (Fula)",
            "Itsekiri",
            "Gbagyi",
            "Idoma",
            "Ebira",
            "Jukun",
            "Igala",
            "Berom (Birom)",
            "Esan",
            "Isoko",
            "Okun (Yoruba dialect)",
            "Ika",
            "English (for reference)"
        ]

        DOMAINS = [
            "General chat",
            "Farming & Agriculture",
            "Business & Finance",
            "Health & Safety (non-medical advice)",
            "Education & Study Help"
        ]

        TONES = [
            "Neutral",
            "Friendly",
            "Professional",
            "Encouraging",
            "Brief"
        ]

        c1, c2, c3 = st.columns(
            [1.2, 1, 1]
        )
        lang = c1.selectbox(
            "Language",
            LANGS,
            index=0,
            key="ml_lang"
        )

        domain = c2.selectbox(
            "Domain",
            DOMAINS,
            index=1,
            key="ml_domain"
        )

        tone = c3.selectbox(
            "Tone",
            TONES,
            index=1,
            key="ml_tone"
        )

        input_mode = st.radio(
            "Input Mode",
            [
                "🎙️ Voice",
                "⌨️ Typing"
            ],
            horizontal=True,
            key="ml_input_mode"
        )

        auto_speak = st.toggle(
            "🔁 Auto-speak reply",
            value=True,
            key="ml_auto_speak"
        )

        tts_lang_hint = st.selectbox(
            "TTS language",
            [
                "auto (best effort)",
                "en",
                "ha",
                "yo",
                "ig"
            ],
            key="ml_tts_code"
        )

        # =================================================
        # OPTIONAL DEPENDENCIES
        # =================================================

        try:

            import speech_recognition as sr

        except Exception:

            sr = None

        try:

            import pyttsx3

        except Exception:

            pyttsx3 = None

        try:

            from gtts import gTTS

        except Exception:

            gTTS = None

        # =================================================
        # OPENAI
        # =================================================

        try:

            from openai import OpenAI

            if os.getenv(
                "OPENAI_API_KEY"
            ):

                client = OpenAI()

            else:

                client = None

        except Exception:

            client = None

        # =================================================
        # MODEL ANSWER
        # =================================================

        def _model_answer(
            user_text
        ):

            system_prompt = f"""
You are Smart Farm AI Smart Tutor.

Current farm:
Farm name: {current_farm_name}
Crop: {current_crop}
Location: {current_location}

Reply entirely in {lang}.
Domain: {domain}.
Tone: {tone}.

Give clear, practical, farmer-friendly guidance.
Use short paragraphs and bullet points when useful.
""".strip()

            if client is not None:

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            {
                                "role": "user",
                                "content": user_text
                            }
                        ],
                        temperature=0.6,
                        max_tokens=380
                    )

                    return (
                        response
                        .choices[0]
                        .message
                        .content
                        or ""
                    ).strip()

                except Exception:

                    pass

            return (
                f"🌱 Smart Farm AI — {lang}\n\n"
                f"Your question: {user_text.strip()}\n\n"
                "1. Identify the main farm problem.\n"
                "2. Check the crop, soil, weather, and farm conditions.\n"
                "3. Apply the safest practical farming action.\n"
                "4. Monitor the result and keep a record.\n\n"
                "💡 Review the farm regularly and use available "
                "Smart Farm AI tools for better decisions."
            )

        # =================================================
        # TEXT TO SPEECH
        # =================================================

        def _speak_text(
            text,
            lang_code="en"
        ):

            if pyttsx3 is not None:

                try:

                    engine = pyttsx3.init()

                    engine.say(
                        text
                    )

                    engine.runAndWait()

                    st.caption(
                        "🔉 Played using offline TTS."
                    )

                    return

                except Exception:

                    pass

            if gTTS is not None:

                try:

                    allowed_codes = {
                        "en",
                        "ha",
                        "yo",
                        "ig"
                    }

                    use_code = (
                        lang_code
                        if lang_code in allowed_codes
                        else "en"
                    )

                    tts = gTTS(
                        text=text,
                        lang=use_code
                    )

                    import tempfile

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp3"
                    ) as tmp:

                        tts.save(
                            tmp.name
                        )

                        st.audio(
                            tmp.name,
                            format="audio/mp3"
                        )

                    return

                except Exception:

                    pass

            st.info(
                "🔇 Audio playback is unavailable."
            )

        # =================================================
        # CONVERSATION HISTORY
        # =================================================

        if "ml_msgs" not in st.session_state:

            st.session_state.ml_msgs = []

        query_text = ""

        # =================================================
        # VOICE / TYPING INPUT
        # =================================================

        if input_mode == "🎙️ Voice":

            if st.button(
                "🎤 Tap to Record",
                key="ml_mic_btn"
            ):

                if sr is None:

                    st.error(
                        "SpeechRecognition is not installed."
                    )

                else:

                    try:

                        recognizer = sr.Recognizer()

                        with sr.Microphone() as source:

                            st.info(
                                "🎤 Listening..."
                            )

                            try:

                                recognizer.adjust_for_ambient_noise(
                                    source,
                                    duration=0.5
                                )

                            except Exception:

                                pass

                            audio = recognizer.listen(
                                source,
                                timeout=4,
                                phrase_time_limit=8
                            )

                        query_text = (
                            recognizer
                            .recognize_google(
                                audio,
                                language="en"
                            )
                        )

                        st.success(
                            f"🗣️ Recognized: {query_text}"
                        )

                    except sr.WaitTimeoutError:

                        st.error(
                            "Listening timed out. "
                            "Please try again."
                        )

                    except sr.UnknownValueError:

                        st.error(
                            "I could not understand the audio. "
                            "Please try again."
                        )

                    except sr.RequestError:
                        st.error(
                            "Speech recognition service "
                            "is unavailable."
                        )

                    except Exception as e:

                        st.error(
                            f"Voice recognition error: {e}"
                        )

            user_text = st.text_area(
                "Your question:",
                value=query_text,
                key="ml_textarea",
                height=120
            )

        else:

            user_text = st.text_area(
                "Type your question / prompt",
                placeholder=(
                    "Ask Smart Farm AI about farming..."
                ),
                key="ml_query",
                height=140
            )

        # =================================================
        # GENERATE TUTOR RESPONSE
        # =================================================

        if st.button(
            "Generate",
            type="primary",
            key="ml_go"
        ):

            if not user_text.strip():

                st.warning(
                    "Please enter a question or prompt."
                )

            else:

                with st.spinner(
                    "Generating..."
                ):

                    reply = _model_answer(
                        user_text
                    )

                if not reply:

                    reply = (
                        "Sorry, I could not generate "
                        "a response right now."
                    )

                st.session_state.ml_msgs.append(
                    (
                        "user",
                        user_text
                    )
                )

                st.session_state.ml_msgs.append(
                    (
                        "assistant",
                        reply
                    )
                )

                st.subheader(
                    "### ✅ Tutor Response"
                )

                st.write(
                    reply
                )

                if auto_speak:

                    code = (
                        "en"
                        if tts_lang_hint.startswith("auto")
                        else tts_lang_hint
                    )

                    _speak_text(
                        reply,
                        code
                    )

        # =================================================
        # CONVERSATION
        # =================================================

        if st.session_state.ml_msgs:

            st.subheader(
                "💬 Conversation"
            )

            for index, message in enumerate(
                st.session_state.ml_msgs
            ):

                role, text = message

                if role == "user":

                    with st.chat_message(
                        "user",
                        avatar="🧑"
                    ):

                        st.write(
                            text
                        )

                else:

                    with st.chat_message(
                        "assistant",
                        avatar="🧠"
                    ):

                        st.write(
                            text
                        )

                        if st.button(
                            "🔊 Speak this reply",
                            key=f"ml_say_{index}"
                        ):

                            code = (
                                "en"
                                if tts_lang_hint.startswith("auto")
                                else tts_lang_hint
                            )

                            _speak_text(
                                text,
                                code
                            )
                            # =====================================================
    # 5. CHATBOT ASSISTANT
    # =====================================================

    elif help_option == "🤖 Chatbot Assistant":

        st.subheader(
            "🤖 Smart Farm AI Chatbot Assistant"
        )

        st.write(
            "Ask me anything about Smart Farm AI "
            "or farming practices."
        )

        chatbot_knowledge = {

            "how to add a crop":
                "Go to Farm Management and add the crop "
                "details.",

            "how to backup data":
                "Go to Support & Help > Data Backup & "
                "Recovery and use the backup option.",

            "how to check soil moisture":
                "Go to Irrigation & Soil or Sensors & "
                "Monitoring to check available soil data.",

            "how to detect crop disease":
                "Go to AI Predictions > Crop Disease "
                "Detection and upload a crop image.",

            "how to use farm plot mapping":
                "Go to Farm Management > Farm Plot Mapping "
                "to add and manage your farm plots.",

            "how to use productivity":
                "Go to Productivity & Records to manage "
                "sales, expenses, yields, loans, inventory, "
                "reports and farm summaries.",

            "how to use calendar":
                "Go to Calendar & Seasons to access planting, "
                "harvest and seasonal task planning."
        }

        user_question = st.text_input(
            "💬 Type your question here:",
            key="chat_q"
        )

        if st.button(
            "🤖 Get Answer",
            key="chat_go"
        ):

            question = (
                user_question or ""
            ).strip().lower()

            if not question:

                st.warning(
                    "Please enter a question."
                )

            else:

                answer = chatbot_knowledge.get(
                    question,
                    "❓ I don't have a specific answer "
                    "for that yet. Please try asking about "
                    "farm management, productivity, irrigation, "
                    "AI predictions, calendar, sensors, or "
                    "other Smart Farm AI features."
                )

                st.info(
                    answer
                )



# =========================

# SIDEBAR MENU

# =========================

menu = st.sidebar.selectbox(

    "📍 Select a Main Section",

    [

        "🌿 Farm Management",

        "📊 Productivity & Records",

        "💧 Irrigation & Soil",

        "💹 Market & Finance",

        "📡 Sensors & Monitoring",

        "🆘 Support & Help",

    ],

    key="main_menu"

)



# =========================

# ROUTER

# =========================

if menu == "🌿 Farm Management":

    st.sidebar.title("🌿 Smart Farm AI")

    st.header("🌿 Farm Management")

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(current_farm, dict):
        current_farm = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_farm_name = current_farm.get(
        "farm_name",
        personalized_profile.get(
            "current_farm_name",
            "Main Farm"
        )
    )

    current_crop = current_farm.get(
        "crop_type",
        personalized_profile.get(
            "crop_type",
            "Not specified"
        )
    )

    current_location = current_farm.get(
        "location",
        personalized_profile.get(
            "location",
            "Not specified"
        )
    )

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    
    farm_option = st.sidebar.selectbox("Select a Feature", [

        "User Account Management",

        "Farm Plot Mapping",

        "Smart Fertilizer & Pesticide Stock Manager",


        "Drone Flight Scheduler",

        "Voice Command Interface"

    ], key="farm_management_option")



    if farm_option == "User Account Management":

        pass

    elif farm_option == "Farm Plot Mapping":

        farm_plot_mapping_ui()

    elif farm_option == "Smart Fertilizer & Pesticide Stock Manager":

        smart_fert_pest_ui()

    

    elif farm_option == "Drone Flight Scheduler":

        drone_flight_scheduler_ui()

    elif farm_option == "Voice Command Interface":

        voice_command_ui()

# ========================================================
# PRODUCTIVITY & RECORDS — 14 FEATURES
# ========================================================

elif menu == "📊 Productivity & Records":

    st.header("📊 Productivity & Records")

    # ========================================================
    # CURRENT FARM CONTEXT
    # ========================================================

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(current_farm, dict):
        current_farm = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_farm_id = current_farm.get(
        "farm_id",
        "main_farm"
    )

    current_farm_name = current_farm.get(
        "farm_name",
        personalized_profile.get(
            "current_farm_name",
            "Main Farm"
        )
    )

    current_crop = current_farm.get(
        "crop_type",
        personalized_profile.get(
            "crop_type",
            "Not specified"
        )
    )

    current_location = current_farm.get(
        "location",
        personalized_profile.get(
            "location",
            "Not specified"
        )
    )

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # ========================================================
    # 14 PRODUCTIVITY FEATURES
    # ========================================================

    productivity_option = st.sidebar.selectbox(
        "📊 Select a Productivity Feature",
        [
            "📈 View Sales Record",
            "➕ Add Sales Record",
            "💰 View Expense",
            "➕ Add Expense",
            "📊 Calculate Profit",
            "👩‍🌾 View Farmer Record",
            "📈 Farm Productivity",
            "🌾 Yield Estimator",
            "💳 Farm Loan Recorder",
            "➕ Add Loan Record",
            "📦 View Inventory",
            "➕ Add Inventory",
            "📄 Generate Report",
            "📊 Farm Summary"
        ],
        key="productivity_feature"
    )

    # ========================================================
    # 1. VIEW SALES RECORD
    # ========================================================

    if productivity_option == "📈 View Sales Record":

        st.subheader("📈 View Sales Record")

        try:
            with open("sales_records.json", "r") as file:
                sales_data = json.load(file)

            if not isinstance(sales_data, list):
                sales_data = []

            farm_sales = [
                entry
                for entry in sales_data
                if str(
                    entry.get("farm_id", "main_farm")
                ) == str(current_farm_id)
            ]

            if farm_sales:
                for entry in farm_sales:
                    st.markdown(
                        f"""
- 📅 Date: {entry.get('date', '')}
- 🛒 Item Sold: {entry.get('item', '')}
- 🔢 Quantity: {entry.get('quantity', 0)}
- 💰 Amount: ₦{entry.get('amount', 0):,.2f}
---
"""
                    )
            else:
                st.info(
                    f"No sales records available for "
                    f"{current_farm_name}."
                )

        except (FileNotFoundError, json.JSONDecodeError):
            st.info(
                f"No sales records available for "
                f"{current_farm_name} yet."
            )

    # ========================================================
    # 2. ADD SALES RECORD
    # ========================================================

    elif productivity_option == "➕ Add Sales Record":

        st.subheader("➕ Add Sales Record")

        item = st.text_input(
            "Enter Item Sold",
            key="prod_sales_item"
        )

        quantity = st.number_input(
            "Enter Quantity",
            min_value=1,
            key="prod_sales_quantity"
        )
        amount = st.number_input(
            "Enter Amount (₦)",
            min_value=0.0,
            key="prod_sales_amount"
        )

        record_date = st.date_input(
            "Select Date",
            key="prod_sales_date"
        )

        if st.button(
            "Save Record",
            key="prod_sales_save"
        ):

            new_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "item": item,
                "quantity": quantity,
                "amount": amount,
                "date": str(record_date)
            }

            try:
                with open(
                    "sales_records.json",
                    "r"
                ) as file:
                    sales_data = json.load(file)

                if not isinstance(sales_data, list):
                    sales_data = []

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):
                sales_data = []

            sales_data.append(new_record)

            with open(
                "sales_records.json",
                "w"
            ) as file:
                json.dump(
                    sales_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Sales record added successfully "
                f"for {current_farm_name}!"
            )

    # ========================================================
    # 3. VIEW EXPENSE
    # ========================================================

    elif productivity_option == "💰 View Expense":

        st.subheader("💰 View Expense Records")

        try:
            with open(
                "expenses.json",
                "r"
            ) as file:
                expense_data = json.load(file)

            if not isinstance(expense_data, list):
                expense_data = []

            farm_expenses = [
                entry
                for entry in expense_data
                if str(
                    entry.get("farm_id", "main_farm")
                ) == str(current_farm_id)
            ]

            if farm_expenses:
                for entry in farm_expenses:
                    st.markdown(
                        f"""
- 📅 Date: {entry.get('Date', '')}
- 📂 Category: {entry.get('Category', '')}
- 💰 Amount: ₦{entry.get('Amount', 0):,.2f}
- 📝 Description: {entry.get('Description', '')}
---
"""
                    )
            else:
                st.info(
                    f"No expense records available for "
                    f"{current_farm_name}."
                )

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            st.info(
                f"No expense records available for "
                f"{current_farm_name} yet."
            )

    # ========================================================
    # 4. ADD EXPENSE
    # ========================================================

    elif productivity_option == "➕ Add Expense":

        st.subheader("➕ Add Expense Record")

        with st.form("productivity_expense_form"):

            expense_date = st.date_input(
                "📅 Date of Expense",
                key="prod_expense_date"
            )

            category = st.selectbox(
                "📂 Expense Category",
                [
                    "Fertilizer",
                    "Pesticide",
                    "Seeds",
                    "Labor",
                    "Fuel",
                    "Maintenance",
                    "Transport",
                    "Others"
                ],
                key="prod_expense_category"
            )

            amount = st.number_input(
                "💰 Amount Spent (₦)",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                key="prod_expense_amount"
            )
            description = st.text_area(
                "📝 Description (Optional)",
                key="prod_expense_description"
            )

            submit_expense = st.form_submit_button(
                "Save Expense Record"
            )

        if submit_expense:

            new_expense = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "Date": str(expense_date),
                "Category": category,
                "Amount": amount,
                "Description": description
            }

            try:
                with open(
                    "expenses.json",
                    "r"
                ) as file:
                    expense_data = json.load(file)

                if not isinstance(expense_data, list):
                    expense_data = []

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):
                expense_data = []

            expense_data.append(new_expense)

            with open(
                "expenses.json",
                "w"
            ) as file:
                json.dump(
                    expense_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Expense recorded successfully "
                f"for {current_farm_name}!"
            )

    # ========================================================
    # 5. CALCULATE PROFIT
    # ========================================================

    elif productivity_option == "📊 Calculate Profit":

        st.subheader("📊 Calculate Profit")

        total_sales = st.number_input(
            "Enter Total Sales (₦)",
            min_value=0.0,
            key="prod_profit_sales"
        )

        total_expenses = st.number_input(
            "Enter Total Expenses (₦)",
            min_value=0.0,
            key="prod_profit_expenses"
        )

        if st.button(
            "Calculate Profit",
            key="prod_profit_button"
        ):

            profit = total_sales - total_expenses

            st.success(
                f"✅ Net Profit for "
                f"{current_farm_name}: "
                f"₦{profit:,.2f}"
            )

    # ========================================================
    # 6. VIEW FARMER RECORD
    # ========================================================

    elif productivity_option == "👩‍🌾 View Farmer Record":

        st.subheader("👩‍🌾 View Farmer Record")

        st.markdown(
            f"""
### 👤 Farmer & Farm Information

- 🌱 Farm: {current_farm_name}
- 🆔 Farm ID: {current_farm_id}
- 🌾 Crop: {current_crop}
- 📍 Location: {current_location}
"""
        )

        if personalized_profile:

            st.divider()

            st.subheader("👤 Personalization Profile")

            for key, value in personalized_profile.items():

                if value not in ["", None]:

                    st.write(
                        f"{key.replace('_', ' ').title()}: "
                        f"{value}"
                    )

    # ========================================================
    # 7. FARM PRODUCTIVITY
    # ========================================================

    elif productivity_option == "📈 Farm Productivity":

        st.subheader("📈 Farm Productivity")

        crop_name = st.text_input(
            "Crop Name",
            value=(
                current_crop
                if current_crop != "Not specified"
                else ""
            ),
            key="prod_crop_name"
        )

        season = st.selectbox(
            "Season",
            [
                "Dry Season",
                "Rainy Season"
            ],
            key="prod_season"
        )

        yield_kg = st.number_input(
            "Total Yield (kg)",
            min_value=0.0,
            key="prod_yield_kg"
        )
        farm_size_value = st.number_input(
            "Farm Size (hectares)",
            min_value=0.0,
            key="prod_farm_size"
        )

        if st.button(
            "Record Productivity",
            key="prod_record_button"
        ):

            st.success(
                f"✅ Productivity recorded for "
                f"{crop_name} ({season}): "
                f"{yield_kg:,.1f} kg on "
                f"{farm_size_value:,.2f} hectares "
                f"for {current_farm_name}."
            )

    # ========================================================
    # 8. YIELD ESTIMATOR
    # ========================================================

    elif productivity_option == "🌾 Yield Estimator":

        st.subheader("🌾 Yield Estimator")

        farm_area = st.number_input(
            "Farm Area (hectares)",
            min_value=0.0,
            key="prod_yield_area"
        )

        average_yield_per_hectare = st.number_input(
            "Expected Yield per Hectare (kg)",
            min_value=0.0,
            key="prod_yield_per_ha"
        )

        if st.button(
            "Estimate Yield",
            key="prod_yield_button"
        ):

            estimated_yield = (
                farm_area *
                average_yield_per_hectare
            )

            st.success(
                f"✅ Estimated Yield for "
                f"{current_farm_name}: "
                f"{estimated_yield:,.0f} kg"
            )

    # ========================================================
    # 9. FARM LOAN RECORDER
    # ========================================================

    elif productivity_option == "💳 Farm Loan Recorder":

        st.subheader("💳 Farm Loan Recorder")

        lender_name = st.text_input(
            "Lender Name",
            key="prod_loan_lender"
        )

        loan_amount = st.number_input(
            "Loan Amount (₦)",
            min_value=0.0,
            key="prod_loan_amount"
        )

        interest_rate = st.number_input(
            "Interest Rate (%)",
            min_value=0.0,
            key="prod_loan_interest"
        )

        repayment_period = st.text_input(
            "Repayment Period",
            key="prod_loan_period"
        )

        if st.button(
            "Record Loan",
            key="prod_loan_record_button"
        ):

            st.success(
                f"✅ Loan recorded for "
                f"{current_farm_name}: "
                f"₦{loan_amount:,.2f} from "
                f"{lender_name} at "
                f"{interest_rate}% for "
                f"{repayment_period}."
            )

    # ========================================================
    # 10. ADD LOAN RECORD
    # ========================================================

    elif productivity_option == "➕ Add Loan Record":

        st.subheader("➕ Add Loan Record")

        loan_purpose = st.text_input(
            "Loan Purpose",
            key="prod_loan_purpose"
        )

        loan_date = st.date_input(
            "Loan Date",
            key="prod_loan_date"
        )

        amount = st.number_input(
            "Loan Amount (₦)",
            min_value=0.0,
            key="prod_loan_amount_single"
        )

        if st.button(
            "Save Loan Record",
            key="prod_loan_save_button"
        ):

            st.success(
                f"✅ Loan for {loan_purpose} "
                f"of ₦{amount:,.2f} on {loan_date} "
                f"saved for {current_farm_name}."
            )# ========================================================
    # 11. VIEW INVENTORY
    # ========================================================

    elif productivity_option == "📦 View Inventory":

        st.subheader("📦 View Inventory Records")

        try:
            with open(
                "inventory.json",
                "r"
            ) as file:
                inventory_data = json.load(file)

            if not isinstance(inventory_data, list):
                inventory_data = []

            farm_inventory = [
                entry
                for entry in inventory_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

            if farm_inventory:

                for entry in farm_inventory:

                    st.markdown(
                        f"""
- 📦 Item: {entry.get('Item', '')}
- 🔢 Quantity: {entry.get('Quantity', 0)}
- 📂 Category: {entry.get('Category', '')}
---
"""
                    )

            else:
                st.info(
                    f"No inventory records available for "
                    f"{current_farm_name}."
                )

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):

            st.info(
                f"No inventory records available for "
                f"{current_farm_name} yet."
            )

    # ========================================================
    # 12. ADD INVENTORY
    # ========================================================

    elif productivity_option == "➕ Add Inventory":

        st.subheader("➕ Add Inventory Item")

        with st.form(
            "productivity_add_inventory_form"
        ):

            item = st.text_input(
                "📦 Item Name",
                key="prod_inventory_item"
            )

            quantity = st.number_input(
                "🔢 Quantity",
                min_value=0,
                step=1,
                key="prod_inventory_quantity"
            )

            category = st.text_input(
                "📂 Category",
                key="prod_inventory_category"
            )

            submit_inventory = st.form_submit_button(
                "💾 Save Inventory Item"
            )

        if submit_inventory:

            new_item = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "Item": item,
                "Quantity": quantity,
                "Category": category
            }

            try:
                with open(
                    "inventory.json",
                    "r"
                ) as file:
                    inventory_data = json.load(file)

                if not isinstance(
                    inventory_data,
                    list
                ):
                    inventory_data = []

            except (
                FileNotFoundError,
                json.JSONDecodeError
            ):
                inventory_data = []

            inventory_data.append(
                new_item
            )

            with open(
                "inventory.json",
                "w"
            ) as file:
                json.dump(
                    inventory_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Inventory item added successfully "
                f"for {current_farm_name}!"
            )

    # ========================================================
    # 13. GENERATE REPORT
    # ========================================================

    elif productivity_option == "📄 Generate Report":

        st.subheader("📄 Generate Farm Report")

        # ----------------------------------------------------
        # LOAD SALES RECORDS
        # ----------------------------------------------------

        try:
            with open(
                "sales_records.json",
                "r"
            ) as file:
                sales_data = json.load(file)

            if not isinstance(
                sales_data,
                list
            ):
                sales_data = []

            farm_sales = [
                entry
                for entry in sales_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            farm_sales = []

        # ----------------------------------------------------
        # LOAD EXPENSE RECORDS
        # ----------------------------------------------------

        try:
            with open(
                "expenses.json",
                "r"
            ) as file:
                expense_data = json.load(file)

            if not isinstance(
                expense_data,
                list
            ):
                expense_data = []

            farm_expenses = [
                entry
                for entry in expense_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            farm_expenses = []

        # ----------------------------------------------------
        # CALCULATE FINANCIAL TOTALS
        # ----------------------------------------------------

        total_sales = sum(
            float(
                entry.get(
                    "amount",
                    0
                )
            )
            for entry in farm_sales
        )

        total_expenses = sum(
            float(
                entry.get(
                    "Amount",
                    0
                )
            )
            for entry in farm_expenses
        )

        profit_loss = (
            total_sales -
            total_expenses
        )

        # ----------------------------------------------------
        # DISPLAY REPORT
        # ----------------------------------------------------

        st.markdown(
            f"""
### 📊 Farm Financial Report

- 🌱 Farm: {current_farm_name}
- 🆔 Farm ID: {current_farm_id}
- 🌾 Crop: {current_crop}
- 📍 Location: {current_location}
- 💰 Total Sales: ₦{total_sales:,.2f}
- 💸 Total Expenses: ₦{total_expenses:,.2f}
- 📈 Profit / Loss: ₦{profit_loss:,.2f}
"""
        )

        if profit_loss > 0:
            st.success(
                f"📈 {current_farm_name} is currently showing "
                f"a profit of ₦{profit_loss:,.2f}."
            )
        elif profit_loss < 0:
            st.warning(
                f"📉 {current_farm_name} is currently showing "
                f"a loss of ₦{abs(profit_loss):,.2f}."
            )
        else:
            st.info(
                f"⚖️ {current_farm_name} currently has "
                f"no recorded profit or loss."
            )

    # ========================================================
    # 14. FARM SUMMARY
    # ========================================================

    elif productivity_option == "📊 Farm Summary":

        st.subheader("📊 Overall Farm Summary")

        # ----------------------------------------------------
        # LOAD SALES RECORDS
        # ----------------------------------------------------

        try:
            with open(
                "sales_records.json",
                "r"
            ) as file:
                sales_data = json.load(file)

            if not isinstance(
                sales_data,
                list
            ):
                sales_data = []

            farm_sales = [
                entry
                for entry in sales_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            farm_sales = []

        # ----------------------------------------------------
        # LOAD EXPENSE RECORDS
        # ----------------------------------------------------

        try:
            with open(
                "expenses.json",
                "r"
            ) as file:
                expense_data = json.load(file)

            if not isinstance(
                expense_data,
                list
            ):
                expense_data = []

            farm_expenses = [
                entry
                for entry in expense_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            farm_expenses = []

        # ----------------------------------------------------
        # LOAD INVENTORY RECORDS
        # ----------------------------------------------------

        try:
            with open(
                "inventory.json",
                "r"
            ) as file:
                inventory_data = json.load(file)

            if not isinstance(
                inventory_data,
                list
            ):
                inventory_data = []

            farm_inventory = [
                entry
                for entry in inventory_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (
            FileNotFoundError,
            json.JSONDecodeError
        ):
            farm_inventory = []

        # ----------------------------------------------------
        # CALCULATE SUMMARY
        # ----------------------------------------------------

        total_sales = sum(
            float(
                entry.get(
                    "amount",
                    0
                )
            )
            for entry in farm_sales
        )

        total_expenses = sum(
            float(
                entry.get(
                    "Amount",
                    0
                )
            )
            for entry in farm_expenses
        )

        net = (
            total_sales -
            total_expenses
        )

        # ----------------------------------------------------
        # DISPLAY FARM SUMMARY
        # ----------------------------------------------------

        st.markdown(
            f"""
### 📊 Farm Summary

- 🌱 Farm: {current_farm_name}
- 🆔 Farm ID: {current_farm_id}
- 🌾 Crop: {current_crop}
- 📍 Location: {current_location}
- 💰 Total Sales: ₦{total_sales:,.2f}
- 💸 Total Expenses: ₦{total_expenses:,.2f}
- 🧮 Net Profit / Loss: ₦{net:,.2f}
- 📦 Inventory Items: {len(farm_inventory)}
"""
        )

        # ----------------------------------------------------
        # SUMMARY STATUS
        # ----------------------------------------------------

        if net > 0:
            st.success(
                f"📈 {current_farm_name} has a net profit of "
                f"₦{net:,.2f}."
            )
        elif net < 0:
            st.warning(
                f"📉 {current_farm_name} has a net loss of "
                f"₦{abs(net):,.2f}."
            )
        else:
            st.info(
                f"⚖️ No net profit or loss has been recorded "
                f"for {current_farm_name} yet."
            )


    





elif menu == "💧 Irrigation & Soil":

    irrigation_ui()



elif menu == "💹 Market & Finance":

    market_finance_ui()


elif menu == "📡 Sensors & Monitoring":
    sensors_monitoring_ui()

elif menu == "🆘 Support & Help":
     support_help_ui()


# 1) --- helpers defined FIRST ---

def k2(name: str) -> str:

    return f"v2_{name}"



def klsd(suffix: str) -> str:

    return f"lsd_{suffix}"


# 🎙 Voice Command (v2) — triggers real buttons/pages
def voice_command_ui_v2():
    import streamlit as st
    import threading

    # ----- Optional deps (kept optional so UI still loads without them)
    try:
        import speech_recognition as sr
    except Exception:
        sr = None

    try:
        import pyttsx3
    except Exception:
        pyttsx3 = None

    # ----- Resolve your v2 main menu session key
    try:
        main_v2_key = k2("main_menu_option")  # your existing helper
    except Exception:
        main_v2_key = "v2_main_menu_option"   # safe fallback

    # ===== Helpers =====
    def _say_async(text: str):
        """Speak text on a background thread if TTS is available."""
        if pyttsx3 is None:
            return
        def _worker():
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass
        threading.Thread(target=_worker, daemon=True).start()

    def _go(page_label: str):
        """Navigate to a v2 page label exactly as in your v2 menu."""
        st.session_state[main_v2_key] = page_label

    def _open_predictions(subtool: str | None = None):
        """Open v2 AI Predictions page and optionally pick a subtool."""
        _go("🧪 AI Predictions")
        if subtool:
            # v2 page reads this and maps to internal tool keys
            st.session_state["ai_prediction_tool"] = subtool
        st.rerun()

    def _open_tips(mode: str):
        """Open AI Farm Tips and set its internal active tool."""
        _go("📚 AI Farm Tips")
        # ktips("active_tool") returns "tips_active_tool" in your setup
        st.session_state["tips_active_tool"] = mode  # "ask" or "daily"
        st.rerun()

    def _open_live_sensor():
        _go("📡 Live Sensor Dashboard")
        st.rerun()

    def _open_perf_indicators():
        _go("📍 Farm Performance Indicators")
        st.rerun()

    def _open_calendar():
        _go("📅 Calendar & Seasons")
        st.rerun()

    def _route_command(c: str) -> bool:
        """Return True if a route matched and navigated."""
        c = c.strip().lower()

        # --- high-confidence intents ---
        if "live sensor" in c or ("sensor" in c and "dashboard" in c):
            _open_live_sensor();  return True
        if "performance" in c and "indicator" in c:
            _open_perf_indicators();  return True
        if "calendar" in c or "season" in c:
            _open_calendar();  return True

        # --- AI Predictions subtools
        if ("disease" in c) or ("diagnose" in c) or ("leaf" in c) or ("blight" in c):
            _open_predictions("Crop Disease Detection");  return True
        if "yield" in c:
            _open_predictions("Yield Prediction");  return True
        if "soil" in c or "ph" in c:
            _open_predictions("Soil Health Check");  return True
        if "prediction" in c or "predictions" in c:
            _open_predictions(None);  return True

        # --- AI Farm Tips
        if "daily tip" in c or ("tip" in c and "daily" in c):
            _open_tips("daily");  return True
        if "ask tip" in c or ("tip" in c and "ask" in c) or ("ai tip" in c):
            _open_tips("ask");  return True

        return False

    # ===== UI =====
    st.header("🎙️ Voice Command (v2)")

    if sr is None:
        st.warning(
            "Speech engine not installed. Install with:\n\n"
            "`pip install SpeechRecognition pyaudio`  "
            "or use an alternative microphone backend."
        )
        return

    # Unique keys to avoid collisions across v2
    btn_key = f"{main_v2_key}_vc2_mic_btn"
    status_key = f"{main_v2_key}_vc2_status"

    # Button to record one utterance
    if st.button("🎤 Speak now", key=btn_key):
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                st.info("Listening... please speak clearly.")
                # Reduce background noise impact
                try:
                    recognizer.adjust_for_ambient_noise(source, duration=0.6)
                except Exception:
                    pass
                # Listen for a short phrase
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=6)

            transcript = None
            error_msg = None

            # Try Google first (requires internet), fall back to Sphinx if available
            try:
                transcript = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                # Try offline pocketsphinx if installed
                try:
                    transcript = recognizer.recognize_sphinx(audio)
                except Exception:
                    error_msg = "I couldn't understand that. Please try again."
            except sr.RequestError:
                # Network issue, try offline if possible
                try:
                    transcript = recognizer.recognize_sphinx(audio)
                except Exception:
                    error_msg = "Network unavailable for speech. Install pocketsphinx for offline use."

            # Handle results
            if transcript:
                st.success(f"You said: “{transcript}”")
                _say_async(f"You said {transcript}")
                if not _route_command(transcript):
                    st.info(
                        "No v2 route matched. Try saying: "
                        "live sensor, performance indicators, calendar, "
                        "disease, yield, soil, predictions, daily tip, ask tip."
                    )
            else:
                st.error(error_msg or "Sorry, I didn't catch that. Please try again.")

        except sr.WaitTimeoutError:
            st.error("Listening timed out. Try again and speak sooner.")
        except OSError as e:
            st.error(f"Microphone error: {e}")
        except Exception as e:
            st.error(f"Voice command error: {e}")

def expanded_crop_calendar_ui():
    import streamlit as st
    import pandas as pd
    import calendar
    from datetime import date

    st.header("📅 Expanded AI Crop Calendar")

    # ---------- SAFE DEFAULTS (only if not already defined globally) ----------
    if "_CROPS" not in globals():
        globals()["_CROPS"] = ["Maize", "Rice", "Cassava", "Tomato"]
    if "_ZONES" not in globals():
        globals()["_ZONES"] = ["Sahel", "Sudan", "Guinea", "Rainforest"]
    if "_TASK_EMOJI" not in globals():
        globals()["_TASK_EMOJI"] = {
            "sow": "🌱", "nursery": "🪴", "transplant": "🌿", "weed": "🧹",
            "spray": "🧪", "topdress": "🧂", "harvest": "🧺", "field_checks": "🔎"
        }

    # Simple schedule builder if you didn't define one elsewhere
    if "_build_schedule" not in globals():
        def _build_schedule(crop: str, zone: str, year: int) -> pd.DataFrame:
            # Dummy windows – replace with real logic / data
            spec = [
                ("sow",          f"{year}-03-10", f"{year}-03-20"),
                ("field_checks", f"{year}-03-21", f"{year}-11-30"),
                ("weed",         f"{year}-04-05", f"{year}-04-06"),
                ("spray",        f"{year}-05-02", f"{year}-05-04"),
                ("topdress",     f"{year}-06-15", f"{year}-06-16"),
                ("harvest",      f"{year}-09-20", f"{year}-09-25"),
            ]
            rows = []
            for task, s, e in spec:
                for d in pd.date_range(s, e, freq="D"):
                    rows.append((pd.to_datetime(d).normalize(), task))
            return pd.DataFrame(rows, columns=["date", "task"])

    # Month×Week grid builder if you didn't define one elsewhere
    if "_month_grid" not in globals():
        def _month_grid(df: pd.DataFrame, year: int) -> pd.DataFrame:
            df = df.copy()
            df["month"] = df["date"].dt.month
            # naive “week-of-month” bucket (1..5)
            df["wom"] = ((df["date"].dt.day - 1) // 7) + 1
            out = []
            for m in range(1, 13):
                sub = df[df["month"] == m]
                row = {"Month": calendar.month_name[m]}
                for w in range(1, 6):
                    tasks = sorted(sub[sub["wom"] == w]["task"].unique())
                    row[f"W{w}"] = ", ".join(tasks) if tasks else ""
                out.append(row)
            return pd.DataFrame(out)

    # ---------- UI CONTROLS ----------
    c1, c2, c3 = st.columns([1.2, 1, 1])
    with c1:
        crop = st.selectbox("Crop", _CROPS, index=0, key="ccal_crop")
    with c2:
        zone = st.selectbox("Agro-ecological Zone (NG)", _ZONES, index=2, key="ccal_zone")
    with c3:
        year = st.number_input("Season Year", min_value=2020, max_value=2100,
                               value=date.today().year, step=1, key="ccal_year")

    cache_key = f"ccal_df_{crop}_{zone}_{int(year)}"
    if cache_key not in st.session_state:
        base = _build_schedule(crop, zone, int(year))
        base = base.copy()
        base["date"] = pd.to_datetime(base["date"]).dt.normalize()
        st.session_state[cache_key] = base

    df = st.session_state[cache_key].copy()
    df["month"] = df["date"].dt.month
    df["code"] = df["task"].map(lambda t: _TASK_EMOJI.get(t, "•") + t[:3].upper())

    # ---------- ADD CUSTOM TASK ----------
    st.subheader("➕ Add Custom Task")
    with st.form("ccal_ct_form", clear_on_submit=False):
        cc1, cc2, cc3 = st.columns([1.2, 1, 1])
        with cc1:
            custom_label = st.text_input("Task label (e.g., Spray, Weeding)", key="ccal_ct_label")
        with cc2:
            default_start = df["date"].min().date()
            custom_start = st.date_input("Start date", value=default_start, key="ccal_ct_start")
        with cc3:
            default_end = (df["date"].min() + pd.Timedelta(days=3)).date()
            custom_end = st.date_input("End date", value=default_end, key="ccal_ct_end")
        submitted = st.form_submit_button("Add Task", use_container_width=True)

    if submitted:
        lbl = (custom_label or "").strip()
        if not lbl:
            st.warning("Enter a task label.")
        elif custom_start > custom_end:
            st.warning("End date must be on/after start date.")
        else:
            rng = pd.date_range(pd.to_datetime(custom_start), pd.to_datetime(custom_end), freq="D")
            extra = pd.DataFrame({"date": rng, "task": lbl})
            new_df = pd.concat([st.session_state[cache_key], extra], ignore_index=True)
            new_df["date"] = pd.to_datetime(new_df["date"]).dt.normalize()
            st.session_state[cache_key] = new_df
            st.success(f"Added custom task: {lbl} ({custom_start} → {custom_end})")
            df = new_df.copy()
            df["month"] = df["date"].dt.month
            df["code"] = df["task"].map(lambda t: _TASK_EMOJI.get(t, "•") + t[:3].upper())

    # ---------- CALENDAR GRID ----------
    st.subheader("🗓️ Calendar Grid (Month × Week)")
    grid = _month_grid(df, int(year))
    st.dataframe(grid, use_container_width=True, hide_index=True)

    # ---------- MONTH TASKS ----------
    st.subheader("📋 Month Tasks (Readable)")
    for m in range(1, 13):
        sub = df[df["month"] == m]
        if sub.empty:
            continue
        with st.expander(calendar.month_name[m]):
            for task in sorted(sub["task"].unique()):
                days = sorted(pd.to_datetime(sub[sub["task"] == task]["date"]).dt.date.unique())
                # collapse contiguous ranges
                span_start = prev = days[0]
                ranges = []
                for d in days[1:]:
                    if (pd.to_datetime(d) - pd.to_datetime(prev)).days > 1:
                        ranges.append((span_start, prev))
                        span_start = d
                    prev = d
                ranges.append((span_start, prev))
                emo = _TASK_EMOJI.get(task, "•")
                for s, e in ranges:
                    if s == e:
                        st.write(f"{emo} **{task}**: {pd.to_datetime(s).strftime('%b %d')}")
                    else:
                        st.write(f"{emo} **{task}**: {pd.to_datetime(s).strftime('%b %d')} → {pd.to_datetime(e).strftime('%b %d')}")

    # ---------- EXPORT ----------
    st.subheader("⬇️ Export")
    csv = df[["date", "task"]].sort_values("date").copy()
    csv["date"] = pd.to_datetime(csv["date"]).dt.strftime("%Y-%m-%d")
    st.download_button(
        "Download CSV",
        csv.to_csv(index=False).encode("utf-8"),
        file_name=f"{crop}_{zone}_{year}_calendar.csv",
        mime="text/csv",
        key="ccal_dl_csv"
    )

    st.success(f"✅ Expanded Crop Calendar generated successfully for {crop} · {zone} · {year}.")


# 2) --- feature function defined NEXT ---

def live_sensor_dashboard_v2():

    import time, random

    import pandas as pd

    from datetime import datetime

    import streamlit as st



    st.header("📡 Live Sensor Dashboard (v2)")

    st.caption("Simulated stream. Replace `read_sensors()` with your real sensor inputs.")



    # init state

    if klsd("log") not in st.session_state:

        st.session_state[klsd("log")] = []

    if klsd("running") not in st.session_state:

        st.session_state[klsd("running")] = True



    # controls

    c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1])

    refresh_rate = c1.slider("⏱️ Refresh (seconds)", 1, 10, 5, key=klsd("refresh"))

    history_size = c2.number_input("🧮 Keep last N rows", 20, 1000, 150, 10, key=klsd("hist"))

    st.session_state[klsd("running")] = c3.toggle("🔄 Live monitoring", value=st.session_state[klsd("running")], key=klsd("toggle"))

    if c4.button("🧹 Clear history", key=klsd("clear")):

        st.session_state[klsd("log")] = []

        st.success("Cleared.")

        st.rerun()



    def read_sensors():

        return {

            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            "Temperature (°C)": round(random.uniform(24.0, 36.5), 1),

            "Humidity (%)": round(random.uniform(40.0, 90.0), 1),

            "Soil Moisture (%)": round(random.uniform(18.0, 70.0), 1),

            "Light (lux)": random.randint(8_000, 60_000),

        }



    if st.session_state[klsd("running")] or not st.session_state[klsd("log")]:

        st.session_state[klsd("log")].append(read_sensors())

        st.session_state[klsd("log")] = st.session_state[klsd("log")][-int(history_size):]



    df = pd.DataFrame(st.session_state[klsd("log")])

    if df.empty:

        st.info("No readings yet. Enable live monitoring to start.")

        return



    latest = df.iloc[-1]

    k1, k2c, k3, k4 = st.columns(4)

    k1.metric("🌡 Temperature", f"{latest['Temperature (°C)']} °C")

    k2c.metric("💧 Humidity", f"{latest['Humidity (%)']} %")

    k3.metric("🌱 Soil Moisture", f"{latest['Soil Moisture (%)']} %")

    k4.metric("🔆 Light", f"{latest['Light (lux)']} lux")



    # simple alerts

    if latest["Soil Moisture (%)"] < 35:

        st.warning("Low soil moisture — consider irrigating soon.")

    if latest["Temperature (°C)"] > 34:

        st.warning("High temperature — risk of heat stress.")

    if latest["Humidity (%)"] > 80:

        st.warning("High humidity — monitor for fungal disease.")



    st.divider()

    st.subheader("📈 Trends")

    chart_df = df.set_index("Timestamp")

    st.line_chart(chart_df[["Temperature (°C)"]])

    st.line_chart(chart_df[["Humidity (%)"]])

    st.line_chart(chart_df[["Soil Moisture (%)"]])

    st.line_chart(chart_df[["Light (lux)"]])



    st.subheader("🗃️ Recent Readings")

    st.dataframe(df.tail(30), use_container_width=True)



    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button("⬇️ Download CSV", csv,

        file_name=f"sensor_readings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",

        mime="text/csv", key=klsd("dl_csv"))



    if st.session_state[klsd("running")]:

        time.sleep(refresh_rate)

        st.rerun()

# ---------- KEY PREFIX HELPERS (single, clean) ----------
def _ccal(name: str) -> str:
    """Expanded AI Crop Calendar widgets."""
    return f"ccal_{name}"

def klsd(name: str) -> str:
    """Live Sensor Dashboard widgets."""
    return f"lsd_{name}"

def kacc(name: str) -> str:
    """Account / User management (v1)."""
    return f"acc_v1_{name}"

def k2(name: str) -> str:
    """Main v2 menu/router prefix."""
    return f"v2_{name}"

def kp2(name: str) -> str:
    """Productivity & Records (v2)."""
    return f"v2_prod_{name}"

def kfm2(name: str) -> str:
    """Farm Management (v2)."""
    return f"v2_farm_{name}"

def kirr2(name: str) -> str:
    """Irrigation & Soil (v2)."""
    return f"v2_irrig_{name}"

def kplot(name: str) -> str:
    """Farm Plot Mapping (v2)."""
    return f"v2_plot_{name}"

def kcal(name: str) -> str:
    """Calendar & Seasons (v2)."""
    return f"v2_cal_{name}"

def kalert(name: str) -> str:
    """Alerts widgets."""
    return f"alerts_{name}"

def ktips(name: str) -> str:
    """AI Farm Tips widgets."""
    return f"tips_{name}"

def kforum(name: str) -> str:
    """Community Forum widgets."""
    return f"v2_forum_{name}"

def kpl(name: str) -> str:
    """Profit & Loss widgets."""
    return f"pl_{name}"

def ap(name: str) -> str:
    """AI Predictions widgets."""
    return f"ai_pred_{name}"

def mkey(name: str) -> str:
    """Market & Economic Tools."""
    return f"market_tools_{name}"

def fi(name: str) -> str:
    """Farm Indicators."""
    return f"farm_ind_{name}"

def kdm(name: str) -> str:
    """Decision-making models."""
    return f"dm_{name}"

def kdr(name: str) -> str:
    """Drone / Irrigation tools."""
    return f"dr_{name}"

def kbak(name: str) -> str:
    """Backup & Recovery."""
    return f"bk_{name}"

def klot(name: str) -> str:
    """Farm Lot Management."""
    return f"lot_{name}"

def sfp(name: str) -> str:
    """Single Feature Page widgets."""
    return f"sfp_{name}"

# =========================
# UPGRADE MENU (second router with unique keys)
# ---------- KEY PREFIX HELPERS (clean) ----------
def _ccal(name: str) -> str: return f"ccal_{name}"
def klsd(name: str) -> str:  return f"lsd_{name}"
def kacc(name: str) -> str:  return f"acc_v1_{name}"
def k2(name: str) -> str:    return f"v2_{name}"
def kp2(name: str) -> str:   return f"v2_prod_{name}"
def kfm2(name: str) -> str:  return f"v2_farm_{name}"
def kirr2(name: str) -> str: return f"v2_irrig_{name}"
def kplot(name: str) -> str: return f"v2_plot_{name}"
def kcal(name: str) -> str:  return f"v2_cal_{name}"
def kalert(name: str) -> str:return f"alerts_{name}"
def ktips(name: str) -> str: return f"tips_{name}"
def kforum(name: str) -> str:return f"v2_forum_{name}"
def kpl(name: str) -> str:   return f"pl_{name}"
def ap(name: str) -> str:    return f"ai_pred_{name}"
def mkey(name: str) -> str:  return f"market_tools_{name}"
def fi(name: str) -> str:    return f"farm_ind_{name}"
def kdm(name: str) -> str:   return f"dm_{name}"
def kdr(name: str) -> str:   return f"dr_{name}"
def kbak(name: str) -> str:  return f"bk_{name}"
def klot(name: str) -> str:  return f"lot_{name}"
def sfp(name: str) -> str:   return f"sfp_{name}"

# =========================
# UPGRADE MENU (second router with unique keys)
# =========================
# Make sure you have this at the very top of your file too:
# import streamlit as st

menu_v2 = st.sidebar.selectbox(
    "📖 Main Menu",
    [
        "🏡 Home",
        "🌿 Farm Management",
        "📊 Productivity & Records",
        "💧 Irrigation & Soil", 
        "📊 farm profit & loss statement",
        "📅 Calendar & Seasons",
        "🧪 AI Predictions",
        "📚 AI Farm Tips",
        "📈 Market & Economic Tools",
        "🧪 Smart Fertilizer & Pesticide",
        "📡 Live Sensor Dashboard",
        "💦 Irrigation Scheduler",
        "🎙️ Voice Command Interface",
        "🚨 Smart Farm Alerts",
        "🚁 Voice-Controlled Drone Irrigation Assistant",
        "🚁 Drone Flight Scheduler",
        "📍 Farm Lot Management",
        "📅 Expanded AI Crop Calendar",
        "🤖 AI Crop Calendar",
        "📈 Decision-Making Models",
        "📍 Farm Performance Indicators",
        "🔒 User Account Management",
],
key=k2("main_menu_option")
)



# ============================================================
# SMART FARM AI — FARMER COMMAND CENTER
# ============================================================

if menu_v2 == "🏡 Home":

    st.header("🏡 Smart Farm AI — Farmer Command Center")

    current_farm = st.session_state.get("current_farm", {})
    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    farm_name = current_farm.get("farm_name", "My Farm")

    crop_name = current_farm.get(
        "crop_type",
        personalized_profile.get("crop_type", "Not specified")
    )

    farm_location = current_farm.get(
        "location",
        personalized_profile.get("location", "Not specified")
    )

    farm_type = current_farm.get(
        "farm_type",
        personalized_profile.get("farm_type", "Not specified")
    )

    farm_size = current_farm.get(
        "farm_size",
        personalized_profile.get("farm_size", "Not specified")
    )

    # ========================================================
    # WELCOME
    # ========================================================

    st.markdown(
        f"""
        ### Welcome back! 🌱

        {farm_name} is your current farm.

        Crop: {crop_name}  
        Location: {farm_location}  
        Farm type: {farm_type}  
        Farm size: {farm_size}
        """
    )

    st.divider()

    # ========================================================
    # FARM OVERVIEW METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("🌱 Current Farm", farm_name)

    with c2:
        st.metric("🌾 Main Crop", crop_name)

    with c3:
        st.metric("📍 Location", farm_location)

    with c4:
        st.metric("📊 Farm Size", farm_size)

    st.divider()

    # ========================================================
    # PERSONALIZED RECOMMENDATIONS
    # ========================================================

    st.subheader("⭐ Recommended for Your Farm")

    if recommended_features:

        for feature in recommended_features[:6]:

            if isinstance(feature, dict):
                feature_name = feature.get(
                    "name",
                    feature.get("Name", "Farm Tool")
                )
            else:
                feature_name = str(feature)

            st.markdown(f"🌿 {feature_name}")

    else:

        st.info(
            "Complete your farm profile to receive personalized "
            "recommendations."
        )

    st.divider()

    # ========================================================
    # QUICK FARM ACTIONS
    # ========================================================

    st.subheader("⚡ Quick Farm Actions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:
        st.info("🌦 Weather & Climate")

    with q2:
        st.info("🚨 Farm Alerts")

    with q3:
        st.info("💧 Irrigation & Soil")

    with q4:
        st.info("🧠 AI Predictions")

    st.divider()

    # ========================================================
    # PRECISION AGRICULTURE
    # ========================================================

    st.subheader("🎯 Precision Agriculture Intelligence")

    pa_analysis = st.session_state.get(
        "pa_analysis",
        {}
    )

    if pa_analysis:

        pa_crop = pa_analysis.get(
            "crop",
            "Not specified"
        )

        pa_location = pa_analysis.get(
            "location",
            "Not specified"
        )

        pa_recommendations = pa_analysis.get(
            "recommendations",
            []
        )

        pa_alerts = pa_analysis.get(
            "alerts",
            []
        )

        pa_priority_actions = pa_analysis.get(
            "priority_actions",
            []
        )

        # ----------------------------------------------------
        # PA SUMMARY
        # ----------------------------------------------------

        p1, p2, p3 = st.columns(3)

        with p1:
            st.metric(
                "🌾 Crop",
                pa_crop
            )

        with p2:
            st.metric(
                "📍 Location",
                pa_location
            )

        with p3:
            st.metric(
                "🧠 PA Recommendations",
                len(pa_recommendations)
            )

        # ----------------------------------------------------
        # PA PRIORITY ACTIONS
        # ----------------------------------------------------

        st.markdown("### ⭐ Priority Actions")

        if pa_priority_actions:

            action_cols = st.columns(2)

            for i, action in enumerate(
                pa_priority_actions[:6]
            ):

                with action_cols[i % 2]:
                    st.info(
                        f"🎯 {action}"
                    )

        # ----------------------------------------------------
        # PA RECOMMENDATIONS
        # ----------------------------------------------------

        st.markdown(
            "### 🌱 Precision Farm Recommendations"
        )

        if pa_recommendations:

            for recommendation in pa_recommendations[:6]:

                st.write(
                    f"• {recommendation}"
                )

        else:

            st.info(
                "Precision Agriculture is ready. "
                "More farm data will improve the recommendations."
            )

        # ----------------------------------------------------
        # PA ALERTS
        # ----------------------------------------------------

        if pa_alerts:

            st.markdown(
                "### ⚠️ Precision Agriculture Alerts"
            )

            for alert in pa_alerts:

                st.warning(alert)

    else:

        st.info(
            "Precision Agriculture intelligence is preparing "
            "for your current farm."
        )

    st.divider()

    # ========================================================
    # CIG — GREEN CHLOROPHYLL INTELLIGENCE
    # ========================================================

    st.subheader(
        "🌿 Green Chlorophyll Intelligence"
    )

    cig_analysis = st.session_state.get(
        "cig_analysis",
        {}
    )

    if cig_analysis:

        cig_crop = cig_analysis.get(
            "crop",
            "Not specified"
        )

        cig_status = cig_analysis.get(
            "status",
            "Waiting for multispectral data"
        )

        cig_value = cig_analysis.get(
            "cig"
        )

        # ----------------------------------------------------
        # CIG SUMMARY
        # ----------------------------------------------------

        g1, g2, g3 = st.columns(3)

        with g1:
            st.metric(
                "🌾 Crop",
                cig_crop
            )

        with g2:

            if cig_value is not None:

                st.metric(
                    "🌿 CIG",
                    f"{cig_value:.2f}"
                )

            else:

                st.metric(
                    "🌿 CIG",
                    "Pending"
                )

        with g3:
            st.metric(
                "📡 Status",
                cig_status
            )

        st.caption(
            "CIG becomes quantitative when suitable "
            "multispectral drone or satellite NIR and "
            "green-band data are available."
        )

        # ----------------------------------------------------
        # CIG RECOMMENDATIONS
        # ----------------------------------------------------

        cig_recommendations = cig_analysis.get(
            "recommendations",
            []
        )

        if cig_recommendations:

            st.markdown(
                "### 🌱 CIG Recommendations"
            )

            for recommendation in cig_recommendations[:4]:

                st.write(
                    f"• {recommendation}"
                )

        # ----------------------------------------------------
        # CIG ALERTS
        # ----------------------------------------------------

        cig_alerts = cig_analysis.get(
            "alerts",
            []
        )

        for alert in cig_alerts:

            st.warning(alert)

    else:
        st.info(
            "Green Chlorophyll Intelligence is ready "
            "for multispectral data."
        )

    st.divider()

    # ========================================================
    # CSA — CLIMATE-SMART AGRICULTURE
    # ========================================================

    st.subheader(
        "🌍 Climate-Smart Agriculture"
    )

    csa_analysis = st.session_state.get(
        "csa_analysis",
        {}
    )

    if csa_analysis:

        csa_crop = csa_analysis.get(
            "crop",
            "Not specified"
        )

        csa_location = csa_analysis.get(
            "location",
            "Not specified"
        )

        # ----------------------------------------------------
        # CSA SUMMARY
        # ----------------------------------------------------

        s1, s2 = st.columns(2)

        with s1:
            st.metric(
                "🌾 Crop",
                csa_crop
            )

        with s2:
            st.metric(
                "📍 Farm Location",
                csa_location
            )

        # ----------------------------------------------------
        # CLIMATE RISKS
        # ----------------------------------------------------

        st.markdown(
            "### 🌦 Climate Risks to Monitor"
        )

        climate_risks = csa_analysis.get(
            "climate_risks",
            []
        )

        for risk in climate_risks[:5]:

            st.warning(
                f"⚠️ {risk}"
            )

        # ----------------------------------------------------
        # ADAPTATION ACTIONS
        # ----------------------------------------------------

        st.markdown(
            "### 🌱 Climate Adaptation Actions"
        )

        adaptation_actions = csa_analysis.get(
            "adaptation_actions",
            []
        )

        for action in adaptation_actions[:5]:

            st.info(
                f"🌱 {action}"
            )

        # ----------------------------------------------------
        # CSA RECOMMENDATIONS
        # ----------------------------------------------------

        st.markdown(
            "### 🧠 Climate-Smart Recommendations"
        )

        csa_recommendations = csa_analysis.get(
            "recommendations",
            []
        )

        for recommendation in csa_recommendations[:5]:

            st.write(
                f"• {recommendation}"
            )

        # ----------------------------------------------------
        # CSA ALERTS
        # ----------------------------------------------------

        csa_alerts = csa_analysis.get(
            "alerts",
            []
        )

        for alert in csa_alerts:

            st.warning(alert)

    else:

        st.info(
            "Climate-Smart Agriculture intelligence is "
            "preparing for your current farm."
        )

elif menu_v2 == "🧑‍🏫 Smart Tutor Multilanguage":

    smart_tutor_voice()

elif menu_v2 == "📅 Expanded AI Crop Calendar":
    expanded_crop_calendar_ui()

elif menu_v2 == "📡 Live Sensor Dashboard":
    live_sensor_dashboard_v2()

elif menu_v2 == "🚁 Drone Flight Scheduler":
    drone_flight_scheduler_ui()

elif menu_v2 == "🚁 Voice-Controlled Drone Irrigation Assistant":
    drone_irrigation_assistant_ui()

elif menu_v2 == "💾 Data Backup & Recovery":
    data_backup_recovery_ui()

elif menu_v2 == "🧪 Smart Fertilizer & Pesticide":
    smart_fert_pest_ui()


elif menu_v2 == "🎙️ Voice Command Interface":
    voice_command_ui()


 
# Help text kept in the code but hidden by default (silent in the app)
_show_help = False  # set to True only for debugging/dev — keep False in production

_help_content = """
**Tips for using the app**
- Use the sidebar menu to switch pages.
- Example commands: `open live sensor dashboard`, `go to predictions`, `open backup`.
- If you see a *StreamlitAPIException about session_state*, it means a menu key was changed **after** its widget was created.
  ✅ Fix: always set defaults before the selectbox, or update via callbacks.
"""

# Render the help expander only when explicitly enabled (otherwise it stays silent)
if _show_help:
    with st.expander("ℹ️ Help — Navigation & Commands"):
        st.markdown(_help_content)
# otherwise nothing is shown in the UI (help works "silently" in the code)
  
# 🏡 HOME
if menu == "🏡 Home":
    st.subheader("Welcome to Smart Farm AI!")
    st.write("Use the sidebar to navigate through available tools.")

# 🌿 FARM MANAGEMENT
elif menu_v2 == "🌿 Farm Management":
    farm_management_ui()

elif menu_v2 == "📊 Productivity & Records":

    st.header("📊 Productivity & Records")

    # =========================================================
    # CURRENT FARM
    # =========================================================

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get(
        "farm_id",
        "main_farm"
    )

    current_farm_name = current_farm.get(
        "farm_name",
        "Main Farm"
    )

    current_crop = current_farm.get(
        "crop_type",
        "Not specified"
    )

    current_location = current_farm.get(
        "location",
        "Not specified"
    )

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # =========================================================
    # PRODUCTIVITY FEATURES
    # =========================================================

    option = st.selectbox(
        "Select a Feature",
        [
            "📈 View Sales Record",
            "➕ Add Sales Record",
            "💰 View Expense",
            "➕ Add Expense",
            "🧮 Calculate Profit",
            "👩‍🌾 View Farmer Record",
            "📊 Farm Productivity",
            "🌾 Yield Estimator",
            "💳 Farm Loan Recorder",
            "➕ Add Loan Record",
            "📦 View Inventory",
            "➕ Add Inventory",
            "📄 Generate Report",
            "📊 Farm Summary",
        ],
        key=kp2("feature")
    )

    # =========================================================
    # ADD SALES RECORD
    # =========================================================

    if option == "➕ Add Sales Record":

        st.subheader("➕ Add Sales Record")

        item = st.text_input(
            "Enter Item Sold",
            key=kp2("sales_item")
        )

        quantity = st.number_input(
            "Enter Quantity",
            min_value=1,
            key=kp2("sales_quantity")
        )

        amount = st.number_input(
            "Enter Amount (₦)",
            min_value=0,
            key=kp2("sales_amount")
        )

        record_date = st.date_input(
            "Select Date",
            key=kp2("sales_date")
        )

        if st.button(
            "Save Record",
            key=kp2("sales_save")
        ):

            new_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "item": item,
                "quantity": quantity,
                "amount": amount,
                "date": str(record_date)
            }

            try:
                with open(
                    "sales_records.json",
                    "r"
                ) as file:
                    sales_data = json.load(file)

            except FileNotFoundError:
                sales_data = []

            sales_data.append(new_record)

            with open(
                "sales_records.json",
                "w"
            ) as file:
                json.dump(
                    sales_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Sales record added for "
                f"{current_farm_name}."
            )

    # =========================================================
    # VIEW SALES RECORD
    # =========================================================

    elif option == "📈 View Sales Record":

        st.subheader("📈 View Sales Record")

        try:
            with open(
                "sales_records.json",
                "r"
            ) as file:
                sales_data = json.load(file)

            farm_sales = [
                entry
                for entry in sales_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

            if farm_sales:

                for entry in farm_sales:

                    st.markdown(
                        f"""
- 📅 Date: {entry.get('date', '')}
- 🛒 Item Sold: {entry.get('item', '')}
- 🔢 Quantity: {entry.get('quantity', 0)}
- 💰 Amount: ₦{entry.get('amount', 0)}
---
"""
                    )

            else:

                st.info(
                    f"No sales records for "
                    f"{current_farm_name}."
                )

        except FileNotFoundError:

            st.warning(
                "No sales record file found yet."
            )

    # =========================================================
    # ADD EXPENSE
    # =========================================================

    elif option == "➕ Add Expense":

        st.subheader("➕ Add Expense Record")

        with st.form(
            kp2("expense_form")
        ):

            expense_date = st.date_input(
                "📅 Date of Expense",
                key=kp2("expense_date")
            )

            category = st.selectbox(
                "📂 Expense Category",
                [
                    "Fertilizer",
                    "Pesticide",
                    "Seeds",
                    "Labor",
                    "Fuel",
                    "Maintenance",
                    "Transport",
                    "Others"
                ],
                key=kp2("expense_category")
            )

            amount = st.number_input(
                "💰 Amount Spent (₦)",
                min_value=0.0,
                step=100.0,
                format="%.2f",
                key=kp2("expense_amount")
            )

            description = st.text_area(
                "📝 Description (Optional)",
                key=kp2("expense_description")
            )

            submit_expense = st.form_submit_button(
                "Save Expense Record"
            )

        if submit_expense:

            new_expense = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "Date": str(expense_date),
                "Category": category,
                "Amount": amount,
                "Description": description
            }

            try:
                with open(
                    "expenses.json",
                    "r"
                ) as file:
                    expense_data = json.load(file)

            except FileNotFoundError:
                expense_data = []

            expense_data.append(new_expense)

            with open(
                "expenses.json",
                "w"
            ) as file:
                json.dump(
                    expense_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Expense recorded for "
                f"{current_farm_name}."
            )

    # =========================================================
    # VIEW EXPENSE
    # =========================================================

    elif option == "💰 View Expense":

        st.subheader("💰 View Expense Records")

        try:
            with open(
                "expenses.json",
                "r"
            ) as file:
                expense_data = json.load(file)

            farm_expenses = [
                entry
                for entry in expense_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

            if farm_expenses:

                for entry in farm_expenses:

                    st.markdown(
                        f"""
- 📅 Date: {entry.get('Date', '')}
- 📂 Category: {entry.get('Category', '')}
- 💰 Amount: ₦{entry.get('Amount', 0)}
- 📝 Description: {entry.get('Description', '')}
---
"""
                    )

            else:

                st.info(
                    f"No expense records for "
                    f"{current_farm_name}."
                )

        except FileNotFoundError:

            st.warning(
                "No expense record file found yet."
            )

    # =========================================================
    # CALCULATE PROFIT
    # =========================================================

    elif option == "🧮 Calculate Profit":

        st.subheader("🧮 Calculate Profit")

        total_sales = st.number_input(
            "Enter Total Sales (₦):",
            min_value=0,
            key=kp2("profit_total_sales")
        )

        total_expenses = st.number_input(
            "Enter Total Expenses (₦):",
            min_value=0,
            key=kp2("profit_total_expenses")
        )

        if st.button(
            "Calculate Profit",
            key=kp2("profit_calc_btn")
        ):

            profit = (
                total_sales -
                total_expenses
            )

            st.success(
                f"✅ Net Profit for "
                f"{current_farm_name}: "
                f"₦{profit:,.2f}"
            )

    # =========================================================
    # VIEW FARMER RECORD
    # =========================================================

    elif option == "👩‍🌾 View Farmer Record":

        st.subheader("👩‍🌾 View Farmer Record")

        st.write(
            "Current farmer profile and farm information:"
        )

        st.write(
            f"🌱 Farm: {current_farm_name}"
        )

        st.write(
            f"🌾 Crop: {current_crop}"
        )

        st.write(
            f"📍 Location: {current_location}"
        )

    # =========================================================
    # FARM PRODUCTIVITY
    # =========================================================

    elif option == "📊 Farm Productivity":

        st.subheader("📊 Farm Productivity")

        crop_name = st.text_input(
            "Crop Name:",
            value=current_crop
            if current_crop != "Not specified"
            else "",
            key=kp2("prod_crop_name")
        )

        season = st.selectbox(
            "Season",
            [
                "Dry Season",
                "Rainy Season"
            ],
            key=kp2("prod_season")
        )

        yield_kg = st.number_input(
            "Total Yield (kg):",
            min_value=0,
            key=kp2("prod_yield_kg")
        )

        farm_size_value = st.number_input(
            "Farm Size (hectares):",
            min_value=0.0,
            key=kp2("prod_farm_size")
        )

        if st.button(
            "Record Productivity",
            key=kp2("prod_record_btn")
        ):

            st.success(
                f"✅ Productivity recorded for "
                f"{crop_name} ({season}): "
                f"{yield_kg} kg on "
                f"{farm_size_value} hectares "
                f"for {current_farm_name}."
            )

    # =========================================================
    # YIELD ESTIMATOR
    # =========================================================

    elif option == "🌾 Yield Estimator":

        st.subheader("🌾 Yield Estimator")

        farm_area = st.number_input(
            "Farm Area (hectares):",
            min_value=0.0,
            key=kp2("yield_farm_area")
        )

        average_yield_per_hectare = st.number_input(
            "Expected Yield per Hectare (kg):",
            min_value=0,
            key=kp2("yield_per_ha")
        )

        if st.button(
            "Estimate Yield",
            key=kp2("yield_estimate_btn")
        ):

            estimated_yield = (
                farm_area *
                average_yield_per_hectare
            )

            st.success(
                f"✅ Estimated Yield for "
                f"{current_farm_name}: "
                f"{estimated_yield:,.0f} kg"
            )
            # =========================================================
    # FARM LOAN RECORDER
    # =========================================================

    elif option == "💳 Farm Loan Recorder":

        st.subheader("💳 Farm Loan Recorder")

        lender_name = st.text_input(
            "Lender Name:",
            key=kp2("loan_lender")
        )

        loan_amount = st.number_input(
            "Loan Amount (₦):",
            min_value=0,
            key=kp2("loan_amount")
        )

        interest_rate = st.number_input(
            "Interest Rate (%):",
            min_value=0.0,
            key=kp2("loan_interest")
        )

        repayment_period = st.text_input(
            "Repayment Period (e.g. 12 months)",
            key=kp2("loan_period")
        )

        if st.button(
            "Record Loan",
            key=kp2("loan_record_btn")
        ):

            st.success(
                f"✅ Loan recorded for "
                f"{current_farm_name}: "
                f"₦{loan_amount:,.2f} from "
                f"{lender_name} at "
                f"{interest_rate}% for "
                f"{repayment_period}"
            )

    # =========================================================
    # ADD LOAN RECORD
    # =========================================================

    elif option == "➕ Add Loan Record":

        st.subheader("➕ Add Loan Record")

        loan_purpose = st.text_input(
            "Loan Purpose:",
            key=kp2("loan_purpose")
        )

        loan_date = st.date_input(
            "Loan Date:",
            key=kp2("loan_date")
        )

        amount = st.number_input(
            "Loan Amount (₦):",
            min_value=0,
            key=kp2("loan_amount_single")
        )

        if st.button(
            "Save Loan Record",
            key=kp2("loan_save_btn")
        ):

            st.success(
                f"✅ Loan for {loan_purpose} "
                f"of ₦{amount:,.2f} on {loan_date} "
                f"saved for {current_farm_name}."
            )

    # =========================================================
    # ADD INVENTORY
    # =========================================================

    elif option == "➕ Add Inventory":

        st.subheader("➕ Add Inventory Item")

        with st.form(
            kp2("inventory_form")
        ):

            item = st.text_input(
                "📦 Item Name",
                key=kp2("inventory_item")
            )

            quantity = st.number_input(
                "🔢 Quantity",
                min_value=0,
                step=1,
                key=kp2("inventory_quantity")
            )

            category = st.text_input(
                "📂 Category (e.g., Fertilizer, Seeds, Tools)",
                key=kp2("inventory_category")
            )

            submit_inventory = st.form_submit_button(
                "Save Inventory Item"
            )

        if submit_inventory:

            new_item = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "Item": item,
                "Quantity": quantity,
                "Category": category
            }

            try:
                with open(
                    "inventory.json",
                    "r"
                ) as file:
                    inventory_data = json.load(file)

            except FileNotFoundError:
                inventory_data = []

            inventory_data.append(new_item)

            with open(
                "inventory.json",
                "w"
            ) as file:
                json.dump(
                    inventory_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Inventory item added for "
                f"{current_farm_name}."
            )

# =========================================================
    # VIEW INVENTORY
    # =========================================================

    elif option == "📦 View Inventory":

        st.subheader("📦 View Inventory Records")

        try:
            with open(
                "inventory.json",
                "r"
            ) as file:
                inventory_data = json.load(file)

            farm_inventory = [
                entry
                for entry in inventory_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

            if farm_inventory:

                for entry in farm_inventory:

                    st.markdown(
                        f"""
- 📦 Item: {entry.get('Item', '')}
- 🔢 Quantity: {entry.get('Quantity', 0)}
- 📂 Category: {entry.get('Category', '')}
---
"""
                    )

            else:

                st.info(
                    f"No inventory records for "
                    f"{current_farm_name}."
                )

        except FileNotFoundError:

            st.warning(
                "No inventory record file found yet."
            )

    # =========================================================
    # GENERATE REPORT
    # =========================================================

    elif option == "📄 Generate Report":

        st.subheader("📄 Generate Farm Report")

        try:
            with open(
                "sales_records.json",
                "r"
            ) as file:
                sales_data = json.load(file)

            farm_sales = [
                entry
                for entry in sales_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except FileNotFoundError:
            farm_sales = []

        try:
            with open(
                "expenses.json",
                "r"
            ) as file:
                expense_data = json.load(file)

            farm_expenses = [
                entry
                for entry in expense_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except FileNotFoundError:
            farm_expenses = []

        total_sales = sum(
            entry.get("amount", 0)
            for entry in farm_sales
        )

        total_expenses = sum(
            entry.get("Amount", 0)
            for entry in farm_expenses
        )

        profit_loss = (
            total_sales -
            total_expenses
        )

        st.markdown(
            f"""
### 📊 Farm Financial Report

- 🌱 Farm: {current_farm_name}
- 💰 Total Sales: ₦{total_sales:,.2f}
- 💸 Total Expenses: ₦{total_expenses:,.2f}
- 📈 Profit / Loss: ₦{profit_loss:,.2f}
"""
        )

    # =========================================================
# FARM SUMMARY
# =========================================================

    elif option == "📊 Farm Summary":

        st.subheader("📊 Overall Farm Summary")

        try:
            with open(
                "sales_records.json",
                "r"
            ) as file:
                sales_data = json.load(file)

            farm_sales = [
                entry
                for entry in sales_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (FileNotFoundError, json.JSONDecodeError):
            farm_sales = []

        try:
            with open(
                "expenses.json",
                "r"
            ) as file:
                expense_data = json.load(file)

            farm_expenses = [
                entry
                for entry in expense_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (FileNotFoundError, json.JSONDecodeError):
            farm_expenses = []

        try:
            with open(
                "inventory.json",
                "r"
            ) as file:
                inventory_data = json.load(file)

            farm_inventory = [
                entry
                for entry in inventory_data
                if str(
                    entry.get(
                        "farm_id",
                        "main_farm"
                    )
                ) == str(current_farm_id)
            ]

        except (FileNotFoundError, json.JSONDecodeError):
            farm_inventory = []

        total_sales = sum(
            float(entry.get("amount", 0) or 0)
            for entry in farm_sales
        )

        total_expenses = sum(
            float(entry.get("Amount", 0) or 0)
            for entry in farm_expenses
        )

        net_profit = total_sales - total_expenses

        st.markdown(
            f"""
### 📊 Overall Farm Summary

- 🌱 Farm: {current_farm_name}
- 🌾 Crop: {current_crop}
- 📍 Location: {current_location}
- 💰 Total Sales: ₦{total_sales:,.2f}
- 💸 Total Expenses: ₦{total_expenses:,.2f}
- 🧮 Net Profit / Loss: ₦{net_profit:,.2f}
- 📦 Inventory Items: {len(farm_inventory)}
"""
        )
        
# =========================================================
# IRRIGATION & SOIL
# =========================================================

elif menu_v2 == "💧 Irrigation & Soil":

    st.header("💧 Irrigation & Soil")

    # ---------------------------------------------------------
    # CURRENT FARM
    # ---------------------------------------------------------

    current_farm = st.session_state.get("current_farm", {})

    if not isinstance(current_farm, dict):
        current_farm = {}

    current_farm_id = current_farm.get("farm_id", "main_farm")
    current_farm_name = current_farm.get("farm_name", "Main Farm")
    current_crop = current_farm.get("crop_type", "Not specified")
    current_location = current_farm.get("location", "Not specified")

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # ---------------------------------------------------------
    # FIVE IRRIGATION & SOIL FEATURES
    # ---------------------------------------------------------

    option = st.selectbox(
        "💧 Select a Feature",
        [
            "💧 Irrigation Schedule",
            "🌱 Soil Health Record",
            "🌱 Soil Moisture Checker",
            "🚰 Water Usage Log",
            "💰 Irrigation Cost Estimator"
        ],
        key="irrigation_soil_feature_v2"
    )

    # =========================================================
    # 1. IRRIGATION SCHEDULE
    # =========================================================

    if option == "💧 Irrigation Schedule":

        st.subheader("💧 Irrigation Schedule")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        irrigation_date = st.date_input(
            "📅 Irrigation Date",
            key="irrigation_schedule_date_v2"
        )

        water_volume = st.number_input(
            "💧 Water Volume (liters)",
            min_value=0.0,
            step=1.0,
            key="irrigation_schedule_volume_v2"
        )

        if st.button(
            "💾 Save Irrigation Record",
            key="irrigation_schedule_save_v2"
        ):

            new_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "date": str(irrigation_date),
                "water_volume": water_volume
            }

            try:
                with open("irrigation_schedule.json", "r") as file:
                    irrigation_data = json.load(file)

                if not isinstance(irrigation_data, list):
                    irrigation_data = []

            except (FileNotFoundError, json.JSONDecodeError):
                irrigation_data = []

            irrigation_data.append(new_record)

            with open("irrigation_schedule.json", "w") as file:
                json.dump(
                    irrigation_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Irrigation record saved for "
                f"{current_farm_name}."
            )

    # =========================================================
    # 2. SOIL HEALTH RECORD
    # =========================================================

    elif option == "🌱 Soil Health Record":

        st.subheader("🌱 Soil Health Record")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        soil_ph = st.number_input(
            "🧪 Soil pH Level",
            min_value=0.0,
            max_value=14.0,
            step=0.1,
            key="irrigation_soil_ph_v2"
        )

        moisture_content = st.number_input(
            "💧 Moisture Content (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key="irrigation_soil_moisture_v2"
        )
        nutrient_content = st.text_input(
            "🌿 Nutrient Content Summary",
            key="irrigation_soil_nutrients_v2"
        )

        test_date = st.date_input(
            "📅 Test Date",
            key="irrigation_soil_date_v2"
        )

        if st.button(
            "💾 Save Soil Health Record",
            key="irrigation_soil_save_v2"
        ):

            soil_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "soil_ph": soil_ph,
                "moisture_content": moisture_content,
                "nutrient_content": nutrient_content,
                "test_date": str(test_date)
            }

            try:
                with open("soil_health_records.json", "r") as file:
                    soil_data = json.load(file)

                if not isinstance(soil_data, list):
                    soil_data = []

            except (FileNotFoundError, json.JSONDecodeError):
                soil_data = []

            soil_data.append(soil_record)

            with open("soil_health_records.json", "w") as file:
                json.dump(
                    soil_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Soil health record saved for "
                f"{current_farm_name}."
            )

        st.divider()

        st.subheader(
            f"📋 Soil Records — {current_farm_name}"
        )

        try:
            with open("soil_health_records.json", "r") as file:
                soil_data = json.load(file)

            if not isinstance(soil_data, list):
                soil_data = []

            farm_soil = [
                entry
                for entry in soil_data
                if str(
                    entry.get("farm_id", "main_farm")
                ) == str(current_farm_id)
            ]

            if farm_soil:

                for entry in farm_soil:

                    st.markdown(
                        f"""
- 📅 Test Date: {entry.get('test_date', '')}
- 🧪 Soil pH: {entry.get('soil_ph', 0)}
- 💧 Moisture: {entry.get('moisture_content', 0)}%
- 🌿 Nutrients: {entry.get('nutrient_content', '')}

---
"""
                    )

            else:

                st.info(
                    f"No soil health records for "
                    f"{current_farm_name}."
                )

        except (FileNotFoundError, json.JSONDecodeError):

            st.info(
                f"No soil health records for "
                f"{current_farm_name} yet."
            )

    # =========================================================
    # 3. SOIL MOISTURE CHECKER
    # =========================================================

    elif option == "🌱 Soil Moisture Checker":

        st.subheader("🌱 Soil Moisture Checker")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        plot_id = st.text_input(
            "🆔 Plot ID",
            key="soil_moisture_plot_id_v2"
        )

        moisture_level = st.slider(
            "💦 Moisture Level (%)",
            min_value=0,
            max_value=100,
            value=50,
            key="soil_moisture_level_v2"
        )

        if st.button(
            "💾 Save Moisture Reading",
            key="soil_moisture_save_v2"
        ):

            moisture_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "plot_id": plot_id,
                "moisture_level": moisture_level
            }

            try:
                with open(
                    "soil_moisture_records.json",
                    "r"
                ) as file:
                    moisture_data = json.load(file)

                if not isinstance(moisture_data, list):
                    moisture_data = []

            except (FileNotFoundError, json.JSONDecodeError):
                moisture_data = []

            moisture_data.append(moisture_record)

            with open(
                "soil_moisture_records.json",
                "w"
            ) as file:
                json.dump(
                    moisture_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ Soil moisture for "
                f"{current_farm_name} recorded as "
                f"{moisture_level}%."
            )

    # =========================================================
    # 4. WATER USAGE LOG
    # =========================================================

    elif option == "🚰 Water Usage Log":

        st.subheader("🚰 Water Usage Log")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        with st.form("water_usage_log_form_v2"):

            water_date = st.date_input(
                "📅 Date of Irrigation",
                key="water_usage_date_v2"
            )

            water_used = st.number_input(
                "💧 Water Used (liters)",
                min_value=0.0,
                step=1.0,
                key="water_usage_amount_v2"
            )

            submitted = st.form_submit_button(
                "💾 Log Water Usage"
            )

        if submitted:

            water_record = {
                "farm_id": current_farm_id,
                "farm_name": current_farm_name,
                "crop_type": current_crop,
                "location": current_location,
                "date": str(water_date),
                "water_used": water_used
            }

            try:
                with open(
                    "water_usage_records.json",
                    "r"
                ) as file:
                    water_data = json.load(file)

                if not isinstance(water_data, list):
                    water_data = []

            except (FileNotFoundError, json.JSONDecodeError):
                water_data = []

            water_data.append(water_record)

            with open(
                "water_usage_records.json",
                "w"
            ) as file:
                json.dump(
                    water_data,
                    file,
                    indent=4
                )

            st.success(
                f"✅ {water_used:,.1f} liters recorded for "
                f"{current_farm_name}."
            )

    # =========================================================
    # 5. IRRIGATION COST ESTIMATOR
    # =========================================================

    elif option == "💰 Irrigation Cost Estimator":

        st.subheader("💰 Irrigation Cost Estimator")

        st.write(f"🌱 Farm: {current_farm_name}")
        st.write(f"🌾 Crop: {current_crop}")
        st.write(f"📍 Location: {current_location}")

        water_volume = st.number_input(
            "🚿 Enter Water Usage (liters)",
            min_value=0.0,
            step=1.0,
            key="irrigation_cost_water_v2"
        )

        cost_per_liter = st.number_input(
            "💸 Cost per Liter (₦)",
            min_value=0.0,
            step=0.01,
            key="irrigation_cost_per_liter_v2"
        )

        if st.button(
            "💰 Estimate Cost",
            key="irrigation_cost_estimate_v2"
        ):

            total_cost = (
                water_volume *
                cost_per_liter
            )

            st.success(
                f"💰 Estimated irrigation cost for "
                f"{current_farm_name}: "
                f"₦{total_cost:,.2f}"
            )



 
# ========================================================
# CALENDAR & SEASONS
# ========================================================

elif menu_v2 == "📅 Calendar & Seasons":

    st.header("📅 Calendar & Seasons")

    # ========================================================
    # CURRENT FARM CONTEXT
    # ========================================================

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(
        current_farm,
        dict
    ):
        current_farm = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(
        personalized_profile,
        dict
    ):
        personalized_profile = {}

    current_farm_id = current_farm.get(
        "farm_id",
        "main_farm"
    )

    current_farm_name = current_farm.get(
        "farm_name",
        personalized_profile.get(
            "current_farm_name",
            "Main Farm"
        )
    )

    current_crop = current_farm.get(
        "crop_type",
        personalized_profile.get(
            "crop_type",
            "Not specified"
        )
    )

    current_location = current_farm.get(
        "location",
        personalized_profile.get(
            "location",
            "Not specified"
        )
    )

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # ========================================================
    # CALENDAR TOOLS
    # ========================================================

    calendar_option = st.selectbox(
        "📅 Select a Calendar Tool",
        [
            "🌱 Planting Calendar",
            "🌾 Harvest Time Estimator",
            "📋 Seasonal Task Planner"
        ],
        key=kcal("option")
    )

    # ========================================================
    # 1. PLANTING CALENDAR
    # ========================================================

    if calendar_option == "🌱 Planting Calendar":

        st.subheader("🌱 AI-Based Planting Calendar")

        crop = st.text_input(
            "Crop Name",
            value=(
                current_crop
                if current_crop != "Not specified"
                else ""
            ),
            key=kcal("planting_crop")
        )

        region = st.text_input(
            "Farm Region",
            value=(
                current_location
                if current_location != "Not specified"
                else ""
            ),
            key=kcal("planting_region")
        )

        if st.button(
            "📅 Generate Planting Schedule",
            key=kcal("btn_generate")
        ):

            if not crop.strip():

                st.warning(
                    "Please enter a crop name."
                )

            elif not region.strip():

                st.warning(
                    "Please enter your farm region."
                )

            else:

                st.success(
                    f"✅ Recommended planting schedule for "
                    f"{crop.title()} in {region.title()}"
                )

                st.write(
                    "🌱 Best planting month: April"
                )

                st.write(
                    "🌾 Expected harvest period: July to August"
                )

                st.write(
                    "💧 Ideal soil moisture: 60%"
                )

                st.write(
                    "🤖 AI Tip: Use sensors to monitor rainfall "
                    "and adjust irrigation."
                )

    # ========================================================
    # 2. HARVEST TIME ESTIMATOR
    # ========================================================

    elif calendar_option == "🌾 Harvest Time Estimator":

        st.subheader("🌾 Harvest Time Estimator")

        crop_type = st.text_input(
            "Crop Type",
            value=(
                current_crop
                if current_crop != "Not specified"
                else ""
            ),
            key=kcal("harvest_crop")
        )

        planting_date = st.date_input(
            "📅 Planting Date",
            key=kcal("planting_date")
        )

        if st.button(
            "🌾 Estimate Harvest Time",
            key=kcal("btn_estimate")
        ):

            if not crop_type.strip():

                st.warning(
                    "Please enter the crop type."
                )

            else:

                est_date = planting_date + timedelta(
                    days=90
                )

                st.success(
                    f"✅ Estimated harvest time for "
                    f"{crop_type.title()} is approximately "
                    f"90 days after planting."
                )

                st.write(
                    f"🌱 Farm: {current_farm_name}"
                )

                st.write(
                    f"📍 Location: {current_location}"
                )

                st.write(
                    "📅 Approximate harvest date:",
                    est_date.strftime("%Y-%m-%d")
                )

                st.write(
                    "🔎 Sensor Alert: Monitor crop ripeness "
                    "using image sensors or NDVI analysis."
                )

    # ========================================================
    # 3. SEASONAL TASK PLANNER
    # ========================================================

    elif calendar_option == "📋 Seasonal Task Planner":

        st.subheader("📋 Seasonal Farm Task Planner")

        season = st.selectbox(
            "Select Season",
            [
                "Dry Season",
                "Rainy Season"
            ],
            key=kcal("season")
        )

        st.write(
            f"🌱 Farm: {current_farm_name}"
        )

        st.write(
            f"🌾 Crop: {current_crop}"
        )

        st.write(
            f"📍 Location: {current_location}"
        )

        if st.button(
            "📋 Show Recommended Tasks",
            key=kcal("btn_tasks")
        ):

            if season == "Rainy Season":

                st.write(
                    "🌧️ Weed control and disease monitoring"
                )

                st.write(
                    "🌱 Fertilizer application planning"
                )

                st.write(
                    "💧 Regular drainage checks"
                )

                st.write(
                    "🔎 Monitor soil moisture and rainfall."
                )

            else:

                st.write(
                    "🌱 Land clearing and soil preparation"
                )

                st.write(
                    "💧 Irrigation planning"
                )

                st.write(
                    "📡 AI sensor calibration for dry-season monitoring"
                )

                st.write(
                    "🌾 Monitor crop water requirements."
                )



# ================================
# 📊 Farm Profit & Loss Statement
# ================================
elif menu_v2 == "📊 farm profit & loss statement":

    st.header("📊 Farm Profit & Loss Statement")

    st.write(
        "Record farm income and expenses, monitor profitability, "
        "and review your farm's financial performance."
    )

    # ------------------------------------------------
    # CURRENT FARM CONTEXT
    # ------------------------------------------------

    current_farm = st.session_state.get(
        "current_farm",
        {}
    )

    if not isinstance(current_farm, dict):
        current_farm = {}

    personalized_profile = st.session_state.get(
        "personalized_profile",
        {}
    )

    if not isinstance(personalized_profile, dict):
        personalized_profile = {}

    current_farm_id = str(
        current_farm.get(
            "farm_id",
            "main_farm"
        )
    )

    current_farm_name = current_farm.get(
        "farm_name",
        personalized_profile.get(
            "current_farm_name",
            "Main Farm"
        )
    )

    current_crop = current_farm.get(
        "crop_type",
        personalized_profile.get(
            "crop_type",
            "Not specified"
        )
    )

    current_location = current_farm.get(
        "location",
        personalized_profile.get(
            "location",
            "Not specified"
        )
    )

    st.info(
        f"🌱 Current Farm: {current_farm_name}  |  "
        f"🌾 Crop: {current_crop}  |  "
        f"📍 Location: {current_location}"
    )

    # ------------------------------------------------
    # NAMESPACED SESSION KEYS
    # ------------------------------------------------

    sales_key = kpl(
        f"sales_df_{current_farm_id}"
    )

    expense_key = kpl(
        f"expense_df_{current_farm_id}"
    )

    # ------------------------------------------------
    # INITIALIZE SALES DATA
    # ------------------------------------------------

    if sales_key not in st.session_state:

        st.session_state[sales_key] = pd.DataFrame(
            columns=[
                "Date",
                "Item",
                "Amount"
            ]
        )

    # ------------------------------------------------
    # INITIALIZE EXPENSE DATA
    # ------------------------------------------------

    if expense_key not in st.session_state:

        st.session_state[expense_key] = pd.DataFrame(
            columns=[
                "Date",
                "Category",
                "Amount"
            ]
        )

    # =================================================
    # ADD INCOME / EXPENSE
    # =================================================

    c1, c2 = st.columns(2)

    # ------------------------------------------------
    # ADD SALE
    # ------------------------------------------------

    with c1:

        st.subheader("➕ Add Sale")

        with st.form(
            kpl(
                f"form_add_sale_{current_farm_id}"
            ),
            clear_on_submit=True
        ):

            s_date = st.date_input(
                "Date",
                value=datetime.now().date(),
                key=kpl(
                    f"s_date_{current_farm_id}"
                )
            )

            s_item = st.text_input(
                "Item",
                placeholder="e.g. Cassava harvest",
                key=kpl(
                    f"s_item_{current_farm_id}"
                )
            )

            s_amt = st.number_input(
                "Amount (₦)",
                min_value=0.0,
                step=100.0,
                key=kpl(
                    f"s_amt_{current_farm_id}"
                )
            )

            add_sale = st.form_submit_button(
                "Add Sale",
                use_container_width=True
            )

        if add_sale:

            if s_item.strip() and s_amt > 0:

                new_sale = pd.DataFrame(
                    [
                        {
                            "Date": str(s_date),
                            "Item": s_item.strip(),
                            "Amount": float(s_amt)
                        }
                    ]
                )

                st.session_state[sales_key] = pd.concat(
                    [
                        st.session_state[sales_key],
                        new_sale
                    ],
                    ignore_index=True
                )

                st.success(
                    "✅ Sale added successfully."
                )

            else:

                st.warning(
                    "Please enter an item and an amount greater than 0."
                )

    # ------------------------------------------------
    # ADD EXPENSE
    # ------------------------------------------------

    with c2:

        st.subheader("➕ Add Expense")

        with st.form(
            kpl(
                f"form_add_expense_{current_farm_id}"
            ),
            clear_on_submit=True
        ):

            e_date = st.date_input(
                "Date",
                value=datetime.now().date(),
                key=kpl(
                    f"e_date_{current_farm_id}"
                )
            )

            e_cat = st.text_input(
                "Category",
                placeholder="e.g. Fertilizer",
                key=kpl(
                    f"e_cat_{current_farm_id}"
                )
            )

            e_amt = st.number_input(
                "Amount (₦)",
                min_value=0.0,
                step=100.0,
                key=kpl(
                    f"e_amt_{current_farm_id}"
                )
            )

            add_exp = st.form_submit_button(
                "Add Expense",
                use_container_width=True
            )

        if add_exp:

            if e_cat.strip() and e_amt > 0:

                new_expense = pd.DataFrame(
                    [
                        {
                            "Date": str(e_date),
                            "Category": e_cat.strip(),
                            "Amount": float(e_amt)
                        }
                    ]
                )

                st.session_state[expense_key] = pd.concat(
                    [
                        st.session_state[expense_key],
                        new_expense
                    ],
                    ignore_index=True
                )

                st.success(
                    "✅ Expense added successfully."
                )

            else:

                st.warning(
                    "Please enter a category and an amount greater than 0."
                )

    st.divider()

    # =================================================
    # SALES TABLE
    # =================================================

    st.subheader("💰 Income (Sales)")

    sales_df = st.session_state[sales_key]

    if not sales_df.empty:

        st.dataframe(
            sales_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No sales recorded for the current farm yet."
        )

    # =================================================
    # EXPENSE TABLE
    # =================================================

    st.subheader("💸 Expenses")

    expense_df = st.session_state[expense_key]

    if not expense_df.empty:

        st.dataframe(
            expense_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No expenses recorded for the current farm yet."
        )

    st.divider()

    # =================================================
    # FINANCIAL CALCULATION
    # =================================================

    total_income = 0.0

    if not sales_df.empty:

        total_income = float(
            pd.to_numeric(
                sales_df["Amount"],
                errors="coerce"
            ).fillna(0).sum()
        )

    total_expense = 0.0

    if not expense_df.empty:
        total_expense = float(
            pd.to_numeric(
                expense_df["Amount"],
                errors="coerce"
            ).fillna(0).sum()
        )

    net_profit = (
        total_income - total_expense
    )

    # =================================================
    # SUMMARY
    # =================================================

    st.subheader("📈 Financial Summary")

    a, b, c = st.columns(3)

    with a:

        st.metric(
            "💰 Total Income",
            f"₦{total_income:,.2f}"
        )

    with b:

        st.metric(
            "💸 Total Expenses",
            f"₦{total_expense:,.2f}"
        )

    with c:

        st.metric(
            "📊 Net Profit",
            f"₦{net_profit:,.2f}",
            delta=f"₦{net_profit:,.2f}",
            delta_color=(
                "normal"
                if net_profit >= 0
                else "inverse"
            )
        )

    # =================================================
    # PROFIT / LOSS STATUS
    # =================================================

    if net_profit > 0:

        st.success(
            f"📈 Your current farm is showing a profit of "
            f"₦{net_profit:,.2f}."
        )

    elif net_profit < 0:

        st.error(
            f"📉 Your current farm is showing a loss of "
            f"₦{abs(net_profit):,.2f}."
        )

    else:

        st.info(
            "⚖️ Income and expenses are currently balanced."
        )

    # =================================================
    # PROFIT / LOSS VISUALIZATION
    # =================================================

    st.markdown(
        "### 📊 Profit/Loss Visualization"
    )

    chart_df = pd.DataFrame(
        {
            "Amount": [
                total_income,
                total_expense,
                net_profit
            ]
        },
        index=[
            "Income",
            "Expenses",
            "Profit"
        ]
    )

    st.bar_chart(
        chart_df,
        use_container_width=True
    )

    # =================================================
    # EXPORT / CLEAR
    # =================================================

    st.divider()

    st.subheader("📦 Data Management")

    x1, x2, x3 = st.columns(3)

    # ------------------------------------------------
    # DOWNLOAD SALES
    # ------------------------------------------------

    with x1:

        st.download_button(
            "⬇️ Download Sales CSV",
            data=sales_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name=(
                f"{current_farm_id}_sales.csv"
            ),
            mime="text/csv",
            key=kpl(
                f"dl_sales_{current_farm_id}"
            ),
            use_container_width=True
        )

    # ------------------------------------------------
    # DOWNLOAD EXPENSES
    # ------------------------------------------------

    with x2:

        st.download_button(
            "⬇️ Download Expenses CSV",
            data=expense_df.to_csv(
                index=False
            ).encode("utf-8"),
            file_name=(
                f"{current_farm_id}_expenses.csv"
            ),
            mime="text/csv",
            key=kpl(
                f"dl_exp_{current_farm_id}"
            ),
            use_container_width=True
        )

    # ------------------------------------------------
    # CLEAR CURRENT FARM DATA
    # ------------------------------------------------

    with x3:

        if st.button(
            "🧹 Clear All",
            key=kpl(
                f"clear_all_{current_farm_id}"
            ),
            use_container_width=True
        ):

            st.session_state[sales_key] = pd.DataFrame(
                columns=[
                    "Date",
                    "Item",
                    "Amount"
                ]
            )

            st.session_state[expense_key] = pd.DataFrame(
                columns=[
                    "Date",
                    "Category",
                    "Amount"
                ]
                )

            st.success(
                "✅ Profit & Loss records cleared for the current farm."
            )

            st.rerun()

elif menu_v2 == "🤖 AI Crop Calendar":
    ai_crop_calendar_ui()

elif menu_v2 == "🧪 AI Predictions":
    ai_predictions_ui()
 

elif menu_v2 in (
    "📍 Farm Performance Indicators",
    "📍 Farm performance Indicators"
):
    farm_performance_indicators_ui()


elif menu_v2 == "📚 AI Farm Tips":
    ai_farm_tips_ui()


elif menu_v2 == "📈 Market & Economic Tools":
    market_economic_tools_ui()

elif menu_v2 == "📈 Decision-Making Models":
    decision_making_models_ui()


elif menu_v2 == "💦 Irrigation Scheduler":
    irrigation_scheduler_ui()

elif menu_v2 == "🚁 Voice-Controlled Drone Irrigation Assistant":
    drone_irrigation_assistant_ui()

# ---------- BACKUP & RECOVERY UI (wrap in a function) ----------
def data_backup_recovery_ui():
    import os, shutil
    from datetime import datetime
    import streamlit as st

    st.header("💾 Data Backup & Recovery")
    st.write("Create a backup of your farm data, restore a previous one, or manage backups.")

    # ensure folders
    data_dir = "farm_data"
    backup_dir = "backups"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    # track active tool
    active_key = kbak("active_tool")
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # triggers
    c1, c2, c3, c4 = st.columns([1.6, 1.6, 1.6, 0.8])
    with c1:
        if st.button("💾 Create Backup", key=kbak("btn_backup")):
            st.session_state[active_key] = "backup"
    with c2:
        if st.button("♻️ Restore Backup", key=kbak("btn_restore")):
            st.session_state[active_key] = "restore"
    with c3:
        if st.button("🗑 Manage Backups", key=kbak("btn_manage")):
            st.session_state[active_key] = "manage"
    with c4:
        if st.button("🔄 Reset", key=kbak("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # Create Backup
    if tool == "backup":
        st.subheader("💾 Create Backup")
        st.write(f"Source folder: `{data_dir}` → Backups in `{backup_dir}`")
        if st.button("📂 Backup Now", key=kbak("do_backup")):
            try:
                backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                backup_path = os.path.join(backup_dir, backup_name)
                shutil.copytree(data_dir, backup_path)
                st.success(f"✅ Backup created successfully: {backup_name}")
            except FileExistsError:
                st.warning("A backup with that name already exists—please try again.")
            except Exception as e:
                st.error(f"❌ Error creating backup: {e}")

    # Restore Backup
    elif tool == "restore":
        st.subheader("♻️ Restore Backup")
        backups = sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))])
        if backups:
            selected_backup = st.selectbox("Select a backup to restore", backups, key=kbak("sel_restore"))
            if st.button("🔄 Restore", key=kbak("do_restore")):
                try:
                    if os.path.exists(data_dir):
                        shutil.rmtree(data_dir)
                    shutil.copytree(os.path.join(backup_dir, selected_backup), data_dir)
                    st.success(f"✅ Backup '{selected_backup}' restored successfully.")
                except Exception as e:
                    st.error(f"❌ Error restoring backup: {e}")
        else:
            st.info("ℹ️ No backups found. Create one first.")

    # Manage Backups
    elif tool == "manage":
        st.subheader("🗑 Manage Backups")
        backups = sorted([d for d in os.listdir(backup_dir) if os.path.isdir(os.path.join(backup_dir, d))])
        if backups:
            selected = st.selectbox("Select a backup", backups, key=kbak("sel_manage"))
            cA, cB = st.columns([1, 1])
            with cA:
                if st.button("🗑 Delete Selected", key=kbak("del_sel")):
                    try:
                        shutil.rmtree(os.path.join(backup_dir, selected))
                        st.success(f"Deleted backup '{selected}'.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting backup: {e}")
            with cB:
                if st.button("📁 Refresh List", key=kbak("refresh")):
                    st.rerun()
        else:
            st.info("No backups to manage yet.")

    else:
        st.info("Choose an action above to create, restore, or manage backups.")


# =========================
# 📦 REQUIRED IMPORTS (top of app.py)
# =========================
import streamlit as st
import pandas as pd
import random
from datetime import datetime, date
import uuid

# =========================
# 🧰 SESSION-STATE HELPERS
# =========================
def _init_state():
    if "stock_items" not in st.session_state:
        # id, name, type, qty, unit, min_level, expiry_date, usage_notes, last_updated
        st.session_state.stock_items = []
    if "stock_usage_logs" not in st.session_state:
        # list of dicts: {id, name, type, action, amount, unit, note, timestamp}
        st.session_state.stock_usage_logs = []
    if "indicator_history" not in st.session_state:
        st.session_state.indicator_history = pd.DataFrame(
            columns=["timestamp", "soil_moisture", "temperature", "humidity",
                     "crop_health_index", "pest_risk", "water_level", "ph", "ec"]
        )

_init_state()


# 📍 Farm Lot Management — Trigger Buttons
# 📍 Farm Lot Management — Trigger Buttons
if (('menu_v2' in globals() and menu_v2 == "📍 Farm Lot Management") or
    ('menu' in globals() and menu   == "📍 Farm Lot Management")):


    import pandas as pd
    from datetime import date
    import uuid

    st.header("📍 Farm Lot Management")

    # ---- state ----
    rows_key  = klot("rows")
    active_key = klot("active_tool")
    if rows_key not in st.session_state:
        st.session_state[rows_key] = []  # list of lot dicts
    if active_key not in st.session_state:
        st.session_state[active_key] = None

    # ---- trigger buttons ----
    c1, c2, c3, c4 = st.columns([1.5, 1.8, 2.0, 0.9])
    with c1:
        if st.button("➕ Add Lot", key=klot("btn_add")):
            st.session_state[active_key] = "add"
    with c2:
        if st.button("📋 View / Edit Lots", key=klot("btn_view")):
            st.session_state[active_key] = "view"
    with c3:
        if st.button("📤 Export / 📥 Import", key=klot("btn_io")):
            st.session_state[active_key] = "io"
    with c4:
        if st.button("🔄 Reset", key=klot("btn_reset")):
            st.session_state[active_key] = None
            st.rerun()

    tool = st.session_state[active_key]

    # ======================
    # Tool: Add Lot
    # ======================
    if tool == "add":
        st.subheader("➕ Add New Lot")
        with st.form(klot("form_add"), clear_on_submit=True):
            cA, cB, cC = st.columns(3)
            with cA:
                name = st.text_input("Lot Name", key=klot("name"))
            with cB:
                area = st.number_input("Area (ha)", min_value=0.0, step=0.1, key=klot("area"))
            with cC:
                status = st.selectbox("Status", ["Fallow", "Prepared", "Planted", "Harvested"], key=klot("status"))

            cD, cE = st.columns(2)
            with cD:
                crop = st.text_input("Crop", key=klot("crop"))
            with cE:
                gps = st.text_input("GPS (lat, lon)", key=klot("gps"))

            notes = st.text_area("Notes", key=klot("notes"))
            submitted = st.form_submit_button("Save Lot", use_container_width=True)

        if submitted:
            if not name.strip():
                st.warning("Please enter a lot name.")
            else:
                st.session_state[rows_key].append({
                    "ID": str(uuid.uuid4())[:8],
                    "Name": name.strip(),
                    "Area (ha)": float(area),
                    "Status": status,
                    "Crop": crop.strip(),
                    "GPS": gps.strip(),
                    "Notes": notes.strip(),
                    "Added": date.today().isoformat(),
                })
                st.success(f"✅ Lot '{name}' saved.")

    # ======================
    # Tool: View / Edit
    # ======================
    elif tool == "view":
        lots = st.session_state.get(rows_key, [])
        if lots:
            st.subheader("📋 Lots")
            df = pd.DataFrame(lots)

            # filters
            f1, f2, f3 = st.columns([1.6, 1.6, 1])
            with f1:
                q = st.text_input("Search (name or crop)", key=klot("q"))
            with f2:
                f_status = st.multiselect("Status filter", ["Fallow", "Prepared", "Planted", "Harvested"], key=klot("f_status"))
            with f3:
                min_area = st.number_input("Min area (ha)", min_value=0.0, step=0.1, key=klot("min_area"))

            mask = pd.Series(True, index=df.index)
            if q:
                mask &= df["Name"].str.contains(q, case=False) | df["Crop"].str.contains(q, case=False)
            if f_status:
                mask &= df["Status"].isin(f_status)
            if min_area > 0:
                mask &= df["Area (ha)"] >= min_area

            view_df = df[mask]
            st.dataframe(view_df, use_container_width=True)

            st.divider()
            st.subheader("✏️ Edit / Delete")
            for _, row in view_df.reset_index(drop=True).iterrows():
                with st.expander(f"📌 {row['Name']} • {row['Area (ha)']} ha • {row['Status']}"):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        new_status = st.selectbox(
                            "Status",
                            ["Fallow", "Prepared", "Planted", "Harvested"],
                            index=["Fallow","Prepared","Planted","Harvested"].index(row["Status"]),
                            key=klot(f"st_{row['ID']}")
                        )
                    with c2:
                        new_area = st.number_input(
                            "Area (ha)", min_value=0.0, step=0.1, value=float(row["Area (ha)"]),
                            key=klot(f"ar_{row['ID']}")
                        )
                    with c3:
                        new_crop = st.text_input("Crop", value=row["Crop"], key=klot(f"cr_{row['ID']}"))

                    g1, g2 = st.columns(2)
                    with g1:
                        new_gps = st.text_input("GPS (lat, lon)", value=row["GPS"], key=klot(f"gps_{row['ID']}"))
                    with g2:
                        new_notes = st.text_area("Notes", value=row["Notes"], key=klot(f"nt_{row['ID']}"))

                    s1, s2 = st.columns(2)
                    with s1:
                        if st.button("💾 Save", key=klot(f"save_{row['ID']}")):
                            for it in st.session_state[rows_key]:
                                if it["ID"] == row["ID"]:
                                    it["Status"] = new_status
                                    it["Area (ha)"] = float(new_area)
                                    it["Crop"] = new_crop
                                    it["GPS"] = new_gps
                                    it["Notes"] = new_notes
                                    st.success("Updated.")
                                    break
                    with s2:
                        if st.button("🗑 Delete", key=klot(f"del_{row['ID']}")):
                            st.session_state[rows_key] = [it for it in st.session_state[rows_key] if it["ID"] != row["ID"]]
                            st.success("Deleted.")
                            st.rerun()
        else:
            st.info("No lots yet. Add one first.")

    # ======================
    # Tool: Export / Import
    # ======================
    elif tool == "io":
        st.subheader("📤 Export / 📥 Import")
        lots = st.session_state.get(rows_key, [])
        df = pd.DataFrame(lots) if lots else pd.DataFrame(columns=["ID","Name","Area (ha)","Status","Crop","GPS","Notes","Added"])

        st.download_button(
            "⬇️ Download Lots CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="farm_lots.csv",
            mime="text/csv",
            key=klot("dl")
        )

        uploaded = st.file_uploader("Upload Lots CSV", type=["csv"], key=klot("upl"))
        if uploaded is not None:
            try:
                imp = pd.read_csv(uploaded)
                required = {"Name","Area (ha)","Status","Crop","GPS","Notes"}
                if not required.issubset(imp.columns):
                    st.warning("CSV must include columns: " + ", ".join(sorted(required)))
                else:
                    count = 0
                    for _, r in imp.iterrows():
                        st.session_state[rows_key].append({
                            "ID": str(uuid.uuid4())[:8],
                            "Name": str(r["Name"]),
                            "Area (ha)": float(r["Area (ha)"]),
                            "Status": str(r["Status"]),
                            "Crop": str(r["Crop"]),
                            "GPS": str(r["GPS"]),
                            "Notes": str(r.get("Notes", "")),
                            "Added": date.today().isoformat(),
                        })
                        count += 1
                    st.success(f"Imported {count} lot(s).")
            except Exception as e:
                st.error(f"Import failed: {e}")

    else:
        st.info("Choose an action above to manage farm lots.")
        
# =========================
# 🧪 SMART FERTILIZER & PESTICIDE STOCK MANAGER (drop-in)
# =======================

# -- initialize session state containers once
def _init_stock_state():
    if "stock_items" not in st.session_state:
        st.session_state.stock_items = []  # list of dicts
    if "stock_usage_logs" not in st.session_state:
        st.session_state.stock_usage_logs = []  # list of dicts

_init_stock_state()

import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date

def _init_stock_state():
    if "stock_items" not in st.session_state:
        st.session_state.stock_items = []  # list of dicts
    if "stock_usage_logs" not in st.session_state:
        st.session_state.stock_usage_logs = []  # list of dicts

def _rerun():
    # works on both new/old Streamlit
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

_init_stock_state()

# ---------- data helpers ----------
def _stock_to_df(items):
    if not items:
        cols = ["id","name","type","qty","unit","min_level","expiry_date","usage_notes","last_updated"]
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(items)

def _log_stock_action(item, action, amount, note):
    st.session_state.stock_usage_logs.append({
        "id": item["id"],
        "name": item["name"],
        "type": item["type"],
        "action": action,   # "use" | "restock"
        "amount": amount,
        "unit": item["unit"],
        "note": note,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# ---------- UI ----------
def smart_fert_pest_ui():
    st.header("🧪 Smart Fertilizer & Pesticide Stock Manager")

    # ---- Add New Item ----
    st.subheader("➕ Add New Item to Stock")
    with st.form(sfp("form_add_item")):
        c1, c2, c3 = st.columns(3)
        with c1:
            item_name = st.text_input("Item Name", key=sfp("add_name"))
            item_type = st.selectbox("Type", ["Fertilizer", "Pesticide"], key=sfp("add_type"))
            unit = st.text_input("Unit", value="kg", key=sfp("add_unit"))
        with c2:
            quantity  = st.number_input("Quantity", min_value=0.0, value=0.0, step=0.1, key=sfp("add_qty"))
            min_level = st.number_input("Reorder Level", min_value=0.0, value=5.0, step=0.1, key=sfp("add_min"))
            expiry_date = st.date_input("Expiry Date", value=date.today(), key=sfp("add_exp"))
        with c3:
            usage_notes = st.text_area("Usage Notes", key=sfp("add_notes"))
        submitted = st.form_submit_button("Add Item")
    if submitted:
        if not item_name.strip():
            st.warning("Please provide an item name.")
        else:
            new_item = {
                "id": str(uuid.uuid4()),
                "name": item_name.strip(),
                "type": item_type,
                "qty": float(quantity),
                "unit": unit.strip() or "kg",
                "min_level": float(min_level),
                "expiry_date": expiry_date.strftime("%Y-%m-%d"),
                "usage_notes": usage_notes.strip(),
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.session_state.stock_items.append(new_item)
            st.success(f"Added '{new_item['name']}' to stock.")
            _rerun()

    # ---- Filters ----
    st.subheader("🔎 Filter & Search")
    f1, f2, f3, f4 = st.columns([2,2,2,2])
    with f1:
        q = st.text_input("Search by name", key=sfp("filter_q"))
    with f2:
        t = st.multiselect("Type filter", ["Fertilizer", "Pesticide"], key=sfp("filter_type"))
    with f3:
        low_stock_only = st.checkbox("Low stock only", key=sfp("filter_low"))
    with f4:
        expiring_only = st.checkbox("Expiring within 30 days", key=sfp("filter_exp"))

    df = _stock_to_df(st.session_state.stock_items)

    if not df.empty:
        mask = pd.Series(True, index=df.index)
        if q:
            mask &= df["name"].str.contains(q, case=False, na=False)
        if t:
            mask &= df["type"].isin(t)
        if low_stock_only:
            mask &= (df["qty"] <= df["min_level"])
        if expiring_only:
            today = pd.Timestamp.today().normalize()
            soon = today + pd.Timedelta(days=30)
            df_dates = pd.to_datetime(df["expiry_date"], errors="coerce")
            mask &= df_dates.between(today, soon, inclusive="both")
        df_view = df[mask].copy()
    else:
        df_view = df

    # ---- Alerts ----
    if not df.empty:
        low_df = df[df["qty"] <= df["min_level"]]
        if not low_df.empty:
            st.error("⚠️ Low stock items detected:")
            for _, r in low_df.iterrows():
                st.write(f"- **{r['name']}** ({r['type']}): {r['qty']} {r['unit']} ≤ reorder level {r['min_level']} {r['unit']}")

        df["expiry_date_dt"] = pd.to_datetime(df["expiry_date"], errors="coerce")
        exp_alert = df[df["expiry_date_dt"] <= (pd.Timestamp.today().normalize() + pd.Timedelta(days=30))]
        if not exp_alert.empty:
            st.warning("⏳ Items nearing expiry (≤ 30 days):")
            for _, r in exp_alert.iterrows():
                days_left = (r["expiry_date_dt"].date() - date.today()).days
                st.write(f"- **{r['name']}** expires in {days_left} day(s) on {r['expiry_date']}")

    # ---- Table ----
    st.subheader("📋 Current Stock")
    st.dataframe(df_view.drop(columns=[c for c in ["expiry_date_dt"] if c in df_view.columns]),
                 use_container_width=True)

    # ---- Row Actions ----
    st.subheader("🛠 Manage Items")
    if not df_view.empty:
        for _, row in df_view.reset_index(drop=True).iterrows():
            with st.expander(f"✏️ {row['name']} • {row['type']} • {row['qty']} {row['unit']}"):
                c1, c2, c3 = st.columns(3)

                # Use
                with c1:
                    use_amount = st.number_input(
                        f"Use amount ({row['unit']})", min_value=0.0, step=0.1, key=sfp(f"use_amt_{row['id']}")
                    )
                    if st.button("➖ Use", key=sfp(f"use_btn_{row['id']}")):
                        if use_amount <= 0:
                            st.warning("Enter a valid amount to use.")
                        elif use_amount > row["qty"]:
                            st.warning("Not enough in stock.")
                        else:
                            for it in st.session_state.stock_items:
                                if it["id"] == row["id"]:
                                    it["qty"] = round(it["qty"] - float(use_amount), 3)
                                    it["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    _log_stock_action(it, "use", float(use_amount), "Used in field application")
                                    st.success(f"Used {use_amount} {it['unit']} from {it['name']}.")
                                    break
                            _rerun()

                # Restock
                with c2:
                    restock_amount = st.number_input(
                        f"Restock amount ({row['unit']})", min_value=0.0, step=0.1, key=sfp(f"restock_amt_{row['id']}")
                    )
                    if st.button("➕ Restock", key=sfp(f"restock_btn_{row['id']}")):
                        if restock_amount <= 0:
                            st.warning("Enter a valid amount to restock.")
                        else:
                            for it in st.session_state.stock_items:
                                if it["id"] == row["id"]:
                                    it["qty"] = round(it["qty"] + float(restock_amount), 3)
                                    it["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    _log_stock_action(it, "restock", float(restock_amount), "Supplier delivery")
                                    st.success(f"Restocked {restock_amount} {it['unit']} to {it['name']}.")
                                    break
                            _rerun()

                # Update settings
                with c3:
                    new_min = st.number_input(
                        "Update reorder level", min_value=0.0, step=0.1, value=float(row["min_level"]),
                        key=sfp(f"upd_min_{row['id']}")
                    )
                    new_exp = st.date_input(
                        "Update expiry date",
                        value=pd.to_datetime(row["expiry_date"], errors="coerce").date()
                              if pd.notna(pd.to_datetime(row["expiry_date"], errors="coerce")) else date.today(),
                        key=sfp(f"upd_exp_{row['id']}")
                    )
                    if st.button("💾 Save updates", key=sfp(f"save_upd_{row['id']}")):
                        for it in st.session_state.stock_items:
                            if it["id"] == row["id"]:
                                it["min_level"] = float(new_min)
                                it["expiry_date"] = new_exp.strftime("%Y-%m-%d")
                                it["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.success("Item settings updated.")
                                break
                        _rerun()

                # Delete
                del_col1, _ = st.columns([1,5])
                with del_col1:
                    if st.button("🗑 Delete item", type="secondary", key=sfp(f"del_{row['id']}")):
                        st.session_state.stock_items = [it for it in st.session_state.stock_items if it["id"] != row["id"]]
                        st.success(f"Deleted {row['name']} from stock.")
                        _rerun()

    # ---- Logs & IO ----
    st.subheader("🧾 Usage & Restock Logs")
    if st.session_state.stock_usage_logs:
        logs_df = pd.DataFrame(st.session_state.stock_usage_logs)
        st.dataframe(logs_df, use_container_width=True)
        st.download_button(
            "Download logs CSV",
            logs_df.to_csv(index=False).encode("utf-8"),
            file_name="stock_usage_logs.csv",
            mime="text/csv",
            key=sfp("dl_logs")
        )
    else:
        st.info("No usage or restock logs yet.")

    st.subheader("📤 Export / 📥 Import")
    exp_df = _stock_to_df(st.session_state.stock_items)
    st.download_button(
        "Download stock CSV",
        exp_df.to_csv(index=False).encode("utf-8"),
        file_name="stock_items.csv",
        mime="text/csv",
        key=sfp("dl_stock")
    )

    uploaded = st.file_uploader("Import stock CSV (id will be regenerated)", type=["csv"], key=sfp("upl_stock"))
    if uploaded is not None:
        try:
            imp = pd.read_csv(uploaded)
            required = {"name","type","qty","unit","min_level","expiry_date","usage_notes"}
            if not required.issubset(set(imp.columns)):
                st.warning(f"CSV must include columns: {', '.join(sorted(required))}")
            else:
                imported = []
                for _, r in imp.iterrows():
                    imported.append({
                        "id": str(uuid.uuid4()),
                        "name": str(r["name"]),
                        "type": str(r["type"]),
                        "qty": float(r["qty"]),
                        "unit": str(r["unit"]),
                        "min_level": float(r["min_level"]),
                        "expiry_date": str(r["expiry_date"]),
                        "usage_notes": str(r.get("usage_notes","")),
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                st.session_state.stock_items.extend(imported)
                st.success(f"Imported {len(imported)} items.")
                _rerun()
        except Exception as e:
            st.error(f"Import failed:{e}")



# ===============================
# 🚨 Smart Farm Alerts
# ===============================

st.header("🚨 Smart Farm Alerts")
st.write("Click a button below to view farm alerts instantly.")

# ---- Ensure session key exists ----
st.session_state.setdefault("active_alert", None)

# ---- Optional: simple speaker (no external deps) ----
def _speak_alert(text: str) -> None:
    # Replace with pyttsx3/gTTS if you want real audio. This is a UI toast/log for now.
    st.toast("🔊 " + text)
    st.write("🔊", text)

# ---- Alert config: key -> (title, render_fn, message, voice_line) ----
_ALERTS = {
    "weather": (
        "🌦 Weather Alert",
        st.info,
        "Heavy rainfall expected tomorrow. Prepare drainage and cover seedlings.",
        "Weather alert: heavy rainfall expected tomorrow. Prepare drainage and cover seedlings."
    ),
    "pest": (
        "🐛 Pest Alert",
        st.warning,
        "Armyworm outbreak detected nearby. Apply the recommended pesticide early.",
        "Pest alert: armyworm outbreak detected nearby. Apply the recommended pesticide early."
    ),
    "soil": (
        "🌱 Soil Alert",
        st.success,
        "Soil moisture is low — consider irrigating this evening.",
        "Soil alert: moisture is low. Consider irrigating this evening."
    ),
    "market": (
        "📈 Market Alert",
        st.info,
        "Maize prices are up 12% this week — it may be a good time to sell.",
        "Market alert: maize prices are up twelve percent this week. It may be a good time to sell."
    ),
    "emergency": (
        "🚨 Emergency Alert",
        st.error,
        "Security breach detected near Gate 2. Notify the team and verify the perimeter now.",
        "Emergency alert: security breach detected near Gate two. Notify the team and verify the perimeter now."
    ),
}

# ---- Trigger buttons row ----
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    if st.button("🌦 Weather", key="btn_weather"):
        st.session_state.active_alert = "weather"
with c2:
    if st.button("🐛 Pest", key="btn_pest"):
        st.session_state.active_alert = "pest"
with c3:
    if st.button("🌱 Soil", key="btn_soil"):
        st.session_state.active_alert = "soil"
with c4:
    if st.button("📈 Market", key="btn_market"):
        st.session_state.active_alert = "market"
with c5:
    if st.button("🚨 Emergency", key="btn_emergency"):
        st.session_state.active_alert = "emergency"

st.divider()


# ---------------------------
# Safe defaults (only if missing)
# ---------------------------
if "_speak_alert" not in globals():
    def _speak_alert(text: str) -> None:
        # Replace with real TTS if you want (pyttsx3 / gTTS). For now: toast + print.
        st.toast("🔊 " + text)
        st.write("🔊", text)

# Simple wrappers (optional; you can pass st.info etc. directly)
def _render_info(msg: str):    st.info(msg)
def _render_warn(msg: str):    st.warning(msg)
def _render_ok(msg: str):      st.success(msg)
def _render_err(msg: str):     st.error(msg)

# Declarative alert config: key -> (title, renderer, message, voice_line)
if "_ALERTS" not in globals():
    _ALERTS = {
        "weather": (
            "🌦 Weather Alert",
            _render_info,
            "Heavy rainfall expected tomorrow. Prepare drainage and cover seedlings.",
            "Weather alert: heavy rainfall expected tomorrow. Prepare drainage and cover seedlings."
        ),
        "pest": (
            "🐛 Pest Alert",
            _render_warn,
            "Armyworm outbreak detected nearby. Apply recommended pesticide early.",
            "Pest alert: armyworm outbreak detected nearby. Apply the recommended pesticide early."
        ),
        "soil": (
            "🌱 Soil Alert",
            _render_ok,
            "Soil moisture is low — consider irrigation this evening.",
            "Soil alert: moisture is low. Consider irrigating this evening."
        ),
        "market": (
            "📈 Market Alert",
            _render_info,
            "Maize prices have increased by 12% this week — good time to sell.",
            "Market alert: maize prices are up twelve percent this week. It may be a good time to sell."
        ),
        "emergency": (
            "🚨 Emergency Alert",
            _render_err,
            "Security breach detected near Gate 2. Notify the team and verify the perimeter now.",
            "Emergency alert: security breach near Gate 2. Notify the team and verify the perimeter now."
        ),
    }

# Ensure session key exists
st.session_state.setdefault("active_alert", None)

# ---------------------------
# Display active alert
# ---------------------------
active_key = st.session_state.get("active_alert")
cfg = _ALERTS.get(active_key)

if cfg:
    title, render_fn, message, voice_line = cfg
    st.subheader(title)
    render_fn(message)
    if st.button("🔊 Read it out", key="alert_readout"):
        _speak_alert(voice_line)
else:
    st.caption("No alert selected yet. Use the tester below to trigger one.")

# ---------------------------
# Tester UI to trigger alerts
# ---------------------------
with st.expander("🔔 Test Smart Farm Alerts"):
    from datetime import datetime

    # Use your global _ALERTS dict if it exists; otherwise show a hint.
    ALERTS = globals().get("_ALERTS", {})
    if not ALERTS:
        st.info(
            "No alerts configured yet. Define `_ALERTS` above, e.g.:\n\n"
            "_ALERTS = {\n"
            "  'Low moisture': {'level':'warning','message':'Soil moisture < 30% — irrigate soon.'},\n"
            "  'High temp': {'level':'error','message':'Temp > 35°C — heat stress risk.'},\n"
            "  'Saved': {'level':'success','message':'Settings saved successfully.'}\n"
            "}"
        )
    else:
        choice = st.selectbox("Choose alert", ["", *list(ALERTS.keys())], key="alert_choice")

        if choice:
            data = ALERTS[choice]
            # Supports either dict entries or plain strings in _ALERTS
            if isinstance(data, dict):
                level = (data.get("level") or "info").lower()
                message = data.get("message") or choice
            else:
                level = "info"
                message = str(data)

            # Show the selected alert
            if level == "success":
                st.success(message)
            elif level == "warning":
                st.warning(message)
            elif level == "error":
                st.error(message)
            else:
                st.info(message)

            # Log it (optional)
            st.session_state.setdefault("alert_log", []).append(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": choice,
                    "level": level,
                    "message": message,
                }
            )

        # Show recent alerts (optional)
        if st.session_state.get("alert_log"):
            st.markdown("**Recent alerts**")
            for row in st.session_state["alert_log"][-10:][::-1]:
                st.write(f"{row['time']} • {row['level'].upper()} • {row['name']}: {row['message']}")


#smart_tutor_voice
def smart_tutor_voice():
    import os
    from datetime import datetime
    import streamlit as st

    # --- optional deps (gracefully handled)
    try:
        import speech_recognition as sr  # mic / audio-to-text
    except Exception:
        sr = None
    try:
        import pyttsx3  # offline TTS
    except Exception:
        pyttsx3 = None
    try:
        from gtts import gTTS  # online TTS fallback
    except Exception:
        gTTS = None

    # translators (optional)
    translator = None
    _gt = None
    try:
        from googletrans import Translator  # pip install googletrans==4.0.0rc1
        translator = "googletrans"
        _gt = Translator()
    except Exception:
        try:
            from deep_translator import GoogleTranslator  # pip install deep-translator
            translator = "deep"
        except Exception:
            translator = None

    # OpenAI (optional)
    client = None
    try:
        from openai import OpenAI  # pip install openai
        if os.getenv("OPENAI_API_KEY"):
            client = OpenAI()
    except Exception:
        client = None

    # --- UI
    st.header("🧑‍🏫 Smart Tutor (Multi-Language) + 🎙️ Voice")
    st.caption("Speak or type your question. I’ll answer and can read the reply aloud.")

    LANGS = [
        "Urhobo","Yorùbá","Hausa","Ịjọ (Ijaw)","Efik (Calabar)","Ịgbò (Igbo)","Edo (Bini)","Tiv",
        "Ibibio","Kanuri","Nupe","Fulfulde (Fula)","Itsekiri","Gbagyi","Idoma","Ebira","Jukun",
        "Igala","Berom (Birom)","Esan","Isoko","Okun (Yoruba dialect)","Ika","English (for reference)"
    ]
    DOMAINS = [
        "General chat","Farming & Agriculture","Business & Finance",
        "Health & Safety (non-medical advice)","Education & Study Help",
    ]
    TONES = ["Neutral","Friendly","Professional","Encouraging","Brief"]

    c1, c2, c3 = st.columns([1.2, 1, 1])
    lang   = c1.selectbox("Language", LANGS, index=0, key="st_lang")
    domain = c2.selectbox("Domain", DOMAINS, index=1, key="st_domain")
    tone   = c3.selectbox("Tone", TONES, index=1, key="st_tone")

    vc1, vc2, vc3 = st.columns([1.1, 1.1, 1])
    input_mode    = vc1.radio("Input Mode", ["🎙️ Voice", "⌨️ Typing"], horizontal=True, key="st_input_mode")
    auto_speak    = vc2.toggle("🔁 Auto-speak reply", value=True, key="st_auto_speak")
    tts_lang_hint = vc3.selectbox(
        "TTS language (for playback)",
        ["auto (best effort)","en","ha","yo","ig"],
        index=0,
        key="st_tts_code"
    )

    # --- helpers
    def _system_prompt(lang_, domain_, tone_):
        return f"""You are a helpful AI that replies entirely in {lang_}.
Tone: {tone_}. Domain focus: {domain_}.
Use clear, culturally appropriate expressions. Avoid slang unless asked.
If a term has no direct {lang_} word, explain briefly in {lang_}.
Keep paragraphs short. Use bullet points for steps/lists.
Do NOT switch to English unless the user asks.""".strip()

    def _translate_to(text, target_code):
        if not translator or not (text or "").strip():
            return text
        try:
            if translator == "googletrans":
                return _gt.translate(text, dest=target_code or "en").text
            else:
                from deep_translator import GoogleTranslator
                return GoogleTranslator(source="auto", target=target_code or "en").translate(text)
        except Exception:
            return text

    def _speak_text(text, lang_code="en"):
        # offline first
        if pyttsx3 is not None:
            try:
                engine = pyttsx3.init()
                try:
                    rate = engine.getProperty("rate")
                    if isinstance(rate, int):
                        engine.setProperty("rate", max(120, min(185, rate)))
                except Exception:
                    pass
                engine.say(text)
                engine.runAndWait()
                st.caption("🔉 Played using offline TTS (pyttsx3).")
                return
            except Exception:
                pass
        # gTTS fallback
        if gTTS is not None:
            try:
                use_code = lang_code if lang_code in {"en","ha","yo","ig"} else "en"
                tts = gTTS(text=text, lang=use_code)
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                    tts.save(tmp.name)
                    st.audio(tmp.name, format="audio/mp3")
                    st.caption("🔉 Played using gTTS.")
                return
            except Exception as e:
                st.warning(f"TTS failed: {e}")
        st.info("🔇 Could not play audio (no TTS engine available).")

    def _model_answer(user_text: str) -> str:
        sys_prompt = _system_prompt(lang, domain, tone)
        if client is not None:
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"system","content":sys_prompt},{"role":"user","content":user_text}],
                    temperature=0.6,
                    max_tokens=380,
                )
                return (resp.choices[0].message.content or "").strip()
            except Exception:
                pass
        # local fallback
        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        header = f"[{lang}] — {domain} • {tone}"
        body_map = {
            "Farming & Agriculture":"• Farm advice (summary):",
            "Business & Finance":"• Business guidance (summary):",
            "Health & Safety (non-medical advice)":"• Safety tips (general):",
            "Education & Study Help":"• Study help (outline):",
            "General chat":"• Response (general):",
        }
        return (
            f"{header}\n"
            f"{body_map.get(domain,'• Response:')}\n"
            f"- 1) Identify main need. 2) Give short, clear guidance. 3) Suggest next step.\n"
            f"- Your request: “{(user_text or '').strip()}”\n"
            f"- Tip: Keep records and review weekly.\n"
            f"— {ts}"
        )

    # --- state
    if "st_msgs" not in st.session_state:
        st.session_state.st_msgs = []

    recognized_box = st.empty()
    query_text = ""

    # --- input (voice or typing)
    if input_mode == "🎙️ Voice":
        c_mic, c_up = st.columns([1, 1])
        mic_clicked = c_mic.button("🎤 Tap to Record", key="st_mic_btn")
        audio_file  = c_up.file_uploader("…or upload WAV/MP3", type=["wav","mp3","m4a"], key="st_audio_upload")

        if mic_clicked:
            if sr is None:
                st.error("SpeechRecognition not installed. Try: `pip install SpeechRecognition pyaudio`")
            else:
                try:
                    recog = sr.Recognizer()
                    with sr.Microphone() as source:
                        st.info("🎤 Listening…")
                        try:
                            recog.adjust_for_ambient_noise(source, duration=0.6)
                        except Exception:
                            pass
                        audio = recog.listen(source, timeout=4, phrase_time_limit=8)
                    st.caption("⏳ Transcribing…")
                    hint_code = {"Yorùbá":"yo","Hausa":"ha","Ịgbò (Igbo)":"ig"}.get(lang, "en")
                    query_text = recog.recognize_google(audio, language=hint_code)
                    recognized_box.success(f"🗣️ Recognized: {query_text}")
                except sr.WaitTimeoutError:
                    st.error("Listening timed out. Try again and speak sooner.")
                except sr.UnknownValueError:
                    st.error("I couldn't understand that. Please try again.")
                except sr.RequestError:
                    st.error("Speech service unavailable. Check internet connection.")
                except Exception as e:
                    st.error(f"Mic/recognition error: {e}")

        if audio_file is not None and sr is not None:
            try:
                recog = sr.Recognizer()
                with sr.AudioFile(audio_file) as source:
                    audio = recog.record(source)
                st.caption("⏳ Transcribing uploaded audio…")
                hint_code = {"Yorùbá":"yo","Hausa":"ha","Ịgbò (Igbo)":"ig"}.get(lang, "en")
                query_text = recog.recognize_google(audio, language=hint_code)
                recognized_box.success(f"🗣️ Recognized: {query_text}")
            except Exception as e:
                st.error(f"Audio transcription failed: {e}")

        default_text = query_text or st.session_state.get("st_last_text", "")
        user_text = st.text_area(
            "Type your question / prompt",
            value=default_text,
            placeholder="e.g., Explain in Yorùbá how to prevent tomato leaf blight this week.",
            height=140,
            key="st_query",
        )
        st.session_state["st_last_text"] = user_text

    else:
        default_text = st.session_state.get("st_last_text", "")
        user_text = st.text_area(
            "Type your question / prompt",
            value=default_text,
            placeholder="e.g., Explain in Yorùbá how to prevent tomato leaf blight this week.",
            height=140,
            key="st_query",
        )
        st.session_state["st_last_text"] = user_text

    st.divider()

    # --- generate
    go = st.button("Generate", type="primary", key="st_go")
    if go:
        if not (user_text or "").strip():
            st.warning("Please enter a question or prompt.")
        else:
            with st.spinner("Generating..."):
                base_reply = _model_answer(user_text)
                lang_to_code = {
                    "English (for reference)": "en",
                    "Yorùbá": "yo",
                    "Hausa": "ha",
                    "Ịgbò (Igbo)": "ig",
                }
                target_code = lang_to_code.get(lang, "en")
                translated = _translate_to(base_reply, target_code) if target_code else base_reply

            st.session_state.st_msgs.append(("user", user_text))
            st.session_state.st_msgs.append(("assistant", translated))

            st.markdown("### ✅ Tutor Response")
            st.write(translated)

            if auto_speak and (translated or "").strip():
                tts_code = None if tts_lang_hint.startswith("auto") else tts_lang_hint
                _speak_text(translated, lang_code=tts_code or target_code or "en")

    # --- history
    if st.session_state.get("st_msgs"):
        st.subheader("💬 Conversation")
        for role, text in st.session_state.st_msgs:
            if role == "user":
                with st.chat_message("user", avatar="🧑"):
                    st.write(text)
            else:
                with st.chat_message("assistant", avatar="🧠"):
                    st.write(text)
                if st.button("🔊 Speak this reply", key=f"st_say_{abs(hash(text))%10**8}"):
                        tts_code = None if tts_lang_hint.startswith("auto") else tts_lang_hint
                        lang_to_code = {
                            "English (for reference)": "en",
                            "Yorùbá": "yo",
                            "Hausa": "ha",
                            "Ịgbò (Igbo)": "ig",
                        }
                        inferred = lang_to_code.get(lang, "en")
                        _speak_text(text, lang_code=(tts_code or inferred or "en"))

    # Only developers who intentionally enable this will see the notes.
if st.session_state.get("_dev_show_tutor_notes", False):

    with st.expander("ℹ️ Notes / Setup"):

        st.markdown("""

        - Voice input: `pip install SpeechRecognition pyaudio` (microphone support)  

        - Offline TTS: `pyttsx3`  

        - Online TTS: `gTTS`  

        - Translation: `googletrans==4.0.0rc1` or `deep-translator` (optional)  

        - Not all listed languages have stable TTS/STT codes; the app will fallback to English playback.  

        - If you set `OPENAI_API_KEY` in the environment, real AI responses will be used; otherwise the app uses a local fallback template.  



        **Developer tips**  

        - To enable these notes temporarily in a session:  

          `st.session_state["_dev_show_tutor_notes"] = True`  

        - Keep this disabled in production to avoid exposing internal setup details.  

        - If speech or TTS features fail, check microphone permissions and re-run the install commands above.  

        """)


