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
    "to support flood and waterlogging response in Odisha."
)

st.divider()

# -----------------------------
# Dashboard metrics
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
    rainfall = st.slider(
        "Rainfall (mm)",
        0, 500, 100
    )

with col2:
    humidity = st.slider(
        "Humidity (%)",
        0, 100, 70
    )

with col3:
    water_level = st.slider(
        "Water Level",
        0, 10, 3
    )

if st.button("🔍 Analyze Risk"):

    input_data = pd.DataFrame({
        "rainfall": [rainfall],
        "humidity": [humidity],
        "water_level": [water_level]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.divider()
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
        "Prototype model: prediction should be validated "
        "with real local observations before operational use."
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
            "⚠️ Computer-vision model is currently in prototype stage."
        )

        st.write("### 📋 Preliminary Assessment")

        st.write(
            "The image has been received successfully. "
            "A trained flood-image model will classify "
            "waterlogging severity in the next stage."
        )

        st.info(
            "Recommended action: verify the location and "
            "avoid entering moving or unknown-depth floodwater."
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

    # Flood / waterlogging detection
    flood_words = [
        "pani", "water", "flood", "banya",
        "ban", "waterlogging", "duba",
        "flooded"
    ]

    medical_words = [
        "injury", "injured", "medical",
        "ambulance", "bleeding"
    ]

    if any(word in text for word in medical_words):

        st.error("🔴 HIGH PRIORITY — MEDICAL EMERGENCY")

        st.write("### 🛟 Recommended Actions")
        st.write("• Move to a safe location if possible.")
        st.write("• Seek immediate medical assistance.")
        st.write("• Contact appropriate local emergency services.")

    elif any(word in text for word in flood_words):

        st.error("🔴 HIGH PRIORITY — FLOOD / WATERLOGGING")

        st.write("### 🛟 Recommended Actions")

        st.write(
            "• Move to a safe or elevated location."
        )

        st.write(
            "• Avoid walking or driving through moving floodwater."
        )

        st.write(
            "• Stay away from electrical equipment "
            "and damaged power lines."
        )

        st.write(
            "• Follow instructions from local authorities."
        )

        st.write("### 📝 Situation Classification")
        st.write("**Type:** Flood / Waterlogging")
        st.write("**Priority:** High")

    else:

        st.info("🟡 MEDIUM PRIORITY — INFORMATION REQUIRED")

        st.write(
            "Please provide more details such as your "
            "situation, water level, location type, or emergency."
        )

st.caption(
    "Odisha Sahayak AI — Hackathon Prototype | "
    "AI predictions are decision-support estimates, not official warnings."
)
