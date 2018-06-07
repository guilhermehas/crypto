from block import Block, GenesisBlock
from transaction import *
from blockchain import *
from wallet import *
from tools import mapv
import pytest
from examples_to_test import blockchain as block_example
from examples_to_test import *

@pytest.fixture
def blockchain():
    return block_example()

def test_blockchain_to_dict(blockchain):
    blockchain_dict = blockchain.to_dict()
    #print(blockchain_dict)

def test_blockchain_wrong(blockchain):
    blockchain.chain[-2].miner_pub_key = b"zzz"
    assert not BlockArray(blockchain).is_correct()
    
def test_blockchain_right(blockchain):
    assert BlockArray(blockchain).is_correct()

def test_change_blockchain(blockchain):
    block = transaction_to_block(transactions[4], 11, blockchain)
    blockArray = BlockArray(blockchain)
    blockArray.add(block)
    previous_len = len(blockchain)

    assert blockchain.substitute(blockArray)
    assert len(blockchain) == len(blockArray)
    assert len(blockchain) == previous_len + 1

def test_dont_change_blockchain(blockchain):
    blockArray = BlockArray(blockchain)
    previous_len = len(blockchain)
    
    assert blockchain.substitute(blockArray)
    assert len(blockchain) == previous_len