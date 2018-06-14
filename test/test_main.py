import pytest

import time
import requests
from threading import Thread
import sys

from main import main

def get_server():
    Server = Thread(target=main)
    Server.daemon = True
    return Server

'''
def test_main_run():
    server = get_server()
    server.start()
    server.join()


def test_running_port_8000():
    sys.argv = ['','--port', '8001','--ip','localhost','--wallet','1']

    server = get_server()
    server.start()
    time.sleep(0.01)

    res = requests.get('http://localhost:8001/blockchain')
    assert res.status_code == 200

def test_update_blockchain():
    sys.argv = ['','--port', '8002','--wallet','1']
    ip1 = f'http://localhost:8002'
    server1 = get_server()
    server1.start()
    time.sleep(0.01)
    
    sys.argv = ['','--port', '8003', '--wallet', '2', '--servers', 'localhost:8002']
    ip2 = f'http://localhost:8003'
    server2 = get_server()
    server2.start()
    time.sleep(0.01)
    
    requests.get(f'{ip1}/mine')
    res = requests.get(f'{ip2}/blockchain')
    assert res.status_code == 200
    blockchain = res.json()
    assert len(blockchain['blocks']) == 1
'''