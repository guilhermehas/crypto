import pytest
from wallet import Wallet
from tools import mapv
from transaction import Transaction
from blockchain import Blockchain
from examples_to_test import blockchain

private_keys = [43, 53, 63, 1]
public_keys = ["abc", "cdb", "234", "44444"]
amounts = [1,1,28,30]
wallets = mapv(lambda private_key: Wallet(private_key), private_keys)

@pytest.mark.parametrize("wallet,output_public_key,amount", 
    zip(wallets,public_keys,amounts))
def test_make_transaction(wallet: Wallet, output_public_key : str, amount: float):
    transaction = Transaction(input=wallet.get_public_key_in_bytes(), outputs=[output_public_key,amount])
    signed_transaction = wallet.sign(transaction)
    assert signed_transaction.is_signed_correctly()

@pytest.mark.parametrize("private_key_n,balance", zip(private_keys,amounts[:3]))
def test_get_balance(blockchain : Blockchain, private_key_n : int, balance : float):
    assert Wallet(private_key_n).get_balance(blockchain) == balance