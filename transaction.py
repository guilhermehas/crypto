from tools import *
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

class Transaction:
    def __init__(self, input: int, outputs, amount: float, signature = None, miner_pub_key = None):
        self.input = input
        self.outputs = outputs
        self.amount = amount
        self.signature = signature
        self.miner_pub_key = miner_pub_key
    
    def __bytes__(self):
        all_data = str((self.input,self.outputs,self.amount))
        return bytes(all_data, "utf-8")
    
    def is_signed_correctly(self):
        public_key = get_public_key_from_bytes(self.input)
        try:
            public_key.verify(self.signature, bytes(self), ec.ECDSA(hashes.SHA256()))
            return True
        except:
            return False
        