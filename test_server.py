import pytest

from examples_to_test import *
from server import *
from examples_to_test import blockchain as get_blockchain

@pytest.fixture
def blockchain():
    return get_blockchain()

def test_same_transaction():
    transaction = transactions[0]
    server = ServerUtils()
    transaction_str = server.to_str(transaction)
    transaction2 = server.to_obj(transaction_str)
    assert transaction.is_equal(transaction2)

def test_receive_blockArray(blockchain):
    server = ServerUtils()
    blockArray = BlockArray(blockchain)
    server.receive_block_array(blockArray)
    assert len(server.blockchain) == 3