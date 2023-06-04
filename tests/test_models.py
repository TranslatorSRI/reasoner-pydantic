from typing import Optional
from reasoner_pydantic.base_model import BaseModel
from reasoner_pydantic.shared import Attribute, BiolinkEntity
from reasoner_pydantic import Message, QNode, QEdge, QueryGraph, Result
from reasoner_pydantic.utils import HashableMapping, HashableSequence, HashableSet


def test_qnode_null_properties():
    """Check that we can parse a QNode with None property values"""
    QNode.parse_obj(
        {
            "ids": None,
            "categories": None,
        }
    )


def test_qedge_null_properties():
    """Check that we can parse a QEdge with None property values"""
    QEdge.parse_obj(
        {
            "subject": "n0",
            "object": "n1",
            "predicates": None,
        }
    )


EXAMPLE_MESSAGE = {
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
            "CHEBI:6802": {},
        },
        "edges": {
            "CHEBI:6801-biolink:treats-MONDO:5148": {
                "subject": "CHEBI:6801",
                "object": "MONDO:5148",
                "predicate": "biolink:treats",
                "sources": [
                    {
                        "resource_id": "kp0",
                        "resource_role": "primary_knowledge_source",
                    }
                ],
                "attributes": [
                    {
                        "attribute_type_id": "biolink:attribute",
                        "value": {"sources": ["a", "b", "c"]},
                        "attributes": [
                            {
                                "attribute_type_id": "biolink:attribute",
                                "value": {"sources": ["a", "b", "c"]},
                                "attributes": [
                                    {
                                        "attribute_type_id": "biolink:attribute",
                                        "value": {"sources": ["a", "b", "c"]},
                                        "attributes": [
                                            {
                                                "attribute_type_id": "biolink:attribute",
                                                "value": {"sources": ["a", "b", "c"]},
                                            }
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
            "CHEBI:6802-biolink:treats-MONDO:5148": {
                "subject": "CHEBI:6802",
                "object": "MONDO:5148",
                "predicate": "biolink:treats",
                "sources": [
                    {
                        "resource_id": "kp0",
                        "resource_role": "primary_knowledge_source",
                    }
                ],
            },
        },
    },
    "results": [
        {
            "node_bindings": {
                "n1": [{"id": "CHEBI:6801"}],
                "n2": [{"id": "MONDO:5148"}],
            },
            "analyses": [
                {
                    "resource_id": "ara0",
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
                            }
                        ]
                    },
                },
                {
                    "resource_id": "ara0",
                    "edge_bindings": {
                        "n1n2": [
                            {
                                "id": "CHEBI:6802-biolink:treats-MONDO:5148",
                            }
                        ]
                    },
                },
                {
                    "resource_id": "ara1",
                    "edge_bindings": {
                        "n1n2": [
                            {
                                "id": "CHEBI:6801-biolink:treats-MONDO:5148",
                            }
                        ]
                    },
                },
            ],
        }
    ],
    "auxiliary_graphs": {"a1": {"edges": ["CHEBI:6801-biolink:treats-MONDO:5148"]}},
}

EXAMPLE_MESSAGE_MULT = {
    "query_graph": {
        "nodes": {
            "n0": {"categories": ["biolink:ChemicalSubstance"]},
            "n1": {"categories": ["biolink:Gene"]},
            "n2": {"categories": ["biolink:Disease"]},
        },
        "edges": {
            "n0n1": {
                "subject": "n0",
                "object": "n1",
                "predicates": ["biolink:related_to"] 
            },
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
            "CHEBI:6802": {},
            "CHEBI:6803": {}
        },
        "edges": {
            "CHEBI:6801-biolink:related_to-MONDO:5148": {
                "subject": "CHEBI:6801",
                "object": "MONDO:5148",
                "predicate": "biolink:related_to",
                "sources": [
                    {
                        "resource_id": "kp0",
                        "resource_role": "primary_knowledge_source",
                    }
                ],
            },
            "CHEBI:6802-biolink:related_t0-MONDO:5148": {
                "subject": "CHEBI:6802",
                "object": "MONDO:5148",
                "predicate": "biolink:related_to",
                "sources": [
                    {
                        "resource_id": "kp0",
                        "resource_role": "primary_knowledge_source",
                    }
                ],
            },
            "CHEBI:6803-biolink:related_to-MONDO:5148": {
                "subject": "CHEBI:6803",
                "object": "MONDO:5148",
                "predicate": "biolink:related_to",
                "sources": [
                    {
                        "resource_id": "kp0",
                        "resource_role": "primary_knowledge_source",
                    }
                ],
            },
        },
    },
    "results": [
        {
            "node_bindings": {
                "n0":[{"id": "CHEBI:6803"}],
                "n1": [{"id": "CHEBI:6801"}, {"id": "CHEBI:6802"}],
                "n2": [{"id": "MONDO:5148"}],
            },
            "analyses": [
                {
                    "resource_id": "ara0",
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
                            }
                        ]
                    },
                },
                {
                    "resource_id": "ara0",
                    "edge_bindings": {
                        "n1n2": [
                            {
                                "id": "CHEBI:6802-biolink:treats-MONDO:5148",
                            }
                        ]
                    },
                },
                {
                    "resource_id": "ara1",
                    "edge_bindings": {
                        "n1n2": [
                            {
                                "id": "CHEBI:6801-biolink:treats-MONDO:5148",
                            }
                        ]
                    },
                },
                {
                    "resource_id": "ara0",
                    "edge_bindings": {
                        "n0n1": [
                            {
                                "id": "CHEBI:6803-biolink:treats-MONDO:5148",
                            }
                        ]
                    },
                }
            ],
        }
    ],
    "auxiliary_graphs": {"a1": {"edges": ["CHEBI:6801-biolink:treats-MONDO:5148"]}},
}


def test_message_hashable():
    """Check that we can hash a message"""

    m = Message.parse_obj(EXAMPLE_MESSAGE)
    h = hash(m)
    assert h

    m2 = Message.parse_obj(EXAMPLE_MESSAGE)
    h2 = hash(m2)

    assert h == h2


def test_message_jsonify():
    """Check that we can jsonify a message"""

    m = Message.parse_obj(EXAMPLE_MESSAGE)
    m_json = m.json()
    m2 = Message.parse_raw(m_json)

    assert m == m2


def test_message_dictify():
    """Check that we can dictify a message"""

    m = Message.parse_obj(EXAMPLE_MESSAGE)
    m_dict = m.dict()
    m2 = Message.parse_obj(m_dict)

    assert m == m2

    assert type(next(iter(m_dict["results"]))) == dict


def test_hash_property_update():
    """Check that we can update the property of an object and the hash changes"""

    # Test on a QNode
    qnode = QNode.parse_obj({"categories": ["biolink:ChemicalSubstance"]})

    h = hash(qnode)

    qnode.is_set = True

    assert hash(qnode) != h


def test_hash_list_update():
    """Check that we can update a list property on an object and the hash changes"""

    # Test on a QNode
    qnode = QNode.parse_obj({"categories": ["biolink:ChemicalSubstance"]})
    h = hash(qnode)

    qnode.categories.append("biolink:Disease")
    assert hash(qnode) != h


def test_hash_dict_update():
    """Check that we can update a dict property on an object and the hash changes"""

    # Test on a QueryGraph
    kg = QueryGraph.parse_obj(EXAMPLE_MESSAGE["query_graph"])
    h = hash(kg)

    kg.nodes["n0"] = kg.nodes["n1"]

    assert hash(kg) != h


def test_hash_deeply_nested_update():
    """
    Check that we can update a deeply nested object and the hash change is propogated
    """

    m = Message.parse_obj(EXAMPLE_MESSAGE)
    h = hash(m)

    m.query_graph.nodes["n1"].categories.append(BiolinkEntity("biolink:Gene"))

    assert hash(m) != h


def test_hash_attribute_values():
    """
    Check that we can hash a dictionary valued attribute
    """

    a = Attribute.parse_obj(
        {
            "attribute_type_id": "biolink:knowledge_source",
            "value": {"sources": ["a", "b", "c"]},
        }
    )
    assert hash(a)


def test_combine_analyses():
    """
    Test that combine analyses function combines analyses
    """
    result = Result.parse_obj(EXAMPLE_MESSAGE_MULT["results"][0])
    result.combine_analyses_by_resource_id()
    r = result.dict()
    assert len(r["analyses"]) == 2
    for analysis in r["analyses"]:
        if analysis["resource_id"] == "ara0":
            assert len(analysis["edge_bindings"]["n1n2"]) == 2
            assert len(analysis["edge_bindings"]["n0n1"]) == 1
