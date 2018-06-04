from collections import defaultdict
from tools import mapv

class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficult = 0
        self.reward = 10
        self.balances = defaultdict(float)
        self.transaction_hashes = set()
    
    def get_difficult(self):
        return self.difficult
    
    def get_transactions(self):
        for block in self.chain:
            if block.transactions:
                yield from block.transactions
    
    def is_new_block_OK(self, block):
        senders = mapv(lambda transaction: transaction.input, block.transactions)
        is_just_one_senders_per_block = len(senders) != len(set(senders))
        if is_just_one_senders_per_block:
            return False

        for transaction in block.transactions:
            if hash(transaction) in self.transaction_hashes:
                return False

            sum_output = transaction.get_sum_outputs()
            if sum_output > self.balances[transaction.input]:
                return False

        if not block.is_mined(self.difficult):
            return False

        if len(self.chain) >= 1:
            is_previous_hash_wrong = block.previous_hash != hash(self.chain[-1])
            if is_previous_hash_wrong:
                return False
        return True

    def add(self, block):
        if self.is_new_block_OK(block):

            self.chain.append(block)
            self.transaction_hashes.add(hash(block))

            for transaction in block.transactions:
                sum_outs = transaction.get_sum_outputs()
                assert sum_outs >= 0

                miner_reward = self.balances[transaction.input] - sum_outs
                assert miner_reward >= 0

                self.balances[block.miner_pub_key] += miner_reward
                self.balances[transaction.input] = 0
                for pub_out, pub_rew in transaction.outputs:
                    self.balances[pub_out] += pub_rew
            self.balances[block.miner_pub_key] += self.reward
        else:
            raise Exception('Blockchain invalid')
    
    def get_last_block(self):
        if self.chain:
            return self.chain[-1]
        else:
            return None

class BlockArray:
    def __init__(self, blocks):
        if isinstance(blocks, Blockchain):
            self.chain = blocks.chain
        else:
            self.chain = blocks
    
    def is_correct(self):
        blockchain = Blockchain()
        for block in self.chain:
            if not blockchain.is_new_block_OK(block):
                return False
            blockchain.add(block)
        return True