from block import Block, GenesisBlock
from transaction import *
from blockchain import *
from wallet import *
from tools import mapv
from crypto import private_to_pub_bytes
import pytest

@pytest.fixture
def blockchain():
    blockchain = Blockchain()

    private_keys = [43,53,63]
    public_keys = mapv(private_to_pub_bytes,private_keys)

    genesis_block = GenesisBlock(miner_pub_key=public_keys[0])
    genesis_block.mine(blockchain.get_difficult())
    blockchain.add(genesis_block)

    miners = [public_keys[1],public_keys[2]]
    outputs_array = [
        [(public_keys[0], 1),(public_keys[1],2)],
        [(public_keys[2],10),(public_keys[1],1)]
    ]

    for key, miner, outputs in zip(private_keys, miners, outputs_array):
        transaction = Wallet(key).sign(Transaction(outputs))
        block = Block(blockchain.get_last_block(), [transaction], miner_pub_key=miner)
        block.mine(blockchain.get_difficult())
        blockchain.add(block)
    
    return blockchain

def test_blockchain_wrong(blockchain):
    blockchain.chain[-2].miner_pub_key = b"zzz"
    assert not BlockArray(blockchain).is_correct()
    
def test_blockchain_right(blockchain):
    assert BlockArray(blockchain).is_correct()
