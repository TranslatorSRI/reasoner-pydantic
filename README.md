# Reasoner-Pydantic

[Pydantic](https://pydantic-docs.helpmanual.io/) models for the [Reasoner API](https://github.com/NCATS-Tangerine/NCATS-ReasonerStdAPI) data formats.

These models are very handy when setting up a Reasoner API with [FastAPI](https://fastapi.tiangolo.com/).

## Example usage

```python
from reasoner_pydantic import (
    Request, Message, QNode,
    KnowledgeGraph, KNode,
    Result, NodeBinding,
)

def answer_question(request):
    request: Request = Request(**request)
    message: Message = request.message

    # sanitize incoming message
    assert message.query_graph.nodes, 'Query graph has no nodes!'
    if message.knowledge_graph is None:
        message.knowledge_graph = KnowledgeGraph(nodes=[], edges=[])
    if message.results is None:
        message.results = []

    # get query graph node
    qnode: QNode = message.query_graph.nodes[0]

    # add knowledge graph node
    knode: KNode = KNode(id='bar')
    message.knowledge_graph.nodes.append(knode)

    # add result
    node_binding: NodeBinding = NodeBinding(
        qg_id=qnode.id,
        kg_id=knode.id,
    )
    result: Result = Result(
        node_bindings=[node_binding],
        edge_bindings=[],
    )
    message.results.append(result)

    return message.json()
```
