# Implementation Plan: Interface de Prédiction de Gravité d'Accidents

**Branch**: `001-streamlit-prediction-ui` | **Date**: 2026-01-30 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-streamlit-prediction-ui/spec.md`

**Note**: This plan follows the constitution-driven development workflow defined in `.specify/memory/constitution.md`

## Summary

Build a Streamlit web interface for accident severity prediction that allows users to input 15 variables across 6 thematic pages, validate inputs comprehensively, and display predictions (grave/non-grave) with confidence scores. The interface connects to an existing FastAPI backend, enforces data quality through dropdown-only inputs with "code — libellé" format, and provides contextual help for all fields based on `data_dictionary_catboost_product15.md`.

**Technical Approach**: Multi-page Streamlit application using session state for navigation, centralized JSON reference for dropdown options, client-side validation before API calls, and visual feedback throughout the user journey.

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**:
- Streamlit (>=1.19.0) - multi-page UI framework
- Requests - HTTP client for FastAPI backend
- Pydantic (>=2.12.5) - input validation models

**Storage**: N/A (session state only, no persistence)
**Testing**: pytest (unit tests for validation logic, integration tests for API interaction)
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge) on tablets and desktops
**Project Type**: Web - Streamlit frontend
**Performance Goals**: <5 seconds response time for 95% of predictions (including API call)
**Constraints**:
- <100 concurrent users (moderate load)
- Responsive design for tablets/desktops (mobile-friendly but not optimized)
- Read-only access to existing FastAPI `/predict` endpoint

**Scale/Scope**: Single Streamlit application with ~6 pages, 15 input fields, validation for ~200+ dropdown options total

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Data Quality First ✅ PASS

- **Requirement**: User input MUST conform to `data_dictionary_catboost_product15.md`
- **Implementation**: All 15 fields use dropdowns with options loaded from centralized JSON reference
- **Validation**: Client-side validation before API submission (100% validation, FR-015)
- **Compliance**: No free-text input (except search within dep dropdown), all codes validated against reference

### Principle II: Model Reproducibility ✅ PASS

- **Requirement**: Environment dependencies MUST be pinned
- **Implementation**: Use existing `pyproject.toml` + `uv.lock` for dependency management
- **Compliance**: No new model artifacts - interface consumes existing `catboost_product15.cbm` via API

### Principle III: API-First Architecture ✅ PASS

- **Requirement**: Streamlit UI MUST connect to FastAPI backend (never load models directly)
- **Implementation**: All predictions via HTTP POST to FastAPI `/predict` endpoint
- **Environment Config**: API URL configurable via `API_URL` environment variable
- **Compliance**: Streamlit app is pure client - no model loading, all business logic in API

### Principle IV: Test-First Development ⚠️ CONDITIONAL

- **Requirement**: TDD mandatory - tests written → user approved → tests fail → then implement
- **Status**: Conditional on user approval
- **Plan**: Contract tests for API schema validation, integration tests for end-to-end flows
- **Note**: Will generate tests in `/speckit.tasks` phase after plan approval

### Principle V: Simplicity & Observability ✅ PASS

- **Requirement**: Streamlit apps MUST remain simple - complex logic belongs in API layer
- **Implementation**:
  - Streamlit handles only: UI rendering, navigation, dropdown population, API calls
  - No business logic in Streamlit (validation logic is data quality, not business logic)
  - Logging for requests (timestamp, status, response time - US-12)
- **Compliance**: YAGNI principle - multi-page form is simplest solution for 15 fields

**GATE RESULT**: ✅ **PASS** - All principles satisfied with one conditional (TDD pending user approval for test generation)

## Project Structure

### Documentation (this feature)

```text
specs/001-streamlit-prediction-ui/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification (already created)
├── research.md          # Phase 0 output (technology choices, best practices)
├── data-model.md        # Phase 1 output (data structures, validation rules)
├── quickstart.md        # Phase 1 output (how to run the interface)
├── contracts/           # Phase 1 output (API contracts, JSON reference schema)
│   ├── api-predict.md   # FastAPI /predict endpoint contract
│   └── ref-schema.json  # JSON schema for reference data
├── checklists/          # Validation checklists
│   └── requirements.md  # Spec quality checklist (already created)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
streamlit_app.py         # Main Streamlit application (existing file to be enhanced)

# New structure to be created:
streamlit_pages/         # Multi-page Streamlit application
├── __init__.py
├── 1_Contexte_Route.py  # Page 1: dep, agg, catr, vma_bucket
├── 2_Infrastructure.py  # Page 2: int, circ
├── 3_Collision.py       # Page 3: col, choc_mode, manv_mode
├── 4_Conducteur.py      # Page 4: driver_age_bucket, driver_trajet_family
├── 5_Conditions.py      # Page 5: lum, atm, minute
└── 6_Recap_Prediction.py # Page 6: summary table + predict button

streamlit_lib/           # Shared utilities for Streamlit app
├── __init__.py
├── reference_loader.py  # Load dropdown options from JSON
├── validation.py        # Client-side validation logic
├── api_client.py        # HTTP client for FastAPI backend
└── session_state.py     # Session state management helpers

data/                    # Reference data (existing)
├── ref_options.json     # NEW: Centralized dropdown options
└── data_dictionary_catboost_product15.md  # Existing reference

tests/                   # Test suite
├── __init__.py
├── integration/         # Integration tests
│   └── test_prediction_flow.py
└── unit/                # Unit tests
    ├── test_validation.py
    └── test_reference_loader.py
```

**Structure Decision**: Web application structure with Streamlit as frontend client. Multi-page Streamlit app pattern (native Streamlit pages/ folder) chosen over single-page tabs for better navigation UX and clearer separation of concerns. Shared utilities in `streamlit_lib/` for reusability across pages. No backend code changes needed - interface is pure consumer of existing FastAPI service.

## Complexity Tracking

> **No violations - this section is empty**

All constitution principles are satisfied without requiring complexity justifications.

## Phase 0: Research & Technology Choices

**Status**: ✅ COMPLETED (inline - no unknowns)

All technical decisions are clear from the constitution and project context:

### Decision Log

#### Multi-Page Architecture

**Decision**: Use Streamlit's native multi-page apps (`pages/` folder pattern)

**Rationale**:
- Native Streamlit support since v1.10.0+
- Automatic sidebar navigation
- Clean URL routing (`?page=X`)
- Simpler than tabs or manual state management

**Alternatives Considered**:
- Single page with `st.tabs()`: Rejected - harder to manage 6 distinct forms, poor UX for complex flows
- Manual routing with URL parameters: Rejected - over-engineering, native solution exists

#### Reference Data Loading

**Decision**: Load dropdown options from centralized JSON file (`data/ref_options.json`)

**Rationale**:
- Single source of truth per US-10
- Easy to update without code changes
- Supports constitution principle (data quality)
- Can be generated from `data_dictionary_catboost_product15.md`

**Alternatives Considered**:
- Hardcode in Python: Rejected - violates single source of truth, hard to maintain
- Load from API: Rejected - unnecessary API dependency, slower, defeats client-side validation

#### Session State Management

**Decision**: Use Streamlit `st.session_state` for preserving selections across pages

**Rationale**:
- Native Streamlit feature (>=0.84.0)
- Automatic persistence during session
- Simple dict-like interface
- No external dependencies needed

**Alternatives Considered**:
- URL query parameters: Rejected - 15 fields = unwieldy URLs, poor UX
- Local storage (JS): Rejected - requires custom components, over-engineering

#### API Client Pattern

**Decision**: Simple `requests` library with retry logic

**Rationale**:
- Standard Python HTTP library
- Already in dependencies
- Sufficient for single endpoint calls
- Easy error handling

**Alternatives Considered**:
- httpx: Rejected - async not needed for Streamlit (sync framework)
- Custom SDK: Rejected - over-engineering for single endpoint

**Output**: No separate research.md needed - all decisions documented above

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions.

**Key Entities**:

1. **PredictionInput** (Pydantic model):
   - 15 fields matching `data_dictionary_catboost_product15.md`
   - Field types: str (dep, vma_bucket, catv_family_4, driver_age_bucket, driver_trajet_family), int (lum, atm, catr, agg, int, circ, col, manv_mode, choc_mode, minute)
   - Validation: Enum constraints for coded fields, range (0-59) for minute

2. **PredictionResult** (Pydantic model):
   - probability: float (0.0-1.0)
   - prediction: Literal["grave", "non_grave"]
   - threshold: float (0.47)
   - inputs_summary: dict (echo of 15 input fields)

3. **ReferenceData** (dict structure):
   - Keyed by field name (e.g., "lum", "atm")
   - Values: list of options [{code, label}]
   - Example: `{"lum": [{"code": 1, "label": "Plein jour"}, ...]}`

4. **SessionState** (Streamlit state):
   - current_page: int (1-6)
   - input_fields: dict (15 field values)
   - last_prediction: PredictionResult | None
   - validation_errors: dict[str, str]

### API Contracts

See [contracts/](contracts/) for OpenAPI schema and detailed contracts.

**Endpoint**: `POST /predict`

**Request**:
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
  "minute": 30
}
```

**Response** (Success - 200):
```json
{
  "probability": 0.68,
  "prediction": "grave",
  "threshold": 0.47
}
```

**Response** (Validation Error - 422):
```json
{
  "detail": [
    {
      "loc": ["body", "lum"],
      "msg": "value must be one of [1, 2, 3, 4, 5]",
      "type": "value_error.const"
    }
  ]
}
```

**Response** (Server Error - 500):
```json
{
  "detail": "Internal server error"
}
```

### Quickstart

See [quickstart.md](quickstart.md) for complete setup and run instructions.

**Quick Run**:
```bash
# 1. Ensure FastAPI backend is running
uv run uvicorn predictor:app --host 0.0.0.0 --port 8000 --reload

# 2. In another terminal, run Streamlit interface
API_URL=http://localhost:8000 uv run streamlit run streamlit_app.py
```

## Implementation Notes

### Multi-Page Navigation Flow

1. User clicks "Nouvelle prédiction" → resets session state, navigates to page 1
2. Each page (1-5) shows relevant fields + "Précédent"/"Suivant" buttons
3. Page 6 shows recap table + "Prédire" button (disabled if fields missing)
4. After prediction, results shown on page 6 with option to start new prediction

### Validation Strategy

**Client-Side (Streamlit)**:
- Check all 15 fields filled before enabling "Prédire" button
- Show field-level errors if invalid selection attempted
- Prevent API call if validation fails

**Server-Side (FastAPI)**:
- Pydantic model validation (redundant safety)
- Return 422 with field-specific errors if validation fails

### Error Handling

- API unavailable (timeout, connection error): Show user-friendly message "Service temporairement indisponible, veuillez réessayer"
- API returns 422: Parse error details and show field-level messages
- API returns 500: Show generic error message + log details for debugging
- Network timeout: 10 second timeout, then error message

### Logging Requirements (US-12)

Log each prediction request:
- Timestamp (ISO 8601)
- Status code (200/422/500/timeout)
- Response time (ms)
- Model version (from API response metadata if available)
- **Do NOT log**: User input values (privacy/GDPR)

Example log:
```
2026-01-30T14:32:15Z | POST /predict | 200 | 245ms | model_v1.0.0
```

## Next Steps

1. ✅ **Plan approval**: Review this implementation plan
2. **Generate tasks**: Run `/speckit.tasks` to create dependency-ordered tasks from this plan
3. **Test-first**: Write tests for each user story before implementation
4. **Implement**: Follow tasks in priority order (P1 → P2 → P3)
5. **Validate**: Ensure all success criteria met (SC-001 to SC-009)

## Compliance Verification

✅ All functional requirements (FR-001 to FR-015) have implementation approach
✅ All UI/UX requirements (UIX-001 to UIX-018) addressed in multi-page design
✅ All success criteria (SC-001 to SC-009) are achievable with planned architecture
✅ Constitution principles respected throughout
✅ No complexity violations requiring justification
