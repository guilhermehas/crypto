from typing import List, Dict, Any, Optional

from hashlib import sha256
from pickle import dumps
from tools import mapv

from transaction import Transaction

class Block:
    def __init__(self, previous_block : Optional['Block'], transactions : List[Transaction], \
        miner_pub_key : Optional[bytes] = None, nounce : int = 0) -> None:
        
        self.transactions = transactions
        self.previous_hash = hash(previous_block)
        self.nounce = nounce
        self.miner_pub_key = miner_pub_key
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "previous_hash": self.previous_hash,
            "nounce": self.nounce,
            "transactions": [trans.to_dict() for trans in self.transactions],
            "miner public key": int(self.miner_pub_key.decode('utf8')) 
            if isinstance(self.miner_pub_key, bytes) else 'None'
        }
  
    def __hash__(self) -> int:
        return int(self.internal_hash().hexdigest(),16)

    def internal_hash(self):
        return sha256(dumps((self.previous_hash, [bytes(it) for it in self.transactions],self.nounce, self.miner_pub_key)))
    
    def is_mined(self, difficult : int) -> bool:
        return hash(self)//(2**(60-8*difficult)) == 0

    def mine(self, difficult : int = 0) -> None:
        for i in range(10**9):
            self.nounce = i
            if self.is_mined(difficult):
                return
        #raise Exception('too difficult to mine')


def GenesisBlock(miner_pub_key : Optional[bytes] = None) -> Block:
    return Block(previous_block=None, transactions=[], miner_pub_key=miner_pub_key)