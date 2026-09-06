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
# --------------------------------------------------
# FLOOD IMAGE ANALYSIS
# --------------------------------------------------

st.divider()

st.header("📷 AI Flood Image Analysis")

st.write(
    "Upload a road or area image for preliminary "
    "waterlogging assessment."
)

uploaded_file = st.file_uploader(
    "📤 Upload flood/road image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Area Image",
        use_container_width=True
    )

    if st.button("🔍 Analyze Image", key="image_analysis"):

        result = analyze_flood_image(image)
        
        flood_detected = result["flood_detected"]
        severity = result["severity"]
        brightness = result["brightness"]
        blue_signal = result["blue_signal"]

        if flood_detected:
    st.warning("🌊 POSSIBLE FLOOD / WATERLOGGING DETECTED")
else:
    st.success("🛣️ NO OBVIOUS FLOOD DETECTED")
       

        st.subheader("📊 Vision Assessment")

        if severity == "HIGH":

            st.error("🔴 HIGH WATERLOGGING INDICATION")

            explanation = (
                "The image shows visual characteristics that "
                "may be associated with significant water presence."
            )

            action = (
                "Avoid entering the affected area. "
                "Move to a safer location if necessary and "
                "verify the situation locally."
            )

        elif severity == "MEDIUM":

            st.warning("🟠 MEDIUM WATERLOGGING INDICATION")

            explanation = (
                "The image shows some visual characteristics "
                "that may indicate possible waterlogging."
            )

            action = (
                "Use caution around the area and avoid "
                "unknown-depth water."
            )

        else:

            st.success("🟢 LOW WATERLOGGING INDICATION")

            explanation = (
                "The image does not show strong visual signals "
                "associated with waterlogging in this prototype."
            )

            action = (
                "Continue to monitor the situation and "
                "follow local authority instructions."
            )

        st.write("### 🧠 AI Assessment")
        st.write(explanation)

        st.write("### 🔎 Visual Signals")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Brightness Signal",
                brightness
            )

        with col2:
            st.metric(
                "Blue-Channel Signal",
                blue_signal
            )

        st.write("### 🛟 Recommended Action")

        st.info(action)

        st.caption(
            "Prototype computer-vision assessment. "
            "This result is not an official flood warning "
            "and has not been validated for operational use."
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
