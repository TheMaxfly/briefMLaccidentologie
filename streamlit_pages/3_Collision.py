"""
Page 3: Collision

Fields: col, choc_mode, manv_mode
"""

import streamlit as st
from streamlit_lib import session_state, reference_loader


st.set_page_config(page_title="Page 3 - Collision", page_icon="💥", layout="centered")

if 'reference_data' not in st.session_state:
    reference_data = reference_loader.load_reference_data()
    session_state.initialize_state(reference_data)

session_state.set_current_page(3)

st.title("💥 Page 3 : Collision")
st.caption("Type de collision, point de choc et manœuvre")

ref_data = session_state.get_reference_data()

# Field: Type de collision (col)
st.subheader("Type de collision")
col_options = reference_loader.get_dropdown_options(ref_data, "col")
current_col = session_state.get_prediction_input("col")

col_index = 0
if current_col:
    formatted_current = reference_loader.format_dropdown_option(current_col,
        reference_loader.get_label_for_code(ref_data, "col", current_col))
    if formatted_current in col_options:
        col_index = col_options.index(formatted_current)

col_selected = st.selectbox("Type de collision", options=col_options, index=col_index, key="col_input")
if col_selected:
    col_code = reference_loader.parse_dropdown_value(col_selected)
    session_state.set_prediction_input("col", col_code)

st.divider()

# Field: Point de choc (choc_mode)
st.subheader("Point de choc initial")
choc_options = reference_loader.get_dropdown_options(ref_data, "choc_mode")
current_choc = session_state.get_prediction_input("choc_mode")

choc_index = 0
if current_choc:
    formatted_current = reference_loader.format_dropdown_option(current_choc,
        reference_loader.get_label_for_code(ref_data, "choc_mode", current_choc))
    if formatted_current in choc_options:
        choc_index = choc_options.index(formatted_current)

choc_selected = st.selectbox("Point de choc", options=choc_options, index=choc_index, key="choc_input")
if choc_selected:
    choc_code = reference_loader.parse_dropdown_value(choc_selected)
    session_state.set_prediction_input("choc_mode", choc_code)

st.divider()

# Field: Manœuvre (manv_mode)
st.subheader("Manœuvre")
manv_options = reference_loader.get_dropdown_options(ref_data, "manv_mode")
current_manv = session_state.get_prediction_input("manv_mode")

manv_index = 0
if current_manv:
    formatted_current = reference_loader.format_dropdown_option(current_manv,
        reference_loader.get_label_for_code(ref_data, "manv_mode", current_manv))
    if formatted_current in manv_options:
        manv_index = manv_options.index(formatted_current)

manv_selected = st.selectbox("Manœuvre", options=manv_options, index=manv_index, key="manv_input")
if manv_selected:
    manv_code = reference_loader.parse_dropdown_value(manv_selected)
    session_state.set_prediction_input("manv_mode", manv_code)

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

st.caption("Page 3/6 • 3 champs sur cette page")
