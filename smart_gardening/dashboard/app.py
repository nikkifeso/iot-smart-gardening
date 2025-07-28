# -*- coding: utf-8 -*-
"""
# Home

Smart Gardening Dashboard - Monitor and manage your garden zones
"""

import sys
import os
import datetime
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
    page_title="Home - Smart Gardening Dashboard", 
    page_icon="🌱", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* Force light mode */
        :root {
            --background-color: #ffffff !important;
            --text-color: #2c3e50 !important;
        }
        
        /* Override Streamlit dark mode */
        .stApp {
            background-color: #ffffff !important;
        }
        
        /* Force light background */
        .main .block-container {
            background-color: #ffffff !important;
        }
        
        /* Override any dark mode text */
        .stMarkdown, .stText, .stSelectbox, .stTextInput, .stNumberInput, .stTextArea, .stSlider {
            color: #2c3e50 !important;
        }
        
        /* Ensure form elements are light */
        .stForm {
            background-color: #D4fd0 !important;
        }
        
        /* Remove header links */
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
            text-decoration: none !important;
            color: inherit !important;
            pointer-events: none !important;
        }
        
        /* Remove header link hover effects */
        h1 a:hover, h2 a:hover, h3 a:hover, h4 a:hover, h5 a:hover, h6 a:hover {
            text-decoration: none !important;
            color: inherit !important;
        }
        
        /* Remove link icon on hover */
        h1 a::after, h2 a::after, h3 a::after, h4 a::after, h5 a::after, h6 a::after {
            content: none !important;
        }
        
        /* Hide any link icons */
        .stMarkdown h1 a::after, .stMarkdown h2 a::after, .stMarkdown h3 a::after, 
        .stMarkdown h4 a::after, .stMarkdown h5 a::after, .stMarkdown h6 a::after {
            display: none !important;
        }
        
        /* Metric value styling - dark text */
        .stMetric [data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #2c3e50 !important;
        }
        
        /* Metric label styling - dark text */
        .stMetric [data-testid="metric-container"] div[data-testid="stMetricLabel"] {
            color: #2c3e50 !important;
        }
        
        /* Additional metric styling for better coverage */
        .stMetric div[data-testid="stMetricValue"] {
            color: #2c3e50 !important;
        }
        
        .stMetric div[data-testid="stMetricLabel"] {
            color: #2c3e50 !important;
        }
        
        /* Target metric text directly */
        .stMetric {
            color: #2c3e50 !important;
        }
        
        /* Ensure all text in metric containers is dark */
        [data-testid="metric-container"] {
            color: #2c3e50 !important;
        }
        
        /* Hide pages navigation */
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        
        /* Hide pages navigation container */
        [data-testid="stSidebarNavItems"] {
            display: none !important;
        }
        
        /* Hide any page navigation elements */
        .css-1d391kg {
            display: none !important;
        }
        
        /* Hide sidebar navigation */
        .css-1lcbmhc {
            display: none !important;
        }
        
        /* Hide navigation toggle button */
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        
        /* Hide sidebar toggle */
        .css-1rs6os {
            display: none !important;
        }
        
        /* Hide any sidebar controls */
        [data-testid="stSidebar"] {
            display: none !important;
        }
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
            color: #754D33 !important;
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
            color: white !important;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            height: 50px;
            min-height: 50px;
            max-height: 50px;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #754D33 !important;
            color: white !important;
        }
        .stButton > button:active {
            color: white !important;
        }
        .stButton > button:focus {
            color: white !important;
        }
        /* Override any #2c3e50 color on buttons to white */
        .stButton > button[style*="#2c3e50"] {
            color: white !important;
        }
        .stButton > button:hover[style*="#2c3e50"] {
            color: white !important;
        }
        .stButton > button:active[style*="#2c3e50"] {
            color: white !important;
        }
        .stButton > button:focus[style*="#2c3e50"] {
            color: white !important;
        }
        /* Paragraph text styling */
        p {
            color: #2c3e50 !important;
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
            color: white !important;
            font-weight: bold;
        }
        .status-warning {
            color: white !important;
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
        /* Hide the sidebar navigation for multipage apps */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        /* Hide sidebar toggle button */
        button[title="Open sidebar"] {
            display: none !important;
        }
        /* Hide any other navigation toggles */
        [data-testid="stSidebarToggle"] {
            display: none !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title and Action buttons row
title_col, _, btn_col1, btn_col2 = st.columns([3, 2, 1, 1])

with title_col:
    st.markdown('<div class="title"><i class="fas fa-seedling";"></i>Smart Gardening Dashboard</div>', unsafe_allow_html=True)

with btn_col1:
    if st.button("Add New Zone", key="add_zone_btn"):
        st.switch_page("pages/add_zone.py")

with btn_col2:
    if st.button("Add Plant to Zone", key="add_plant_btn"):
        st.switch_page("pages/add_plant.py")

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
st.markdown("### Garden Zones Overview", unsafe_allow_html=True)
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



# Create horizontal scrollable container for zones
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

# Create one column per zone
cols = st.columns(len(zones))  # e.g., 3 zones = st.columns(3)

# Display each zone in its column
for col, zone in zip(cols, zones):
    # Simulated values
    moisture = zone.moisture
    ph = zone.ph
    threshold = MOISTURE_THRESHOLDS.get(zone.id, 30)  # Default threshold if not found
    pump_status = zone.pump_status

    # Control pump
    if moisture < threshold:
        control_pump(zone.id, True)
        pump_status = "ON"
        # Update last watered time when pump is activated
        zone.last_watered = datetime.datetime.now()
        # Update database
        db_zone = session.query(ZoneModel).filter(ZoneModel.id == zone.id).first()
        if db_zone:
            db_zone.last_watered = zone.last_watered
            session.commit()
    else:
        control_pump(zone.id, False)
        pump_status = "OFF"

    pump_color = "green" if pump_status == "ON" else "red"

    # Render zone info in its column
    with col:
          # Zone name
        # st.markdown(f"<div class='zone-name'>{zone.name}</div>", unsafe_allow_html=True)

       
        # Zone header with ID and name
        if st.button(f"Zone {zone.name}", key=f"zone_{zone.id}_header_btn"):
            st.session_state.selected_zone_id = zone.id
            st.switch_page("pages/zone_details.py")
        
      
        st.metric(label="Moisture Level (%)", value=moisture)

        st.metric(label="pH Level", value=ph)

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