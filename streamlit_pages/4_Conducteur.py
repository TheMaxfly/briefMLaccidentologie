"""
Page 4: Conducteur

Fields: driver_age_bucket, driver_trajet_family, catv_family_4
"""

import streamlit as st
from streamlit_lib import session_state, reference_loader


st.set_page_config(page_title="Page 4 - Conducteur", page_icon="👤", layout="centered")

if 'reference_data' not in st.session_state:
    reference_data = reference_loader.load_reference_data()
    session_state.initialize_state(reference_data)

session_state.set_current_page(4)

st.title("👤 Page 4 : Conducteur et Véhicule")
st.caption("Informations sur le conducteur et le type de véhicule")

ref_data = session_state.get_reference_data()

# Field: Classe d'âge conducteur
st.subheader("Classe d'âge du conducteur")
age_options = reference_loader.get_dropdown_options(ref_data, "driver_age_bucket")
current_age = session_state.get_prediction_input("driver_age_bucket")

age_index = 0
if current_age:
    formatted_current = reference_loader.format_dropdown_option(current_age,
        reference_loader.get_label_for_code(ref_data, "driver_age_bucket", current_age))
    if formatted_current in age_options:
        age_index = age_options.index(formatted_current)

age_selected = st.selectbox("Classe d'âge", options=age_options, index=age_index, key="age_input")
if age_selected:
    age_code = reference_loader.parse_dropdown_value(age_selected)
    session_state.set_prediction_input("driver_age_bucket", age_code)

st.divider()

# Field: Famille de trajet
st.subheader("Type de trajet")
trajet_options = reference_loader.get_dropdown_options(ref_data, "driver_trajet_family")
current_trajet = session_state.get_prediction_input("driver_trajet_family")

trajet_index = 0
if current_trajet:
    formatted_current = reference_loader.format_dropdown_option(current_trajet,
        reference_loader.get_label_for_code(ref_data, "driver_trajet_family", current_trajet))
    if formatted_current in trajet_options:
        trajet_index = trajet_options.index(formatted_current)

trajet_selected = st.selectbox("Type de trajet", options=trajet_options, index=trajet_index, key="trajet_input")
if trajet_selected:
    trajet_code = reference_loader.parse_dropdown_value(trajet_selected)
    session_state.set_prediction_input("driver_trajet_family", trajet_code)

st.divider()

# Field: Famille de véhicule
st.subheader("Famille de véhicule")
catv_options = reference_loader.get_dropdown_options(ref_data, "catv_family_4")
current_catv = session_state.get_prediction_input("catv_family_4")

catv_index = 0
if current_catv:
    formatted_current = reference_loader.format_dropdown_option(current_catv,
        reference_loader.get_label_for_code(ref_data, "catv_family_4", current_catv))
    if formatted_current in catv_options:
        catv_index = catv_options.index(formatted_current)

catv_selected = st.selectbox("Famille de véhicule", options=catv_options, index=catv_index, key="catv_input")
if catv_selected:
    catv_code = reference_loader.parse_dropdown_value(catv_selected)
    session_state.set_prediction_input("catv_family_4", catv_code)

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

st.caption("Page 4/6 • 3 champs sur cette page")
