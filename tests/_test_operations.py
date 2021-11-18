"""Test alignment with OpenAPI schema."""
import json

import httpx
import yaml

from reasoner_pydantic.workflow import operations

TAG = "v1.2"
response = httpx.get(f"http://standards.ncats.io/workflow/1.0.0/schema")
response = httpx.get(f"http://standards.ncats.io/operation/1.0.0/schema")
reference_schemas = yaml.load(
    response.text,
    Loader=yaml.FullLoader,
)["$defs"]


def test_openapi():
    """Test alignment with OpenAPI schema."""
    for obj in operations:
        print("\n", obj.__name__)

        schema = obj.schema_json(indent=4)

        print("  produced schema: ", schema)
        print(
            "  reference schema: ",
            json.dumps(reference_schemas[obj.__name__], indent=4),
        )
