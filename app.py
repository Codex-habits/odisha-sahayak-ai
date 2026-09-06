import streamlit as st
import pickle
import pandas as pd
from pathlib import Path

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
    else:
        st.success("🟢 LOW FLOOD RISK")

    st.metric(
        "Model Flood Probability",
        f"{probability * 100:.1f}%"
    )

    st.caption(
        "Prototype model. Predictions should be validated "
        "with real local observations."
    )

# -----------------------------
# Image Analysis
# -----------------------------
st.divider()
st.header("📷 AI Flood Image Analysis")

uploaded_file = st.file_uploader(
    "Upload a road/area image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded image",
        use_container_width=True
    )

    if st.button("🔍 Analyze Image"):

        st.warning(
            "⚠️ Computer-vision model is currently "
            "in prototype stage."
        )

        st.write("### 📋 Preliminary Assessment")

        st.write(
            "Image received successfully. A trained "
            "computer-vision model will classify "
            "waterlogging severity in the next stage."
        )

        st.info(
            "Recommended action: avoid moving or "
            "unknown-depth floodwater."
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

    text = question.lower()

    # Keywords
    flood_words = [
        "pani", "water", "flood", "banya",
        "ban", "waterlogging", "duba",
        "flooded", "paani", "ପାଣି", "ବନ୍ୟା"
    ]

    danger_words = [
        "trapped", "stuck", "ataki",
        "danger", "dangerous",
        "rescue", "bachao",
        "drowning", "dubu", "dubi"
    ]

    damage_words = [
        "damaged", "damage", "damaged house",
        "ghara damaged", "house damaged",
        "collapse", "collapsed", "bhangi",
        "ଭାଙ୍ଗି", "ଘର ଭାଙ୍ଗି"
    ]

    medical_words = [
        "injury", "injured", "medical",
        "ambulance", "bleeding",
        "hospital", "doctor", "injured person"
    ]

    fire_words = [
        "fire", "agni", "agni lagichi",
        "ଅଗ୍ନି", "ନିଆଁ", "fire lagichi"
    ]

    earthquake_words = [
        "earthquake", "bhukampa",
        "ଭୂକମ୍ପ", "tremor"
    ]

    road_words = [
        "road blocked", "roadblock",
        "road blockage", "rasta blocked",
        "rasta band", "road band"
    ]

    # CRITICAL: Person trapped / drowning
    if any(word in text for word in danger_words):

        st.error("🚨 CRITICAL PRIORITY — PERSON IN DANGER")

        st.write("### 🛟 Immediate Actions")

        st.write(
            "• Move to a safe location if you can do so safely."
        )

        st.write(
            "• Do not enter deep or fast-moving water to rescue someone."
        )

        st.write(
            "• Contact appropriate local emergency services immediately."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Person in Danger")
        st.write("**Priority:** Critical")

    # Medical emergency
    elif any(word in text for word in medical_words):

        st.error("🔴 HIGH PRIORITY — MEDICAL EMERGENCY")

        st.write("### 🛟 Recommended Actions")

        st.write(
            "• Seek immediate medical assistance."
        )

        st.write(
            "• Move to a safe location if possible."
        )

        st.write(
            "• Contact appropriate local emergency services."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Medical Emergency")
        st.write("**Priority:** High")

    # Fire
    elif any(word in text for word in fire_words):

        st.error("🔴 HIGH PRIORITY — FIRE EMERGENCY")

        st.write("### 🛟 Recommended Actions")

        st.write(
            "• Move away from the fire and smoke."
        )

        st.write(
            "• Do not re-enter the affected building."
        )

        st.write(
            "• Contact the appropriate emergency services."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Fire")
        st.write("**Priority:** High")

    # Earthquake
    elif any(word in text for word in earthquake_words):

        st.error("🔴 HIGH PRIORITY — EARTHQUAKE")

        st.write("### 🛟 Recommended Actions")

        st.write(
            "• Move away from damaged buildings and structures."
        )

        st.write(
            "• Watch for falling objects and damaged electrical lines."
        )

        st.write(
            "• Follow official instructions and seek emergency help if needed."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Earthquake")
        st.write("**Priority:** High")

    # Flood + serious damage
    elif (
        any(word in text for word in flood_words)
        and any(word in text for word in damage_words)
    ):

        st.error("🔴 HIGH PRIORITY — FLOOD + DAMAGE")

        st.write("### 🛟 Recommended Actions")

        st.write(
            "• Move to a safe or elevated location."
        )

        st.write(
            "• Avoid damaged buildings and unsafe structures."
        )

        st.write(
            "• Stay away from electrical equipment and damaged power lines."
        )

        st.write(
            "• Follow instructions from local authorities."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Flood + Infrastructure Damage")
        st.write("**Priority:** High")

    # Flood / waterlogging
    elif any(word in text for word in flood_words):

        st.warning("🟠 MEDIUM PRIORITY — FLOOD / WATERLOGGING")

        st.write("### 🛟 Recommended Actions")

        st.write(
            "• Move to a safe location if water is rising."
        )

        st.write(
            "• Avoid walking or driving through moving floodwater."
        )

        st.write(
            "• Stay away from electrical equipment and damaged power lines."
        )

        st.write(
            "• Follow local authority instructions."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Flood / Waterlogging")
        st.write("**Priority:** Medium")

    # Road blockage
    elif any(word in text for word in road_words):

        st.warning("🟠 MEDIUM PRIORITY — ROAD BLOCKAGE")

        st.write("### 🛟 Recommended Actions")

        st.write(
            "• Avoid the blocked route."
        )

        st.write(
            "• Use an alternative safe route if available."
        )

        st.write(
            "• Report the obstruction to the appropriate local authority."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Road Blockage")
        st.write("**Priority:** Medium")

    # Unknown situation
    else:

        st.info("🟡 INFORMATION REQUIRED")

        st.write(
            "Please provide more details about the emergency, "
            "such as flooding, injury, fire, earthquake, "
            "road blockage, or a person in danger."
        )

st.caption(
    "Odisha Sahayak AI — Hackathon Prototype | "
    "AI predictions are decision-support estimates, "
    "not official warnings."
)
