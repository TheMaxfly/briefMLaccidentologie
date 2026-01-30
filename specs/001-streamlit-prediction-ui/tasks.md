# Tasks: Interface de Prédiction de Gravité d'Accidents

**Input**: Design documents from `/specs/001-streamlit-prediction-ui/`
**Prerequisites**: plan.md (✅), spec.md (✅), data-model.md (✅), contracts/ (✅)

**Tests**: This feature follows TDD approach - test tasks are included and MUST be written before implementation per constitution principle IV.

**Organization**: Tasks are grouped by user story (US-01 to US-12) to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3...)
- Include exact file paths in descriptions

## Path Conventions

- **Streamlit app**: `streamlit_app.py`, `streamlit_pages/`, `streamlit_lib/` at repository root
- **Reference data**: `data/ref_options.json`
- **Tests**: `tests/integration/`, `tests/unit/`
- Paths shown below use absolute file paths from project root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create streamlit_pages directory with __init__.py
- [ ] T002 Create streamlit_lib directory with __init__.py
- [ ] T003 [P] Create tests/integration directory with __init__.py
- [ ] T004 [P] Create tests/unit directory with __init__.py
- [ ] T005 [P] Create data directory if not exists

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Reference Data Generation

- [ ] T006 Generate data/ref_options.json from data_dictionary_catboost_product15.md with all 15 fields (107 dep codes, lum 1-5, atm -1/1-9, etc.)

### Core Shared Modules

- [ ] T007 [P] Create streamlit_lib/models.py with PredictionInput and PredictionResult Pydantic models per data-model.md
- [ ] T008 [P] Create streamlit_lib/reference_loader.py with load_reference_data() function to load and validate data/ref_options.json
- [ ] T009 [P] Create streamlit_lib/session_state.py with helper functions for session state management (initialize_state, get_current_page, etc.)
- [ ] T010 [P] Create streamlit_lib/api_client.py with call_predict_api() function using requests library with 10s timeout
- [ ] T011 [P] Create streamlit_lib/validation.py with is_form_complete() and validate_field() functions

### Contract Tests (TDD - MUST FAIL before API exists)

- [ ] T012 [P] Write contract test in tests/integration/test_api_contract.py for POST /predict endpoint (valid request → 200 OK)
- [ ] T013 [P] Write contract test in tests/integration/test_api_contract.py for validation error (invalid lum → 422)
- [ ] T014 [P] Write contract test in tests/integration/test_api_contract.py for missing field error (missing dep → 422)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: EPIC 1 - User Story 1 (US-01) - Démarrer une nouvelle prédiction 🎯 MVP

**Goal**: User can click "Nouvelle prédiction" button to reset form and see progress indicator

**Independent Test**: User clicks "Nouvelle prédiction", sees all fields cleared, and progress shows "Page 1/6"

**Priority**: P1 (MVP - blocking for all other stories)

### Tests for US-01 (TDD - write and verify FAIL before implementation)

- [ ] T015 [P] [US1] Write integration test in tests/integration/test_us01_reset.py for "Nouvelle prédiction" button clears all session state
- [ ] T016 [P] [US1] Write integration test in tests/integration/test_us01_reset.py for progress indicator displays "Page 1/6" after reset

### Implementation for US-01

- [ ] T017 [US1] Update streamlit_app.py to load reference data on init using reference_loader.load_reference_data()
- [ ] T018 [US1] Add "Nouvelle prédiction" button in streamlit_app.py sidebar that resets session_state and navigates to page 1
- [ ] T019 [US1] Add progress indicator in streamlit_app.py sidebar showing "Page X/6" using st.session_state.current_page
- [ ] T020 [US1] Verify tests pass: run pytest tests/integration/test_us01_reset.py

**Checkpoint**: US-01 complete and testable - user can reset form and see progress

---

## Phase 4: EPIC 1 - User Story 2 (US-02) - Saisie multi-pages claire (Priority: P1)

**Goal**: User navigates through 6 pages with Précédent/Suivant buttons, fields grouped logically

**Independent Test**: User can navigate from Page 1 to Page 6 and back, selections are preserved, all fields are dropdowns

**Priority**: P1 (Core navigation - required for MVP)

### Tests for US-02 (TDD)

- [ ] T021 [P] [US2] Write integration test in tests/integration/test_us02_navigation.py for navigation Page 1→2→3→4→5→6 preserves selections
- [ ] T022 [P] [US2] Write integration test in tests/integration/test_us02_navigation.py for Précédent button disabled on Page 1
- [ ] T023 [P] [US2] Write integration test in tests/integration/test_us02_navigation.py for all fields are dropdowns (no text inputs except dep search)

### Implementation for US-02

- [ ] T024 [P] [US2] Create streamlit_pages/1_Contexte_Route.py with dropdowns for dep, agg, catr, vma_bucket + Suivant button
- [ ] T025 [P] [US2] Create streamlit_pages/2_Infrastructure.py with dropdowns for int, circ + Précédent/Suivant buttons
- [ ] T026 [P] [US2] Create streamlit_pages/3_Collision.py with dropdowns for col, choc_mode, manv_mode + Précédent/Suivant buttons
- [ ] T027 [P] [US2] Create streamlit_pages/4_Conducteur.py with dropdowns for driver_age_bucket, driver_trajet_family + Précédent/Suivant buttons
- [ ] T028 [P] [US2] Create streamlit_pages/5_Conditions.py with dropdowns for lum, atm, minute + Précédent/Suivant buttons
- [ ] T029 [US2] Create streamlit_pages/6_Recap_Prediction.py with summary table placeholder + disabled "Prédire" button
- [ ] T030 [US2] Implement navigation logic in each page: Précédent decrements current_page, Suivant increments current_page
- [ ] T031 [US2] Implement session state preservation: each page saves selections to st.session_state.prediction_inputs
- [ ] T032 [US2] Verify tests pass: run pytest tests/integration/test_us02_navigation.py

**Checkpoint**: US-02 complete - user can navigate all 6 pages with preserved state

---

## Phase 5: EPIC 1 - User Story 3 (US-03) - Affichage "Code + Libellé" (Priority: P1)

**Goal**: Every dropdown displays "code — libellé" format (e.g., "1 — Plein jour")

**Independent Test**: User opens any dropdown and sees all options formatted as "code — libellé"

**Priority**: P1 (Data quality requirement from constitution)

### Tests for US-03 (TDD)

- [ ] T033 [P] [US3] Write unit test in tests/unit/test_dropdown_format.py for reference_loader formats options as "code — libellé"
- [ ] T034 [P] [US3] Write integration test in tests/integration/test_us03_dropdown_display.py for lum dropdown shows "1 — Plein jour"

### Implementation for US-03

- [ ] T035 [US3] Update streamlit_lib/reference_loader.py to add format_dropdown_option(code, label) → "code — libellé" function
- [ ] T036 [P] [US3] Update streamlit_pages/1_Contexte_Route.py dropdowns to use format_dropdown_option for all 4 fields
- [ ] T037 [P] [US3] Update streamlit_pages/2_Infrastructure.py dropdowns to use format_dropdown_option for all 2 fields
- [ ] T038 [P] [US3] Update streamlit_pages/3_Collision.py dropdowns to use format_dropdown_option for all 3 fields
- [ ] T039 [P] [US3] Update streamlit_pages/4_Conducteur.py dropdowns to use format_dropdown_option for all 2 fields
- [ ] T040 [P] [US3] Update streamlit_pages/5_Conditions.py dropdowns to use format_dropdown_option for all 3 fields
- [ ] T041 [US3] Verify tests pass: run pytest tests/unit/test_dropdown_format.py tests/integration/test_us03_dropdown_display.py

**Checkpoint**: US-03 complete - all dropdowns display standardized "code — libellé" format

---

## Phase 6: EPIC 1 - User Story 4 (US-04) - Valeurs "Non renseigné" (Priority: P2)

**Goal**: User can select "Non renseigné" option for fields that support it

**Independent Test**: User selects "Non renseigné" for atm field, API receives -1

**Priority**: P2 (Flexibility feature - not blocking for basic MVP)

### Tests for US-04 (TDD)

- [ ] T042 [P] [US4] Write integration test in tests/integration/test_us04_not_specified.py for atm "-1 — Non renseigné" selection → API receives -1

### Implementation for US-04

- [ ] T043 [P] [US4] Verify data/ref_options.json includes "-1 — Non renseigné" for atm, circ, col fields per data dictionary
- [ ] T044 [P] [US4] Verify minute dropdown includes "-1 — Non renseigné" option in streamlit_pages/5_Conditions.py
- [ ] T045 [US4] Verify tests pass: run pytest tests/integration/test_us04_not_specified.py

**Checkpoint**: US-04 complete - user can select "Non renseigné" where applicable

---

## Phase 7: EPIC 2 - User Story 5 (US-05) - Validation "15 champs requis" (Priority: P1)

**Goal**: "Prédire" button is disabled until all 15 fields are filled, clear message shows missing fields

**Independent Test**: User with 14/15 fields filled sees disabled button + message "Page 5: minute non renseigné"

**Priority**: P1 (Data quality gate - critical for constitution compliance)

### Tests for US-05 (TDD)

- [ ] T046 [P] [US5] Write unit test in tests/unit/test_validation.py for is_form_complete() returns False with 14/15 fields
- [ ] T047 [P] [US5] Write unit test in tests/unit/test_validation.py for is_form_complete() returns True with all 15 fields
- [ ] T048 [P] [US5] Write integration test in tests/integration/test_us05_validation.py for disabled "Prédire" button when fields missing

### Implementation for US-05

- [ ] T049 [US5] Implement is_form_complete() in streamlit_lib/validation.py to check all 15 fields in prediction_inputs
- [ ] T050 [US5] Implement get_missing_fields() in streamlit_lib/validation.py to return list of missing fields with page numbers
- [ ] T051 [US5] Update streamlit_pages/6_Recap_Prediction.py to disable "Prédire" button if not is_form_complete()
- [ ] T052 [US5] Add missing fields message in streamlit_pages/6_Recap_Prediction.py showing "Page X: field_name non renseigné"
- [ ] T053 [US5] Verify tests pass: run pytest tests/unit/test_validation.py tests/integration/test_us05_validation.py

**Checkpoint**: US-05 complete - validation prevents incomplete submissions

---

## Phase 8: EPIC 2 - User Story 6 (US-06) - Validation minute dropdown (Priority: P1)

**Goal**: Minute field is dropdown 0-59 (+ "Non renseigné"), no text input possible

**Independent Test**: User cannot type text in minute field, can only select from dropdown

**Priority**: P1 (Prevents common data quality errors)

### Tests for US-06 (TDD)

- [ ] T054 [P] [US6] Write integration test in tests/integration/test_us06_minute_dropdown.py for minute field is selectbox, not text_input

### Implementation for US-06

- [ ] T055 [US6] Verify streamlit_pages/5_Conditions.py minute field uses st.selectbox (not st.number_input or st.text_input)
- [ ] T056 [US6] Verify data/ref_options.json includes 61 minute options: -1, 0-59 with labels
- [ ] T057 [US6] Verify tests pass: run pytest tests/integration/test_us06_minute_dropdown.py

**Checkpoint**: US-06 complete - minute validation prevents format errors

---

## Phase 9: EPIC 3 - User Story 7 (US-07) - Probabilité + classe (seuil 0.47) (Priority: P1)

**Goal**: User sees prediction result with probability (0-1), classe (grave/non-grave), and threshold 0.47

**Independent Test**: User submits form → sees "Probabilité: 0.68", "Classe: grave", "Seuil: 0.47"

**Priority**: P1 (Core feature value - reason for interface existence)

### Tests for US-07 (TDD)

- [ ] T058 [P] [US7] Write integration test in tests/integration/test_us07_prediction.py for successful API call displays probability and class
- [ ] T059 [P] [US7] Write integration test in tests/integration/test_us07_prediction.py for probability ≥0.47 → class "grave"
- [ ] T060 [P] [US7] Write integration test in tests/integration/test_us07_prediction.py for probability <0.47 → class "non_grave"

### Implementation for US-07

- [ ] T061 [US7] Implement predict button handler in streamlit_pages/6_Recap_Prediction.py to call api_client.call_predict_api()
- [ ] T062 [US7] Add loading spinner during API call using st.spinner("Prédiction en cours...")
- [ ] T063 [US7] Display prediction result in streamlit_pages/6_Recap_Prediction.py with probability, class, threshold
- [ ] T064 [US7] Add visual styling: color-coded result (red for "grave", green for "non_grave")
- [ ] T065 [US7] Add interpretation text: "Accident grave détecté" or "Accident non-grave"
- [ ] T066 [US7] Verify tests pass: run pytest tests/integration/test_us07_prediction.py

**Checkpoint**: US-07 complete - core prediction functionality works end-to-end

---

## Phase 10: EPIC 3 - User Story 8 (US-08) - Récapitulatif des 15 champs (Priority: P2)

**Goal**: Page 6 shows summary table with all 15 fields (champ | code | libellé) before prediction

**Independent Test**: User on Page 6 sees table with 15 rows showing their selections

**Priority**: P2 (UX improvement - helps verify before submission)

### Tests for US-08 (TDD)

- [ ] T067 [P] [US8] Write integration test in tests/integration/test_us08_recap.py for Page 6 displays all 15 field selections in table

### Implementation for US-08

- [ ] T068 [US8] Implement generate_recap_table() in streamlit_lib/session_state.py to create DataFrame from prediction_inputs + reference_data
- [ ] T069 [US8] Update streamlit_pages/6_Recap_Prediction.py to display recap table using st.dataframe() before "Prédire" button
- [ ] T070 [US8] Add "Modifier" links in recap table that navigate back to appropriate page (e.g., "lum" → Page 5)
- [ ] T071 [US8] Verify tests pass: run pytest tests/integration/test_us08_recap.py

**Checkpoint**: US-08 complete - user can review selections before submitting

---

## Phase 11: EPIC 4 - User Story 9 (US-09) - Aide contextuelle par champ (Priority: P2)

**Goal**: Each field has info icon ("ℹ️") that shows definition + code table when clicked

**Independent Test**: User clicks "ℹ️" next to "lum" field → sees modal/expander with definition + table of codes 1-5

**Priority**: P2 (Accessibility for non-experts)

### Tests for US-09 (TDD)

- [ ] T072 [P] [US9] Write integration test in tests/integration/test_us09_help.py for info icon exists for each field
- [ ] T073 [P] [US9] Write unit test in tests/unit/test_reference_loader.py for get_field_help() returns definition + code table

### Implementation for US-09

- [ ] T074 [US9] Add field definitions to data/ref_options.json (or create separate help_text.json) with definition + examples per field
- [ ] T075 [US9] Implement get_field_help(field_name) in streamlit_lib/reference_loader.py to load help text
- [ ] T076 [P] [US9] Update streamlit_pages/1_Contexte_Route.py to add st.expander with help text below each field
- [ ] T077 [P] [US9] Update streamlit_pages/2_Infrastructure.py to add st.expander with help text below each field
- [ ] T078 [P] [US9] Update streamlit_pages/3_Collision.py to add st.expander with help text below each field
- [ ] T079 [P] [US9] Update streamlit_pages/4_Conducteur.py to add st.expander with help text below each field
- [ ] T080 [P] [US9] Update streamlit_pages/5_Conditions.py to add st.expander with help text below each field
- [ ] T081 [US9] Verify tests pass: run pytest tests/unit/test_reference_loader.py tests/integration/test_us09_help.py

**Checkpoint**: US-09 complete - contextual help available for all fields

---

## Phase 12: EPIC 4 - User Story 10 (US-10) - Référentiel JSON centralisé (Priority: P3)

**Goal**: All dropdown options loaded from centralized JSON file (no hardcoded options in code)

**Independent Test**: Developer updates data/ref_options.json with new code → interface reflects change without code modification

**Priority**: P3 (Architecture/maintainability - not user-facing)

### Tests for US-10 (TDD)

- [ ] T082 [P] [US10] Write unit test in tests/unit/test_reference_loader.py for load_reference_data() validates against JSON schema
- [ ] T083 [P] [US10] Write unit test in tests/unit/test_reference_loader.py for invalid JSON raises clear error

### Implementation for US-10

- [ ] T084 [US10] Validate data/ref_options.json against contracts/ref-schema.json using jsonschema library
- [ ] T085 [US10] Add schema validation in streamlit_lib/reference_loader.py load_reference_data() with clear error messages
- [ ] T086 [US10] Verify no hardcoded option lists exist in any streamlit_pages/*.py files (all use reference_data from session_state)
- [ ] T087 [US10] Verify tests pass: run pytest tests/unit/test_reference_loader.py

**Checkpoint**: US-10 complete - centralized reference data architecture validated

---

## Phase 13: EPIC 5 - User Story 11 (US-11) - Accessibilité et mobile-first (Priority: P2)

**Goal**: Dropdowns are usable on mobile (large touch targets), good contrast, responsive layout

**Independent Test**: Interface opens on tablet/mobile → dropdowns are tappable, text is readable

**Priority**: P2 (Extends audience but not blocking for desktop MVP)

### Tests for US-11 (TDD)

- [ ] T088 [P] [US11] Write visual regression test in tests/integration/test_us11_accessibility.py for mobile viewport (375px width)

### Implementation for US-11

- [ ] T089 [US11] Add Streamlit config in .streamlit/config.toml with theme.primaryColor and theme.backgroundColor for accessibility
- [ ] T090 [P] [US11] Review all streamlit_pages/*.py for st.selectbox usage - ensure no custom CSS that breaks mobile
- [ ] T091 [US11] Add viewport meta tag support (verify Streamlit default handles this)
- [ ] T092 [US11] Test manually on mobile device or Chrome DevTools mobile emulator
- [ ] T093 [US11] Verify tests pass: run pytest tests/integration/test_us11_accessibility.py

**Checkpoint**: US-11 complete - interface is mobile-friendly

---

## Phase 14: EPIC 5 - User Story 12 (US-12) - Observabilité minimale (Priority: P3)

**Goal**: Log each prediction request with timestamp, status, response time, model version (no user data)

**Independent Test**: Developer checks logs after prediction → sees timestamp, status code, latency

**Priority**: P3 (Ops/debugging - not user-facing)

### Tests for US-12 (TDD)

- [ ] T094 [P] [US12] Write unit test in tests/unit/test_api_client.py for call_predict_api() logs request metadata

### Implementation for US-12

- [ ] T095 [US12] Add logging.basicConfig in streamlit_app.py with INFO level and timestamp format
- [ ] T096 [US12] Update streamlit_lib/api_client.py call_predict_api() to log: timestamp, status code, response_time_ms
- [ ] T097 [US12] Ensure NO user input data is logged (only metadata: status, latency, model version if available)
- [ ] T098 [US12] Add example log output to quickstart.md showing expected format
- [ ] T099 [US12] Verify tests pass: run pytest tests/unit/test_api_client.py

**Checkpoint**: US-12 complete - observability logging in place

---

## Phase 15: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T100 [P] Add error handling in streamlit_pages/6_Recap_Prediction.py for API timeout (>10s) → "Service temporairement indisponible"
- [ ] T101 [P] Add error handling in streamlit_pages/6_Recap_Prediction.py for API 422 → parse field errors and display
- [ ] T102 [P] Add error handling in streamlit_pages/6_Recap_Prediction.py for API 500 → "Erreur serveur"
- [ ] T103 [P] Add search functionality in streamlit_pages/1_Contexte_Route.py for dep dropdown (107 codes) using st.text_input filter
- [ ] T104 Update quickstart.md with final run instructions and troubleshooting section
- [ ] T105 Run all tests: pytest tests/ --cov=streamlit_lib --cov-report=html
- [ ] T106 Manual end-to-end test: complete full flow from Page 1 to prediction result
- [ ] T107 Verify constitution compliance: all dropdowns, no model loading, API-only predictions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
  - T006 (ref_options.json) is critical - without it, no dropdowns work
  - T007-T011 (shared modules) are parallel but must all complete before user stories
- **User Stories (Phase 3-14)**: All depend on Foundational phase completion
  - **US-01 (Phase 3)**: BLOCKING for all other stories (provides navigation infrastructure)
  - **US-02 (Phase 4)**: Depends on US-01 (uses navigation + reset)
  - **US-03 (Phase 5)**: Depends on US-02 (enhances dropdowns created in US-02)
  - **US-04 (Phase 6)**: Independent of US-03, can run in parallel after US-02
  - **US-05 (Phase 7)**: Depends on US-02 (validates form created in US-02)
  - **US-06 (Phase 8)**: Independent of US-05, can run in parallel after US-02
  - **US-07 (Phase 9)**: Depends on US-05 (uses validation), Depends on US-02 (uses form)
  - **US-08 (Phase 10)**: Independent of US-07, depends on US-02
  - **US-09 (Phase 11)**: Independent of all, can run after US-02
  - **US-10 (Phase 12)**: Architecture validation, can run anytime after Foundational
  - **US-11 (Phase 13)**: Independent, can run after US-02
  - **US-12 (Phase 14)**: Independent, can run after US-07
- **Polish (Phase 15)**: Depends on all desired user stories being complete

### Critical Path (Minimum for MVP)

```
Setup → Foundational → US-01 → US-02 → US-05 → US-07 → Polish (minimal)
```

This gives you: Navigation, Form, Validation, Prediction = complete MVP

### User Story Dependencies (Simplified)

```
Foundational (MUST complete first)
    ↓
US-01 (Navigation foundation - BLOCKING)
    ↓
US-02 (Multi-page form - BLOCKING)
    ↓
    ├─→ US-03 (Dropdown format - enhances US-02)
    ├─→ US-04 (Non-renseigné - enhances US-02)
    ├─→ US-05 (Validation - validates US-02) → US-07 (Prediction - uses US-05)
    ├─→ US-06 (Minute dropdown - part of US-02)
    ├─→ US-08 (Recap table - uses US-02)
    ├─→ US-09 (Help text - enhances US-02)
    ├─→ US-10 (JSON reference - architecture)
    ├─→ US-11 (Mobile - enhances US-02)
    └─→ US-12 (Logging - enhances US-07)
```

### Within Each User Story

- **Tests MUST be written FIRST** and verified to FAIL before implementation (TDD)
- **Models** before services (if applicable)
- **Shared utilities** before page components
- **Core implementation** before enhancements
- **Story complete** before moving to next priority

### Parallel Opportunities

#### Foundational Phase (can run in parallel after T006)

```bash
# After data/ref_options.json is generated (T006):
T007 [P] models.py
T008 [P] reference_loader.py
T009 [P] session_state.py
T010 [P] api_client.py
T011 [P] validation.py
T012 [P] Contract test 1
T013 [P] Contract test 2
T014 [P] Contract test 3
```

#### US-02 Implementation (can run in parallel after tests)

```bash
# After US-02 tests written (T021-T023):
T024 [P] Page 1_Contexte_Route.py
T025 [P] Page 2_Infrastructure.py
T026 [P] Page 3_Collision.py
T027 [P] Page 4_Conducteur.py
T028 [P] Page 5_Conditions.py
# T029 must wait (6_Recap depends on others existing)
```

#### US-03 Implementation (can run in parallel)

```bash
# After format_dropdown_option implemented (T035):
T036 [P] Update Page 1
T037 [P] Update Page 2
T038 [P] Update Page 3
T039 [P] Update Page 4
T040 [P] Update Page 5
```

#### US-09 Implementation (can run in parallel)

```bash
# After get_field_help implemented (T075):
T076 [P] Add help to Page 1
T077 [P] Add help to Page 2
T078 [P] Add help to Page 3
T079 [P] Add help to Page 4
T080 [P] Add help to Page 5
```

#### Polish Phase (can run in parallel)

```bash
T100 [P] Timeout error handling
T101 [P] 422 error handling
T102 [P] 500 error handling
T103 [P] Dep search functionality
```

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

**Goal**: Get a working prediction interface as fast as possible

**Recommended Scope**:
1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: US-01 (Reset + progress)
4. Complete Phase 4: US-02 (Multi-page navigation)
5. Complete Phase 7: US-05 (Validation)
6. Complete Phase 9: US-07 (Prediction)
7. Minimal Phase 15: T100-T102 (Error handling), T106 (E2E test)

**Result**: Functional 6-page form with validation and prediction = **DEMO-READY MVP**

**Timeline Estimate**: ~15-20 tasks = could be completed in 1-2 days with focused effort

### Incremental Delivery (After MVP)

1. **MVP deployed** → Users can make predictions
2. **Add US-03** → Better UX with "code — libellé" format
3. **Add US-08** → Recap table for verification
4. **Add US-09** → Help text for non-experts
5. **Add US-04 + US-06** → Flexibility with "Non renseigné"
6. **Add US-11** → Mobile support
7. **Add US-10 + US-12** → Architecture improvements + logging

**Benefit**: Each increment adds value without breaking previous functionality

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (critical path)
2. **Once Foundational done + US-01 + US-02 complete**:
   - Developer A: US-03 + US-04 (dropdown enhancements)
   - Developer B: US-05 + US-07 (validation + prediction)
   - Developer C: US-08 + US-09 (recap + help)
3. **Stories integrate independently** - no merge conflicts expected

---

## Test Execution Strategy

### TDD Workflow (Per User Story)

1. **Write tests** for user story (e.g., T021-T023 for US-02)
2. **Run tests** → verify they FAIL (pytest tests/integration/test_us02_*.py)
3. **Implement** user story (e.g., T024-T032 for US-02)
4. **Run tests** → verify they PASS
5. **Checkpoint**: User story is complete and verified

### Test Suite Organization

```
tests/
├── integration/
│   ├── test_api_contract.py         # Foundational contract tests
│   ├── test_us01_reset.py           # US-01 tests
│   ├── test_us02_navigation.py      # US-02 tests
│   ├── test_us03_dropdown_display.py# US-03 tests
│   ├── test_us04_not_specified.py   # US-04 tests
│   ├── test_us05_validation.py      # US-05 tests
│   ├── test_us06_minute_dropdown.py # US-06 tests
│   ├── test_us07_prediction.py      # US-07 tests
│   ├── test_us08_recap.py           # US-08 tests
│   ├── test_us09_help.py            # US-09 tests
│   ├── test_us11_accessibility.py   # US-11 tests
│   └── __init__.py
└── unit/
    ├── test_validation.py           # US-05 unit tests
    ├── test_dropdown_format.py      # US-03 unit tests
    ├── test_reference_loader.py     # US-09, US-10 unit tests
    ├── test_api_client.py           # US-12 unit tests
    └── __init__.py
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run only user story 2 tests
pytest tests/integration/test_us02_navigation.py -v

# Run with coverage
pytest tests/ --cov=streamlit_lib --cov=streamlit_pages --cov-report=html

# Run only integration tests
pytest tests/integration/ -v

# Run only unit tests
pytest tests/unit/ -v
```

---

## Notes

- **[P] tasks** = different files, no dependencies → can run in parallel
- **[Story] labels** = map task to specific user story for traceability
- Each user story should be **independently completable and testable**
- **Verify tests FAIL before implementing** (TDD discipline)
- **Commit after each user story** or logical group (e.g., after Phase 3, after Phase 4)
- **Stop at any checkpoint** to validate story independently
- **Avoid**: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Summary

- **Total Tasks**: 107 tasks
- **Phases**: 15 (Setup + Foundational + 12 User Stories + Polish)
- **Parallel Opportunities**: ~40 tasks marked [P] can run concurrently
- **MVP Scope**: ~20 tasks (Phases 1, 2, 3, 4, 7, 9 + minimal polish)
- **Test Tasks**: 26 test tasks (TDD approach)
- **Implementation Tasks**: 81 implementation + polish tasks

**Estimated Timeline**:
- MVP: 1-2 days (focused effort, single developer)
- Full Feature: 3-5 days (all 12 user stories, single developer)
- Full Feature (team of 3): 2-3 days (parallel user stories)

**Next Step**: Execute tasks in order, starting with Phase 1 (Setup) → Phase 2 (Foundational) → MVP user stories (US-01, US-02, US-05, US-07)
