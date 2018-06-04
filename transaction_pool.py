from heapq import heappush, heappop
from blockchain import *

class TransactionPool:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.transactions = []

    def receive_transaction(self, transaction):
        money_spent = transaction.get_sum_outputs()
        miner_money = self.blockchain.balances[transaction.input] - money_spent
        is_valid_transaction = miner_money >= 0 and \
            hash(transaction) not in self.blockchain.transaction_hashes
        
        if is_valid_transaction:
            heappush(self.transactions,(-miner_money,transaction))

        return is_valid_transaction
    
    def get_best_transactions(self, n):
        best_transactions = []
        while n > 0 and self.transactions:
            best_transactions.append(heappop(self.transactions)[1])
            n -= 1
        
        return best_transactions

