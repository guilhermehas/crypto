# test_app.py
import pytest
from flask import url_for
from json import dumps
from base64 import b64encode
import pickle

from examples_to_test import blockchain
from blockchain import BlockArray

MINER_PUB_KEY = 1
MINER_REWARD = 10
AMOUNT_TRANS = 1

@pytest.fixture
def transaction():
    transaction_dict = {
        'sender': MINER_PUB_KEY,
        'receiver': 2,
        'amount': AMOUNT_TRANS
    }
    return transaction_dict

def test_get_blockchain(client):
    res = client.get('blockchain')
    assert res.status_code == 200
    assert res.json == {'balances': {}, 'blocks': []}

class add:
    def __init__(self, transaction):
        self.transaction = transaction
    def to(self,client):
            res = client.post(url_for('add_transaction'), \
                            data=dumps(self.transaction), \
                            content_type='application/json')
            return res


def test_add_transaction(client, transaction):
    res = add(transaction).to(client)
    assert res.status_code == 200

def test_wrong_transaction(client):
    transaction = {'sender': 0, 'receiver': 2, 'amount': -1}
    res = add(transaction).to(client)
    assert res.status_code == 403

def test_mining(client):
    res = client.get('mine')
    assert res.status_code == 200
    
    res = client.get('blockchain')
    blockchain = res.json
    balances = blockchain['balances']
    assert balances[str(MINER_PUB_KEY)] == MINER_REWARD

def test_two_mining(client):
    client.get('mine')
    client.get('mine')
    
    res = client.get('blockchain')
    blockchain = res.json
    balances = blockchain['balances']
    assert balances[str(MINER_PUB_KEY)] == 2*MINER_REWARD

def test_mining_with_transactions(client, transaction):
    client.get('mine')
    add(transaction).to(client)
    client.get('mine')
    
    res = client.get('blockchain')
    blockchain = res.json
    balances = blockchain['balances']
    assert balances[str(MINER_PUB_KEY)] == 2*MINER_REWARD-AMOUNT_TRANS

def test_receive_blockchain(client, blockchain):
    blockArray = BlockArray(blockchain)
    blockchain_bytes = b64encode(pickle.dumps(blockArray))
    res = client.post(url_for('receive_blockchain'), \
                      data=blockchain_bytes)
    
    assert res.status_code == 200

    res = client.get('blockchain')
    blockchain = res.json
    assert len(blockchain['blocks']) == 3
    
def test_receive_ips(client):
    ips = ['localhost:8888']
    res = client.post(url_for('receive_ips'), \
                      data=dumps(ips))
    assert res.status_code == 200

    res = client.get(url_for('get_ips'))
    assert res.status_code == 200
    assert res.json == ips
