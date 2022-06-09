"""Test workflow things."""
from reasoner_pydantic import Query

query = {
    "workflow": [
        {
            "id": "fill",
            "parameters": {"denylist": ["ARAX"]},
            "runner_parameters": {"allowlist": ["ARAGORN"]},
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

query2 = {
    "workflow": [
        {
            "id": "fill",
            "parameters": { "allow_list": ["infores:cohd"],
                "qedge_keys": [
                    "e0"
                ]
            }
        },
        {
            "id": "overlay_compute_ngd",
            "parameters": {
                "virtual_relation_label": "N1",
                "qnode_keys": [
                    "n0",
                    "n1"
                ]
            }
        },
        {
            "id": "bind"
        },
        {
            "id": "score"
        },
        {
            "id": "filter_results_top_n",
            "parameters": {
                "max_results": 3
            }
        },
        {
            "id": "fill",
            "parameters": {
                "qedge_keys": [
                    "e1",
                    "e2",
                    "e3",
                    "e4"
                ]
            }
        },
        {
            "id": "bind"
        },
        {
            "id": "score"
        }
    ],
    "message": {
        "query_graph": {
            "edges": {
                "e0": {
                    "subject": "n0",
                    "object": "n1",
                    "predicates": [
                        "biolink:has_real_world_evidence_of_association_with"
                    ]
                },
                "e1": {
                    "subject": "n1",
                    "object": "n2",
                    "predicates": [
                        "biolink:increases_activity_of"
                    ]
                },
                "e2": {
                    "subject": "n3",
                    "object": "n2",
                    "predicates": [
                        "biolink:increases_activity_of"
                    ]
                },
                "e3": {
                    "subject": "n1",
                    "object": "n2",
                    "predicates": [
                        "biolink:decreases_activity_of"
                    ],
                    "option_group_id": "decr"
                },
                "e4": {
                    "subject": "n3",
                    "object": "n2",
                    "predicates": [
                        "biolink:decreases_activity_of"
                    ],
                    "option_group_id": "decr"
                }
            },
            "nodes": {
                "n0": {
                    "ids": [
                        "MONDO:0009061"
                    ],
                    "is_set": "false",
                    "name": "MONDO:0009061"
                },
                "n1": {
                    "is_set": "false",
                    "categories": [
                        "biolink:ChemicalEntity"
                    ]
                },
                "n2": {
                    "is_set": "false",
                    "categories": [
                        "biolink:Gene",
                        "biolink:Protein"
                    ]
                },
                "n3": {
                    "is_set": "false",
                    "categories": [
                        "biolink:ChemicalEntity"
                    ]
                }
            }
        }
    }
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

def test_workflow2():
    query_obj = Query(**query)
    query_dict = query_obj.dict()
    assert "parameters" in query_dict["workflow"][0].keys()
