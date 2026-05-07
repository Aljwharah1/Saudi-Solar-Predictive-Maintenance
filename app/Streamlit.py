import streamlit as st
import requests

st.set_page_config(page_title="Sudair Solar Monitor", layout="wide")

st.title("☀️ Sudair Solar Plant: AI Maintenance Monitor")
st.markdown("---")

# 1. Sidebar for User Input
st.sidebar.header("Sensor Real-time Data")
ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 10.0, 60.0, 35.0)
module_temp = st.sidebar.slider("Module Temperature (°C)", 10.0, 80.0, 50.0)
irradiation = st.sidebar.slider("Irradiation (W/m²)", 0.0, 1.2, 0.8)
dust_level = st.sidebar.slider("Dust Level (Normalized)", 0.0, 1.0, 0.2)

# 2. Prepare the data for the API
input_data = {
    "ambient_temp": ambient_temp,
    "module_temp": module_temp,
    "irradiation": irradiation,
    "dust_level": dust_level
}

# 3. Button to trigger prediction
if st.button("Analyze Panel Status"):
    # Connect to our FastAPI
    response = requests.post("http://0.0.0.0:8000/predict", json=input_data)
    
    if response.status_code == 200:
        result = response.json()
        
        # Display Results
        st.subheader("Result:")
        if result["need_maintenance"] == 1:
            st.error(f"🚨 {result['system_status']}")
        else:
            st.success(f"✅ {result['system_status']}")
            
        st.metric(label="Confidence Level", value=result["confidence"])
    else:
        st.error("Could not connect to the AI Engine.")
