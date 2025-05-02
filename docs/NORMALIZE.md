# Edge ID Normalizing

Typically, edge ids are normalized on Message/Response validation, or on updating one Message/Response with another.

If you wish to avoid this:

```python
from reasoner_pydantic import Message

# Avoid normalization on creation
m = Message.model_validate(<your message dict>, context={"normalize": False})

# Avoid normalization when updating:
m.update(<your other message model>, normalize=False)
```
