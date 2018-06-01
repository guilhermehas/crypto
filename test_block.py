from block import *

def test_first_block():
    data = 'abc'
    genesis_block = GenesisBlock(data=data)
    assert genesis_block.data == data