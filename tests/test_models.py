from reasoner_pydantic import Message, QNode, QEdge
from reasoner_pydantic.utils import HashableMapping

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

def test_hashable_message():
    """ Check that we can hash and update a message correctly """
    m = Message.parse_obj({
        "query_graph": {
            "nodes" : {
                "n1" : {"categories" : ["biolink:ChemicalSubstance"]}
            },
            "edges" : {}
        },
        "knowledge_graph": {
            "nodes" : {},
            "edges" : {}
        },
        "results": [],
    })

    assert isinstance(m.query_graph.nodes, HashableMapping) # HashableMapping
    assert isinstance(m.query_graph.nodes["n1"], HashableMapping) # dict??
