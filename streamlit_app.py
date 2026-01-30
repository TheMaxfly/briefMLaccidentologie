"""
Streamlit app for accident severity prediction.

This is the main entry point for the Streamlit interface.
It provides a multi-page form to collect 15 input variables and call the FastAPI prediction endpoint.

Architecture:
- Uses streamlit_lib modules for session state, validation, and API calls
- Loads reference data from data/ref_options.json
- Implements constitution principle III (API-First)
"""

import streamlit as st
from streamlit_lib import reference_loader, session_state


# Configure Streamlit page
st.set_page_config(
    page_title="Prédiction de Gravité d'Accidents",
    page_icon="🚗",
    layout="centered",
    initial_sidebar_state="expanded"
)


# T017: Load reference data on initialization
@st.cache_data
def load_reference_data():
    """Load reference data from JSON file (cached)."""
    try:
        return reference_loader.load_reference_data()
    except Exception as e:
        st.error(f"Erreur lors du chargement des données de référence: {e}")
        st.stop()


# Initialize reference data
reference_data = load_reference_data()

# Initialize session state
session_state.initialize_state(reference_data)


# Sidebar: Navigation and controls
with st.sidebar:
    st.header("Navigation")

    # T019: Progress indicator showing "Page X/6"
    current_page = session_state.get_current_page()
    st.progress(current_page / 6, text=f"**Page {current_page}/6**")

    st.divider()

    # T018: "Nouvelle prédiction" button that resets session state
    if st.button("🔄 Nouvelle prédiction", use_container_width=True):
        session_state.reset_form()
        st.rerun()

    st.divider()

    # Show completion status
    completion = session_state.is_form_complete()
    if completion:
        st.success("✅ Formulaire complet")
    else:
        filled_count = len([
            f for f in [
                "dep", "lum", "atm", "catr", "agg", "int", "circ",
                "col", "vma_bucket", "catv_family_4", "manv_mode",
                "driver_age_bucket", "choc_mode", "driver_trajet_family", "minute"
            ]
            if session_state.get_prediction_input(f) is not None
        ])
        st.info(f"📝 {filled_count}/15 champs remplis")


# Main content area
st.title("🚗 Prédiction de Gravité d'Accidents")
st.caption("Interface Streamlit pour la prédiction de la gravité des accidents de la route")

# Display current page content
if current_page == 1:
    st.header("Page 1 : Contexte Route")
    st.info("🚧 Cette page sera implémentée dans US-02 (Navigation multi-pages)")
    st.write("Champs à remplir :")
    st.write("- Département (dep)")
    st.write("- Agglomération (agg)")
    st.write("- Catégorie de route (catr)")
    st.write("- Vitesse maximale autorisée (vma_bucket)")

    if st.button("Suivant →", key="page1_next"):
        session_state.navigate_next()
        st.rerun()

elif current_page == 2:
    st.header("Page 2 : Infrastructure")
    st.info("🚧 Cette page sera implémentée dans US-02")
    st.write("Champs à remplir :")
    st.write("- Type d'intersection (int)")
    st.write("- Régime de circulation (circ)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Précédent", key="page2_prev"):
            session_state.navigate_previous()
            st.rerun()
    with col2:
        if st.button("Suivant →", key="page2_next"):
            session_state.navigate_next()
            st.rerun()

elif current_page == 3:
    st.header("Page 3 : Collision")
    st.info("🚧 Cette page sera implémentée dans US-02")
    st.write("Champs à remplir :")
    st.write("- Type de collision (col)")
    st.write("- Point de choc (choc_mode)")
    st.write("- Manœuvre (manv_mode)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Précédent", key="page3_prev"):
            session_state.navigate_previous()
            st.rerun()
    with col2:
        if st.button("Suivant →", key="page3_next"):
            session_state.navigate_next()
            st.rerun()

elif current_page == 4:
    st.header("Page 4 : Conducteur")
    st.info("🚧 Cette page sera implémentée dans US-02")
    st.write("Champs à remplir :")
    st.write("- Classe d'âge conducteur (driver_age_bucket)")
    st.write("- Famille de trajet (driver_trajet_family)")
    st.write("- Famille de véhicule (catv_family_4)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Précédent", key="page4_prev"):
            session_state.navigate_previous()
            st.rerun()
    with col2:
        if st.button("Suivant →", key="page4_next"):
            session_state.navigate_next()
            st.rerun()

elif current_page == 5:
    st.header("Page 5 : Conditions")
    st.info("🚧 Cette page sera implémentée dans US-02")
    st.write("Champs à remplir :")
    st.write("- Conditions d'éclairage (lum)")
    st.write("- Conditions atmosphériques (atm)")
    st.write("- Minute de l'heure (minute)")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Précédent", key="page5_prev"):
            session_state.navigate_previous()
            st.rerun()
    with col2:
        if st.button("Suivant →", key="page5_next"):
            session_state.navigate_next()
            st.rerun()

elif current_page == 6:
    st.header("Page 6 : Récapitulatif et Prédiction")
    st.info("🚧 Cette page sera implémentée dans US-02 et US-07")
    st.write("Cette page affichera :")
    st.write("- Récapitulatif des 15 champs saisis")
    st.write("- Bouton 'Prédire' (activé si formulaire complet)")
    st.write("- Résultat de la prédiction")

    if st.button("← Précédent", key="page6_prev"):
        session_state.navigate_previous()
        st.rerun()

else:
    st.error(f"Page invalide : {current_page}")


# Footer
st.divider()
st.caption("Application développée selon l'architecture Speckit • Constitution-driven development")


# Debug info (development only - can be removed in production)
with st.expander("🔧 Debug Info"):
    st.write("**Session State:**")
    st.write(f"- Current page: {current_page}")
    st.write(f"- Form complete: {session_state.is_form_complete()}")
    st.write(f"- Prediction inputs: {len(session_state.get_all_prediction_inputs())} fields")

    all_inputs = session_state.get_all_prediction_inputs()
    if all_inputs:
        st.json(all_inputs)

    st.write("**Reference Data Loaded:**")
    st.write(f"- Total fields: {len(reference_data)}")
    for field_name in list(reference_data.keys())[:5]:  # Show first 5 fields
        st.write(f"  - {field_name}: {len(reference_data[field_name])} options")
    st.caption("... et 10 autres champs")
