from crypto import *
from copy import deepcopy

class Wallet:
    def __init__(self, private_key):
        self.private_key = get_private_key(private_key)
    
    def get_public_key(self):
        return self.private_key.public_key()

    def get_public_key_in_bytes(self):
        return pub_to_bytes(self.get_public_key())
    
    def sign(self,transaction):
        signed_transaction = deepcopy(transaction)
        signature = get_signature(self.private_key, bytes(transaction))
        signed_transaction.signature = signature
        return signed_transaction
    
    def get_balance(self,blockchain):
        pass