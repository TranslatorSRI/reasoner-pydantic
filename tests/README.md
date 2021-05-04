# Testing reasoner-pydantic

[![Test status via GitHub Actions](https://github.com/TranslatorSRI/reasoner-pydantic/workflows/test/badge.svg)](https://github.com/TranslatorSRI/reasoner-pydantic/actions?query=workflow%3Atest)

### Content

* [`test_openapi.py`](test_openapi.py):

  To verify that our pydantic models are aligned with [TRAPI](https://github.com/NCATSTranslator/ReasonerAPI), we load each standard component schema and compare it against the schema generated for the corresponding pydantic model.

### Workflow

Tests are run automatically via GitHub Actions on each pull request and each push to `main`.
