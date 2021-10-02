from reasoner_pydantic import QNode, QEdge, Message

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


def test_frozendict():
    """ Test that the frozen dict method provides a hash """
    m = Message.parse_obj({
        "query_graph": {
            "nodes": {
                "n0": {
                    "categories": [
                        "biolink:Gene"
                    ]
                },
                "n1": {
                    "ids": [
                        "CHEBI:45783"
                    ],
                    "categories": [
                        "biolink:ChemicalSubstance"
                    ]
                }
            },
            "edges": {
                "e01": {
                    "subject": "n0",
                    "object": "n1",
                    "predicates": [
                        "biolink:related_to"
                    ]
                }
            }
        }
    })

    m_frozen_sets = m.frozendict(setify=True)
    assert isinstance(
        m_frozen_sets["query_graph"]["nodes"]["n0"]["categories"],
        frozenset
    )
    assert hash(m_frozen_sets)

    m_frozen_tuples = m.frozendict()
    assert isinstance(
        m_frozen_tuples["query_graph"]["nodes"]["n0"]["categories"],
        tuple
    )
    assert hash(m_frozen_tuples)
