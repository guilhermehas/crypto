class Block:
    def __init__(self, previous_block, data: str):
        self.data = data
        self.previous_hash = hash(previous_block)
    
    def __hash__(self):
        return hash((self.previous_hash, self.data))

def GenesisBlock(data: str):
    return Block(previous_block=None, data=data)