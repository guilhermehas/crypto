from flask import Flask, jsonify
from blockchain import Blockchain

def create_app():
    app = Flask(__name__)
    blockchain = Blockchain()

    @app.route('/blockchain', methods=['GET'])
    def blockchain_web():
        return jsonify(blockchain.to_dict())

    return app