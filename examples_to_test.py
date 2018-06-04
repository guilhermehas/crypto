from transaction import *
from wallet import *
from tools import *
from crypto import *
from blockchain import *
from block import *

tuple_transactions = [
    (43, [(43, 28)]),
    (53, [(2, 0.001)]),
    (63, [(41, 1234)]),
    (43, [(44, 143553)]),
]

def to_transaction(data):
    sender_key, outs = data
    wallet = Wallet(sender_key)
    def to_out(out):
        #print("aqui",out)
        return [private_to_pub_bytes(out[0]), out[1]]
    transaction = Transaction(outputs=mapv(to_out, outs))
    signed_transaction = wallet.sign(transaction)
    return signed_transaction

transactions = mapv(to_transaction, tuple_transactions)

def blockchain():
    blockchain = Blockchain()

    private_keys = [43,53,63]
    public_keys = mapv(private_to_pub_bytes,private_keys)

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