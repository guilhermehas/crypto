import pytest

from examples_to_test import *
from server import *
from examples_to_test import blockchain as get_blockchain
from wallet import *

@pytest.fixture
def blockchain():
    return get_blockchain()

@pytest.fixture
def server():
    wallet= Wallet(3)
    return ServerUtils(wallet)

def test_same_transaction(server):
    transaction = transactions[0]
    transaction_str = server.to_str(transaction)
    transaction2 = server.to_obj(transaction_str)
    assert transaction.is_equal(transaction2)

def test_receive_blockArray(blockchain, server):
    blockArray = BlockArray(blockchain)
    server.receive_block_array(blockArray)
    assert len(server.blockchain) == 3

def test_receive_transaction(server, blockchain):
    transaction = transactions[0]
    len_blockchain_before = len(server.blockchain)

    server.receive_transaction(transaction)
    server.mine()

    len_blockchain_after = len(server.blockchain)
    assert len_blockchain_after == len_blockchain_before + 1