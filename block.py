from hashlib import sha256
from pickle import dumps
from tools import to_tuple

class Block:
    def __init__(self, previous_block, transactions, miner_pub_key=None, nounce=0):
        self.transactions = transactions
        self.previous_hash = hash(previous_block)
        self.nounce = nounce
        self.miner_pub_key = miner_pub_key
    
    def __hash__(self):
        return int(self.internal_hash().hexdigest(),16)

    def internal_hash(self):
        return sha256(dumps((self.previous_hash, to_tuple(self.transactions),self.nounce, self.miner_pub_key)))
    
    def is_mined(self,difficult):
        return hash(self)//(2**(60-8*difficult)) == 0

    def mine(self, difficult):
        for i in range(10**9):
            self.nounce = i
            if self.is_mined(difficult):
                #print(i)
                return
        raise Exception('too difficult to mine')


def GenesisBlock(miner_pub_key=None):
    return Block(previous_block=None, transactions=None, miner_pub_key=miner_pub_key)