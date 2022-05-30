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
from reasoner_pydantic.utils import HashableSet


def test_manipulation():
    """Test manipulation."""
    request: Query = Query(
        **{
            "message": {
                "query_graph": {
                    "nodes": {"x": {}},
                    "edges": {},
                }
            }
        }
    )

    message: Message = request.message
    message.knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    message.results = HashableSet[Result]()

    # get query graph node
    assert message.query_graph.nodes, "Query graph contains no nodes!"
    qnode_id = next(iter(message.query_graph.nodes))

    # add knowledge graph node
    knode: Node = Node()
    knode_id = "foo:bar"
    message.knowledge_graph.nodes[knode_id] = knode

    # add result
    node_binding: NodeBinding = NodeBinding(
        id=knode_id,
    )
    result: Result = Result(
        node_bindings={qnode_id: [node_binding]},
        edge_bindings={},
        foo="bar",
    )
    message.results.add(result)

    message.json()


def test_singletons():
    """Test that str-valued `categories` works."""
    qnode = QNode(
        **{
            "ids": ["MONDO:0005737"],
            "categories": ["biolink:Disease"],
        }
    )
