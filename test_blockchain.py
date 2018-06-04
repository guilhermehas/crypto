from block import Block, GenesisBlock
from transaction import *
from blockchain import *
from wallet import *
from tools import mapv
from crypto import private_to_pub_bytes
import pytest
from examples_to_test import blockchain as block_example

@pytest.fixture
def blockchain():
    return block_example()

def test_blockchain_wrong(blockchain):
    blockchain.chain[-2].miner_pub_key = b"zzz"
    assert not BlockArray(blockchain).is_correct()
    
def test_blockchain_right(blockchain):
    assert BlockArray(blockchain).is_correct()
