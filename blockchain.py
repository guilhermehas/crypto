from collections import defaultdict
from tools import mapv
from transaction import *
from copy import deepcopy

class Blockchain:
    def __init__(self):
        self.reset()

    def reset(self):
        self.chain = []
        self.difficult = 0
        self.reward = 10
        self.balances = defaultdict(float)
        self.transaction_hashes = set()
    
    def copy(self, blockchain):
        self.chain = deepcopy(blockchain.chain)
        self.difficult = blockchain.difficult
        self.reward = blockchain.reward
        self.balances = deepcopy(blockchain.balances)
        self.transaction_hashes = deepcopy(blockchain.transaction_hashes)
    
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

        def is_transaction_right(transaction):
            if not transaction.is_signed_correctly():
                return False
            
            if hash(transaction) in self.transaction_hashes:
                return False

            sum_output = transaction.get_sum_outputs()
            if sum_output > self.balances[transaction.input]:
                return False
            return True

        if block.transactions and not(any(map(is_transaction_right,block.transactions))):
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

            for transaction in block.transactions:
                self.transaction_hashes.add(hash(transaction))
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
    
    def substitute(self, blockArray):
        if len(blockArray) < len(self):
            return False
        new_blockchain = blockArray.to_blockchain()
        if new_blockchain is None:
            return False
        self.copy(new_blockchain)
        return True

    
    def __len__(self):
        return len(self.chain)

    def get_last_block(self):
        if self.chain:
            return self.chain[-1]
        else:
            return None

class BlockArray:
    def __init__(self, blocks):
        if isinstance(blocks, Blockchain):
            self.chain = deepcopy(blocks.chain)
        else:
            self.chain = deepcopy(blocks)
    
    def to_blockchain(self):
        blockchain = Blockchain()
        for block in self.chain:
            if not blockchain.is_new_block_OK(block):
                return None
            blockchain.add(block)
        return blockchain

    def is_correct(self):
        if self.to_blockchain() is None:
            return False
        return True
    
    def add(self, block):
        self.chain.append(block)
    
    def __len__(self):
        return len(self.chain)