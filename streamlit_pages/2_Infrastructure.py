"""
Page 2: Infrastructure

Fields: int, circ
"""

import streamlit as st
from streamlit_lib import session_state, reference_loader


st.set_page_config(page_title="Page 2 - Infrastructure", page_icon="🚦", layout="centered")

if 'reference_data' not in st.session_state:
    reference_data = reference_loader.load_reference_data()
    session_state.initialize_state(reference_data)

session_state.set_current_page(2)

st.title("🚦 Page 2 : Infrastructure")
st.caption("Type d'intersection et régime de circulation")

ref_data = session_state.get_reference_data()

# Field: Type d'intersection (int)
st.subheader("Type d'intersection")
int_options = reference_loader.get_dropdown_options(ref_data, "int")
current_int = session_state.get_prediction_input("int")

int_index = 0
if current_int:
    formatted_current = reference_loader.format_dropdown_option(current_int,
        reference_loader.get_label_for_code(ref_data, "int", current_int))
    if formatted_current in int_options:
        int_index = int_options.index(formatted_current)

int_selected = st.selectbox("Type d'intersection", options=int_options, index=int_index, key="int_input")
if int_selected:
    int_code = reference_loader.parse_dropdown_value(int_selected)
    session_state.set_prediction_input("int", int_code)

st.divider()

# Field: Régime de circulation (circ)
st.subheader("Régime de circulation")
circ_options = reference_loader.get_dropdown_options(ref_data, "circ")
current_circ = session_state.get_prediction_input("circ")

circ_index = 0
if current_circ:
    formatted_current = reference_loader.format_dropdown_option(current_circ,
        reference_loader.get_label_for_code(ref_data, "circ", current_circ))
    if formatted_current in circ_options:
        circ_index = circ_options.index(formatted_current)

circ_selected = st.selectbox("Régime de circulation", options=circ_options, index=circ_index, key="circ_input")
if circ_selected:
    circ_code = reference_loader.parse_dropdown_value(circ_selected)
    session_state.set_prediction_input("circ", circ_code)

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

st.caption("Page 2/6 • 2 champs sur cette page")
