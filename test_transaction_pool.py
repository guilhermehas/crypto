from transaction_pool import *
from examples_to_test import blockchain as block_example
from examples_to_test import *
from blockchain import *
from tools import mapv
import pytest

@pytest.fixture
def blockchain():
    return block_example()

# 63 -> 28
# 53 -> 1
# 43 -> 1

@pytest.fixture
def transactionPool():
    transactionPool = TransactionPool()
    return transactionPool

def test_receive_transaction(transactionPool, blockchain):
    transaction = to_transaction((63, [(43, 28)]))
    assert transactionPool.receive_transaction(blockchain, transaction)

    transaction = to_transaction((63, [(43, 13)]))
    assert transactionPool.receive_transaction(blockchain, transaction)

def test_transaction_wrong(transactionPool, blockchain):
    transaction = to_transaction((63, [(43, 29)]))
    assert not transactionPool.receive_transaction(blockchain, transaction)

def test_add_same_transaction(blockchain):
    transaction = to_transaction((63, [(63, 27)]))
    block = Block(blockchain.get_last_block(), [transaction])
    block.mine()
    blockchain.add(block)
    transactionPool = TransactionPool()
    assert not transactionPool.receive_transaction(blockchain, transaction)

def test_pick_best_transactions(transactionPool, blockchain):
    transactions = mapv(to_transaction, (((63, [(63, 1)])), (63, [(63, 9)]), (63, [(63, 27)])))
    for i in (2,0,1):
        transactionPool.receive_transaction(blockchain, transactions[i])
    picked_transactions = transactionPool.get_best_transactions(blockchain, 3)
    indexes = mapv(lambda trans: transactions.index(trans), picked_transactions)
    assert indexes == [0,1,2]


    