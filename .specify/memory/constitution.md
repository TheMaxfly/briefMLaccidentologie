<!--
  Sync Impact Report
  ==================
  Version: 1.1.1 → 1.1.2
  Rationale: Update spec-template.md with Streamlit UI/UX requirements (PATCH - template alignment)

  Modified Principles: N/A
  Added Sections: N/A
  Removed Sections: N/A

  Templates Status:
    ✅ .specify/templates/plan-template.md - reviewed, no updates needed
    ✅ .specify/templates/spec-template.md - UPDATED with UI/UX Requirements section
    ✅ .specify/templates/tasks-template.md - reviewed, no updates needed

  Template Updates:
    - spec-template.md: Added "UI/UX Requirements" section with 15 requirements
      * Input collection for 15 model variables (UIX-001 to UIX-004)
      * User guidance and help text (UIX-005 to UIX-008)
      * User experience standards (UIX-009 to UIX-012)
      * Accessibility requirements (UIX-013 to UIX-015)

  Follow-up TODOs:
    - RATIFICATION_DATE needs to be set by project owner/team

  Previous Changes:
  ------------------
  Version: 1.1.0 → 1.1.1 (2026-01-30)
  - Added data dictionary requirement for user input validation
  - Enforced Pydantic models derived from data_dictionary_catboost_product15.md
  - Required dropdowns in Streamlit for coded variables

  Version: 1.0.0 → 1.1.0 (2026-01-30)
  - Added Technical Stack section with FastAPI, Streamlit, and CatBoost specifics

  Version: 0.0.0 → 1.0.0 (2026-01-30)
  - Initial constitution creation for BriefML project
  - Established 5 core principles
  - Added Model Governance, Development Workflow, and Governance sections
-->

# BriefML Constitution

## Technical Stack

**ML Framework**: CatBoost (gradient boosting)
- Primary model: `catboost_product15.cbm`
- Model inputs: 15 variables defined in `data_dictionary_catboost_product15.md`
- Use CatBoost for production models (handles categorical features natively, robust to overfitting)

**API Layer**: FastAPI
- All model endpoints exposed via FastAPI REST API
- Async support for high-throughput predictions
- Automatic OpenAPI documentation
- Pydantic models for request/response validation

**User Interface**: Streamlit
- Interactive web interface for model demonstration and exploration
- Connects to FastAPI backend via HTTP
- Environment variable configuration (`API_URL`)

**Python Environment**: Python 3.12+
- Dependency management via `uv` (pyproject.toml + uv.lock)
- Key dependencies: pandas, numpy, scikit-learn, FastAPI, Streamlit

## Core Principles

### I. Data Quality First

Every ML model is only as good as its training data. Data quality is non-negotiable.

**Rules**:
- All data sources MUST be documented with data dictionaries
- User input MUST conform to `data_dictionary_catboost_product15.md` (15 variables, codes, categories)
- Data pipelines MUST include validation steps (schema checks, range validation, null handling)
- Feature engineering logic MUST be explicitly documented and version-controlled
- Data quality metrics MUST be tracked (completeness, consistency, accuracy)
- Invalid input codes/values MUST be rejected with clear error messages

**Rationale**: ML models trained on poor-quality data will produce unreliable predictions. Data quality issues are the root cause of most production ML failures.

### II. Model Reproducibility

All model training, evaluation, and deployment processes MUST be fully reproducible.

**Rules**:
- Random seeds MUST be set and documented
- All hyperparameters MUST be version-controlled (config files, not hardcoded)
- Training datasets MUST be versioned or uniquely identified
- Model artifacts MUST include metadata (training date, data version, hyperparameters, metrics)
- Environment dependencies MUST be pinned (pyproject.toml, uv.lock)

**Rationale**: Reproducibility enables debugging, auditing, and incremental improvement. Non-reproducible models cannot be trusted in production.

### III. API-First Architecture

All ML models MUST expose functionality via clean, well-documented FastAPI REST APIs.

**Rules**:
- Every model MUST have a `/health` endpoint for monitoring
- API contracts MUST use Pydantic models derived from `data_dictionary_catboost_product15.md`
- Pydantic models MUST enforce field types, valid codes, and value ranges per data dictionary
- Prediction endpoints MUST validate inputs and return structured errors with invalid field details
- FastAPI automatic documentation (`/docs`) MUST be kept up-to-date
- APIs MUST support both single predictions and batch predictions where appropriate
- Response times MUST be monitored and logged
- Streamlit UI MUST connect to FastAPI backend (never load models directly in UI)
- Streamlit forms MUST use dropdowns for coded variables (lum, atm, catr, etc.) with labels from data dictionary

**Rationale**: API-first design with FastAPI decouples model logic from client applications, enables multiple consumers (Streamlit, external systems), and facilitates A/B testing and model versioning.

### IV. Test-First Development (NON-NEGOTIABLE)

TDD is mandatory for all feature development. Tests written → User approved → Tests fail → Then implement.

**Rules**:
- Contract tests MUST be written before API implementation
- Integration tests MUST cover critical user journeys
- Model performance tests MUST establish baseline metrics before changes
- Red-Green-Refactor cycle strictly enforced
- No code merged without passing tests

**Rationale**: ML systems are complex and brittle. Tests prevent regressions, document expected behavior, and catch integration issues early.

### V. Simplicity & Observability

Start simple. Every layer of complexity must be justified. Systems MUST be observable.

**Rules**:
- Use CatBoost for gradient boosting models (tree-based, interpretable, production-ready)
- Avoid deep learning unless complexity is justified for the specific use case
- Every abstraction layer MUST solve a concrete problem (no premature optimization)
- Structured logging REQUIRED for all FastAPI requests, model predictions, and errors
- Metrics MUST be exposed (prediction latency, error rates, model performance)
- YAGNI principle: implement only what is needed now
- Streamlit apps MUST remain simple - complex logic belongs in the API layer

**Rationale**: CatBoost provides excellent performance for tabular data without deep learning complexity. Complex systems are harder to debug, maintain, and explain. Observability is critical for diagnosing production issues and understanding model behavior.

## Model Governance

**Model Versioning**:
- Models MUST be versioned using semantic versioning: `MAJOR.MINOR.PATCH`
  - MAJOR: Model architecture change or training data source change
  - MINOR: Hyperparameter tuning or feature engineering changes
  - PATCH: Bug fixes, code refactoring (no model changes)
- Model metadata MUST include: version, training date, data version, performance metrics

**Model Validation**:
- New models MUST meet or exceed baseline performance on test set
- Model performance MUST be validated on out-of-time data where applicable
- Model fairness checks MUST be performed if model impacts different demographic groups

**Model Deployment**:
- CatBoost model artifacts (`.cbm` files) MUST be stored with version control
- Model metadata JSON files MUST accompany model artifacts
- FastAPI service MUST load models from versioned artifact paths
- Deployment MUST include canary testing (shadow mode or A/B test)
- Rollback plan MUST be documented before production deployment
- Streamlit interface MUST point to correct API version via `API_URL` environment variable

## Development Workflow

**Feature Development Process**:
1. Feature specification (`/speckit.specify`) - define user stories and requirements
2. Implementation planning (`/speckit.plan`) - design approach and technical details
3. Task breakdown (`/speckit.tasks`) - create dependency-ordered tasks
4. Test-first implementation - write tests, ensure they fail, then implement
5. Code review - verify compliance with constitution and quality standards
6. Deployment - follow model governance rules

**Code Review Requirements**:
- All PRs MUST verify constitution compliance
- Model changes MUST include performance comparison (new vs baseline)
- API changes MUST include updated documentation and contract tests
- Data pipeline changes MUST include data quality validation

**Quality Gates**:
- Tests MUST pass before merge
- Code coverage MUST meet project standards (if established)
- Model performance MUST meet minimum thresholds
- API response times MUST meet SLA requirements (if established)

## Governance

**Amendment Procedure**:
- Constitution changes MUST be proposed with rationale and impact analysis
- Changes MUST be reviewed by project owner/team before adoption
- Amendment MUST include version bump and update to dependent templates
- Breaking changes (MAJOR version) require migration plan

**Versioning Policy**:
- Follow semantic versioning: `MAJOR.MINOR.PATCH`
- Update `LAST_AMENDED_DATE` when changes are made
- Maintain Sync Impact Report at top of this file

**Compliance Review**:
- All PRs/reviews MUST verify compliance with core principles
- Complexity MUST be justified in plan.md Complexity Tracking section
- Use `.specify/templates/` for consistent feature development workflow

**Version**: 1.1.2 | **Ratified**: TODO(RATIFICATION_DATE): set by project owner | **Last Amended**: 2026-01-30
