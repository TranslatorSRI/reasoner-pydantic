from reasoner_pydantic import QNode, QEdge

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
