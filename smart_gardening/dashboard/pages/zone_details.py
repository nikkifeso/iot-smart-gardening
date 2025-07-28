import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from db.database import session, ZoneModel, PlantModel, SensorReading
from core.zone import Zone
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="Zone Details - Smart Gardening Dashboard",
    page_icon="🌱",
    layout="wide"
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
        .stMarkdown, .stText, .stButton, .stSelectbox, .stTextInput, .stNumberInput, .stTextArea, .stSlider {
            color: #2c3e50 !important;
        }
        
        /* Ensure form elements are light */
        .stForm {
            background-color: #D4fd0 !important;
        }
        
        /* Metric value styling - dark text */
        .stMetric [data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #2c3e50 !important;
        }
        
        /* Metric label styling - dark text */
        .stMetric [data-testid="metric-container"] div[data-testid="stMetricLabel"] {
            color: #2c3e50 !important;
        }
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        .title {
            font-size: 36px;
            color: #35B925;
            text-align: center;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .stButton > button {
            background-color: #35B925;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
            height: 50px;
            min-height: 50px;
            max-height: 50px;
        }
        .stButton > button:hover {
            background-color: #754D33 !important;
            color: white !important;
        }
        .zone-header {
            background-color: #35B925;
            color: #2c3e50;
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            text-align: center;
        }
        .metric-card {
            background-color: #D4fd0;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #88c030;
            margin: 10px 0;
            min-height: 200px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        .metric-card p {
            margin: 8px 0;
            line-height: 1.4;
        }
        .plant-card {
            background-color: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #35B925;
            margin: 10px 0;
        }
        .status-good {
            color: white !important;
            font-weight: bold;
        }
        .status-warning {
            color: white !important;
            font-weight: bold;
        }
        .status-critical {
            color: white !important;
            font-weight: bold;
        }
        /* Paragraph text styling */
        p {
            color: #2c3e50 !important;
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
    </style>
""", unsafe_allow_html=True)

# Get zone ID from URL parameters or session state
zone_id = st.query_params.get("zone_id", None)
if not zone_id:
    zone_id = st.session_state.get("selected_zone_id")

if not zone_id:
    st.error("No zone selected. Please go back to the dashboard and select a zone.")
    if st.button("← Back to Dashboard"):
        st.switch_page("../app.py")
    st.stop()

# Set URL parameter if not already set
if not st.query_params.get("zone_id"):
    st.query_params["zone_id"] = str(zone_id)

# Load zone data
try:
    zone = session.query(ZoneModel).filter(ZoneModel.id == int(zone_id)).first()
    if not zone:
        st.error("Zone not found.")
        if st.button("Back to Dashboard"):
            st.switch_page("app.py")
        st.stop()
except Exception as e:
    st.error(f"Error loading zone: {str(e)}")
    if st.button("Back to Dashboard"):
        st.switch_page("app.py")
    st.stop()

# Back button
col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("Back to Dashboard"):
        st.switch_page("app.py")

# Zone header
with col2:
    st.markdown(f"""
    <div class="zone-header">
        <h1>Zone {zone.id} - {zone.name}</h1>
        <p>Plant Type: {zone.plant_type}</p>
    </div>
    """, unsafe_allow_html=True)

# Zone details in columns
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Zone Configuration", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-card">
        <p><strong>Moisture Threshold:</strong> {zone.moisture_threshold}%</p>
        <p><strong>pH Range:</strong> {zone.ph_min} - {zone.ph_max}</p>
        <p><strong>Created:</strong> {zone.created_at.strftime('%B %d, %Y') if zone.created_at else 'Unknown'}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("### Current Status", unsafe_allow_html=True)
    # Simulated values
    current_moisture = 45  # This would come from actual sensors
    current_ph = 6.5
    pump_status = "ON" if current_moisture < zone.moisture_threshold else "OFF"
    
    moisture_status_class = "status-good" if current_moisture >= zone.moisture_threshold else "status-warning"
    
    st.markdown(f"""
    <div class="metric-card">
        <p><strong>Current Moisture:</strong> <span class="{moisture_status_class}">{current_moisture}%</span></p>
        <p><strong>Current pH:</strong> {current_ph}</p>
        <p><strong>Pump Status:</strong> <span class="status-{'good' if pump_status == 'ON' else 'warning'}">{pump_status}</span></p>
        <p><strong>Last Watered:</strong> {zone.last_watered.strftime('%Y-%m-%d %H:%M') if zone.last_watered is not None else 'Never'}</p>
    </div>
    """, unsafe_allow_html=True)

# Plants in this zone
st.markdown("### Plants in This Zone", unsafe_allow_html=True)

plants = session.query(PlantModel).filter(PlantModel.zone_id == zone.id).all()

if plants:
    for plant in plants:
        st.markdown(f"""
        <div class="metric-card">
            <h4>{plant.name}</h4>
            <p><strong>Type:</strong> {plant.plant_type}</p>
            <p><strong>Planted:</strong> {plant.planting_date.strftime('%B %d, %Y') if plant.planting_date else 'Unknown'}</p>
            {f'<p><strong>Notes:</strong> {plant.notes}</p>' if plant.notes else ''}
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="metric-card">
        <p><em>No plants added to this zone yet.</em></p>
    </div>
    """, unsafe_allow_html=True)

# Recent sensor readings
st.markdown("### Recent Sensor Readings", unsafe_allow_html=True)

# Get recent readings (last 7 days)
recent_readings = session.query(SensorReading).filter(
    SensorReading.zone_id == zone.id,
    SensorReading.timestamp >= datetime.now() - timedelta(days=7)
).order_by(SensorReading.timestamp.desc()).limit(10).all()

if recent_readings:
    # Prepare data for the chart
    chart_data = []
    for reading in recent_readings:
        chart_data.append({
            "Date": reading.timestamp.strftime('%Y-%m-%d %H:%M'),
            "Moisture (%)": reading.moisture,
            "pH": reading.ph
        })
    
    # Create line chart
    import pandas as pd
    
    # Convert to DataFrame for easier charting
    df = pd.DataFrame(chart_data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')  # Sort by date for proper line chart
    
    # Create tabs for chart and table view
    tab1, tab2 = st.tabs(["📊 Chart View", "📋 Table View"])
    
    with tab1:
        # Line chart for moisture levels
        st.markdown("#### Moisture Levels Over Time")
        st.line_chart(df.set_index('Date')['Moisture (%)'])
        
        # Line chart for pH levels
        st.markdown("#### pH Levels Over Time")
        st.line_chart(df.set_index('Date')['pH'])
        
        # Combined chart
        st.markdown("#### Combined Sensor Readings")
        combined_chart = df.set_index('Date')[['Moisture (%)', 'pH']]
        st.line_chart(combined_chart)
    
    with tab2:
        # Display data in table format
        st.dataframe(df, use_container_width=True)
else:
    st.markdown("""
    <div class="metric-card">
        <p><em>No recent sensor readings available.</em></p>
    </div>
    """, unsafe_allow_html=True)

# Action buttons
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Add Plant to This Zone"):
        st.session_state.selected_zone_id = zone.id
        st.switch_page("pages/add_plant.py") 