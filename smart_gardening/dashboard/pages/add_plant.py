import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from db.database import session, ZoneModel, PlantModel
from datetime import date

# Page configuration
st.set_page_config(
    page_title="Add Plant - Smart Gardening Dashboard",
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
        .stMarkdown, .stText, .stSelectbox, .stTextInput, .stNumberInput, .stTextArea, .stSlider {
            color: #2c3e50 !important;
        }
        
        /* Ensure form elements are light */
        .stForm {
            background-color: #D4fd0 !important;
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
        /* Override any #2c3e50 color on buttons to dark */
        .stButton > button[style*="#2c3e50"] {
            color: #2c3e50 !important;
        }
        .stButton > button:hover[style*="#2c3e50"] {
            color: #2c3e50 !important;
        }
        .stButton > button:active[style*="#2c3e50"] {
            color: #2c3e50 !important;
        }
        .stButton > button:focus[style*="#2c3e50"] {
            color: #2c3e50 !important;
        }
        .stForm {
            
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
        .zone-info {
            background-color: #e8f5e8;
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #35B925;
            margin: 10px 0;
            color: #333333;
        }
        /* Input field text color - white */
        .stTextInput > div > div > input {
            color: white !important;
        }
        .stNumberInput > div > div > input {
            color: white !important;
        }
        .stTextArea > div > div > textarea {
            color: white !important;
        }
        .stSelectbox > div > div > div {
            color: white !important;
        }
        .stSlider > div > div > div > div {
            color: white !important;
        }
        /* Form labels */
        .stForm label {
            color: #333333 !important;
            font-weight: 600;
        }
        /* Section headers */
        h3 {
            color: #333333 !important;
        }
        /* Paragraph text styling */
        p {
            color: #2c3e50 !important;
        }
        
    
        .stFormSubmitButton > button {
            background-color: #e8f5e8 !important;
            color: #2c3e50 !important;
            border: none !important;
            padding: 10px 20px !important;
            border-radius: 5px !important;
            font-weight: 600 !important;
            height: 50px !important;
            min-height: 50px !important;
            max-height: 50px !important;
            width: 100% !important;
        }
        
        .stFormSubmitButton > button:hover {
            background-color: #d4e8d4 !important;
            color: #2c3e50 !important;
        }
        
        .stFormSubmitButton > button:active {
            color: #2c3e50 !important;
        }
        
        /* Cancel button styling - light red background */
        .stFormSubmitButton > button:has-text("Cancel") {
            background-color: #ffebee !important;
            color: #c62828 !important;
        }
        
        .stFormSubmitButton > button:has-text("Cancel"):hover {
            background-color: #ffcdd2 !important;
            color: #c62828 !important;
        }
        
        .stFormSubmitButton > button:has-text("Cancel"):active {
            color: #c62828 !important;
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
        
        /* Slider styling - remove red color */
        .stSlider > div > div > div > div {
            background-color: #35B925 !important;
        }
        
        .stSlider > div > div > div > div > div {
            background-color: #35B925 !important;
        }
        
        /* Slider track styling */
        .stSlider > div > div > div > div > div > div {
            background-color: #35B925 !important;
        }
        
        /* Slider thumb styling */
        .stSlider > div > div > div > div > div > div > div {
            background-color: #35B925 !important;
            border-color: #35B925 !important;
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

st.markdown('<h1 class="title"><i class="fas fa-seedling"></i> Add Plant to Zone</h1>', unsafe_allow_html=True)

if st.button("← Back to Dashboard", key="back_to_dashboard"):
    st.switch_page("app.py")

st.markdown("---")

try:
    zones = session.query(ZoneModel).all()
    if not zones:
        st.markdown("""
        <div class="error-message">
        <i class="fas fa-times-circle" style="color: #dc3545; margin-right: 8px;"></i><strong>No zones found!</strong> Please create a zone first before adding plants.
        </div>
        """, unsafe_allow_html=True)
        st.stop()
except Exception as e:
    st.markdown(f"""
    <div class="error-message">
    <i class="fas fa-times-circle" style="color: #dc3545; margin-right: 8px;"></i><strong>Error loading zones:</strong> {str(e)}
    </div>
    """, unsafe_allow_html=True)
    st.stop()

st.markdown("### Select Zone", unsafe_allow_html=True)
zone_options = {f"Zone {zone.id} - {zone.name}": zone.id for zone in zones}
selected_zone_name = st.selectbox("Choose a zone:", list(zone_options.keys()))

if selected_zone_name:
    selected_zone_id = zone_options[selected_zone_name]
    selected_zone = session.query(ZoneModel).filter(ZoneModel.id == selected_zone_id).first()
    
    st.markdown(f"""
    <div class="zone-info">
    <strong>Selected Zone:</strong> {selected_zone.name}<br>
    <strong>Plant Type:</strong> {selected_zone.plant_type}<br>
    <strong>Moisture Threshold:</strong> {selected_zone.moisture_threshold}%
    </div>
    """, unsafe_allow_html=True)

with st.form("add_plant_form"):
    st.markdown("### Plant Information", unsafe_allow_html=True)
    
    plant_name = st.text_input("Plant Name", placeholder="e.g., Cherry Tomato, Basil, Marigold")
    plant_type = st.text_input("Plant Type", placeholder="e.g., Vegetable, Herb, Flower")
    planting_date = st.date_input("Planting Date", value=date.today())
    notes = st.text_area("Notes (Optional)", placeholder="e.g., Special care instructions, variety info")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        submit = st.form_submit_button("Add Plant")
    
    with col2:
        reset = st.form_submit_button("Reset Form")
    
    with col3:
        cancel = st.form_submit_button("Cancel")

if submit and selected_zone_name:
    if plant_name and plant_type:
        try:
            new_plant = PlantModel(
                zone_id=selected_zone_id,
                name=plant_name,
                plant_type=plant_type,
                planting_date=planting_date,
                notes=notes
            )
            
            session.add(new_plant)
            session.commit()
            
            st.markdown(f"""
            <div class="success-message">
            <i class="fas fa-check-circle" style="color: #35B925; margin-right: 8px;"></i><strong>Plant added successfully!</strong><br>
            Plant: {plant_name}<br>
            Type: {plant_type}<br>
            Zone: {selected_zone.name}<br>
            Planting Date: {planting_date}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <script>
                setTimeout(function(){
                    window.location.href = "app.py";
                }, 3000);
            </script>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.markdown(f"""
            <div class="error-message">
            <i class="fas fa-times-circle" style="color: #dc3545; margin-right: 8px;"></i><strong>Error adding plant:</strong> {str(e)}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="error-message">
        <i class="fas fa-exclamation-triangle" style="color: #dc3545; margin-right: 8px;"></i><strong>Please fill in all required fields:</strong> Plant Name and Plant Type
        </div>
        """, unsafe_allow_html=True)

elif reset:
    st.rerun()

elif cancel:
                st.switch_page("app.py")

# Display existing plants in selected zone
if selected_zone_name:
    st.markdown("---")
    st.markdown("### Plants in Selected Zone", unsafe_allow_html=True)
    
    try:
        existing_plants = session.query(PlantModel).filter(PlantModel.zone_id == selected_zone_id).all()
        
        if existing_plants:
            for plant in existing_plants:
                st.markdown(f"""
                <div class="zone-info">
                <strong>{plant.name}</strong> ({plant.plant_type})<br>
                <em>Planted: {plant.planting_date}</em>
                {f'<br><em>Notes: {plant.notes}</em>' if plant.notes else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<em>No plants added to this zone yet.</em>")
            
    except Exception as e:
        st.markdown(f"""
        <div class="error-message">
        <i class="fas fa-times-circle" style="color: #dc3545; margin-right: 8px;"></i><strong>Error loading plants:</strong> {str(e)}
        </div>
        """, unsafe_allow_html=True) 