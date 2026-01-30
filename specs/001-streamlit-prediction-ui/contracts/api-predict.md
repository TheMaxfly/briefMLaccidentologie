# API Contract: POST /predict

**Feature**: `001-streamlit-prediction-ui`
**Created**: 2026-01-30
**Purpose**: Define the contract for the FastAPI prediction endpoint consumed by the Streamlit interface

## Endpoint

**URL**: `/predict`
**Method**: `POST`
**Content-Type**: `application/json`
**Authentication**: None (public endpoint)

## Request Schema

### Headers

```http
POST /predict HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Accept: application/json
```

### Body (JSON)

**Type**: `PredictionInput` (Pydantic model)

**Required Fields** (all 15 variables):

```json
{
  "dep": "string",           // Département (code INSEE, e.g., "59", "75", "2A", "971")
  "lum": integer,            // Luminosité (1-5)
  "atm": integer,            // Conditions atmosphériques (-1 or 1-9)
  "catr": integer,           // Catégorie de route (1-7, 9)
  "agg": integer,            // Agglomération (1-2)
  "int": integer,            // Type d'intersection (1-9)
  "circ": integer,           // Régime de circulation (-1 or 1-4)
  "col": integer,            // Type de collision (-1 or 1-7)
  "vma_bucket": "string",    // Classe de VMA ("<=30", "31-50", ..., "inconnue")
  "catv_family_4": "string", // Famille de véhicule (4 classes)
  "manv_mode": integer,      // Manœuvre (-1 or 0-26)
  "driver_age_bucket": "string",      // Classe d'âge ("<18", "18-24", ..., "unknown")
  "choc_mode": integer,      // Point de choc (-1 or 0-9)
  "driver_trajet_family": "string",   // Famille de trajet ("trajet_1", ..., "unknown")
  "time_bucket": "string"    // Tranche horaire ("night_00_05", "morning_06_11", "afternoon_12_17", "evening_18_23")
}
```

### Example Request

```json
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

## Response Schemas

### Success Response (200 OK)

**Type**: `PredictionResult` (Pydantic model)

**Fields**:

```json
{
  "probability": float,      // Probabilité d'accident grave (0.0-1.0)
  "prediction": "string",    // Classe prédite ("grave" | "non_grave")
  "threshold": float         // Seuil de décision appliqué (0.47)
}
```

**Example**:

```json
{
  "probability": 0.68,
  "prediction": "grave",
  "threshold": 0.47
}
```

**Rules**:
- `prediction = "grave"` if `probability >= 0.47`, else `"non_grave"`
- `threshold` is always `0.47` (as per data dictionary)

### Validation Error Response (422 Unprocessable Entity)

**Type**: FastAPI ValidationError

**Fields**:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

**Example**:

```json
{
  "detail": [
    {
      "loc": ["body", "lum"],
      "msg": "value must be one of [1, 2, 3, 4, 5]",
      "type": "value_error.const"
    },
    {
      "loc": ["body", "time_bucket"],
      "msg": "ensure this value is less than or equal to 59",
      "type": "value_error.number.not_le"
    }
  ]
}
```

**Common Validation Errors**:

| Field | Error | Message |
|-------|-------|---------|
| `lum` | Invalid code | "value must be one of [1, 2, 3, 4, 5]" |
| `dep` | Unknown department | "value is not a valid department code" |
| `time_bucket` | Invalid value | "value is not a valid enumeration member" |
| `vma_bucket` | Invalid bucket | "value must be one of ['<=30', '31-50', ...]" |
| (any) | Missing field | "field required" |

### Server Error Response (500 Internal Server Error)

**Type**: Generic error

**Fields**:

```json
{
  "detail": "string"
}
```

**Example**:

```json
{
  "detail": "Model inference failed"
}
```

**Causes**:
- Model loading failure
- Inference error
- Unexpected exception

## Field Validation Rules

### String Fields

| Field | Valid Values | Example |
|-------|-------------|---------|
| `dep` | 107 department codes (see data dictionary) | "59", "75", "2A", "971" |
| `vma_bucket` | `["<=30", "31-50", "51-80", "81-90", "91-110", "111-130", ">130", "inconnue"]` | "51-80" |
| `catv_family_4` | `["voitures_utilitaires", "2rm_3rm", "lourds_tc_agri_autres", "vulnerables"]` | "voitures_utilitaires" |
| `driver_age_bucket` | `["<18", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+", "unknown"]` | "25-34" |
| `driver_trajet_family` | `["trajet_1", "trajet_2", "trajet_3", "trajet_4", "trajet_5", "trajet_9", "unknown"]` | "trajet_1" |

### Integer Fields

| Field | Valid Values | Description |
|-------|-------------|-------------|
| `lum` | `[1, 2, 3, 4, 5]` | Luminosité |
| `atm` | `[-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]` | Conditions atmosphériques |
| `catr` | `[1, 2, 3, 4, 5, 6, 7, 9]` | Catégorie de route |
| `agg` | `[1, 2]` | Agglomération |
| `int` | `[1, 2, 3, 4, 5, 6, 7, 8, 9]` | Type d'intersection |
| `circ` | `[-1, 1, 2, 3, 4]` | Régime de circulation |
| `col` | `[-1, 1, 2, 3, 4, 5, 6, 7]` | Type de collision |
| `manv_mode` | `[-1, 0, 1, 2, ..., 26]` | Manœuvre (mode) |
| `choc_mode` | `[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]` | Point de choc (mode) |
| `time_bucket` | `night_00_05`, `morning_06_11`, `afternoon_12_17`, `evening_18_23` | Tranche horaire |

## Environment Configuration

**Environment Variable**: `API_URL`

**Default**: `http://localhost:8000`

**Usage in Streamlit**:

```python
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")
PREDICT_ENDPOINT = f"{API_URL}/predict"
```

**Deployment Examples**:

```bash
# Development
API_URL=http://localhost:8000 streamlit run streamlit_app.py

# Staging
API_URL=https://staging-api.example.com streamlit run streamlit_app.py

# Production
API_URL=https://api.example.com streamlit run streamlit_app.py
```

## Error Handling Strategy

### Client-Side (Streamlit)

```python
import requests
from requests.exceptions import RequestException, Timeout

def call_predict_api(inputs):
    try:
        response = requests.post(
            PREDICT_ENDPOINT,
            json=inputs,
            timeout=10  # 10 second timeout
        )
        response.raise_for_status()
        return response.json()

    except Timeout:
        return {
            "error": "timeout",
            "message": "Le service met trop de temps à répondre. Veuillez réessayer."
        }

    except RequestException as e:
        if e.response and e.response.status_code == 422:
            # Validation error - parse details
            return {
                "error": "validation",
                "details": e.response.json()["detail"]
            }
        elif e.response and e.response.status_code >= 500:
            # Server error
            return {
                "error": "server",
                "message": "Une erreur s'est produite côté serveur. Veuillez réessayer."
            }
        else:
            # Network/connection error
            return {
                "error": "network",
                "message": "Service temporairement indisponible. Veuillez réessayer."
            }
```

## Testing

### Contract Test (Pytest)

```python
import pytest
import requests

API_URL = "http://localhost:8000"

def test_predict_endpoint_success():
    """Test successful prediction with valid inputs"""
    payload = {
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

    response = requests.post(f"{API_URL}/predict", json=payload)
    assert response.status_code == 200

    result = response.json()
    assert "probability" in result
    assert "prediction" in result
    assert "threshold" in result
    assert 0.0 <= result["probability"] <= 1.0
    assert result["prediction"] in ["grave", "non_grave"]
    assert result["threshold"] == 0.47


def test_predict_endpoint_validation_error():
    """Test validation error with invalid lum code"""
    payload = {
        "dep": "59",
        "lum": 99,  # Invalid code
        # ... rest of valid fields
    }

    response = requests.post(f"{API_URL}/predict", json=payload)
    assert response.status_code == 422

    error = response.json()
    assert "detail" in error
    assert any(err["loc"] == ["body", "lum"] for err in error["detail"])


def test_predict_endpoint_missing_field():
    """Test validation error with missing required field"""
    payload = {
        "dep": "59",
        # Missing lum and other fields
    }

    response = requests.post(f"{API_URL}/predict", json=payload)
    assert response.status_code == 422
```

## Compliance

### Constitution Principle III: API-First Architecture ✅

- **Requirement**: Streamlit UI MUST connect to FastAPI backend
- **Implementation**: All predictions via HTTP POST to `/predict`
- **Validation**: No model loading in Streamlit - pure API consumer

### Functional Requirements

- **FR-003**: Interface sends data to API via this contract
- **FR-004**: Response includes probability and class
- **FR-005**: Threshold 0.47 applied in response
- **FR-007**: 422/500 errors handled with clear messages

### Data Dictionary Compliance

All 15 fields match exactly:
- Field names: Exact match with `data_dictionary_catboost_product15.md`
- Field types: Correct types (int vs str)
- Value ranges: Validated against BAAC nomenclature
- Threshold: 0.47 as specified in data dictionary

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-01-30 | 1.0.0 | Initial contract definition |
