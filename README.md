# Reasoner-Pydantic

[![Test status via GitHub Actions](https://github.com/TranslatorSRI/reasoner-pydantic/workflows/test/badge.svg)](https://github.com/TranslatorSRI/reasoner-pydantic/actions?query=workflow%3Atest) [ℹ️](tests/README.md)

[Pydantic](https://pydantic-docs.helpmanual.io/) models for the [Reasoner API](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI) data formats.

These models are very handy when setting up a Reasoner API with [FastAPI](https://fastapi.tiangolo.com/).

## Example usage

```python
from reasoner_pydantic import (
    Query, Message, QNode,
    KnowledgeGraph, KNode,
    Result, NodeBinding,
)

def answer_question(request):
    request: Query = Query(**request)
    message: Message = request.message

    # sanitize incoming message
    assert message.query_graph.nodes, 'Query graph has no nodes!'
    if message.knowledge_graph is None:
        message.knowledge_graph = KnowledgeGraph(nodes={}, edges={})
    if message.results is None:
        message.results = []

    # get query graph node
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
        foo='bar',
    )
    message.results.append(result)

    return message.json()
```
