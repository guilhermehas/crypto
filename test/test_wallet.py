import pytest
from wallet import *
from tools import mapv, zipv
from transaction import *

private_keys = [123, b'32', 234, 1]
public_keys = ["abc", "cdb", "234", "44444"]
amounts = [1,2.3,102]
wallets = mapv(lambda private_key: Wallet(1), private_keys)

pygen_pw = pytest.mark.parametrize("private_key,wallet", 
    zip(private_keys, wallets))

pygen_w = pytest.mark.parametrize("wallet", wallets)

pygen_wt = pytest.mark.parametrize("wallet,output_public_key,amount", 
    zip(wallets,public_keys,amounts))

@pygen_wt
def test_make_transaction(wallet,output_public_key,amount):
    transaction = Transaction(input=wallet.get_public_key_in_bytes(), outputs=[output_public_key,amount])
    signed_transaction = wallet.sign(transaction)
    assert signed_transaction.is_signed_correctly()