"""
Page 5: Conditions

Fields: lum, atm, minute
"""

import streamlit as st
from streamlit_lib import session_state, reference_loader


st.set_page_config(page_title="Page 5 - Conditions", page_icon="🌤️", layout="centered")

if 'reference_data' not in st.session_state:
    reference_data = reference_loader.load_reference_data()
    session_state.initialize_state(reference_data)

session_state.set_current_page(5)

st.title("🌤️ Page 5 : Conditions")
st.caption("Conditions d'éclairage, météorologiques et heure")

ref_data = session_state.get_reference_data()

# Field: Conditions d'éclairage (lum)
st.subheader("Conditions d'éclairage")
lum_options = reference_loader.get_dropdown_options(ref_data, "lum")
current_lum = session_state.get_prediction_input("lum")

lum_index = 0
if current_lum:
    formatted_current = reference_loader.format_dropdown_option(current_lum,
        reference_loader.get_label_for_code(ref_data, "lum", current_lum))
    if formatted_current in lum_options:
        lum_index = lum_options.index(formatted_current)

lum_selected = st.selectbox("Luminosité", options=lum_options, index=lum_index, key="lum_input")
if lum_selected:
    lum_code = reference_loader.parse_dropdown_value(lum_selected)
    session_state.set_prediction_input("lum", lum_code)

st.divider()

# Field: Conditions atmosphériques (atm)
st.subheader("Conditions atmosphériques")
atm_options = reference_loader.get_dropdown_options(ref_data, "atm")
current_atm = session_state.get_prediction_input("atm")

atm_index = 0
if current_atm:
    formatted_current = reference_loader.format_dropdown_option(current_atm,
        reference_loader.get_label_for_code(ref_data, "atm", current_atm))
    if formatted_current in atm_options:
        atm_index = atm_options.index(formatted_current)

atm_selected = st.selectbox("Conditions atmosphériques", options=atm_options, index=atm_index, key="atm_input")
if atm_selected:
    atm_code = reference_loader.parse_dropdown_value(atm_selected)
    session_state.set_prediction_input("atm", atm_code)

st.divider()

# Field: Minute (minute)
st.subheader("Minute de l'heure")
minute_options = reference_loader.get_dropdown_options(ref_data, "minute")
current_minute = session_state.get_prediction_input("minute")

minute_index = 0
if current_minute is not None:
    formatted_current = reference_loader.format_dropdown_option(current_minute,
        reference_loader.get_label_for_code(ref_data, "minute", current_minute))
    if formatted_current in minute_options:
        minute_index = minute_options.index(formatted_current)

minute_selected = st.selectbox("Minute (0-59)", options=minute_options, index=minute_index, key="minute_input",
                                help="Minute de l'heure de l'accident")
if minute_selected:
    minute_code = reference_loader.parse_dropdown_value(minute_selected)
    session_state.set_prediction_input("minute", minute_code)

st.divider()

# Navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Précédent", use_container_width=True):
        session_state.navigate_previous()
        st.rerun()
with col2:
    if st.button("Suivant →", use_container_width=True, type="primary"):
        session_state.navigate_next()
        session_state.update_form_complete_status()
        st.rerun()

st.caption("Page 5/6 • 3 champs sur cette page")
