from typing import Any, Dict, Optional, Iterable, Union, List, Dict, Set

from copy import deepcopy

from collections import defaultdict
from tools import mapv
from transaction import Transaction
from block import Block

class Blockchain:
    def __init__(self) -> None:
        self.difficult : int = 0
        self.chain : List[Block] = []
        self.reward : int = 10
        self.balances : Dict[Any,float] = defaultdict(float)
        self.transaction_hashes : Set[Any] = set()

    def reset(self) -> None:
        self.chain : List[Block] = []
        self.balances : Dict[Any,float] = defaultdict(float)
        self.transaction_hashes : Set[Any] = set()
    
    def to_dict(self) -> Dict[str,Any]:
        return {
            'balances': [(int(key.decode('utf8')), qt) for key, qt in self.balances.items()],
            'blocks': [block.to_dict() for block in self.chain]
        }
    
    
    def copy(self, blockchain : 'Blockchain') -> None:
        self.reset()
        self.chain = deepcopy(blockchain.chain)
        self.difficult = blockchain.difficult
        self.reward = blockchain.reward
        self.balances = deepcopy(blockchain.balances)
        self.transaction_hashes = deepcopy(blockchain.transaction_hashes)
    
    def get_difficult(self) -> int:
        return self.difficult
    
    def get_transactions(self) -> Iterable[Transaction]:
        for block in self.chain:
            if block.transactions:
                yield from block.transactions
    
    def is_new_block_OK(self, block : Block) -> bool:
        senders = mapv(lambda transaction: transaction.input, block.transactions)
        is_just_one_senders_per_block = len(senders) != len(set(senders))
        if is_just_one_senders_per_block:
            return False

        def is_transaction_right(transaction : Transaction) -> bool:
            if not transaction.is_signed_correctly():
                return False
            
            if hash(transaction) in self.transaction_hashes:
                return False

            sum_output = transaction.get_sum_outputs()
            if sum_output > self.balances[transaction.input]:
                return False
            return True

        if block.transactions and not(any(map(is_transaction_right,block.transactions))):
            return False

        if not block.is_mined(self.difficult):
            return False

        if len(self.chain) >= 1:
            is_previous_hash_wrong = block.previous_hash != hash(self.chain[-1])
            if is_previous_hash_wrong:
                return False
        return True

    def add(self, block : Block) -> None:
        if self.is_new_block_OK(block):

            self.chain.append(block)

            for transaction in block.transactions:
                self.transaction_hashes.add(hash(transaction))
                sum_outs = transaction.get_sum_outputs()
                assert sum_outs >= 0

                miner_reward = self.balances[transaction.input] - sum_outs
                assert miner_reward >= 0

                self.balances[transaction.input] = 0
                self.balances[block.miner_pub_key] += miner_reward
                for pub_out, pub_rew in transaction.outputs:
                    self.balances[pub_out] += pub_rew
            self.balances[block.miner_pub_key] += self.reward
        else:
            raise Exception('Blockchain invalid')
    
    def substitute(self, blockArray : 'BlockArray'):
        if len(blockArray) < len(self):
            return False
        new_blockchain = blockArray.to_blockchain()
        if new_blockchain is None:
            return False
        self.copy(new_blockchain)
        return True

    
    def __len__(self) -> int:
        return len(self.chain)

    def get_last_block(self) -> Optional[Block]:
        if self.chain:
            return self.chain[-1]
        else:
            return None

class BlockArray:
    def __init__(self, blocks : Union[List[Block], Blockchain]) -> None:
        if isinstance(blocks, Blockchain):
            self.chain = deepcopy(blocks.chain)
        else:
            self.chain = deepcopy(blocks)
    
    def to_blockchain(self) -> Optional[Blockchain]:
        blockchain = Blockchain()
        for block in self.chain:
            if not blockchain.is_new_block_OK(block):
                return None
            blockchain.add(block)
        return blockchain

    def is_correct(self) -> bool:
        if self.to_blockchain() is None:
            return False
        return True
    
    def add(self, block : Block) -> None:
        self.chain.append(block)
    
    def __len__(self) -> int:
        return len(self.chain)