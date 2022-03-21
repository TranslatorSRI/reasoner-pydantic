"""Test workflow things."""
from reasoner_pydantic import Query

query = {
    "workflow": [
        {
            "id": "fill",
            "parameters": {
                "denylist": [
                    "ARAX"
                ]
            },
            "runner_parameters": {
                "allowlist": [
                    "ARAGORN"
                ]
            }
        },
        {"id": "bind"},
        {
            "id": "overlay_compute_ngd",
            "parameters": {
                "qnode_keys": ["n0", "n1"],
                "virtual_relation_label": "NGD1",
            },
        },
        {"id": "complete_results"},
        {"id": "filter_results_top_n", "parameters": {"max_results": 50}},
    ],
    "message": {
        "query_graph": {
            "nodes": {
                "n0": {"categories": ["biolink:Gene"]},
                "n1": {
                    "ids": ["CHEBI:45783"],
                    "categories": ["biolink:ChemicalSubstance"],
                },
            },
            "edges": {
                "e01": {
                    "subject": "n0",
                    "object": "n1",
                    "predicates": ["biolink:related_to"],
                }
            },
        }
    },
}


def test_workflow():
    """Test construction of a Query with a workflow."""
    query_obj = Query(**query)
    query_dict = query_obj.dict()
    assert "runner_parameters" in query_dict["workflow"][0].keys()
    assert "parameters" in query_dict["workflow"][0].keys()
    assert "allowlist" in query_dict["workflow"][0]["runner_parameters"].keys()
    assert "denylist" in query_dict["workflow"][0]["parameters"].keys()
    assert "ARAGORN" in query_dict["workflow"][0]["runner_parameters"]["allowlist"]
    assert "ARAX" in query_dict["workflow"][0]["parameters"]["denylist"]
