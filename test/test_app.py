# test_app.py
import pytest
from flask import url_for
from json import dumps

MINER_PUB_KEY = 1
MINER_REWARD = 10

@pytest.fixture
def transaction():
    transaction_dict = {
        'sender': MINER_PUB_KEY,
        'receiver': 2,
        'amount': 1
    }
    return transaction_dict

def test_get_blockchain(client):
    res = client.get('blockchain')
    assert res.status_code == 200
    assert res.json == {'balances': {}, 'blocks': []}

def add(transaction):
    class ClassNameLess:
        def to(self, client):
            res = client.post(url_for('add_transaction'), \
                            data=dumps(transaction), \
                            content_type='application/json')
            return res
    return ClassNameLess()

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
    assert blockchain['balances'][str(MINER_PUB_KEY)] == MINER_REWARD
