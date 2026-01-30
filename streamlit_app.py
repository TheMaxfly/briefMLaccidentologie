import os
from typing import Any, Dict, List, Tuple

import requests
import streamlit as st


def _api_base_url() -> str:
    return os.getenv("API_URL", "http://localhost:8000").rstrip("/")


DEP_CODES: List[str] = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "2A",
    "2B",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59",
    "60",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "70",
    "71",
    "72",
    "73",
    "74",
    "75",
    "76",
    "77",
    "78",
    "79",
    "80",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "90",
    "91",
    "92",
    "93",
    "94",
    "95",
    "971",
    "972",
    "973",
    "974",
    "975",
    "976",
    "977",
    "978",
    "986",
    "987",
    "988",
]

LUM: List[Tuple[int, str]] = [
    (1, "Plein jour"),
    (2, "Crepuscule ou aube"),
    (3, "Nuit sans eclairage public"),
    (4, "Nuit avec eclairage public non allume"),
    (5, "Nuit avec eclairage public allume"),
]

ATM: List[Tuple[int, str]] = [
    (-1, "Non renseigne"),
    (1, "Normale"),
    (2, "Pluie legere"),
    (3, "Pluie forte"),
    (4, "Neige / grele"),
    (5, "Brouillard / fumee"),
    (6, "Vent fort / tempete"),
    (7, "Temps eblouissant"),
    (8, "Temps couvert"),
    (9, "Autre"),
]

AGG: List[Tuple[int, str]] = [(1, "Hors agglomeration"), (2, "En agglomeration")]

CATR: List[Tuple[int, str]] = [
    (1, "Autoroute"),
    (2, "Route nationale"),
    (3, "Route departementale"),
    (4, "Voie communale"),
    (5, "Hors reseau public"),
    (6, "Parking public"),
    (7, "Routes de metropole urbaine"),
    (9, "Autre"),
]

INT: List[Tuple[int, str]] = [
    (1, "Hors intersection"),
    (2, "Intersection en X"),
    (3, "Intersection en T"),
    (4, "Intersection en Y"),
    (5, "Intersection >4 branches"),
    (6, "Giratoire"),
    (7, "Place"),
    (8, "Passage a niveau"),
    (9, "Autre intersection"),
]

CIRC: List[Tuple[int, str]] = [
    (-1, "Non renseigne"),
    (1, "Sens unique"),
    (2, "Bidirectionnelle"),
    (3, "Chaussees separees"),
    (4, "Voies a affectation variable"),
]

COL: List[Tuple[int, str]] = [
    (-1, "Non renseigne"),
    (1, "2 vehicules - frontale"),
    (2, "2 vehicules - arriere"),
    (3, "2 vehicules - cote"),
    (4, "3+ vehicules - en chaine"),
    (5, "3+ vehicules - collisions multiples"),
    (6, "Autre collision"),
    (7, "Sans collision"),
]

VMA_BUCKET: List[str] = ["<=30", "31-50", "51-80", "81-90", "91-110", "111-130", ">130", "inconnue"]

CATV_FAMILY_4: List[str] = [
    "voitures_utilitaires",
    "2rm_3rm",
    "lourds_tc_agri_autres",
    "vulnerables",
]

DRIVER_AGE_BUCKET: List[str] = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+", "unknown"]
DRIVER_TRAJET_FAMILY: List[str] = ["trajet_1", "trajet_2", "trajet_3", "trajet_4", "trajet_5", "trajet_9", "unknown"]

MANV_MODE: List[Tuple[int, str]] = [
    (-1, "Non renseigne"),
    (0, "Inconnue"),
    (1, "Sans changement de direction"),
    (2, "Meme sens, meme file"),
    (3, "Entre 2 files"),
    (4, "Marche arriere"),
    (5, "Contresens"),
    (6, "Franchissant TPC"),
    (7, "Couloir bus meme sens"),
    (8, "Couloir bus sens inverse"),
    (9, "S inserant"),
    (10, "Demi-tour sur chaussee"),
    (11, "Change file gauche"),
    (12, "Change file droite"),
    (13, "Deporte gauche"),
    (14, "Deporte droite"),
    (15, "Tournant gauche"),
    (16, "Tournant droite"),
    (17, "Depassant gauche"),
    (18, "Depassant droite"),
    (19, "Traversant chaussee"),
    (20, "Stationnement"),
    (21, "Evitement"),
    (22, "Ouverture de porte"),
    (23, "Arrete (hors stationnement)"),
    (24, "En stationnement (avec occupants)"),
    (25, "Circulant sur trottoir"),
    (26, "Autres manoeuvres"),
]

CHOC_MODE: List[Tuple[int, str]] = [
    (-1, "Non renseigne"),
    (0, "Aucun"),
    (1, "Avant"),
    (2, "Avant droit"),
    (3, "Avant gauche"),
    (4, "Arriere"),
    (5, "Arriere droit"),
    (6, "Arriere gauche"),
    (7, "Cote droit"),
    (8, "Cote gauche"),
    (9, "Chocs multiples / tonneaux"),
]


def _format_opt(opts: List[Tuple[int, str]]) -> Dict[int, str]:
    return {code: f"{code} — {label}" for code, label in opts}


def _get_json(url: str, timeout_s: float = 5.0) -> Dict[str, Any]:
    r = requests.get(url, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


def _post_json(url: str, payload: Dict[str, Any], timeout_s: float = 15.0) -> Dict[str, Any]:
    r = requests.post(url, json=payload, timeout=timeout_s)
    r.raise_for_status()
    return r.json()


st.set_page_config(page_title="Accidents — Prediction gravite", layout="centered")

st.title("Accidents — Prediction de gravite")
st.caption("UI Streamlit qui consomme l'API FastAPI (/health, /predict).")

with st.sidebar:
    st.header("Connexion API")
    api_base = st.text_input("API base URL", value=_api_base_url(), help="Ex: http://localhost:8000")
    api_base = api_base.rstrip("/")

    if st.button("Tester /health"):
        try:
            health = _get_json(f"{api_base}/health")
            st.success("OK")
            st.json(health)
        except Exception as e:
            st.error(f"Erreur /health: {e}")

st.subheader("Saisie des 15 variables (product15)")

lum_fmt = _format_opt(LUM)
atm_fmt = _format_opt(ATM)
agg_fmt = _format_opt(AGG)
catr_fmt = _format_opt(CATR)
int_fmt = _format_opt(INT)
circ_fmt = _format_opt(CIRC)
col_fmt = _format_opt(COL)
manv_fmt = _format_opt(MANV_MODE)
choc_fmt = _format_opt(CHOC_MODE)

with st.form("predict_form"):
    c1, c2 = st.columns(2)

    with c1:
        dep = st.selectbox("dep (Departement)", DEP_CODES, index=DEP_CODES.index("75") if "75" in DEP_CODES else 0)
        lum = st.selectbox("lum (Luminosite)", list(lum_fmt.keys()), format_func=lambda k: lum_fmt[k])
        atm = st.selectbox("atm (Atmosphere)", list(atm_fmt.keys()), format_func=lambda k: atm_fmt[k], index=1)
        catr = st.selectbox("catr (Categorie route)", list(catr_fmt.keys()), format_func=lambda k: catr_fmt[k], index=2)
        agg = st.selectbox("agg (Agglomeration)", list(agg_fmt.keys()), format_func=lambda k: agg_fmt[k], index=1)
        itx = st.selectbox("int (Intersection)", list(int_fmt.keys()), format_func=lambda k: int_fmt[k], index=0)
        circ = st.selectbox("circ (Regime circulation)", list(circ_fmt.keys()), format_func=lambda k: circ_fmt[k], index=1)
        col = st.selectbox("col (Type collision)", list(col_fmt.keys()), format_func=lambda k: col_fmt[k], index=2)

    with c2:
        vma_bucket = st.selectbox("vma_bucket (VMA bucket)", VMA_BUCKET, index=2)
        catv_family_4 = st.selectbox("catv_family_4 (Famille vehicule)", CATV_FAMILY_4, index=0)
        manv_mode = st.selectbox("manv_mode (Manoeuvre)", list(manv_fmt.keys()), format_func=lambda k: manv_fmt[k], index=2)
        driver_age_bucket = st.selectbox("driver_age_bucket (Age bucket)", DRIVER_AGE_BUCKET, index=2)
        choc_mode = st.selectbox("choc_mode (Point de choc)", list(choc_fmt.keys()), format_func=lambda k: choc_fmt[k], index=2)
        driver_trajet_family = st.selectbox(
            "driver_trajet_family (Trajet famille)", DRIVER_TRAJET_FAMILY, index=0
        )
        minute = st.slider("minute (0-59)", min_value=0, max_value=59, value=40)

    submitted = st.form_submit_button("Predire")

if submitted:
    payload = {
        "data": {
            "dep": str(dep),
            "lum": int(lum),
            "atm": int(atm),
            "catr": int(catr),
            "agg": int(agg),
            "int": int(itx),
            "circ": int(circ),
            "col": int(col),
            "vma_bucket": str(vma_bucket),
            "catv_family_4": str(catv_family_4),
            "manv_mode": int(manv_mode),
            "driver_age_bucket": str(driver_age_bucket),
            "choc_mode": int(choc_mode),
            "driver_trajet_family": str(driver_trajet_family),
            "minute": int(minute),
        }
    }

    try:
        resp = _post_json(f"{api_base}/predict", payload)
        st.success(f"Prediction: {resp.get('label')} (classe={resp.get('pred_class')})")
        st.metric("Proba accident grave", f"{float(resp.get('proba', 0.0)):.3f}")
        st.caption(f"Seuil: {resp.get('threshold')}")
        with st.expander("Details (debug)"):
            st.write("Payload envoye")
            st.json(payload)
            st.write("Reponse brute")
            st.json(resp)
    except requests.HTTPError as e:
        st.error(f"Erreur HTTP: {e}")
        try:
            st.json(e.response.json())
        except Exception:
            st.text(e.response.text if e.response is not None else str(e))
        with st.expander("Payload (debug)"):
            st.json(payload)
    except Exception as e:
        st.error(f"Erreur: {e}")
        with st.expander("Payload (debug)"):
            st.json(payload)

