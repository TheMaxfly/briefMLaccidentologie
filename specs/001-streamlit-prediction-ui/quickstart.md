# Quickstart: Interface de Prédiction de Gravité d'Accidents

**Feature**: `001-streamlit-prediction-ui`
**Created**: 2026-01-30
**Purpose**: Get the Streamlit prediction interface running in under 5 minutes

## Prerequisites

- Python 3.12+ installed
- `uv` package manager installed (see [uv documentation](https://github.com/astral-sh/uv))
- FastAPI backend running (see Backend Setup below)
- Git repository cloned

## Quick Start (3 Steps)

### 1. Ensure FastAPI Backend is Running

The Streamlit interface requires the FastAPI backend to be running first.

```bash
# In terminal 1 - Start FastAPI backend
uv run uvicorn predictor:app --host 0.0.0.0 --port 8000 --reload
```

**Verify backend is running**:
```bash
curl -s http://localhost:8000/health
# Should return: {"status": "ok"} or similar
```

### 2. Generate Reference Data (First Time Only)

The interface needs `data/ref_options.json` to populate dropdowns.

**Option A - Generate from Data Dictionary** (recommended):
```bash
# TODO: Create script to parse data_dictionary_catboost_product15.md
# python scripts/generate_ref_options.py \
#   --input data_dictionary_catboost_product15.md \
#   --output data/ref_options.json
```

**Option B - Use Sample Reference Data** (for testing):
```bash
# Create minimal ref_options.json manually (see Structure below)
mkdir -p data
# Copy sample from contracts/ref-schema.json and fill with actual data
```

### 3. Run Streamlit Interface

```bash
# In terminal 2 - Start Streamlit interface
API_URL=http://localhost:8000 uv run streamlit run streamlit_app.py
```

**Expected output**:
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

**Open browser**: Navigate to [http://localhost:8501](http://localhost:8501)

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_URL` | `http://localhost:8000` | FastAPI backend URL |
| `STREAMLIT_SERVER_PORT` | `8501` | Streamlit server port |
| `STREAMLIT_SERVER_ADDRESS` | `localhost` | Streamlit bind address |

**Custom Configuration**:
```bash
# Different API URL (staging/production)
API_URL=https://api-staging.example.com uv run streamlit run streamlit_app.py

# Custom port
API_URL=http://localhost:8000 \
STREAMLIT_SERVER_PORT=8080 \
uv run streamlit run streamlit_app.py
```

## Project Structure Overview

```text
BriefML/
├── streamlit_app.py                # Main entry point
├── streamlit_pages/                # Multi-page app structure
│   ├── 1_Contexte_Route.py        # Page 1: dep, agg, catr, vma_bucket
│   ├── 2_Infrastructure.py        # Page 2: int, circ
│   ├── 3_Collision.py             # Page 3: col, choc_mode, manv_mode
│   ├── 4_Conducteur.py            # Page 4: driver_age_bucket, driver_trajet_family
│   ├── 5_Conditions.py            # Page 5: lum, atm, time_bucket
│   └── 6_Recap_Prediction.py      # Page 6: summary + predict button
├── streamlit_lib/                  # Shared utilities
│   ├── reference_loader.py        # Load ref_options.json
│   ├── validation.py              # Client-side validation
│   ├── api_client.py              # FastAPI HTTP client
│   └── session_state.py           # Session state helpers
├── data/
│   ├── ref_options.json           # Dropdown options (generated)
│   └── data_dictionary_catboost_product15.md  # Reference
├── predictor.py                    # FastAPI backend (existing)
└── model/
    └── catboost_product15.cbm      # Trained model (existing)
```

## Reference Data Structure

The `data/ref_options.json` file must follow this structure:

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
    ...
  ],
  "atm": [
    {"code": -1, "label": "Non renseigné"},
    {"code": 1, "label": "Normale"},
    ...
  ],
  ...
}
```

**Validation**: Must pass schema in `contracts/ref-schema.json`

**Generate from Data Dictionary**:
See `data_dictionary_catboost_product15.md` for complete code tables.

## Development Workflow

### 1. Initial Setup

```bash
# Clone repository (if not already)
git clone <repo-url>
cd BriefML

# Switch to feature branch
git checkout 001-streamlit-prediction-ui

# Install dependencies (via uv)
uv sync
```

### 2. Running Tests

```bash
# Run all tests
uv run pytest

# Run only integration tests
uv run pytest tests/integration/

# Run with coverage
uv run pytest --cov=streamlit_lib --cov-report=html
```

### 3. Development Mode

**Backend** (auto-reload on code changes):
```bash
uv run uvicorn predictor:app --reload
```

**Frontend** (auto-reload on code changes):
```bash
API_URL=http://localhost:8000 uv run streamlit run streamlit_app.py
```

Streamlit automatically reloads when you save `.py` files.

### 4. Debugging

**Enable Streamlit Debug Mode**:
```bash
STREAMLIT_SERVER_RUN_ON_SAVE=true \
STREAMLIT_LOGGER_LEVEL=debug \
uv run streamlit run streamlit_app.py
```

**Check API Connection**:
```bash
# Test prediction endpoint manually
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Troubleshooting

### Issue: "Connection refused" error

**Cause**: FastAPI backend not running

**Solution**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start it
uv run uvicorn predictor:app --port 8000
```

### Issue: "ref_options.json not found"

**Cause**: Reference data file missing

**Solution**:
```bash
# Check if file exists
ls -la data/ref_options.json

# If missing, generate it (or create manually)
# See "Generate Reference Data" section above
```

### Issue: Dropdown options not displaying

**Cause**: Invalid JSON format in ref_options.json

**Solution**:
```bash
# Validate JSON syntax
python -m json.tool data/ref_options.json

# Validate against schema
# pip install jsonschema
python -c "
import json
import jsonschema

with open('data/ref_options.json') as f:
    data = json.load(f)
with open('specs/001-streamlit-prediction-ui/contracts/ref-schema.json') as f:
    schema = json.load(f)

jsonschema.validate(data, schema)
print('✓ Valid')
"
```

### Issue: "ModuleNotFoundError" for streamlit_lib

**Cause**: Module not in Python path

**Solution**:
```bash
# Ensure you're running from project root
pwd  # Should show .../BriefML

# Run streamlit from project root
uv run streamlit run streamlit_app.py
```

### Issue: Session state not persisting between pages

**Cause**: Not using st.session_state correctly

**Solution**: Check that `streamlit_lib/session_state.py` is properly initialized on each page.

## Production Deployment

### Docker (Recommended)

```dockerfile
# Dockerfile for Streamlit interface
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Copy application code
COPY streamlit_app.py ./
COPY streamlit_pages/ ./streamlit_pages/
COPY streamlit_lib/ ./streamlit_lib/
COPY data/ ./data/

# Expose Streamlit port
EXPOSE 8501

# Set API URL via environment variable
ENV API_URL=http://api:8000

# Run Streamlit
CMD ["uv", "run", "streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and Run**:
```bash
# Build image
docker build -t briefml-ui:latest .

# Run container
docker run -p 8501:8501 \
  -e API_URL=http://localhost:8000 \
  briefml-ui:latest
```

### Docker Compose (Full Stack)

```yaml
version: '3.8'

services:
  api:
    build: .
    command: uvicorn predictor:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    volumes:
      - ./model:/app/model

  ui:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
    depends_on:
      - api
```

**Run Full Stack**:
```bash
docker-compose up
```

## Performance Tips

1. **Cache Reference Data**: Load `ref_options.json` once and cache in session state
2. **Optimize API Calls**: Only call `/predict` when form is complete and user clicks "Prédire"
3. **Use Connection Pooling**: Reuse HTTP connections for multiple predictions
4. **Enable Streamlit Caching**: Use `@st.cache_data` for reference data loading

## Next Steps

1. ✅ **Interface running**: You should see the multi-page form
2. **Test User Flow**: Go through all 6 pages and submit a prediction
3. **Verify Output**: Check that prediction (grave/non-grave) + probability displays correctly
4. **Run Tests**: `uv run pytest tests/integration/test_prediction_flow.py`

## Support

- **Issues**: Report bugs in GitHub issues
- **Documentation**: See `specs/001-streamlit-prediction-ui/` for detailed docs
- **API Reference**: Check FastAPI docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## Related Documentation

- [Implementation Plan](plan.md) - Overall architecture and design
- [Data Model](data-model.md) - Entity definitions and validation rules
- [API Contract](contracts/api-predict.md) - `/predict` endpoint specification
- [Constitution](../../.specify/memory/constitution.md) - Development principles and workflow
