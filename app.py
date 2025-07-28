import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from simulator.simulator import SensorSimulator, get_default_zones
from actuators.pump import control_pump
from config import ZONES, MOISTURE_THRESHOLDS
from core.zone import Zone

from db.database import init_db, session, SensorReading, ZoneModel, PlantModel
init_db()

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
            color: #35B925;
            text-align: center;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .zone-header {
            background-color: #35B925;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 18px;
        }
        .zone-name {
            font-size: 20px;
            color: #754D33;
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
        }
        .button-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        .stButton > button {
            background-color: #35B925;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #88c030;
        }
        .metric-container {
            background-color: #D4fd0;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            border-left: 4px solid #35B925;
        }
        .plant-list {
            background-color: #D4fd0;
            padding: 10px;
            border-radius: 8px;
            margin: 10px 0;
            border: 1px solid #88c030;
        }
        .status-good {
            color: #35B925;
            font-weight: bold;
        }
        .status-warning {
            color: #754D33;
            font-weight: bold;
        }
        /* Metric styling */
        .stMetric {
            background-color: #D4fd0;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            border: 1px solid #88c030;
        }
        /* Form styling */
        .stForm {
            background-color: #D4fd0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #88c030;
        }
        /* Horizontal scroll container */
        .scroll-container {
            overflow-x: auto;
            white-space: nowrap;
            padding: 10px 0;
        }
        .zone-column {
            display: inline-block;
            min-width: 300px;
            max-width: 350px;
            margin-right: 20px;
            vertical-align: top;
        }
        /* Custom scrollbar */
        .scroll-container::-webkit-scrollbar {
            height: 8px;
        }
        .scroll-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        .scroll-container::-webkit-scrollbar-thumb {
            background: #35B925;
            border-radius: 4px;
        }
        .scroll-container::-webkit-scrollbar-thumb:hover {
            background: #88c030;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🌿 Smart Gardening Dashboard</div>', unsafe_allow_html=True)

# Load zones from database
def load_zones_from_db():
    """Load zones from database and convert to Zone objects"""
    db_zones = session.query(ZoneModel).all()
    zones = []
    
    for db_zone in db_zones:
        zone = Zone.from_db_model(db_zone)
        # Load plants for this zone
        plants = session.query(PlantModel).filter(PlantModel.zone_id == db_zone.id).all()
        zone.plants = [
            {
                'name': plant.name,
                'type': plant.plant_type,
                'planting_date': plant.planting_date.strftime('%Y-%m-%d') if plant.planting_date else None,
                'notes': plant.notes
            }
            for plant in plants
        ]
        zones.append(zone)
    
    return zones

# Initialize zones from database or default
if "zones" not in st.session_state:
    db_zones = load_zones_from_db()
    if not db_zones:
        # If no zones in DB, create default zones
        default_zones = get_default_zones()
        for zone in default_zones:
            # Save default zones to database
            db_zone = ZoneModel(**zone.to_dict())
            session.add(db_zone)
            session.commit()
            zone.id = db_zone.id  # Update with database ID
        db_zones = load_zones_from_db()
    st.session_state.zones = db_zones

zones = st.session_state.zones
simulator = SensorSimulator(zones)
simulator.simulate()

# Zone summary section
st.markdown("### 📍 Garden Zones Overview")
zone_summary_cols = st.columns(len(zones))
for i, zone in enumerate(zones):
    with zone_summary_cols[i]:
        moisture_status = "🟢 Good" if zone.moisture >= MOISTURE_THRESHOLDS.get(zone.id, 30) else "🔴 Low"
        st.markdown(f"""
        <div class='metric-container'>
        <strong>Zone {zone.id} - {zone.name}</strong><br>
        Plant Type: {zone.plant_type}<br>
        Moisture: {moisture_status} ({zone.moisture}%)
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")  # Separator line

# Action buttons row
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("➕ Add New Zone", key="add_zone_btn"):
        st.switch_page("pages/1_Add_Zone.py")

with col2:
    if st.button("🌱 Add Plant to Zone", key="add_plant_btn"):
        st.switch_page("pages/2_Add_Plant.py")

# Create horizontal scrollable container for zones
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

# Display each zone in its own column
for zone in zones:
    # Simulated values
    moisture = zone.moisture
    ph = zone.ph
    threshold = MOISTURE_THRESHOLDS.get(zone.id, 30)  # Default threshold if not found
    pump_status = zone.pump_status

    # Control pump
    if moisture < threshold:
        control_pump(zone.id, True)
        pump_status = "ON"
    else:
        control_pump(zone.id, False)
        pump_status = "OFF"

    pump_color = "green" if pump_status == "ON" else "red"

    # Render zone info in its own column
    st.markdown(f'<div class="zone-column">', unsafe_allow_html=True)
    
    # Zone header with ID and name
    st.markdown(f"<div class='zone-header'>Zone {zone.id}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='zone-name'>{zone.name}</div>", unsafe_allow_html=True)

    # Zone details
    st.markdown(f"<div class='metric-container'><strong>Plant Type:</strong> {zone.plant_type}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-container'><strong>Moisture Threshold:</strong> {threshold}%</div>", unsafe_allow_html=True)
    
    st.metric(label="Moisture Level (%)", value=moisture)
    st.progress(min(int(moisture), 100))

    st.metric(label="pH Level", value=ph)

    # Pump status with color coding
    pump_status_class = "status-good" if pump_status == "ON" else "status-warning"
    st.markdown(f"<div class='metric-container'><strong>Pump Status:</strong> <span class='{pump_status_class}'>{pump_status}</span></div>", unsafe_allow_html=True)
    
    # Display plants in this zone
    if hasattr(zone, 'plants') and zone.plants:
        st.markdown("<div class='plant-list'><strong>Plants:</strong>", unsafe_allow_html=True)
        for plant in zone.plants:
            st.markdown(f"• {plant['name']} ({plant['type']})")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='plant-list'><em>No plants added yet</em></div>", unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Save sensor readings to database
for zone in zones:
    reading = SensorReading(
        zone_id=zone.id,
        moisture=zone.moisture,
        ph=zone.ph
    )
    session.add(reading)
    session.commit()