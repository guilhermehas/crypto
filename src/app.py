from json import loads

from flask import Flask, jsonify, request
from forms import TransactionForm

from blockchain import Blockchain
from block import GenesisBlock
from crypto import PublicKey, PrivateKey

def create_app():
    app = Flask(__name__)
    blockchain = Blockchain()
    miner_key = PrivateKey(1).public_key().to_bytes()

    @app.route('/blockchain')
    def blockchain_web():
        return jsonify(blockchain.to_dict())

    @app.route('/addtransaction', methods=['POST'])
    def add_transaction():
        form = TransactionForm(**request.json)
        if form.validate():
            return ''
        return '', 403
    
    @app.route('/mine')
    def mine():
        genesis_block = GenesisBlock(miner_pub_key=miner_key)
        genesis_block.mine(blockchain.get_difficult())
        blockchain.add(genesis_block)
        return ''

    return app