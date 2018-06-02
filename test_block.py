import pytest
from block import *


pygen = pytest.mark.parametrize("data", 
    ["abc", "cdb", "234", "44444"])

@pygen
def test_first_block(data: str):
    genesis_block = GenesisBlock(data=data)
    assert genesis_block.data == data

@pytest.fixture
def genesis_block():
    return GenesisBlock(data="abc")

@pygen
def test_second_block(data):
    block = Block(previous_block=genesis_block, data=data)
    assert block.data == data
    assert hash(genesis_block) == block.previous_hash

@pytest.mark.parametrize("data1,data2", [ 
    (None, ''),
    ('', '0'),
    ('abc', 'ab'),
    ('1', 1),
 ])
def test_diferent_hashes(data1, data2):
    block1, block2 = map(lambda data: GenesisBlock(data), (data1,data2))
    assert hash(block1) != hash(block2)
    