from crypto import *
import pickle
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

class Transaction:
    def __init__(self, input: int, outputs, signature = None, miner_pub_key = None):
        self.input = input
        self.outputs = outputs
        self.signature = signature
        self.miner_pub_key = miner_pub_key
    
    def __bytes__(self):
        all_data = pickle.dumps((self.input,self.outputs))
        return all_data
    
    def is_signed_correctly(self):
        return is_signed_correctly(self.signature, bytes(self), get_public_key(self.input))