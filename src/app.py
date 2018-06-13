from typing import List

from json import loads
from base64 import b64decode
import pickle

from flask import Flask, jsonify, request
from forms import TransactionForm

from blockchain import Blockchain, BlockArray
from transaction_pool import TransactionPool
from transaction import Transaction
from wallet import Wallet
from block import GenesisBlock, Block
from crypto import PublicKey, PrivateKey

def create_app():
    app = Flask(__name__)
    
    blockchain = Blockchain()
    transactionPool = TransactionPool()
    ips_connected : List[str] = []

    miner_key_int = 1
    miner_key = PrivateKey(miner_key_int).public_key().to_bytes()

    @app.route('/blockchain')
    def blockchain_web():
        return jsonify(blockchain.to_dict())

    @app.route('/addtransaction', methods=['POST'])
    def add_transaction():
        transaction_dict = request.json
        form = TransactionForm(**transaction_dict)
        if form.validate():
            wallet = Wallet(miner_key_int)
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

        return ''
    
    @app.route('/receiveblockchain', methods=['POST'])
    def receive_blockchain():
        blockArray = pickle.loads(b64decode(request.data))
        if isinstance(blockArray, BlockArray):
            blockchain.substitute(blockArray)
            return ''
        return '', 403

    @app.route('/receiveips', methods=['POST'])
    def receive_ips():
        ips = loads(request.data.decode('utf-8'))
        if isinstance(ips, list):
            for ip in ips:
                ips_connected.append(ip)
            return ''
        return ''
    
    @app.route('/getips')
    def get_ips():
        return jsonify(ips_connected)

    return app