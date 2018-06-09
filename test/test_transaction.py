import pytest
from transaction import *
from wallet import *
from crypto import *


@pytest.mark.parametrize("sender_key,receiver_key,amount", [ 
    (43, 53, 0),
    (53, 43, 0.001),
    (63, 43, 1234),
])
def test_transaction(sender_key : int, receiver_key : int, amount: float):
    receiver_pub_key = PrivateKey(receiver_key).public_key().to_bytes()
    transaction = Transaction(outputs = [(receiver_pub_key, amount)])
    wallet = Wallet(sender_key)
    signed_transaction = wallet.sign(transaction)

    assert signed_transaction.is_signed_correctly()
