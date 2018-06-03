from block import Block, GenesisBlock
from transaction import *
from blockchain import *
import pytest

@pytest.fixture
def blockchain():
    blockchain = Blockchain()

    genesis_block = GenesisBlock(miner_pub_key=b'abc')
    genesis_block.mine(blockchain.get_difficult())
    blockchain.add(genesis_block)

    pubs_keys = [b"abc",b"p1"]
    miners = [b"p1",b"p2"]
    outputs_array = [
        [(b"abc", 1),(b"p1",2)],
        [(b"p2",10),(b"p1",1)]
    ]

    for key, miner, outputs in zip(pubs_keys, miners, outputs_array):
        transaction = Transaction(key, outputs)
        block = Block(blockchain.get_last_block(), [transaction], miner_pub_key=miner)
        block.mine(blockchain.get_difficult())
        blockchain.add(block)
    
    return blockchain

def test_blockchain_wrong(blockchain):
    blockchain.chain[-2].miner_pub_key = b"zzz"
    assert not blockchain.is_correct()
    
def test_blockchain_right(blockchain):
    assert blockchain.is_correct()
