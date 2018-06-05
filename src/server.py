from pickle import dumps, loads
import pickle
from base64 import b64encode, b64decode
from blockchain import *
from transaction_pool import *
from block import *
from wallet import *

class ServerUtils():
    def __init__(self, wallet):
        self.blockchain =  Blockchain()
        self.transactionPool = TransactionPool()
        self.wallet = wallet
    
    def receive_block_array(self, blockArray):
        self.blockchain.substitute(blockArray)
    
    def receive_transaction(self, transaction):
        self.transactionPool.receive_transaction(self.blockchain, transaction)
    
    def get_blockchain_str(self):
        return str(self.blockchain.to_dict())
    
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
    
    def get_command_blockchain(self):
        command = {
            'agent': 'machine',
            'command': 'blockchain',
            'blockchain': self.to_str(BlockArray(self.blockchain))
        }
        return command
    
    def execute(self, command_dict):
        command = command_dict.get('command', '')
        agent = command_dict.get('agent', '')
        
        if agent == 'machine':
            if command == 'transaction':
                self.receive_transaction(self.to_obj(command_dict['transaction']))
            elif command == 'blockchain':
                print(f"receiving {self.to_obj(command_dict['blockchain']).is_correct()}")
                self.receive_block_array(self.to_obj(command_dict['blockchain']))
        elif agent == 'person':
            if command == 'mine':
                self.mine()
                return {"message": "mined", 'command': 'blockchain'}
            elif command == 'transaction':
                receiver = command_dict['receiver']
                receiver_pub = Wallet(receiver).get_public_key_in_bytes()

                sender = command_dict['sender']
                wallet_sender = Wallet(sender)
                amount = command_dict['amount']

                transaction = Transaction(outputs=[(receiver_pub, amount)])
                transaction = wallet_sender.sign(transaction)
                self.receive_transaction(transaction)
            elif command == 'blockchain':
                return {'message': self.blockchain.to_dict()}


        return {'message': ''}