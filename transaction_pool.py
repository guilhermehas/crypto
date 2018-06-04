from heapq import heappush, heappop
from blockchain import *

class TransactionPool:
    def __init__(self):
        #self.blockchain = blockchain
        self.transactions = []
    
    def get_miner_money(self, blockchain, transaction):
        money_spent = transaction.get_sum_outputs()
        miner_money = blockchain.balances[transaction.input] - money_spent
        return miner_money

    def is_transaction_right(self, blockchain, transaction):
        miner_money = self.get_miner_money(blockchain, transaction)
        is_valid_transaction = miner_money >= 0 and \
            hash(transaction) not in blockchain.transaction_hashes
        
        return is_valid_transaction

    def receive_transaction(self, blockchain, transaction):
        is_valid_transaction = self.is_transaction_right(blockchain, transaction)
        if is_valid_transaction:
            heappush(self.transactions,(-self.get_miner_money(blockchain, transaction),transaction))

        return is_valid_transaction
    
    def get_best_transactions(self, blockchain, n):
        best_transactions = []
        while n > 0 and self.transactions:
            transaction = heappop(self.transactions)[1]
            if self.is_transaction_right(blockchain, transaction):
                best_transactions.append(transaction)
                n -= 1
        
        return best_transactions

