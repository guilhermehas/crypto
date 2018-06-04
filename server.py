from pickle import dumps, loads
import pickle
from base64 import b64encode, b64decode
from blockchain import *
from transaction_pool import *
from block import *

class ServerUtils():
    def __init__(self, wallet):
        self.blockchain =  Blockchain()
        self.transactionPool = TransactionPool()
        self.wallet = wallet
    
    def receive_block_array(self, blockArray):
        self.blockchain.substitute(blockArray)
    
    def receive_transaction(self, transaction):
        self.transactionPool.receive_transaction(self.blockchain, transaction)
    
    def mine(self):
        transactions = self.transactionPool.get_best_transactions(self.blockchain, 1)
        block = Block(self.blockchain.get_last_block(), transactions,  \
            miner_pub_key=self.wallet.get_public_key_in_bytes())
        block.mine(self.blockchain.get_difficult())
        self.blockchain.add(block)
    
    def to_str(self, obj):
        return str(b64encode(dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)), 'utf8')
    
    def to_obj(self, string):
        return loads(b64decode(string))