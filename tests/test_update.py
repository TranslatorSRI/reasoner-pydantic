import copy

from reasoner_pydantic import Attribute, Message


# Some sample attributes
ATTRIBUTE_A = {
    "attribute_type_id": "biolink:aggregate_knowledge_source",
    "value": "https://automat.renci.org/",
    "attributes": [
        {"attribute_type_id": "biolink:publication", "value": "pubmed_central"},
        {"attribute_type_id": "biolink:has_p-value_evidence", "value": 0.04},
    ],
}

ATTRIBUTE_B = {
    "attribute_type_id": "biolink:publication",
    "value": "pubmed_central",
    "attributes": [
        {"attribute_type_id": "biolink:has_original_source", "value": True},
    ],
}

ATTRIBUTE_A = Attribute.parse_obj(ATTRIBUTE_A)
ATTRIBUTE_B = Attribute.parse_obj(ATTRIBUTE_B)


def test_result_merging():
    """Test that duplicate results are merged correctly"""

    kg = {
        "nodes": {"kn0": {}, "kn1": {}},
        "edges": {
            "ke0": {
                "subject": "kn0",
                "object": "kn1",
                "predicate": "biolink:ameliorates",
            }
        },
    }
    message_a = {
        "knowledge_graph": copy.deepcopy(kg),
        "results": [
            {
                "node_bindings": {"n0": [{"id": "kn0"}]},
                "edge_bindings": {"e0": [{"id": "ke0"}]},
                "analyses": [
                    {
                        "source": "infores:ara1",
                        "edge_binding_attributes": {"e0": {"ke0": [ATTRIBUTE_A]}},
                        "score": 1,
                    }
                ],
            }
        ],
    }

    message_b = {
        "knowledge_graph": copy.deepcopy(kg),
        "results": [
            {
                "node_bindings": {"n0": [{"id": "kn0"}]},
                "edge_bindings": {"e0": [{"id": "ke0"}]},
                "analyses": [
                    {
                        "source": "infores:ara2",
                        "edge_binding_attributes": {"e0": {"ke0": [ATTRIBUTE_B]}},
                        "score": 2,
                    }
                ],
            },
        ],
    }

    m = Message.merge(message_a, message_b)

    m_dict = m.to_dict()
    assert len(m_dict["results"]) == 1
    assert len(m_dict["results"][0]["analyses"]) == 2


def test_different_result_merging():
    """Test that different results are not merged"""

    message_a = {
        "knowledge_graph": {
            "nodes": {"kn0": {}, "kn1": {}},
            "edges": {
                "ke0": {
                    "subject": "kn0",
                    "object": "kn1",
                    "predicate": "biolink:ameliorates",
                }
            },
        },
        "results": [
            {
                "node_bindings": {"n0": [{"id": "kn0"}]},
                "edge_bindings": {"e0": [{"id": "ke0"}]},
                "analyses": [
                    {
                        "source": "infores:ara1",
                        "edge_binding_attributes": {"e0": {"ke0": [ATTRIBUTE_B]}},
                        "score": 2,
                    }
                ],
            }
        ],
    }

    message_b = {
        "knowledge_graph": {
            "nodes": {"kn0": {}, "kn1": {}},
            "edges": {
                "ke1": {
                    "subject": "kn0",
                    "object": "kn1",
                    "predicate": "biolink:is_related_to",
                }
            },
        },
        "results": [
            {
                "node_bindings": {"n0": [{"id": "kn0"}]},
                "edge_bindings": {"e0": [{"id": "ke1"}]},
                "analyses": [
                    {
                        "source": "infores:ara2",
                        "edge_binding_attributes": {"e0": {"ke1": [ATTRIBUTE_A]}},
                        "score": 1,
                    }
                ],
            }
        ],
    }

    m = Message.merge(message_a, message_b)

    assert len(m.results) == 2


def test_deduplicate_results_out_of_order():
    """
    Test that we successfully deduplicate results when given
    the same results but in a different order
    """

    message = {
        "knowledge_graph": {"nodes": {}, "edges": {}},
        "results": [
            {
                "node_bindings": {
                    "a": [{"id": "CHEBI:88916"}, {"id": "MONDO:0011122"}],
                },
                "edge_bindings": {},
            },
            {
                "node_bindings": {
                    "a": [{"id": "MONDO:0011122"}, {"id": "CHEBI:88916"}],
                },
                "edge_bindings": {},
            },
        ],
    }

    m = Message.parse_obj(message)
    assert len(m.results) == 1


def test_deduplicate_results_different():
    """
    Test that we don't deduplicate results when given
    different binding information
    """

    message = {
        "knowledge_graph": {"nodes": {}, "edges": {}},
        "results": [
            {
                "node_bindings": {
                    "b": [{"id": "CHEBI:88916"}, {"id": "MONDO:0011122"}],
                },
                "edge_bindings": {},
            },
            {
                "node_bindings": {
                    "a": [{"id": "MONDO:0011122"}, {"id": "CHEBI:88916"}],
                },
                "edge_bindings": {},
            },
        ],
    }

    m = Message.parse_obj(message)
    assert len(m.results) == 2


def test_merge_knowledge_graph_nodes():
    """
    Test that we do a smart merge when given knowledge
    graph nodes with the same keys
    """

    message_a = {
        "knowledge_graph": {
            "nodes": {
                "MONDO:1": {
                    "name": "Ebola",
                    "categories": ["biolink:Disease"],
                    "attributes": [ATTRIBUTE_A],
                }
            },
            "edges": {},
        },
        "results": [],
    }

    message_b = {
        "knowledge_graph": {
            "nodes": {
                "MONDO:1": {
                    "name": "Ebola Hemorrhagic Fever",
                    "categories": ["biolink:DiseaseOrPhenotypicFeature"],
                    "attributes": [ATTRIBUTE_B],
                }
            },
            "edges": {},
        },
        "results": [],
    }

    m = Message.merge(message_a, message_b)

    # Validate output
    nodes = m.knowledge_graph.nodes
    assert len(nodes) == 1
    node = next(iter(nodes.values()))

    assert ATTRIBUTE_A in node.attributes
    assert ATTRIBUTE_B in node.attributes


def test_normalize_knowledge_graph_edges():
    """
    Test that KG edge IDs are normalized, so even if we pass
    in edges with the same name they are not merged by default
    """

    message_a = {
        "knowledge_graph": {
            "nodes": {"MONDO:1": {}, "CHEBI:1": {}},
            "edges": {
                "n0n1": {
                    "subject": "MONDO:1",
                    "object": "CHEBI:1",
                    "predicate": "biolink:treated_by",
                    "attributes": [ATTRIBUTE_A],
                }
            },
        },
        "results": [{"node_bindings": [], "edge_bindings": {"qe0": [{"id": "n0n1"}]}}],
    }

    message_b = {
        "knowledge_graph": {
            "nodes": {"MONDO:1": {}, "CHEBI:1": {}},
            "edges": {
                "n0n1": {
                    "subject": "MONDO:1",
                    "object": "CHEBI:1",
                    "predicate": "biolink:treated_by",
                    "attributes": [ATTRIBUTE_B],
                }
            },
        },
        "results": [],
    }

    m = Message.merge(message_a, message_b)

    # Check that we combined edges without source
    edges = m.knowledge_graph.edges
    assert len(edges) == 1

    # Check that the result was updated to point to the correct edge
    edge_id, edge = next(iter(edges.items()))
    result = next(iter(m.results))
    assert next(iter(result.edge_bindings["qe0"])).id == edge_id


def test_merge_identical_attributes():
    """
    Tests that identical attributes are merged
    """

    message_a = {
        "knowledge_graph": {
            "nodes": {
                "MONDO:1": {
                    "name": "Ebola",
                    "categories": ["biolink:Disease"],
                    "attributes": [ATTRIBUTE_A],
                }
            },
            "edges": {},
        },
        "results": [],
    }

    message_b = {
        "knowledge_graph": {
            "nodes": {
                "MONDO:1": {
                    "name": "Ebola Hemorrhagic Fever",
                    "categories": ["biolink:DiseaseOrPhenotypicFeature"],
                    "attributes": [ATTRIBUTE_A],
                }
            },
            "edges": {},
        },
        "results": [],
    }

    m = Message.merge(message_a, message_b)

    # Validate output
    nodes = m.knowledge_graph.nodes
    assert len(nodes) == 1
    node = next(iter(nodes.values()))

    assert ATTRIBUTE_A in node.attributes
    assert len(node.attributes) == 1


def test_merge_edges():
    """
    Tests that edges are merged when simple
    """

    kg = {
        "nodes": {
            "MONDO:1": {
                "name": "Ebola",
                "categories": ["biolink:Disease"],
                "attributes": [ATTRIBUTE_A],
            },
            "NCBI:1": {
                "name": "NPC1",
                "categories": ["biolink:Gene"],
                "attributes": [ATTRIBUTE_B],
            },
        },
        "edges": {},
    }
    kg_a = copy.deepcopy(kg)
    kg_a["edges"] = {
        "e1": {
            "subject": "MONDO:1",
            "predicate": "biolink:is_related_to",
            "object": "NCBI:1",
        }
    }
    message_a = {
        "knowledge_graph": kg_a,
        "results": [],
    }

    kg_b = copy.deepcopy(kg)
    kg_b["edges"] = {
        "e1": {
            "subject": "MONDO:1",
            "predicate": "biolink:is_related_to",
            "object": "NCBI:1",
        }
    }
    message_b = {
        "knowledge_graph": kg_b,
        "results": [],
    }

    m = Message.merge(message_a, message_b)

    # Validate output
    edges = m.knowledge_graph.edges
    assert len(edges) == 1


def test_merge_edges_with_sources():
    """
    Tests that identical attributes are merged
    """

    kg = {
        "nodes": {
            "MONDO:1": {
                "name": "Ebola",
                "categories": ["biolink:Disease"],
                "attributes": [ATTRIBUTE_A],
            },
            "NCBI:1": {
                "name": "NPC1",
                "categories": ["biolink:Gene"],
                "attributes": [ATTRIBUTE_B],
            },
        },
        "edges": {},
    }
    kg_a = copy.deepcopy(kg)
    kg_a["edges"] = {
        "e1": {
            "subject": "MONDO:1",
            "predicate": "biolink:is_related_to",
            "object": "NCBI:1",
            "sources": [
                {
                    "resource": "infores:ara1",
                    "resource_role": "biolink:aggregator_knowledge_source",
                    "retrievals": [
                        {
                            "retrieved_from": "infores:kp1",
                        }
                    ],
                },
                {
                    "resource": "infores:kp1",
                    "resource_role": "biolink:original_knowledge_source",
                    "retrievals": [{"retrieved_from": "offline_db"}],
                },
            ],
        }
    }
    message_a = {
        "knowledge_graph": kg_a,
        "results": [],
    }

    kg_b = copy.deepcopy(kg)
    kg_b["edges"] = {
        "e1": {
            "subject": "MONDO:1",
            "predicate": "biolink:is_related_to",
            "object": "NCBI:1",
            "sources": [
                {
                    "resource": "infores:ara2",
                    "resource_role": "biolink:aggregator_knowledge_source",
                    "retrievals": [
                        {
                            "retrieved_from": "infores:kp1",
                        }
                    ],
                },
                {
                    "resource": "infores:kp1",
                    "resource_role": "biolink:original_knowledge_source",
                    "retrievals": [{"retrieved_from": "offline_db"}],
                },
            ],
        }
    }

    message_b = {
        "knowledge_graph": kg_b,
        "results": [],
    }

    m = Message.merge(message_a, message_b)

    # Validate output
    m_dict = m.to_dict()
    edges = m_dict["knowledge_graph"]["edges"]

    assert len(edges.keys()) == 1

    edge = edges[list(edges.keys())[0]]
    assert len(edge["sources"]) == 3


def test_merge_edges_with_different_sources():
    """
    Tests that different original sources are not merged
    """

    kg = {
        "nodes": {
            "MONDO:1": {
                "name": "Ebola",
                "categories": ["biolink:Disease"],
                "attributes": [ATTRIBUTE_A],
            },
            "NCBI:1": {
                "name": "NPC1",
                "categories": ["biolink:Gene"],
                "attributes": [ATTRIBUTE_B],
            },
        },
        "edges": {},
    }
    kg_a = copy.deepcopy(kg)
    kg_a["edges"] = {
        "e1": {
            "subject": "MONDO:1",
            "predicate": "biolink:is_related_to",
            "object": "NCBI:1",
            "sources": [
                {
                    "resource": "infores:ara1",
                    "resource_role": "biolink:aggregator_knowledge_source",
                    "retrievals": [
                        {
                            "retrieved_from": "infores:kp1",
                        }
                    ],
                },
                {
                    "resource": "infores:kp1",
                    "resource_role": "biolink:original_knowledge_source",
                    "retrievals": [{"retrieved_from": "offline_db"}],
                },
            ],
        }
    }
    message_a = {
        "knowledge_graph": kg_a,
        "results": [],
    }

    kg_b = copy.deepcopy(kg)
    kg_b["edges"] = {
        "e1": {
            "subject": "MONDO:1",
            "predicate": "biolink:is_related_to",
            "object": "NCBI:1",
            "sources": [
                {
                    "resource": "infores:ara2",
                    "resource_role": "biolink:aggregator_knowledge_source",
                    "retrievals": [
                        {
                            "retrieved_from": "infores:kp1",
                        }
                    ],
                },
                {
                    "resource": "infores:kp2",
                    "resource_role": "biolink:primary_knowledge_source",
                    "retrievals": [{"retrieved_from": "offline_db"}],
                },
            ],
        }
    }

    message_b = {
        "knowledge_graph": kg_b,
        "results": [],
    }

    m = Message.merge(message_a, message_b)

    # Validate output
    m_dict = m.to_dict()
    edges = m_dict["knowledge_graph"]["edges"]

    assert len(edges) == 2
