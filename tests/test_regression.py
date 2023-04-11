from reasoner_pydantic import Result
from reasoner_pydantic.utils import HashableSequence

EXAMPLE_RESULT = {
    "node_bindings": {
        "n1": [{"id": "CHEBI:6801"}],
        "n2": [{"id": "MONDO:5148"}],
    },
    "edge_bindings": {
        "n1n2": [
            {
                "id": "CHEBI:6801-biolink:treats-MONDO:5148",
                "attributes": [
                    {
                        "attribute_type_id": "biolink:knowledge_source",
                        "value": {"sources": ["a", "b", "c"]},
                    }
                ],
            },
        ],
    },
    "raw_data": ["test"],
}


def test_result_hashable():
    """Check that we can hash a result with extra properties"""

    result_obj = Result.from_obj(EXAMPLE_RESULT)
    result_dict = result_obj.dict()

    assert len(result_dict["raw_data"]) == 1
    assert type(result_obj.raw_data) == HashableSequence
    assert result_obj.raw_data[0] == "test"
