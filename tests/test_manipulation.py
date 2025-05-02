"""Test manipulation."""

from reasoner_pydantic import (
    Query,
    Message,
    QNode,
    KnowledgeGraph,
    Node,
    Result,
    NodeBinding,
)
from reasoner_pydantic.results import Results
from reasoner_pydantic.shared import CURIE


def test_manipulation():
    """Test manipulation."""
    request: Query = Query.model_validate(
        {
            "message": {
                "query_graph": {
                    "nodes": {"x": {}},
                    "edges": {},
                }
            }
        }
    )

    message: Message = request.message
    message.knowledge_graph = KnowledgeGraph()
    message.results = Results()

    # get query graph node
    assert message.query_graph is not None
    assert message.query_graph.nodes, "Query graph contains no nodes!"
    qnode_id = next(iter(message.query_graph.nodes))

    # add knowledge graph node
    knode: Node = Node.model_validate(
        dict(categories=["biolink:NamedThing"], attributes=[])
    )
    knode_id = CURIE("foo:bar")
    message.knowledge_graph.nodes[knode_id] = knode

    # add result
    node_binding: NodeBinding = NodeBinding.model_validate(
        dict(id=knode_id, attributes=[])
    )
    result: Result = Result.model_validate(
        dict(
            node_bindings={qnode_id: [node_binding]},
            analyses=[],
            foo="bar",
        )
    )
    message.results.add(result)

    print(message.model_dump_json())


def test_singletons():
    """Test that str-valued `categories` works."""
    _qnode = QNode.model_validate(
        {
            "ids": ["MONDO:0005737"],
            "categories": ["biolink:Disease"],
        }
    )
