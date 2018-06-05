from hashlib import sha256
from pickle import dumps
from tools import *

class Block:
    def __init__(self, previous_block, transactions, miner_pub_key=None, nounce=0):
        self.transactions = transactions
        self.previous_hash = hash(previous_block)
        self.nounce = nounce
        self.miner_pub_key = miner_pub_key
    
    def to_dict(self):
        return {
            "previous_hash": self.previous_hash,
            "nounce": self.nounce,
            "transactions": [trans.to_dict() for trans in self.transactions],
            "miner public key": int(self.miner_pub_key.decode('utf8'))
        }
  
    def __hash__(self):
        return int(self.internal_hash().hexdigest(),16)

    def internal_hash(self):
        return sha256(dumps((self.previous_hash, [bytes(it) for it in self.transactions],self.nounce, self.miner_pub_key)))
    
    def is_mined(self,difficult):
        return hash(self)//(2**(60-8*difficult)) == 0

    def mine(self, difficult=0):
        for i in range(10**9):
            self.nounce = i
            if self.is_mined(difficult):
                #print(i)
                return
        raise Exception('too difficult to mine')


def GenesisBlock(miner_pub_key=None):
    return Block(previous_block=None, transactions=[], miner_pub_key=miner_pub_key)