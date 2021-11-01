from reasoner_pydantic.shared import Attribute, BiolinkEntity
from reasoner_pydantic import Message, QNode, QEdge, QueryGraph

def test_qnode_null_properties():
    """ Check that we can parse a QNode with None property values """
    QNode.parse_obj({
        "ids": None,
        "categories": None,
    })

def test_qedge_null_properties():
    """ Check that we can parse a QEdge with None property values """
    QEdge.parse_obj({
        "subject" : "n0",
        "object" : "n1",
        "predicates": None,
    })

EXAMPLE_MESSAGE = {
    "query_graph": {
        "nodes" : {
            "n1" : {
                "categories" : ["biolink:ChemicalSubstance"]
            }
        },
        "edges" : {}
    },
    "knowledge_graph": {
        "nodes" : {},
        "edges" : {}
    },
    "results": [],
}

def test_message_hashable():
    """ Check that we can hash a message """

    m = Message.parse_obj(EXAMPLE_MESSAGE)
    h = hash(m)
    assert h

    m2 = Message.parse_obj(EXAMPLE_MESSAGE)
    h2 = hash(m2)

    assert h == h2


def test_hash_property_update():
    """ Check that we can update the property of an object and the hash changes """

    # Test on a QNode
    qnode = QNode.parse_obj({"categories" : ["biolink:ChemicalSubstance"]})

    h = hash(qnode)

    qnode.is_set = True

    assert hash(qnode) != h


def test_hash_list_update():
    """ Check that we can update a list property on an object and the hash changes """

    # Test on a QNode
    qnode = QNode.parse_obj({"categories" : ["biolink:ChemicalSubstance"]})
    h = hash(qnode)

    qnode.categories.append("biolink:Disease")
    assert hash(qnode) != h

def test_hash_dict_update():
    """ Check that we can update a dict property on an object and the hash changes """

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

    m.query_graph.nodes['n1'].categories.append(
        BiolinkEntity.parse_obj("biolink:Gene")
    )

    assert hash(m) != h


def test_hash_attribute_values():
    """
    Check that we can hash a dictionary valued attribute
    """

    a = Attribute.parse_obj({
        "attribute_type_id": "biolink:knowledge_source",
        "value": {"sources" : ["a", "b", "c"]},
    })
    assert hash(a)
