"""Test alignment with OpenAPI schema."""
import json

import httpx
import yaml

from reasoner_pydantic import components


class NormDecoder(json.JSONDecoder):
    """JSON decoder that reduces schemas the their functional core."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        json.JSONDecoder.__init__(
            self,
            object_hook=self.object_hook,
            *args,
            **kwargs,
        )

    def object_hook(self, dct):
        """Object hook."""
        if "$ref" in dct:
            if dct["$ref"].startswith("#/definitions/"):
                ref = "#/components/schemas" + dct["$ref"][13:]
            else:
                ref = dct["$ref"]
            return {
                "$ref": ref
            }

        # This is potentially problematic in general... #
        if "anyOf" in dct:
            dct["oneOf"] = dct.pop("anyOf")
        #################################################

        dct.pop("title", None)
        dct.pop("description", None)
        dct.pop("example", None)
        dct.pop("externalDocs", None)
        if dct.get("additionalProperties", None) is True:
            dct.pop("additionalProperties")
        if list(dct.keys()) == ["allOf"]:
            if len(dct["allOf"]) == 1:
                return dct["allOf"][0]
        return dct


TAG = "v1.2"
response = httpx.get(f"https://raw.githubusercontent.com/NCATSTranslator/ReasonerAPI/{TAG}/TranslatorReasonerAPI.yaml")
reference_schemas = yaml.load(
    response.text,
    Loader=yaml.FullLoader,
)["components"]["schemas"]
reference_schemas = json.loads(
    json.dumps(reference_schemas),
    cls=NormDecoder,
)


def test_openapi():
    """Test alignment with OpenAPI schema."""
    for obj in components:
        print(obj.__name__)

        schema = json.loads(obj.schema_json(), cls=NormDecoder)

        schema.pop("definitions", None)
        try:
            assert schema == reference_schemas[obj.__name__]
        except AssertionError:
            print("  produced schema: ", schema)
            print("  reference schema: ", reference_schemas[obj.__name__])
            raise
