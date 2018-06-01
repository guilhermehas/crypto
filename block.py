class Block:
    def __init__(self, data):
        self.data = data

def GenesisBlock(data: str):
    return Block(data=data)