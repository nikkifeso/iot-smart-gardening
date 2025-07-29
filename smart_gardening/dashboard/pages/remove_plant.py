import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from db.database import session, ZoneModel, remove_plant, get_plant_by_id

st.set_page_config(
    page_title="Remove Plant - Smart Gardening Dashboard",
    page_icon="🌱",
    layout="wide"
)
zone_id = st.session_state.get("remove_zone_id", None)
plant_id = st.session_state.get("remove_plant_id", None)

if not zone_id or not plant_id:
    st.error("No plant selected for removal.")
    st.stop()

zone = session.query(ZoneModel).filter(ZoneModel.id == int(zone_id)).first()
if not zone:
    st.error("Zone not found.")
    st.stop()

plant = get_plant_by_id(int(plant_id))
if not plant:
    st.error("Plant not found.")
    st.stop()
    
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
        
        /* Ensure span elements have dark text */
        span {
            color: #2c3e50 !important;
        }
        
        /* Ensure form elements are light */
        .stForm {
            background-color: #D4fd0 !important;
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
        .stButton > button:active {
            color: #2c3e50 !important;
        }
        .stButton > button:focus {
            color: #2c3e50 !important;
        }

        .stForm {
            background-color: #D4fd0;
            padding: 15px;
            border-radius: 10px;
            border: 2px solid #88c030;
        }
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #c3e6cb;
            margin: 10px 0;
        }
        .error-message {
            background-color: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #f5c6cb;
            margin: 10px 0;
        }
        .warning-message {
            background-color: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ffeaa7;
            margin: 10px 0;
        }
        .plant-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }

        
        /* Primary remove button styling - light red background */
        .stButton > button[type="primary"]:has-text("Remove Plant") {
            background-color: #ffebee !important;
            color: #c62828 !important;
            border: 1px solid #c62828 !important;
            font-weight: bold !important;
        }
        
        .stButton > button[type="primary"]:has-text("Remove Plant"):hover {
            background-color: #ffcdd2 !important;
            color: #c62828 !important;
            border: 1px solid #c62828 !important;
        }
        
        .stButton > button[type="primary"]:has-text("Remove Plant"):active {
            background-color: #ffcdd2 !important;
            color: #c62828 !important;
        }
        
        .stButton > button[type="primary"]:has-text("Remove Plant"):focus {
            background-color: #ffebee !important;
            color: #c62828 !important;
            border: 1px solid #c62828 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="title"><i class="fas fa-trash"></i> Remove Plant</h1>', unsafe_allow_html=True)

if plant.zone_id != int(zone_id):
    st.error("Plant does not belong to this zone.")
    if st.button("← Back to Zone Details"):
        st.query_params["zone_id"] = str(zone_id)
        st.switch_page("pages/zone_details.py")
    st.stop()

st.markdown("### Plant Information", unsafe_allow_html=True)
st.markdown(f"""
<div class="plant-card">
    <h4>{plant.name}</h4>
    <p><strong>Type:</strong> {plant.plant_type}</p>
    <p><strong>Zone:</strong> {zone.name} (Zone {zone.id})</p>
    <p><strong>Planted:</strong> {plant.planting_date.strftime('%B %d, %Y') if plant.planting_date else 'Unknown'}</p>
    {f'<p><strong>Notes:</strong> {plant.notes}</p>' if plant.notes else ''}
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="warning-message">
    <strong><i class="fas fa-exclamation-triangle"></i> Warning:</strong> 
    This action cannot be undone. The plant will be permanently removed from the database.
</div>
""", unsafe_allow_html=True)

st.markdown("### Confirmation", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("← Cancel", key="cancel"):
        st.query_params["zone_id"] = str(zone_id)
        st.switch_page("pages/zone_details.py")

with col2:
    pass

with col3:
    if st.button("❌ Remove Plant", key="remove", type="primary"):
        if remove_plant(plant.id):
            st.markdown("""
            <div class="success-message">
                <strong><i class="fas fa-check-circle"></i> Success!</strong> 
                Plant has been removed successfully.
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("Redirecting to zone details...")
            st.query_params["zone_id"] = str(zone_id)
            st.switch_page("pages/zone_details.py")
        else:
            st.markdown("""
            <div class="error-message">
                <strong><i class="fas fa-times-circle"></i> Error!</strong> 
                Failed to remove plant. Please try again.
            </div>
            """, unsafe_allow_html=True)
