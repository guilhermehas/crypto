class Wallet:
    def __init__(self, private_key: str):
        self.private_key = private_key
    
    def get_public_key(self):
        return self.private_key