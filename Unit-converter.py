import streamlit as st
import pandas as pd
from datetime import datetime


st.set_page_config(page_title="UnitMate Converter", page_icon="🔧", layout="wide")

 # styling
st.markdown("""
<style>
    html, body, .main {
        background-color: #f5f7fa;
        color: #31333F;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #0055ff;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.4rem 1rem;
        font-weight: bold;
    }
    .stSelectbox, .stNumberInput>div>div>input {
        border-radius: 6px;
    }
    .highlight-box {
        background: grey;
        border-left: 6px solid #0055ff;
        padding: 1rem;
        border-radius: 6px;
        margin-top: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .footer {
        font-size: 0.9rem;
        color: #888;
        text-align: center;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)


st.title(" 🧮 UnitMate - Unit Converter")
st.caption("### Quickly convert between common measurement units in a fresh layout.")


if "category" not in st.session_state:
    st.session_state.category = "Length"
if "history" not in st.session_state:
    st.session_state.history = []


UNITS = {
    "Length": {
        "units": ["Meters", "Kilometers", "Miles", "Yards", "Feet", "Inches"],
        "base": "Meters",
        "values": {
            "Meters": 1, "Kilometers": 1000, "Miles": 1609.34,
            "Yards": 0.9144, "Feet": 0.3048, "Inches": 0.0254
        }
    },
    "Weight": {
        "units": ["Kilograms", "Grams", "Pounds", "Ounces"],
        "base": "Kilograms",
        "values": {
            "Kilograms": 1, "Grams": 0.001, "Pounds": 0.453592, "Ounces": 0.0283495
        }
    },
    "Temperature": {
        "units": ["Celsius", "Fahrenheit", "Kelvin"],
        "base": None,
        "values": {}
    }
}


st.subheader("Choose a Measurement Type:")
cols = st.columns(len(UNITS))
for i, cat in enumerate(UNITS):
    if cols[i].button(cat):
        st.session_state.category = cat
       

category = st.session_state.category


st.markdown("### Enter Your Values")
col1, col2 = st.columns(2)
with col1:
    value = st.number_input("Value", value=1.0)
    from_unit = st.selectbox("From Unit", UNITS[category]["units"])
with col2:
    to_unit = st.selectbox("To Unit", UNITS[category]["units"])

st.markdown("### Conversion Result")
def convert_units(cat, val, from_u, to_u):
    if cat == "Temperature":
        if from_u == to_u:
            return val
        elif from_u == "Celsius" and to_u == "Fahrenheit":
            return (val * 9/5) + 32
        elif from_u == "Celsius" and to_u == "Kelvin":
            return val + 273.15
        elif from_u == "Fahrenheit" and to_u == "Celsius":
            return (val - 32) * 5/9
        elif from_u == "Fahrenheit" and to_u == "Kelvin":
            return ((val - 32) * 5/9) + 273.15
        elif from_u == "Kelvin" and to_u == "Celsius":
            return val - 273.15
        elif from_u == "Kelvin" and to_u == "Fahrenheit":
            return ((val - 273.15) * 9/5) + 32
    else:
        base_val = val * UNITS[cat]["values"][from_u]
        return base_val / UNITS[cat]["values"][to_u]

result = convert_units(category, value, from_unit, to_unit)


st.markdown(f"""
<div class="highlight-box ">
    <h4>Result</h4>
    <p style="font-size: 1.5rem;"><strong>{value} {from_unit}</strong> is equal to <strong>{result:.4g} {to_unit}</strong></p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Save Conversion History")
st.markdown("You can save this conversion to your history for future reference.")


if st.button("Save this conversion"):
    st.session_state.history.insert(0, {
        "Type": category,
        "From": f"{value} {from_unit}",
        "To": f"{result:.4g} {to_unit}",
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


if st.session_state.history:
    st.subheader("Recent Conversions")
    st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)
    if st.button("Clear History"):
        st.session_state.history = []
       
st.markdown("----")
st.markdown("### About UnitMate")
st.markdown(""" UnitMate is a simple and efficient unit converter that helps you convert between various units of measurement. Whether you're converting length, weight, or temperature, UnitMate makes it easy to get accurate results quickly. """)
st.markdown("### Features")

st.markdown("""
- **User-Friendly Interface**: Designed for ease of use with a clean layout.
- **Multiple Categories**: Convert between length, weight, and temperature.
- **Conversion History**: Save and view your recent conversions.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.
""")

st.markdown("----")

st.markdown('<div class="footer">🚀 Created with ❤️ • Designed by Fayaz ALI</div>', unsafe_allow_html=True)
