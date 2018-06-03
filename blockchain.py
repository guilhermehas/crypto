class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficult = 0
    
    def get_difficult(self):
        return self.difficult
    
    def add(self, block):
        self.chain.append(block)
    
    def get_last_block(self):
        if self.chain:
            return self.chain[-1]
        else:
            return None
    
    def is_correct(self):
        for i, block in enumerate(self.chain):
            if not block.is_mined(self.difficult):
                return False
            if i >= 1:
                is_previous_hash_wrong = block.previous_hash != hash(self.chain[i-1])
                if is_previous_hash_wrong:
                    return False
        return True