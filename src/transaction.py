from typing import Optional, Dict, Any
import pickle

from crypto import PrivateKey, PublicKey

class Transaction:
    def __init__(self, outputs, input=None, timestamp : int = 0, signature : Optional[bytes] = None) -> None:
        self.input = input
        self.outputs = outputs
        self.signature = signature
        self.timestamp = timestamp
    
    
    def __bytes__(self) -> bytes:
        to_compress = (self.input, self.outputs, self.timestamp)
        all_data = bytes(str(to_compress), encoding="utf-8")
        return all_data
    
    def __hash__(self):
        return hash(bytes(self))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "input": hash(self.input), 
            "outputs": [(hash(pub),out) for pub,out in self.outputs],
            "signature": hash(self.signature),
            "timestamp": self.timestamp
        }
    
    def is_signed_correctly(self) -> bool:
        return PublicKey(self.input).verify(self.signature, bytes(self))
    
    def get_sum_outputs(self) -> float:
        sum_output = 0
        for _, out in self.outputs:
            sum_output += out
        return sum_output

    def is_equal(self, transaction: 'Transaction') -> bool:
        return self.input == transaction.input and \
            self.outputs == transaction.outputs and \
            self.timestamp == transaction.timestamp