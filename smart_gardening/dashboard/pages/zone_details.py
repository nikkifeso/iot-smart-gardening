import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from db.database import session, ZoneModel, PlantModel, SensorReading
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Zone Details - Smart Gardening Dashboard",
    page_icon="🌱",
    layout="wide"
)

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
        
        /* Metric value styling - dark text */
        .stMetric [data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #2c3e50 !important;
        }
        
        /* Metric label styling - dark text */
        .stMetric [data-testid="metric-container"] div[data-testid="stMetricLabel"] {
            color: #2c3e50 !important;
        }
        .title {
            font-size: 36px;
            color: #35B925;
            text-align: center;
            font-weight: bold;
            margin-bottom: 30px;
        }
        .stButton > button {
            background-color: #e8f5e8;
            color: #2c3e50 !important;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            height: 50px;
            min-height: 50px;
            max-height: 50px;
        }
        .stButton > button:hover {
            background-color: #d4e8d4 !important;
            color: #2c3e50 !important;
        }
        .stButton > button:focus {
            color: #2c3e50 !important;
        }

        /* Target remove buttons by their key attribute */
        div[data-testid="stButton"] button[data-testid*="remove_"] {
            background-color: #ffebee !important;
            color: #c62828 !important;
            border: 1px solid #c62828 !important;
            font-weight: bold !important;
            width: 50% !important;
            margin-top: 16px !important;
        }
        
        div[data-testid="stButton"] button[data-testid*="remove_"]:hover {
            background-color: #ffcdd2 !important;
            color: #c62828 !important;
            border: 1px solid #c62828 !important;
        }
        

        .zone-header {
            background-color: #e8f5e8;
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

        /* Paragraph text styling */
        p {
            color: #2c3e50 !important;
        }
        
        /* Ensure span elements have dark text */
        span {
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
    </style>
""", unsafe_allow_html=True)

zone_id = st.query_params.get("zone_id", None)
if not zone_id:
    zone_id = st.session_state.get("selected_zone_id")

if not zone_id:
    st.error("No zone selected. Please go back to the dashboard and select a zone.")
    if st.button("← Back to Dashboard"):
        st.switch_page("app.py")
    st.stop()

if not st.query_params.get("zone_id"):
    st.query_params["zone_id"] = str(zone_id)

try:
    zone = session.query(ZoneModel).filter(ZoneModel.id == int(zone_id)).first()
    if not zone:
        st.error("Zone not found.")
        if st.button("← Back to Dashboard"):
            st.switch_page("app.py")
        st.stop()
except Exception as e:
    st.error(f"Error loading zone: {str(e)}")
    if st.button("← Back to Dashboard"):
        st.switch_page("app.py")
    st.stop()

col1, col2, col3 = st.columns([1, 3, 1])
with col1:
    if st.button("← Back to Dashboard"):
        st.switch_page("app.py")

with col2:
    st.markdown(f"""
    <div class="zone-header">
        <h1>Zone {zone.id} - {zone.name}</h1>
        <p>Plant Type: {zone.plant_type}</p>
    </div>
    """, unsafe_allow_html=True)

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
    
    latest_reading = session.query(SensorReading).filter(
        SensorReading.zone_id == zone.id
    ).order_by(SensorReading.timestamp.desc()).first()
    
    if latest_reading:
        current_moisture = latest_reading.moisture
        current_ph = latest_reading.ph
    else:
        current_moisture = 45
        current_ph = 6.5
    
    pump_status = "ON" if current_moisture < zone.moisture_threshold else "OFF"
    
    moisture_status_class = "status-good" if current_moisture >= zone.moisture_threshold else "status-warning"
    
    if zone.ph_min <= current_ph <= zone.ph_max:
        ph_status_class = "status-good"
        ph_status_text = "🟢 Good"
    elif current_ph < zone.ph_min:
        ph_status_class = "status-warning"
        ph_status_text = "🔴 Too Acidic"
    else:
        ph_status_class = "status-warning"
        ph_status_text = "🔵 Too Alkaline"
    
    
    st.markdown(f"""
    <div class="metric-card">
        <p><strong>Current Moisture:</strong> <span>{current_moisture:.1f}%</span></p>
        <p><strong>Current pH:</strong> {current_ph:.1f}</p>
        <p><strong>Pump Status:</strong> <span>{pump_status}</span></p>
        <p><strong>Last Watered:</strong> {zone.last_watered.strftime('%Y-%m-%d %H:%M') if zone.last_watered is not None else 'Never'}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Plants in This Zone", unsafe_allow_html=True)


plants = session.query(PlantModel).filter(PlantModel.zone_id == zone.id).all()

if plants:
    for plant in plants:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>{plant.name}</h4>
                <p><strong>Type:</strong> {plant.plant_type}</p>
                <p><strong>Planted:</strong> {plant.planting_date.strftime('%B %d, %Y') if plant.planting_date else 'Unknown'}</p>
                {f'<p><strong>Notes:</strong> {plant.notes}</p>' if plant.notes else ''}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("❌", key=f"remove_{plant.id}", type="secondary"):
                st.session_state.remove_zone_id = zone.id
                st.session_state.remove_plant_id = plant.id
                st.switch_page("pages/remove_plant.py")

else:
    st.markdown("""
    <div class="metric-card">
        <p><em>No plants added to this zone yet.</em></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Recent Sensor Readings", unsafe_allow_html=True)

recent_readings = session.query(SensorReading).filter(
    SensorReading.zone_id == zone.id,
    SensorReading.timestamp >= datetime.now() - timedelta(days=7)
).order_by(SensorReading.timestamp.desc()).limit(10).all()

if recent_readings:
    chart_data = []
    for reading in recent_readings:
        chart_data.append({
            "Date": reading.timestamp.strftime('%Y-%m-%d %H:%M'),
            "Moisture (%)": reading.moisture,
            "pH": reading.ph
        })
    
    import pandas as pd
    
    df = pd.DataFrame(chart_data)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    tab1, tab2 = st.tabs(["📊 Chart View", "📋 Table View"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Moisture Levels Over Time")
            st.line_chart(df.set_index('Date')['Moisture (%)'])
        
        with col2:
            st.markdown("#### pH Levels Over Time")
            st.line_chart(df.set_index('Date')['pH'])
    
    
    with tab2:
        st.dataframe(df, use_container_width=True)
else:
    st.markdown("""
    <div class="metric-card">
        <p><em>No recent sensor readings available.</em></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("Add Plant to This Zone"):
        st.session_state.selected_zone_id = zone.id
        st.switch_page("pages/add_plant.py") 