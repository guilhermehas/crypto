import pytest
from transaction import *

@pytest.mark.parametrize("sender_key,receiver_key,amount,signature", [ 
    ('abc', 'abc', 0, '2222'),
    ('', '', 0.001, 'avc'),
    ('678', '', 1234, '2323'),
    ('123', 'fff', 143553, '5fvv'),
])
def test_transaction(sender_key: str, receiver_key: str, amount: float, signature: str):
    transaction = Transaction(input=sender_key, outputs=[receiver_key,amount], signature=signature)
    assert transaction.input == sender_key
    assert transaction.outputs[0] == receiver_key
    assert transaction.outputs[1] == amount
    assert transaction.signature == signature
