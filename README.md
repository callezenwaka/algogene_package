# krane
AWS Scholarship Capstone Project - A light-weight bioinformatics package

## Folder structure
```bash
krane/
├── src/
│   └── krane/
│       ├── __init__.py         # Package version and top-level imports
│       ├── core/
│       │   ├── __init__.py
│       │   ├── models.py       # Pydantic/data models
│       │   └── sequence.py     # Core sequence analysis logic
│       ├── web/
│       │   ├── __init__.py
│       │   ├── app.py          # FastAPI application setup
│       │   ├── routes/
│       │   │   ├── __init__.py
│       │   │   ├── sequence.py # Sequence-related endpoints
│       │   │   └── utils.py    # Utility endpoints
│       │   ├── schemas/
│       │   │   ├── __init__.py
│       │   │   └── sequence.py # Request/Response models
│       │   └── templates/      # For web interface if needed
│       └── cli/
│           ├── __init__.py
│           └── commands.py     # CLI commands
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_web.py
├── pyproject.toml             # Project metadata and dependencies
├── README.md
└── LICENSE
```

## Generate requirements.txt

### Install pip-tools
```bash
pip install pip-tools
```

### Generate requirements.txt from pyproject.toml
```bash
pip-compile pyproject.toml -o requirements.txt
```

### Generate dev requirements (includes test dependencies)
```bash
pip-compile pyproject.toml --extra dev --extra test -o requirements-dev.txt
```

## Install package

### Dev mode
```
python3 -m pip install --editable .
```

### How to use krane

```bash
pip install krane
```

### Install the package in development mode:
```bash
pip install -e .
```

## Run web application

### Using the installed command
```bash
krane-web
```

### Running directly with uvicorn
```bash
uvicorn krane.web.app:app --reload
```

## Use command line

### Analyze a sequence
```bash
krane analyze ATCG --type DNA --label "Test"
```

### Generate random sequence
```
krane generate --length 20 --type DNA
```

### Read FASTA file
```
krane read-fasta sequence.fasta
```

## Automated Test

### Install test dependencies
```
pip install -e ".[test]"
```

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run with coverage report
```bash
pytest --cov=krane
```

### Run all tests together
```bash
pytest tests/ -v
```

### Run specific test file
```bash
pytest tests/test_web.py
pytest tests/test_core.py
```

### Run tests matching a pattern
```bash
pytest -k "test_sequence"
```

## Deployment Process

### Deployment to Pypi 
- Create PyPI account and get API token
- Add PYPI_API_TOKEN to GitHub repository secrets

### For PyPI
```bash
# Tag a new version
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
# This triggers PyPI workflow
```

### Deployment to GAE 
- Create Google Cloud project
- Create service account with App Engine Admin role
- Download JSON key
- Add to GitHub secrets:
 * GCP_PROJECT_ID: Your project ID
 * GCP_SA_KEY: The entire JSON key content

### For Google App Engine:
```bash
# Push to main branch
git push origin main

# This triggers GAE workflow
```

## Testing the deployments

### After PyPI deployment:
```bash
# In a new virtual environment
pip install krane

# Test library
python -c "from krane.core import Sequence; print(Sequence('ATCG', 'DNA').transcription())"

# Test CLI
krane --help
```

### After GAE deployment:
```bash
# Your app will be available at
https://<project-id>.appspot.com/
```