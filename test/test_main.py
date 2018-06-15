import pytest
import sys

from main import get_args, get_server

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