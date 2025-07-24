import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from simulator.simulator import SensorSimulator, get_default_zones
from actuators.pump import control_pump
from config import ZONES, MOISTURE_THRESHOLDS

# Page configuration
st.set_page_config(
    page_title="Smart Gardening Dashboard", 
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .title {
            font-size: 42px;
            color: #228B22;
            text-align: center;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .zone-box {
            background-color: #f0fff0;
            padding: 20px;
            border-radius: 15px;
            margin: 10px;
            box-shadow: 2px 2px 10px rgba(0, 128, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🌿 Smart Gardening Dashboard</div>', unsafe_allow_html=True)

# Initialize zones and simulator
zones = get_default_zones()
simulator = SensorSimulator(zones)
simulator.simulate()

# Create one column per zone
cols = st.columns(len(zones))  # e.g., 3 zones = st.columns(3)

# Display each zone in its column
for col, zone in zip(cols, zones):
    # Simulated values
    moisture = zone.moisture
    ph = zone.ph
    threshold = MOISTURE_THRESHOLDS[zone.id]
    pump_status = zone.pump_status

    # Control pump
    if moisture < threshold:
        control_pump(zone.id, True)
        pump_status = "ON"
    else:
        control_pump(zone.id, False)
        pump_status = "OFF"

    pump_color = "green" if pump_status == "ON" else "red"

    # Render zone info in its column
    with col:
        st.markdown(f"<div class='zone-box'><h3>Zone {zone.id} – {zone.name}</h3>", unsafe_allow_html=True)

        st.metric(label="Moisture Level (%)", value=moisture)
        st.progress(min(int(moisture), 100))

        st.metric(label="pH Level", value=ph)

        st.markdown(f"**Pump Status:** <span style='color:{pump_color}'>{pump_status}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with st.expander("➕ Add New Zone"):
    with st.form("new_zone_form"):
        new_id = st.text_input("Zone ID")
        name = st.text_input("Zone Name")
        plant_type = st.selectbox("Plant Type", ["Tomato", "Lettuce", "Cucumber", "Pepper"])
        moisture_threshold = st.number_input("Moisture Threshold (%)", min_value=0, max_value=100, value=30)
        ph_min = st.number_input("pH Range Min", min_value=0.0, max_value=14.0, value=6.0)
        ph_max = st.number_input("pH Range Max", min_value=0.0, max_value=14.0, value=7.5)

        submitted = st.form_submit_button("Create Zone")

        if submitted:
            from core.zone import Zone  # Import if needed
            new_zone = Zone(
                id=new_id,
                name=name,
                plant_type=plant_type,
                moisture_threshold=moisture_threshold,
                ph_range=(ph_min, ph_max)
            )
            zones.append(new_zone)
            MOISTURE_THRESHOLDS[new_id] = moisture_threshold
            st.success(f"Zone '{name}' created successfully!")

    if "zones" not in st.session_state:
        st.session_state.zones = get_default_zones()

    zones = st.session_state.zones
    simulator = SensorSimulator(zones)
    simulator.simulate()