import streamlit as st

st.set_page_config(
    page_title="Odisha Sahayak AI",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 Odisha Sahayak AI")
st.subheader("Predict. Detect. Respond.")

st.write(
    "AI-powered disaster assistance platform designed "
    "to support flood and waterlogging response in Odisha."
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Risk Level", "MEDIUM")
    
with col2:
    st.metric("Reports Today", "24")
    
with col3:
    st.metric("Areas Monitored", "12")

st.divider()

st.header("📊 Flood Risk Assessment")

rainfall = st.slider(
    "Rainfall (mm)",
    min_value=0,
    max_value=500,
    value=100
)

if rainfall < 100:
    risk = "🟢 LOW RISK"
elif rainfall < 200:
    risk = "🟡 MEDIUM RISK"
else:
    risk = "🔴 HIGH RISK"

st.subheader(f"AI Risk Assessment: {risk}")

st.divider()

st.header("📷 Flood Image Analysis")

uploaded_file = st.file_uploader(
    "Upload an image of a road/area",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    st.image(
        uploaded_file,
        caption="Uploaded image",
        use_container_width=True
    )

    st.info(
        "Image received. Computer Vision analysis "
        "will be integrated in the next module."
    )

st.divider()

st.header("🤖 Odia Emergency Assistant")

user_question = st.text_input(
    "Ask your emergency question:"
)

if user_question:
    st.write("ପରିସ୍ଥିତି ଅନୁଯାୟୀ ସୁରକ୍ଷିତ ସ୍ଥାନକୁ ଯାଆନ୍ତୁ।")
    st.write(
        "For emergencies, contact the appropriate local emergency services."
    )
