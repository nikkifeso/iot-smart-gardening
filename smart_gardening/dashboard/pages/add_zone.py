import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import streamlit as st
from db.database import session, ZoneModel
from core.zone import Zone

# Page configuration
st.set_page_config(
    page_title="Add Zone - Smart Gardening Dashboard",
    page_icon="➕",
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
        }
        .stButton > button:hover {
            background-color: #754D33 !important;
            color: white !important;
        }
        .stButton > button:active {
            color: white !important;
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
        /* Improve text readability */
        .stTextInput > div > div > input {
            color: #333333;
        }
        .stNumberInput > div > div > input {
            color: #333333;
        }
        .stTextArea > div > div > textarea {
            color: #333333;
        }
        .stSlider > div > div > div > div {
            color: #333333;
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
        
        /* Form submit button styling - consistent with main buttons */
        .stFormSubmitButton > button {
            background-color: #35B925 !important;
            color: white !important;
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
            background-color: #754D33 !important;
            color: white !important;
        }
        
        .stFormSubmitButton > button:active {
            color: white !important;
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
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="title"><i class="fas fa-plus-circle"></i> Add New Zone</h1>', unsafe_allow_html=True)

# Back button
if st.button("Back to Dashboard", key="back_to_dashboard"):
    st.switch_page("app.py")

st.markdown("---")

# Zone creation form
with st.form("add_zone_form"):
    st.markdown("### Zone Information", unsafe_allow_html=True)
    
    zone_name = st.text_input("Zone Name", placeholder="e.g., Vegetable Garden, Herb Corner")
    plant_type = st.text_input("Plant Type", placeholder="e.g., Tomatoes, Herbs, Flowers")
    moisture_threshold = st.slider("Moisture Threshold (%)", min_value=10, max_value=90, value=30, step=5)
    
    ph_min = st.number_input("pH Range - Minimum", min_value=0.0, max_value=14.0, value=6.0, step=0.1)
    ph_max = st.number_input("pH Range - Maximum", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        submit = st.form_submit_button("Create Zone")
    
    with col2:
        reset = st.form_submit_button("Reset Form")
    
    with col3:
        cancel = st.form_submit_button("Cancel")

# Handle form submission
if submit:
    if zone_name and plant_type:
        try:
            # Create new zone
            new_zone = ZoneModel(
                name=zone_name,
                plant_type=plant_type,
                moisture_threshold=moisture_threshold,
                ph_min=ph_min,
                ph_max=ph_max
            )
            
            session.add(new_zone)
            session.commit()
            
            st.markdown(f"""
            <div class="success-message">
            <i class="fas fa-check-circle" style="color: #35B925; margin-right: 8px;"></i><strong>Zone added successfully!</strong><br>
            <p>Zone: {zone_name}</p>
            <p>Plant Type: {plant_type}</p>
            <p>Moisture Threshold: {moisture_threshold}%</p>
            <p>pH Range: {ph_min} - {ph_max}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Auto-redirect after 3 seconds
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
            <i class="fas fa-times-circle" style="color: #dc3545; margin-right: 8px;"></i><strong>Error adding zone:</strong> {str(e)}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="error-message">
        <i class="fas fa-exclamation-triangle" style="color: #dc3545; margin-right: 8px;"></i><strong>Please fill in all required fields:</strong> Zone Name, Plant Type, Moisture Threshold, pH Range
        </div>
        """, unsafe_allow_html=True)

elif reset:
    st.rerun()

elif cancel:
                st.switch_page("app.py") 