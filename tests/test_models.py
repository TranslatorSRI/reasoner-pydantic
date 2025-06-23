from typing import Optional
from pydantic import ValidationError
from reasoner_pydantic.base_model import BaseModel
from reasoner_pydantic.shared import Attribute, BiolinkEntity
from reasoner_pydantic import Message, QNode, QEdge, QueryGraph, Result, Response
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
            "CHEBI:6801": {"categories": ["biolink:NamedThing"], "attributes": []},
            "MONDO:5148": {"categories": ["biolink:NamedThing"], "attributes": []},
            "CHEBI:6802": {"categories": ["biolink:NamedThing"], "attributes": []},
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
                "attributes": [],
            },
        },
    },
    "results": [
        {
            "node_bindings": {
                "n1": [{"id": "CHEBI:6801", "attributes": []}],
                "n2": [{"id": "MONDO:5148", "attributes": []}],
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
                    "attributes": [],
                },
                {
                    "resource_id": "ara0",
                    "edge_bindings": {
                        "n1n2": [
                            {
                                "id": "CHEBI:6802-biolink:treats-MONDO:5148",
                                "attributes": [],
                            }
                        ]
                    },
                    "attributes": [],
                },
                {
                    "resource_id": "ara1",
                    "edge_bindings": {
                        "n1n2": [
                            {
                                "id": "CHEBI:6801-biolink:treats-MONDO:5148",
                                "attributes": [],
                            }
                        ]
                    },
                    "attributes": [],
                },
            ],
        }
    ],
    "auxiliary_graphs": {
        "a1": {"edges": ["CHEBI:6801-biolink:treats-MONDO:5148"], "attributes": []}
    },
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
                "predicates": ["biolink:related_to"],
            },
            "n1n2": {
                "subject": "n1",
                "object": "n2",
                "predicates": ["biolink:related_to"],
            },
        },
    },
    "knowledge_graph": {
        "nodes": {
            "CHEBI:6801": {"categories": ["biolink:NamedThing"], "attributes": []},
            "MONDO:5148": {"categories": ["biolink:NamedThing"], "attributes": []},
            "CHEBI:6802": {"categories": ["biolink:NamedThing"], "attributes": []},
            "CHEBI:6803": {"categories": ["biolink:NamedThing"], "attributes": []},
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
                "attributes": [],
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
                "attributes": [],
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
                "attributes": [],
            },
        },
    },
    "results": [
        {
            "node_bindings": {
                "n0": [{"id": "CHEBI:6803", "attributes": []}],
                "n1": [
                    {"id": "CHEBI:6801", "attributes": []},
                    {"id": "CHEBI:6802", "attributes": []},
                ],
                "n2": [{"id": "MONDO:5148", "attributes": []}],
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
                                "attributes": [],
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
                                "attributes": [],
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
                                "attributes": [],
                            }
                        ]
                    },
                },
            ],
        }
    ],
    "auxiliary_graphs": {"a1": {"edges": ["CHEBI:6801-biolink:treats-MONDO:5148"]}},
}

PATHFINDER_MESSAGE = {
    "query_graph": {
        "nodes": {
            "n0": {"ids": ["MONDO:0005011"]},
            "n1": {"ids": ["MONDO:0005180"]},
        },
        "paths": {
            "p0": {
                "subject": "n0",
                "object": "n1",
                "constraints": [{"intermediate_categories": ["biolink:Gene"]}],
            }
        },
    },
    "knowledge_graph": {
        "nodes": {
            "MONDO:0005011": {"categories": ["biolink:Disease"], "attributes": []},
            "MONDO:0005180": {"categories": ["biolink:Disease"], "attributes": []},
            "NCBIGene:120892": {"categories": ["biolink:Gene"], "attributes": []},
        },
        "edges": {
            "e0": {
                "subject": "MONDO:0005011",
                "object": "NCBIGene:120892",
                "predicate": "biolink:condition_associated_with_gene",
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
                        "attributes": [],
                    }
                ],
            },
            "e1": {
                "subject": "NCBIGene:120892",
                "object": "MONDO:0005180",
                "predicate": "biolink:biomarker_for",
                "sources": [
                    {
                        "resource_id": "kp0",
                        "resource_role": "primary_knowledge_source",
                    }
                ],
                "attributes": [],
            },
        },
    },
    "results": [
        {
            "node_bindings": {
                "n1": [{"id": "MONDO:0005011", "attributes": []}],
                "n2": [{"id": "MONDO:0005180", "attributes": []}],
            },
            "analyses": [
                {
                    "resource_id": "ara0",
                    "path_bindings": {"p0": [{"id": "a0", "attributes": []}]},
                }
            ],
        }
    ],
    "auxiliary_graphs": {"a0": {"edges": ["e0", "e1"], "attributes": []}},
}

INVALID_PATHFINDER_QUERY = {
    "query_graph": {
        "nodes": {
            "n0": {"ids": ["MONDO:0005011"]},
            "n1": {"ids": ["MONDO:0005180"]},
        },
        "paths": {
            "p0": {
                "subject": "n0",
                "object": "n1",
                "constraints": [{"intermediate_categories": []}],
            }
        },
    }
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


def test_response():
    """
    Test that response object is parsed properly
    """

    response = Response.parse_obj({"message": EXAMPLE_MESSAGE})
    assert isinstance(response, Response)


def test_pathfinder_message():
    """
    Test that pathfinder messages can be parsed.
    """

    message = Message.parse_obj(PATHFINDER_MESSAGE)

    assert isinstance(message, Message)

def test_invalid_pathfinder_query():
    """"
    Test that pathfinder message with empty intermediate categories errors.
    """

    try:
        message = Message.parse_obj(INVALID_PATHFINDER_QUERY)
    except Exception as e:
        assert isinstance(e, ValidationError)