from transaction import *
from wallet import *
from tools import *
from crypto import *
from blockchain import *
from block import *
import pytest

tuple_transactions = [
    (43, [(43, 28)]),
    (53, [(2, 0.001)]),
    (63, [(41, 1234)]),
    (43, [(44, 143553)]),
    (63, [(43, 0.1)]),
    (63, [(53, 1.1)]),
]

def to_transaction(data):
    sender_key, outs = data
    wallet = Wallet(sender_key)
    def to_out(out):
        return [PrivateKey(out[0]).public_key().to_bytes(), out[1]]
    transaction = Transaction(outputs=mapv(to_out, outs))
    signed_transaction = wallet.sign(transaction)
    return signed_transaction

transactions = mapv(to_transaction, tuple_transactions)

def transaction_to_block(transaction, miner, blockchain):
    miner = PrivateKey(miner).public_key().to_bytes()

    block = Block(blockchain.get_last_block(), [transaction], miner_pub_key=miner)
    block.mine(blockchain.get_difficult())
    return block

# 63 -> 28
# 53 -> 1
# 43 -> 1

@pytest.fixture
def blockchain():
    blockchain = Blockchain()

    private_keys = [43,53,63]
    public_keys = mapv(lambda priv: PrivateKey(priv).public_key().to_bytes(),private_keys)

    genesis_block = GenesisBlock(miner_pub_key=public_keys[0])
    genesis_block.mine(blockchain.get_difficult())
    blockchain.add(genesis_block)

    miners = [public_keys[1],public_keys[2]]
    outputs_array = [
        [(public_keys[0], 1),(public_keys[1],2)],
        [(public_keys[2],10),(public_keys[1],1)]
    ]

    for key, miner, outputs in zip(private_keys, miners, outputs_array):
        transaction = Wallet(key).sign(Transaction(outputs))
        block = Block(blockchain.get_last_block(), [transaction], miner_pub_key=miner)
        block.mine(blockchain.get_difficult())
        blockchain.add(block)
    
    return blockchain