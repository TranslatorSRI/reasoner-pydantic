# Testing reasoner-pydantic

### Content

* [`test_openapi.py`](test_openapi.py):

  To verify that our pydantic models are aligned with [TRAPI](https://github.com/NCATSTranslator/ReasonerAPI), we load each standard component schema and compare it against the schema generated for the corresponding pydantic model.

### Workflow

Tests are run automatically via GitHub Actions on each pull request.
