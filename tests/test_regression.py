from reasoner_pydantic import Result

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
    "raw_data": ["test"]
}


def test_result_hashable():
    """Check that we can hash a result"""

    m = Result.parse_obj(EXAMPLE_RESULT)
    print(m)
    h = hash(m)
    assert h

    m2 = Result.parse_obj(EXAMPLE_RESULT)
    h2 = hash(m2)

    assert h == h2
