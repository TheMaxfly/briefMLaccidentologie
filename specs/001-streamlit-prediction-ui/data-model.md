# Data Model: Interface de Prédiction de Gravité d'Accidents

**Feature**: `001-streamlit-prediction-ui`
**Created**: 2026-01-30
**Purpose**: Define data structures, validation rules, and state management for the Streamlit prediction interface

## Overview

This document defines the data entities used in the Streamlit interface for accident severity prediction. All entities are based on the `data_dictionary_catboost_product15.md` reference and must conform to constitution principle I (Data Quality First).

## Core Entities

### 1. PredictionInput

**Purpose**: Represents the 15 input variables required for accident severity prediction.

**Type**: Pydantic BaseModel (for validation)

**Fields**:

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| `dep` | `str` | Must be in valid department codes (107 values) | Département (INSEE code) |
| `lum` | `int` | Must be in [1, 2, 3, 4, 5] | Conditions d'éclairage (luminosité) |
| `atm` | `int` | Must be in [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9] | Conditions atmosphériques |
| `catr` | `int` | Must be in [1, 2, 3, 4, 5, 6, 7, 9] | Catégorie de route |
| `agg` | `int` | Must be in [1, 2] | Agglomération (hors/en) |
| `int` | `int` | Must be in [1, 2, 3, 4, 5, 6, 7, 8, 9] | Type d'intersection |
| `circ` | `int` | Must be in [-1, 1, 2, 3, 4] | Régime de circulation |
| `col` | `int` | Must be in [-1, 1, 2, 3, 4, 5, 6, 7] | Type de collision |
| `vma_bucket` | `str` | Must be in ["<=30", "31-50", "51-80", "81-90", "91-110", "111-130", ">130", "inconnue"] | Vitesse maximale autorisée (classe) |
| `catv_family_4` | `str` | Must be in ["voitures_utilitaires", "2rm_3rm", "lourds_tc_agri_autres", "vulnerables"] | Famille de véhicule (4 classes) |
| `manv_mode` | `int` | Must be in [-1, 0, 1, 2, ..., 26] | Manœuvre (mode) |
| `driver_age_bucket` | `str` | Must be in ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+", "unknown"] | Classe d'âge conducteur |
| `choc_mode` | `int` | Must be in [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9] | Point de choc initial (mode) |
| `driver_trajet_family` | `str` | Must be in ["trajet_1", "trajet_2", "trajet_3", "trajet_4", "trajet_5", "trajet_9", "unknown"] | Famille de trajet conducteur |
| `time_bucket` | `str` | Must be in ["night_00_05", "morning_06_11", "afternoon_12_17", "evening_18_23"] | Tranche horaire |

**Example**:
```python
{
    "dep": "59",
    "lum": 1,
    "atm": 1,
    "catr": 3,
    "agg": 2,
    "int": 1,
    "circ": 2,
    "col": 3,
    "vma_bucket": "51-80",
    "catv_family_4": "voitures_utilitaires",
    "manv_mode": 1,
    "driver_age_bucket": "25-34",
    "choc_mode": 1,
    "driver_trajet_family": "trajet_1",
    "time_bucket": "morning_06_11"
}
```

**Validation Rules**:
- All fields are **required** (no null values allowed)
- Coded fields (int) must match BAAC nomenclature exactly
- Categorical fields (str) must match predefined buckets/families
- Field names must match exactly (case-sensitive)

---

### 2. PredictionResult

**Purpose**: Represents the prediction output from the FastAPI backend.

**Type**: Pydantic BaseModel

**Fields**:

| Field | Type | Validation | Description |
|-------|------|------------|-------------|
| `probability` | `float` | Must be in range [0.0, 1.0] | Probabilité d'accident grave |
| `prediction` | `Literal["grave", "non_grave"]` | Must be one of two values | Classe prédite (basée sur seuil 0.47) |
| `threshold` | `float` | Must be 0.47 | Seuil de décision appliqué |
| `inputs_summary` | `dict[str, Any]` | Optional, contains echoed inputs | Résumé des entrées (pour vérification) |

**Example**:
```python
{
    "probability": 0.68,
    "prediction": "grave",
    "threshold": 0.47,
    "inputs_summary": {
        "dep": "59",
        "lum": 1,
        # ... (tous les 15 champs)
    }
}
```

**Validation Rules**:
- `probability` must be between 0.0 and 1.0 inclusive
- `prediction` must be "grave" if probability >= threshold, else "non_grave"
- `threshold` must always be 0.47 (as per data dictionary rule)

**Derived Logic**:
```python
prediction = "grave" if probability >= 0.47 else "non_grave"
```

---

### 3. ReferenceData

**Purpose**: Centralized dropdown options for all 15 input fields.

**Type**: JSON structure loaded from `data/ref_options.json`

**Structure**:
```json
{
  "dep": [
    {"code": "01", "label": "Ain"},
    {"code": "02", "label": "Aisne"},
    ...
  ],
  "lum": [
    {"code": 1, "label": "Plein jour"},
    {"code": 2, "label": "Crépuscule ou aube"},
    {"code": 3, "label": "Nuit sans éclairage public"},
    {"code": 4, "label": "Nuit avec éclairage public non allumé"},
    {"code": 5, "label": "Nuit avec éclairage public allumé"}
  ],
  "atm": [
    {"code": -1, "label": "Non renseigné"},
    {"code": 1, "label": "Normale"},
    {"code": 2, "label": "Pluie légère"},
    ...
  ],
  ...
}
```

**Schema**:
- Top-level keys: field names (str)
- Values: arrays of option objects
- Option object:
  - `code`: int or str (matches field type)
  - `label`: str (French description)

**Validation Rules**:
- All 15 fields MUST have entries
- Each field MUST have at least 1 option
- Codes MUST match validation constraints in PredictionInput
- Labels MUST be in French

---

### 4. SessionState

**Purpose**: Manage user session state across multi-page navigation in Streamlit.

**Type**: Streamlit `st.session_state` dictionary

**Fields**:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `current_page` | `int` | 1 | Current page number (1-6) |
| `prediction_inputs` | `dict[str, Any]` | {} | User-selected values for 15 fields |
| `last_prediction` | `PredictionResult \| None` | None | Last prediction result (if any) |
| `validation_errors` | `dict[str, str]` | {} | Field-level validation errors |
| `reference_data` | `ReferenceData` | Loaded on init | Dropdown options (cached) |
| `is_form_complete` | `bool` | False | Whether all 15 fields are filled |

**Example**:
```python
st.session_state = {
    "current_page": 3,
    "prediction_inputs": {
        "dep": "59",
        "lum": 1,
        "atm": 1,
        # ... (only fields filled so far)
    },
    "last_prediction": None,
    "validation_errors": {},
    "reference_data": { ... },  # Loaded from JSON
    "is_form_complete": False
}
```

**State Transitions**:

1. **Initialize**: Load reference data, set current_page=1, empty prediction_inputs
2. **Navigate Next**: Increment current_page, preserve prediction_inputs
3. **Navigate Previous**: Decrement current_page, preserve prediction_inputs
4. **Reset**: Clear prediction_inputs, set current_page=1, clear last_prediction
5. **Submit Prediction**: Call API, set last_prediction, remain on page 6
6. **Field Update**: Update prediction_inputs[field], recompute is_form_complete

**Validation Logic**:
```python
def is_form_complete(prediction_inputs):
    required_fields = ["dep", "lum", "atm", "catr", "agg", "int", "circ",
                       "col", "vma_bucket", "catv_family_4", "manv_mode",
                       "driver_age_bucket", "choc_mode", "driver_trajet_family", "time_bucket"]
    return all(field in prediction_inputs and prediction_inputs[field] is not None
               for field in required_fields)
```

---

## State Machine: Multi-Page Navigation

**States**: Pages 1-6

**Transitions**:

```
[Page 1] --Suivant--> [Page 2] --Suivant--> [Page 3] --Suivant--> [Page 4]
  ^                     |                      |                      |
  |                     v                      v                      v
[Reset]            [Page 1]<--Précédent    [Page 2]<--Précédent   [Page 3]<--Précédent

[Page 4] --Suivant--> [Page 5] --Suivant--> [Page 6]
  |                      |                      |
  v                      v                      |
[Page 3]<--Précédent [Page 4]<--Précédent    [API Call] --> [Show Result] --> [Reset or Retry]
```

**Constraints**:
- Précédent button disabled on Page 1
- Suivant button always enabled (allow partial progress)
- Prédire button on Page 6 disabled if `is_form_complete == False`
- Reset button available on all pages

---

## Data Validation Strategy

### Client-Side (Streamlit)

**Level 1: Dropdown Constraints**
- Only valid options available in dropdowns (enforced by ReferenceData)
- User cannot select invalid code

**Level 2: Form Completeness**
- Check all 15 fields filled before enabling "Prédire" button
- Show missing field indicators on Page 6 recap

**Level 3: Pre-Submission Validation**
- Validate field types match expected (redundant, but defensive)
- Catch any edge cases before API call

### Server-Side (FastAPI)

**Level 4: Pydantic Model Validation**
- FastAPI backend validates with Pydantic models
- Returns 422 with field-level errors if invalid

**Redundancy Justification**: Client-side validation prevents unnecessary API calls and improves UX (immediate feedback). Server-side validation is security/integrity layer (never trust client).

---

## Error Handling

### Validation Errors

**Source**: Client-side or API 422 response

**Display**:
- Field-level error messages (red text below field)
- Summary message on Page 6: "Veuillez corriger les erreurs avant de soumettre"

**Example**:
```python
validation_errors = {
    "lum": "Valeur invalide. Choisissez parmi: 1-5",
    "time_bucket": "Tranche horaire invalide (attendu: night_00_05, morning_06_11, afternoon_12_17, evening_18_23)"
}
```

### API Errors

**Connection Error** (timeout, network failure):
```python
error_message = "Service temporairement indisponible, veuillez réessayer dans quelques instants."
display_type = "error"  # Red alert box
```

**Server Error** (500):
```python
error_message = "Une erreur s'est produite lors de la prédiction. Veuillez réessayer."
display_type = "error"
log_details = True  # Log for debugging
```

**Unknown Data Combination**:
```python
warning_message = "Attention: Cette combinaison de variables est rare. Le niveau de confiance peut être affecté."
display_type = "warning"  # Orange alert box
```

---

## Data Persistence

**Session Scope**: Data persists only during active Streamlit session

**No Persistence**:
- No database
- No file storage
- No browser local storage

**Justification**: Constitution assumption #8 (pas de données sensibles) + out-of-scope item (historique des prédictions)

**Session Cleanup**: Data cleared when:
- User clicks "Nouvelle prédiction" (explicit reset)
- User closes browser tab (automatic session end)
- Server restarts (all sessions lost)

---

## Reference Data Generation

**Source**: `data_dictionary_catboost_product15.md`

**Process**:
1. Parse markdown file to extract code tables
2. Transform to JSON structure (ReferenceData format)
3. Save to `data/ref_options.json`
4. Version control JSON file with repository

**Automation** (optional future enhancement):
```bash
# Script to regenerate ref_options.json from data dictionary
python scripts/generate_ref_options.py \
  --input data_dictionary_catboost_product15.md \
  --output data/ref_options.json
```

---

## Compliance Mapping

### Constitution Principle I: Data Quality First

✅ **User input conforms to data dictionary**:
- All codes validated against `data_dictionary_catboost_product15.md`
- ReferenceData loaded from centralized JSON
- Client-side validation before API submission

✅ **Invalid codes rejected with clear error messages**:
- Dropdown constraints prevent invalid selection
- Validation errors show field-specific messages

### Functional Requirements

- **FR-001**: PredictionInput entity covers all 15 variables
- **FR-002**: SessionState.is_form_complete validates all fields
- **FR-006**: Loading indicator during API call (not in data model, but UX requirement)
- **FR-010**: Page 6 recap uses prediction_inputs dict to generate summary table
- **FR-013**: ReferenceData loaded from JSON (US-10 requirement)

### UI/UX Requirements

- **UIX-001**: PredictionInput defines all 15 fields
- **UIX-003**: ReferenceData.option format includes "code — libellé"
- **UIX-012**: PredictionResult includes all display elements (probability, class, threshold)

---

## Next Steps

1. Implement Pydantic models in `streamlit_lib/models.py`
2. Create `data/ref_options.json` from data dictionary
3. Implement `streamlit_lib/reference_loader.py` to load ReferenceData
4. Implement `streamlit_lib/session_state.py` for state management helpers
5. Implement `streamlit_lib/validation.py` for client-side validation logic
