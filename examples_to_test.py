from transaction import *
from wallet import *
from tools import *

tuple_transactions = [
    (13, b'abc', 0),
    (1, b'', 0.001),
    (3, b'', 1234),
    (43, b'fff', 143553),
]


def to_transaction(data):
    sender_key, receiver_key, amount = data
    wallet = Wallet(sender_key)
    transaction = Transaction(outputs=[receiver_key,amount])
    signed_transaction = wallet.sign(transaction)
    return signed_transaction

transactions = mapv(to_transaction, tuple_transactions)