import pytest
import sys

from main import get_args

def test_get_args():
    sys.argv = ['','--port', '8000']
    args = get_args()
    assert args.port == 8000
    assert args.servers == []
    assert isinstance(args.wallet, int)
    assert args.wallet > 0