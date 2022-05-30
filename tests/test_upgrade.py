from reasoner_pydantic import Attribute, Message

EXAMPLE_MESSAGE_1p2 = {
    "query_graph": {
        "nodes": {
            "n1": {"categories": ["biolink:ChemicalSubstance"]},
            "n2": {"categories": ["biolink:Disease"]},
        },
        "edges": {
            "n1n2": {
                "subject": "n1",
                "object": "n2",
                "predicates": ["biolink:related_to"],
            }
        },
    },
    "knowledge_graph": {
        "nodes": {
            "CHEBI:6801": {},
            "MONDO:5148": {},
        },
        "edges": {
            "CHEBI:6801-biolink:treats-MONDO:5148": {
                "subject": "CHEBI:6801",
                "object": "MONDO:5148",
                "predicate": "biolink:treats",
                "attributes": [
                    {
                        "attribute_type_id": "biolink:original_knowledge_source",
                        "value": "inforres:kp1",
                    }
                ],
            }
        },
    },
    "results": [
        {
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
                                "attribute_type_id": "EDAM:1699",
                                "value": 888,
                            }
                        ],
                    }
                ]
            },
            "score": 999,
        }
    ],
}


def test_1p2_upgrade():

    m = Message.upgrade('1.2', EXAMPLE_MESSAGE_1p2)
    assert len(m.results) == 1
    # TODO: additional validation of the output