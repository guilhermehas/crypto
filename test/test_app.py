# test_app.py
import pytest
from flask import url_for

def test_get_blockchain(client):
    res = client.get('blockchain')
    assert res.status_code == 200
    assert res.json == {'balances': [], 'blocks': []}