from crypto import *
import pickle
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

class Transaction:
    def __init__(self, input, outputs, signature = None):
        self.input = input
        self.outputs = outputs
        self.signature = signature
    
    def __bytes__(self):
        all_data = pickle.dumps((self.input,self.outputs))
        return all_data
    
    def is_signed_correctly(self):
        return is_signed_correctly(self.signature, bytes(self), get_public_key(self.input))