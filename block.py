from hashlib import sha256
from pickle import dumps

class Block:
    def __init__(self, previous_block, transactions, nounce=0):
        self.transactions = transactions
        self.previous_hash = hash(previous_block)
        self.nounce = nounce
    
    def __hash__(self):
        return int(self.internal_hash().hexdigest(),16)

    def internal_hash(self):
        return sha256(dumps((self.previous_hash, tuple(self.transactions),self.nounce)))

    def mine(self, difficult):
        for i in range(10**9):
            self.nounce = i
            #print("aqui",hash(self))
            is_mined = hash(self)//(2**(60-8*difficult)) == 0
            if is_mined:
                #print(i)
                return
        raise Exception('too difficult to mine')


def GenesisBlock(transactions):
    return Block(previous_block=None, transactions=transactions)