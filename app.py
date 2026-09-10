import streamlit as st
import pickle
import pandas as pd
from pathlib import Path
from PIL import Image
from data.models.vision_model import analyze_flood_image



st.set_page_config(
    page_title="Odisha Sahayak AI",
    page_icon="🌊",
    layout="wide"
)

# -----------------------------
# Load ML model
# -----------------------------
MODEL_PATH = Path("data/models/flood_risk_model.pkl")

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)
# -----------------------------
# Flood Risk State
# -----------------------------

if "flood_risk_status" not in st.session_state:
    st.session_state.flood_risk_status = "MONITORING"

if "flood_probability" not in st.session_state:
    st.session_state.flood_probability = 0.0

# -----------------------------
# Header
# -----------------------------
st.title("🌊 Odisha Sahayak AI")
st.subheader("Predict. Detect. Respond.")

st.write(
    "AI-powered disaster assistance platform designed "
    "to support flood and emergency response in Odisha."
)

st.divider()

# -----------------------------
# Dashboard
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("AI Model", "Random Forest")

with col2:
    st.metric("Reports Today", "24")

with col3:
    st.metric("Areas Monitored", "12")

st.divider()
# --------------------------------------------------
# DISASTER SITUATION DASHBOARD
# --------------------------------------------------

st.header("🛰️ Odisha Disaster Situation Dashboard")

st.write(
    "Prototype monitoring view showing example disaster-risk "
    "locations across Odisha."
)

# Demo monitoring locations
# These are illustrative prototype locations,
# not live government data.

monitoring_data = pd.DataFrame({
    "Location": [
        "Bhubaneswar",
        "Puri",
        "Cuttack",
        "Balasore",
        "Kendrapara",
        "Jagatsinghpur"
    ],
    "Latitude": [
        20.2961,
        19.8135,
        20.4625,
        21.4942,
        20.5017,
        20.2644
    ],
    "Longitude": [
        85.8245,
        85.8312,
        85.8828,
        86.9317,
        86.4220,
        86.1711
    ],
    "Risk Status": [
        "Monitoring",
        "High",
        "Medium",
        "Monitoring",
        "High",
        "Medium"
    ]
})

st.subheader("📍 Monitoring Map")

st.map(
    monitoring_data,
    latitude="Latitude",
    longitude="Longitude",
    size=150,
    zoom=7
    
)

st.caption(
    "⚠️ Prototype map using illustrative monitoring data. "
    "Locations and risk statuses are not live official warnings."
)

st.subheader("📊 Area Monitoring Status")

st.dataframe(
    monitoring_data[
        ["Location", "Risk Status"]
    ],
    use_container_width=True,
    hide_index=True
)
# --------------------------------------------------
# DISASTER COMMAND PANEL
# --------------------------------------------------

st.divider()

st.header("🚨 Disaster Command Panel")

st.write(
    "Unified prototype status panel combining "
    "the available Odisha Sahayak AI modules."
)

cmd1, cmd2, cmd3, cmd4 = st.columns(4)

with cmd1:

    risk_status = st.session_state.flood_risk_status

    if risk_status == "HIGH":
        st.metric(
            "🌊 Flood Risk",
            "🔴 HIGH"
        )

    elif risk_status == "LOW":
        st.metric(
            "🌊 Flood Risk",
            "🟢 LOW"
        )

    else:
        st.metric(
            "🌊 Flood Risk",
            "🟡 MONITORING"
        )

with cmd2:
    st.metric(
        "📷 Vision AI",
        "ONLINE"
    )

with cmd3:
    st.metric(
        "🚨 Emergency Engine",
        "ONLINE"
    )

with cmd4:
    st.metric(
        "📍 Areas Monitored",
        "12"
    )

st.subheader("🟢 AI System Status")

status1, status2, status3 = st.columns(3)

with status1:
    st.success("🧠 Flood Risk Model\n\nONLINE")

with status2:
    st.success("📷 Vision Analysis\n\nONLINE")

with status3:
    st.success("🚨 Emergency Response\n\nONLINE")

st.info(
    "This command panel is a hackathon prototype. "
    "Displayed monitoring values are illustrative and "
    "are not live government disaster warnings."
)

# -----------------------------
# Flood Risk Prediction
# -----------------------------
st.header("🧠 AI Flood Risk Prediction")

col1, col2, col3 = st.columns(3)

with col1:
    rainfall = st.slider("Rainfall (mm)", 0, 500, 100)

with col2:
    humidity = st.slider("Humidity (%)", 0, 100, 70)

with col3:
    water_level = st.slider("Water Level", 0, 10, 3)

if st.button("🔍 Analyze Risk"):

    input_data = pd.DataFrame({
        "rainfall": [rainfall],
        "humidity": [humidity],
        "water_level": [water_level]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("📊 AI Assessment")

if prediction == 1:

    st.error("🔴 HIGH FLOOD RISK")

    st.session_state.flood_risk_status = "HIGH"
    st.session_state.flood_probability = probability * 100
else:

    st.success("🟢 LOW FLOOD RISK")

    st.session_state.flood_risk_status = "LOW"
    st.session_state.flood_probability = probability * 100

    st.metric(
        "Model Flood Probability",
        f"{probability * 100:.1f}%"
    )

    st.caption(
        "Prototype model. Predictions should be validated "
        "with real local observations."
    )
# --------------------------------------------------
# FLOOD IMAGE ANALYSIS
# --------------------------------------------------

st.divider()

st.header("📷 AI Flood Image Analysis")

st.write(
    "Upload a road, street, outdoor area, or "
    "waterlogging photograph for AI assessment."
)

uploaded_file = st.file_uploader(
    "📤 Upload image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

    if st.button("🔍 Analyze Image", key="image_analysis"):

        with st.spinner("🤖 AI is analyzing the image..."):

            result = analyze_flood_image(image)

        # -----------------------------------------
        # Extract AI result
        # -----------------------------------------

        valid_scene = result["valid_scene"]
        flood_detected = result["flood_detected"]
        severity = result["severity"]
        confidence = result.get("confidence", 0)

        # -----------------------------------------
        # INVALID IMAGE
        # -----------------------------------------

        if not valid_scene:

            st.error(
                "❌ INVALID IMAGE FOR FLOOD ANALYSIS"
            )

            st.warning(
                result["assessment"]
            )

        # -----------------------------------------
        # VALID IMAGE
        # -----------------------------------------

        else:

            if flood_detected:

                st.warning(
                    "🌊 POSSIBLE FLOOD / "
                    "WATERLOGGING DETECTED"
                )

            else:

                st.success(
                    "🛣️ NO OBVIOUS FLOOD DETECTED"
                )

            st.subheader("📊 Vision Assessment")

            if severity == "HIGH":

                st.error(
                    "🔴 HIGH FLOOD / "
                    "WATERLOGGING INDICATION"
                )

            elif severity == "MEDIUM":

                st.warning(
                    "🟠 MEDIUM FLOOD INDICATION"
                )

            else:

                st.success(
                    "🟢 LOW FLOOD INDICATION"
                )

            st.write("### 🧠 AI Assessment")

            st.write(
                result["assessment"]
            )

            st.write("### 🤖 AI Vision Confidence")
            confidence  =result.get("confidence", 0)
            

            st.metric(
                "Classification Confidence",
                f"{confidence:.1f}%"
            )

            st.write(
                "### 🛟 Recommended Action"
            )

            if flood_detected:

                st.info(
                    "Avoid entering unknown-depth "
                    "floodwater and follow local "
                    "authority instructions."
                )

            else:

                st.info(
                    "No strong flood indication was "
                    "identified by the prototype. "
                    "Continue monitoring the situation."
                )

            st.caption(
                "Prototype AI vision assessment. "
                "This result is not an official flood "
                "warning and has not been validated "
                "for operational use."
            )
# -----------------------------
# Emergency Response Engine
# -----------------------------
st.divider()
st.header("🚨 Emergency Response Engine")

question = st.text_input(
    "Describe your emergency:",
    placeholder="Example: Mo area re bahut pani achhi..."
)

if question:

    text = question.lower().strip()

    flood_words = [
        "pani", "paani", "water", "flood",
        "banya", "ban", "waterlogging",
        "duba", "flooded", "ପାଣି", "ବନ୍ୟା"
    ]

    danger_words = [
        "trapped", "stuck", "ataki",
        "danger", "dangerous", "rescue",
        "bachao", "drowning", "dubu", "dubi"
    ]

    damage_words = [
        "damage",
        "damaged",
        "ghara",
        "house",
        "collapse",
        "collapsed",
        "bhangi",
        "ଭାଙ୍ଗି",
        "ଘର"
    ]

    medical_words = [
        "injury", "injured", "medical",
        "ambulance", "bleeding",
        "hospital", "doctor"
    ]

    fire_words = [
        "fire", "agni",
        "ନିଆଁ", "ଅଗ୍ନି"
    ]

    earthquake_words = [
        "earthquake", "bhukampa",
        "ଭୂକମ୍ପ", "tremor"
    ]

    road_words = [
        "road blocked",
        "roadblock",
        "road blockage",
        "rasta blocked",
        "rasta band",
        "road band"
    ]

    # CRITICAL
    if any(word in text for word in danger_words):

        st.error("🚨 CRITICAL PRIORITY — IMMEDIATE DANGER")

        st.write("### 🛟 Recommended Actions")
        st.write("• Move to a safe location if possible.")
        st.write("• Seek immediate rescue assistance.")
        st.write("• Follow local authority instructions.")

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Immediate Danger / Rescue")
        st.write("**Priority:** Critical")

    # MEDICAL
    elif any(word in text for word in medical_words):

        st.error("🔴 HIGH PRIORITY — MEDICAL EMERGENCY")

        st.write("### 🛟 Recommended Actions")
        st.write("• Move to a safe location.")
        st.write("• Seek immediate medical assistance.")
        st.write("• Contact appropriate local emergency services.")

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Medical Emergency")
        st.write("**Priority:** High")

    # FIRE
    elif any(word in text for word in fire_words):

        st.error("🔴 HIGH PRIORITY — FIRE EMERGENCY")

        st.write("### 🛟 Recommended Actions")
        st.write("• Move away from fire and smoke.")
        st.write("• Do not enter an unsafe building.")
        st.write("• Seek emergency assistance.")

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Fire")
        st.write("**Priority:** High")

    # EARTHQUAKE
    elif any(word in text for word in earthquake_words):

        st.error("🔴 HIGH PRIORITY — EARTHQUAKE")

        st.write("### 🛟 Recommended Actions")
        st.write("• Move to a safe open area if possible.")
        st.write("• Stay away from damaged buildings.")
        st.write("• Follow local authority instructions.")

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Earthquake")
        st.write("**Priority:** High")

    # DAMAGE
    elif any(word in text for word in damage_words):

        st.error("🔴 HIGH PRIORITY — STRUCTURAL DAMAGE")

        st.write("### 🛟 Recommended Actions")
        st.write("• Stay away from damaged or unstable buildings.")
        st.write("• Do not enter a damaged structure.")
        st.write("• Move to a safe open area if possible.")
        st.write("• Report the damage to local authorities.")

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Structural / Property Damage")
        st.write("**Priority:** High")

    # FLOOD
    elif any(word in text for word in flood_words):

        st.warning("🟠 MEDIUM PRIORITY — FLOOD / WATERLOGGING")

        st.write("### 🛟 Recommended Actions")
        st.write("• Move to a safe or elevated location.")
        st.write("• Avoid moving or unknown-depth floodwater.")
        st.write("• Follow local authority instructions.")

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Flood / Waterlogging")
        st.write("**Priority:** Medium")

    # ROAD BLOCK
    elif any(word in text for word in road_words):

        st.warning("🟠 MEDIUM PRIORITY — ROAD BLOCKAGE")

        st.write("### 🛟 Recommended Actions")
        st.write("• Avoid the blocked route.")
        st.write("• Use an alternative safe route if available.")
        st.write("• Report the blockage.")

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Road Blockage")
        st.write("**Priority:** Medium")

    # UNKNOWN
    else:

        st.info("🟡 INFORMATION REQUIRED")

        st.write(
            "Please provide more details such as your "
            "situation, location, or emergency."
        )
st.caption(
    "Odisha Sahayak AI — Hackathon Prototype | "
    "AI predictions are decision-support estimates, "
    "not official warnings."
)
