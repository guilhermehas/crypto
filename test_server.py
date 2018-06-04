from examples_to_test import *
from server import *

def test_same_transaction():
    transaction = transactions[0]
    server = ServerUtils()
    transaction_str = server.to_str(transaction)
    transaction2 = server.to_obj(transaction_str)
    assert transaction.is_equal(transaction2)