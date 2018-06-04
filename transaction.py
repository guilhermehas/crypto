from crypto import *
import pickle
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes

class Transaction:
    def __init__(self, outputs, input=None, timestamp = 0, signature = None):
        self.input = input
        self.outputs = outputs
        self.signature = signature
        self.timestamp = timestamp
    
    def __bytes__(self):
        to_compress = (self.input, self.outputs, self.timestamp)
        all_data = bytes(str(to_compress), encoding="utf-8")
        return all_data
    
    def is_signed_correctly(self):
        return is_signed_correctly(self.signature, bytes(self), get_public_key(self.input))
    
    def get_sum_outputs(self):
        sum_output = 0
        for _, out in self.outputs:
            sum_output += out
        return sum_output

    def is_equal(self, transaction):
        return self.input == transaction.input and \
            self.outputs == transaction.outputs and \
            self.timestamp == transaction.timestamp

            ##self.signature == transaction.signature and \