import streamlit as st
import pickle
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Odisha Sahayak AI",
    page_icon="🌊",
    layout="wide"
)

# Load trained ML model
MODEL_PATH = Path("data/models/flood_risk_model.pkl")

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

st.title("🌊 Odisha Sahayak AI")
st.subheader("Predict. Detect. Respond.")

st.write(
    "AI-powered disaster assistance platform designed "
    "to support flood and waterlogging response in Odisha."
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("AI Model", "Random Forest")

with col2:
    st.metric("Reports Today", "24")

with col3:
    st.metric("Areas Monitored", "12")

st.divider()

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

    if prediction == 1:
        st.error("🔴 HIGH FLOOD RISK")
    else:
        st.success("🟢 LOW FLOOD RISK")

    st.metric(
        "AI Flood Probability",
        f"{probability * 100:.1f}%"
    )

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

        st.info("Analyzing image...")

        # Prototype image-analysis stage
        # A trained computer-vision model will be connected here.
        
        st.warning(
            "⚠️ Prototype analysis: "
            "A trained flood-image dataset/model is required "
            "for reliable waterlogging detection."
        )

        st.write("📌 Suggested next action:")
        st.write(
            "Collect the location and report the image "
            "to the disaster-response system."
        )

st.divider()

st.header("🤖 Odia Emergency Assistant")

question = st.text_input(
    "Ask your emergency question:"
)

if question:
    st.info(
        "ଦୟାକରି ସୁରକ୍ଷିତ ସ୍ଥାନକୁ ଯାଆନ୍ତୁ ଏବଂ "
        "ବନ୍ୟା ପାଣିରେ ପ୍ରବେଶ କରନ୍ତୁ ନାହିଁ।"
    )

    st.write(
        "For immediate emergencies, contact appropriate "
        "local emergency services."
    )
