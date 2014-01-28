Serializable
============

Serializable is simple transfer object library to create simple serializable objects.


## Usage:

Define your transfer objects first.

```python
from serializable.base import AbstractObject


class PaymentObject(AbstractObject):
    attributes = ['transaction_id', 'amount']

class OrderObject(AbstractObject):
    attributes = ['order_id', 'payment']
    schema = {'payment': PaymentObject}
```

Serialization:
```python
order = OrderObject(order_id='OR0000001', payment=PaymentObject(transaction_id='TR000002', amount=100))

serialized = order.serialize()

"""
serialized contains now:

{'data': {'order_id': 'OR0000001',
  'payment': {'data': {'amount': 100, 'transaction_id': 'TR000002'},
   'object_type': '__main__.PaymentObject'}},
 'object_type': '__main__.OrderObject'}
"""

```

Deserialization:
```python
order = OrderObject()
order.deserialize(serialized)

print order.get_order_id()
"""
result:
OR0000001
"""

print order.get_payment().get_transaction_id()
"""
result:
TR000002
"""
```