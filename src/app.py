from typing import List

from json import loads, dumps
from base64 import b64decode, b64encode
import pickle
import requests

from flask import Flask, jsonify, request
from forms import TransactionForm

from blockchain import Blockchain, BlockArray
from transaction_pool import TransactionPool
from transaction import Transaction
from wallet import Wallet
from block import GenesisBlock, Block
from crypto import PublicKey, PrivateKey

def create_app(my_ip : str = 'localhost:5000', key : int = 1, servers : List[str] = []):
    app = Flask(__name__)
    
    blockchain = Blockchain()
    transactionPool = TransactionPool()

    miner_key = PrivateKey(key).public_key().to_bytes()

    def send_my_ip():
        server_data = servers+[my_ip]
        for server in servers:
            requests.post(f'http://{server}/receiveips', \
                          data=dumps(server_data))

    def send_blockchain():
        for server in servers:
            blockArray = BlockArray(blockchain)
            blockchain_bytes = b64encode(pickle.dumps(blockArray))
            requests.post(f'http://{server}/receiveblockchain', \
                          data=blockchain_bytes)

    send_my_ip()

    @app.route('/blockchain')
    def blockchain_web():
        return jsonify(blockchain.to_dict())

    @app.route('/addtransaction', methods=['POST'])
    def add_transaction():
        transaction_dict = request.json
        form = TransactionForm(**transaction_dict)
        if form.validate():
            wallet = Wallet(key)
            transaction = Transaction(outputs=[ 
                (PrivateKey(transaction_dict['receiver']).public_key().to_bytes(),
                transaction_dict['amount'])])
            signed_transaction = wallet.sign(transaction)
            transactionPool.receive_transaction(blockchain, signed_transaction)
            return ''
        return '', 403
    
    @app.route('/mine')
    def mine():
        if len(blockchain) == 0:
            genesis_block = GenesisBlock(miner_pub_key=miner_key)
            genesis_block.mine(blockchain.get_difficult())
            blockchain.add(genesis_block)
        else:
            block = Block(previous_block=blockchain.chain[-1], miner_pub_key=miner_key, \
                transactions=transactionPool.get_best_transactions(blockchain,1))
            block.mine(blockchain.get_difficult())
            blockchain.add(block)
        send_blockchain()
        return ''
    
    @app.route('/receiveblockchain', methods=['POST'])
    def receive_blockchain():
        blockArray = pickle.loads(b64decode(request.data))
        if isinstance(blockArray, BlockArray):
            len_before = len(blockchain)
            blockchain.substitute(blockArray)
            len_after = len(blockchain)
            if len_after > len_before:
                send_blockchain()
            return ''
        return '', 403

    @app.route('/receiveips', methods=['POST'])
    def receive_ips():
        ips = loads(request.data.decode('utf-8'))
        if isinstance(ips, list):
            for ip in ips:
                if ip not in servers and ip != my_ip:
                    print(f'Received {ip}')
                    servers.append(ip)
        return ''
    
    @app.route('/getips')
    def get_ips():
        return jsonify(servers)

    return app