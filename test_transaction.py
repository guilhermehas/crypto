import pytest
from transaction import *
from wallet import *
from crypto import *


@pytest.mark.parametrize("sender_key,receiver_key,amount", [ 
    (43, 53, 0),
    (53, 43, 0.001),
    (63, 43, 1234),
])
def test_transaction(sender_key, receiver_key, amount: float):
    receiver_pub_key = private_to_pub_bytes(receiver_key)
    transaction = Transaction(outputs = [(receiver_pub_key, amount)])
    wallet = Wallet(sender_key)
    signed_transaction = wallet.sign(transaction)

    assert signed_transaction.is_signed_correctly()
    print(signed_transaction)
