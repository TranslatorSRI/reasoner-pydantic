"""Test workflow things."""
from reasoner_pydantic import Query

query = {
    "workflow": [
        {"id": "fill"},
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
    Query(**query)
