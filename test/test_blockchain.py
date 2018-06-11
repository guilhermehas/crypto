import pytest

from block import Block, GenesisBlock
from transaction import Transaction
from blockchain import BlockArray, Blockchain
from wallet import Wallet
from tools import mapv
from examples_to_test import transaction_to_block, transactions, blockchain, to_transaction

def test_blockchain_to_dict(blockchain : Blockchain):
    blockchain_dict = blockchain.to_dict()
    assert blockchain_dict is not None

def test_blockchain_wrong(blockchain : Blockchain):
    blockchain.chain[-2].miner_pub_key = b"zzz"
    barray = BlockArray(blockchain)
    assert not barray.is_correct()
    assert not blockchain.substitute(barray)
    with pytest.raises(Exception) as excinfo:   
        blockchain.add(blockchain.chain[0])
    assert str(excinfo.value) == 'Blockchain invalid'

def test_getting_transactions(blockchain : Blockchain):
    transactions = list(blockchain.get_transactions())
    assert len(transactions) > 0

def test_blockchain_small(blockchain : Blockchain):
    small_blockchain = Blockchain()
    small_blockchain.copy(blockchain)
    small_blockchain.chain.pop()

    assert not blockchain.substitute(small_blockchain)
    
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

def test_blockchain_not_mined(blockchain : Blockchain):
    block = blockchain.chain.pop()
    new_blockchain = BlockArray(blockchain).to_blockchain()
    new_blockchain.difficult = 5
    assert not new_blockchain.is_new_block_OK(block)

def test_blockchain_same_transaction(blockchain : Blockchain):
    transaction = blockchain.chain[-1].transactions[0]
    block = Block(previous_block=blockchain.chain[-1], transactions=[transaction])
    block.mine(blockchain.get_difficult())
    assert not blockchain.is_new_block_OK(block)

def test_blockchain_wrong_signature(blockchain : Blockchain):
    transaction = blockchain.chain[-1].transactions[0]
    transaction.signature = None
    block = Block(previous_block=blockchain.chain[-1], transactions=[transaction])
    block.mine(blockchain.get_difficult())
    assert not blockchain.is_new_block_OK(block)

def test_blockchain_two_signatures_in_block(blockchain : Blockchain):
    transactions = mapv(to_transaction, [(63, [(43, 11,)]), (63, [(42, 3)])])
    block = Block(previous_block=blockchain.chain[-1], transactions=transactions)
    block.mine(blockchain.get_difficult())
    assert not blockchain.is_new_block_OK(block)

def test_dont_change_blockchain(blockchain : Blockchain):
    blockArray = BlockArray(blockchain)
    previous_len = len(blockchain)
    
    assert blockchain.substitute(blockArray)
    assert len(blockchain) == previous_len