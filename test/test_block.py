import pytest
from typing import List
from block import Block, GenesisBlock
from tools import mapv
from transaction import Transaction

blocks_data_tuples = [
    [('abc', 'abc', 0),
    ('', '', 0.001)],
    [('678', '', 1234),
    ('123', 'fff', 143553)]
]

block_data_transactions = mapv(lambda transactions:
    [Transaction(input=sender_key, outputs=[(receiver_key, amount)])
        for sender_key, receiver_key, amount in transactions],
blocks_data_tuples)

pygen = pytest.mark.parametrize('transactions',block_data_transactions)

@pytest.fixture
def genesis_block():
    return GenesisBlock(miner_pub_key=b'123')

@pytest.fixture
def second_block(genesis_block : Block, transactions : List[Transaction]):
    return Block(previous_block=genesis_block, transactions=transactions, miner_pub_key=b'321')

@pygen
def test_second_block(transactions : List[Transaction], second_block : Block, genesis_block : Block):
    assert second_block.transactions == transactions
    assert hash(genesis_block) == second_block.previous_hash
    block_dict = second_block.to_dict()
    for el in ["previous_hash", "nounce", "transactions", "miner public key"]:
        assert el in block_dict

@pygen
def test_mining_block(transactions : List[Transaction]):
    block = Block(previous_block=genesis_block ,transactions=transactions)
    block.mine(difficult=0)
    assert block.is_mined(difficult=0)

@pytest.mark.parametrize("pub_key1,pub_key2", [(b"123", b"321")] )
def test_diferent_hashes(pub_key1 : bytes, pub_key2 : bytes):
    block1, block2 = map(lambda pub_key: GenesisBlock(miner_pub_key=pub_key), (pub_key1,pub_key2))
    assert hash(block1) != hash(block2)