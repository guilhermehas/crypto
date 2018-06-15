import pytest
import mock

import sys

from main import get_args, get_server, init, main
import main as module

def test_get_args():
    sys.argv = ['','--port', '8000']
    args = get_args()
    assert args.port == 8000
    assert args.servers == []
    assert isinstance(args.wallet, int)
    assert args.wallet > 0

def test_get_server():
    args = get_args()
    server = get_server(args)
    assert server is not None

def test_init():
  with mock.patch.object(module, "main", return_value=42):
    with mock.patch.object(module, "__name__", "__main__"):
      with mock.patch.object(module.sys,'exit') as mock_exit:
         module.init()
         assert mock_exit.call_args[0][0] == 42

class MockServer:
    def __init__(self,args):
        return
    def run(self,port):
        return

def test_main():
    with mock.patch.object(module, "get_server", return_value=MockServer({})):
        main()
