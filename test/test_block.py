import pytest
from block import *
from tools import mapv
from transaction import Transaction

blocks_data_tuples = [
    [('abc', 'abc', 0),
    ('', '', 0.001)],
    [('678', '', 1234),
    ('123', 'fff', 143553)]
]

block_data_transactions = mapv(lambda transactions:
[Transaction(input=sender_key, outputs=[receiver_key, amount])
for sender_key, receiver_key, amount in transactions],
blocks_data_tuples)

pygen = pytest.mark.parametrize('transactions',block_data_transactions)

@pytest.fixture
def genesis_block():
    return GenesisBlock(miner_pub_key=b'123')

@pygen
def test_second_block(transactions):
    block = Block(previous_block=genesis_block, transactions=transactions)
    assert block.transactions == transactions
    assert hash(genesis_block) == block.previous_hash

@pygen
def test_mining_block(transactions):
    block = Block(previous_block=genesis_block ,transactions=transactions)
    block.mine(difficult=0)

@pytest.mark.parametrize("pub_key1,pub_key2", [(b"123", b"321")] )
def test_diferent_hashes(pub_key1, pub_key2):
    block1, block2 = map(lambda pub_key: GenesisBlock(miner_pub_key=pub_key), (pub_key1,pub_key2))
    assert hash(block1) != hash(block2)