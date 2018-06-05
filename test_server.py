import pytest

from examples_to_test import *
from server import *
from examples_to_test import blockchain as get_blockchain
from wallet import *
import random

@pytest.fixture
def blockchain():
    return get_blockchain()

@pytest.fixture
def server():
    wallet= Wallet(3)
    return ServerUtils(wallet)

def test_print_blockchain(blockchain, server):
    server.receive_block_array(BlockArray(blockchain))
    msg = server.get_blockchain_str()
    assert isinstance(msg, str)


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

def test_mine(server):
    server.mine()
    assert len(server.blockchain) == 1

def test_mine_command(server, blockchain):
    transaction = transactions[0]
    len_blockchain_before = len(server.blockchain)

    server.receive_transaction(transaction)
    command = {
        'agent': 'person',
        'command': 'mine'
    }
    ret = server.execute(command)
    assert ret == 'mined'

    len_blockchain_after = len(server.blockchain)
    assert len_blockchain_after == len_blockchain_before + 1

def test_transaction_command_person(server, blockchain):
    server.receive_block_array(BlockArray(blockchain))
    command = {
        'agent': 'person',
        'command': 'transaction',
        'sender': 63,
        'receiver': 53,
        'amount': 1
    }
    len_before = len(server.transactionPool.transactions)
    server.execute(command)
    len_after = len(server.transactionPool.transactions)
    assert len_after == len_before + 1
