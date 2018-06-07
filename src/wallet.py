from crypto import *
from copy import deepcopy

class Wallet:
    def __init__(self, private_key_number):
        self.private_key = PrivateKey(private_key_number)
    
    def get_public_key(self):
        return self.private_key.public_key()

    def get_public_key_in_bytes(self):
        return self.get_public_key().to_bytes()
    
    def sign(self,transaction):
        signed_transaction = deepcopy(transaction)

        if signed_transaction.input is None:
            signed_transaction.input = self.get_public_key_in_bytes()
        
        signature = self.private_key.sign(bytes(signed_transaction))
        signed_transaction.signature = signature
        return signed_transaction
    
    def get_balance(self,blockchain):
        pass