from block import Block, GenesisBlock
from transaction import *
from blockchain import BlockArray, Blockchain
from wallet import *
from tools import mapv
import pytest
from examples_to_test import *

def test_blockchain_to_dict(blockchain : Blockchain):
    blockchain_dict = blockchain.to_dict()
    #print(blockchain_dict)

def test_blockchain_wrong(blockchain : Blockchain):
    blockchain.chain[-2].miner_pub_key = b"zzz"
    assert not BlockArray(blockchain).is_correct()
    
def test_blockchain_right(blockchain : Blockchain):
    assert BlockArray(blockchain).is_correct()

def test_change_blockchain(blockchain : Blockchain):
    block = transaction_to_block(transactions[4], 11, blockchain)
    blockArray = BlockArray(blockchain)
    blockArray.add(block)
    previous_len = len(blockchain)

    assert blockchain.substitute(blockArray)
    assert len(blockchain) == len(blockArray)
    assert len(blockchain) == previous_len + 1

def test_dont_change_blockchain(blockchain : Blockchain):
    blockArray = BlockArray(blockchain)
    previous_len = len(blockchain)
    
    assert blockchain.substitute(blockArray)
    assert len(blockchain) == previous_len