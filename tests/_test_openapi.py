"""Test alignment with OpenAPI schema."""
import json

import httpx
import yaml

from reasoner_pydantic import components

TAG = "v1.2"
response = httpx.get(
    f"https://raw.githubusercontent.com/NCATSTranslator/ReasonerAPI/{TAG}/TranslatorReasonerAPI.yaml"
)
reference_schemas = yaml.load(response.text, Loader=yaml.FullLoader,)[
    "components"
]["schemas"]


def test_openapi():
    """Test alignment with OpenAPI schema."""
    for obj in components:
        print("\n", obj.__name__)

        schema = obj.schema_json(indent=4)

        print("  produced schema: ", schema)
        print(
            "  reference schema: ",
            json.dumps(reference_schemas[obj.__name__], indent=4),
        )
