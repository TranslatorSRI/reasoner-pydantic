"""Test alignment with OpenAPI schema."""
import json

import httpx
import yaml

from reasoner_pydantic.workflow import Workflow

TAG = "v1.2"
response = httpx.get(f"http://standards.ncats.io/workflow/1.0.0/schema")
reference_schema = yaml.load(
    response.text,
    Loader=yaml.FullLoader,
)


def test_openapi():
    """Test alignment with OpenAPI schema."""
    print("\n", Workflow.__name__)

    schema = Workflow.schema_json(indent=4)

    print("  produced schema: ", schema)
    print("  reference schema: ", json.dumps(reference_schema, indent=4))
