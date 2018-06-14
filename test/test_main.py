import pytest

import time
import requests
from threading import Thread
import sys
from collections import namedtuple

from thread_utils import ServerThread

class Args:
    def __init__(self, wallet=1, servers=[]):
        self.wallet = wallet
        self.servers = servers
        self.port = None
        self.ip = 'localhost'

def to_dict(wallet=1, servers=[]):
    return Args(wallet=wallet, servers=servers)

ps = [0,0]

@pytest.fixture
def p1():
    server_thread = ServerThread()
    server_thread.setup(Args(wallet=1))
    server_thread.start()

    p1 = server_thread.port
    ps[0] = p1
    yield server_thread.port

    server_thread.stop()
    server_thread.join()

@pytest.fixture
def p2():
    server_thread = ServerThread()
    server_thread.setup(Args(wallet=2, servers=[f'localhost:{ps[0]}']))
    server_thread.start()
    time.sleep(0.01)

    yield server_thread.port

    server_thread.stop()
    server_thread.join()

@pytest.mark.skip(reason="test too long")
def test_both_server(p1, p2):
    assert True

@pytest.mark.skip(reason="test too long")
def test_server_running(p1, p2):
    res = requests.get(f'http://localhost:{p1}/blockchain')
    assert res.status_code == 200

@pytest.mark.skip(reason="test too long")
def test_update_blockchain(p1, p2):
    ip1 = f'http://localhost:{p1}'
    
    ip2 = f'http://localhost:{p2}'
    
    requests.get(f'{ip1}/mine')
    res = requests.get(f'{ip2}/blockchain')
    assert res.status_code == 200
    blockchain = res.json()
    assert len(blockchain['blocks']) == 1
