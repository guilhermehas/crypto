import pytest
from wallet import *

pygen = pytest.mark.parametrize("private_key", 
    ["abc", "cdb", "234", "44444"])

@pygen
def test_create_wallet(private_key):
    wallet = Wallet(private_key = private_key)
    assert wallet.private_key == private_key

@pygen
def test_public_key(private_key):
    wallet = Wallet(private_key = private_key)
    assert wallet.get_public_key() == private_key
