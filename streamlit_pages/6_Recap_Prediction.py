"""
Page 6: Récapitulatif et Prédiction

Shows summary of all 15 fields and prediction button
"""

import streamlit as st
from streamlit_lib import session_state, reference_loader, validation, api_client


st.set_page_config(page_title="Page 6 - Prédiction", page_icon="🎯", layout="centered")

if 'reference_data' not in st.session_state:
    reference_data = reference_loader.load_reference_data()
    session_state.initialize_state(reference_data)

session_state.set_current_page(6)

st.title("🎯 Page 6 : Récapitulatif et Prédiction")
st.caption("Vérifiez vos saisies avant de lancer la prédiction")

ref_data = session_state.get_reference_data()
all_inputs = session_state.get_all_prediction_inputs()

# Check if form is complete
session_state.update_form_complete_status()
is_complete = session_state.is_form_complete()

# Display summary table (US-08)
st.subheader("📋 Récapitulatif de vos saisies")

if len(all_inputs) > 0:
    st.info(f"✏️ {len(all_inputs)}/15 champs renseignés")

    # Generate and display recap table
    recap_df = session_state.generate_recap_table(all_inputs, ref_data)

    # Display table with st.dataframe
    st.dataframe(
        recap_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Champ": st.column_config.TextColumn("Champ", width="medium"),
            "Code": st.column_config.TextColumn("Code", width="small"),
            "Libellé": st.column_config.TextColumn("Libellé", width="large"),
            "Page": st.column_config.NumberColumn("Page", width="small", format="%d")
        }
    )

    # Add "Modifier" buttons grouped by page (T070)
    st.caption("💡 Pour modifier un champ, cliquez sur le bouton de la page correspondante")

    # Create buttons for each page that has data
    pages_with_data = sorted(recap_df["Page"].unique())
    if len(pages_with_data) > 0:
        # Display buttons in columns
        num_pages = len(pages_with_data)
        cols = st.columns(min(num_pages, 6))

        for idx, page_num in enumerate(pages_with_data):
            with cols[idx % 6]:
                # Count fields on this page
                fields_on_page = recap_df[recap_df["Page"] == page_num]
                field_count = len(fields_on_page)

                if st.button(
                    f"📝 Page {page_num} ({field_count})",
                    key=f"modify_page_{page_num}",
                    use_container_width=True,
                    help=f"Modifier les {field_count} champ(s) de la page {page_num}"
                ):
                    session_state.set_current_page(page_num)
                    st.rerun()
else:
    st.warning("Aucun champ renseigné. Veuillez remplir le formulaire.")

# Show missing fields if form incomplete
if not is_complete:
    st.divider()
    missing_message = validation.format_missing_fields_message(all_inputs)
    if missing_message:
        st.error(missing_message)

st.divider()

# Prediction button (disabled if form incomplete)
st.subheader("🔮 Lancer la prédiction")

if not is_complete:
    st.button("Prédire", disabled=True, use_container_width=True, type="primary",
              help="Veuillez remplir les 15 champs obligatoires")
    st.caption("⚠️ Le bouton sera activé une fois tous les champs remplis")
else:
    if st.button("Prédire", use_container_width=True, type="primary"):
        # T061-T062: Call API with loading spinner
        with st.spinner("🔮 Prédiction en cours..."):
            response = api_client.call_predict_api(all_inputs)

        # T063-T065: Display prediction result or error
        if api_client.is_success_response(response):
            # Success: Display prediction result
            st.success("✅ Prédiction effectuée avec succès !")

            # Display probability as metric
            probability = response["probability"]
            prediction_class = response["prediction"]
            threshold = response["threshold"]

            # T064: Visual styling - color-coded result
            st.divider()

            # Display probability metric
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label="Probabilité d'accident grave",
                    value=f"{probability:.2%}",
                    delta=f"Seuil: {threshold:.2%}"
                )

            with col2:
                # T065: Interpretation text with visual styling
                if prediction_class == "grave":
                    st.error(
                        f"🚨 **ACCIDENT GRAVE**\n\n"
                        f"La probabilité ({probability:.2%}) est supérieure ou égale au seuil ({threshold:.2%}). "
                        f"Ce contexte présente un risque élevé d'accident grave."
                    )
                else:
                    st.success(
                        f"✅ **ACCIDENT NON-GRAVE**\n\n"
                        f"La probabilité ({probability:.2%}) est inférieure au seuil ({threshold:.2%}). "
                        f"Ce contexte présente un risque faible d'accident grave."
                    )

            # Store prediction result in session state for later use
            session_state.set_last_prediction(response)

        else:
            # Error: Display formatted error message
            st.error("❌ Erreur lors de la prédiction")
            error_message = api_client.format_error_message(response)
            st.error(error_message)

st.divider()

# Navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("← Précédent", use_container_width=True):
        session_state.navigate_previous()
        st.rerun()
with col2:
    st.caption("Vous êtes sur la dernière page")

st.caption("Page 6/6 • Récapitulatif et prédiction")
