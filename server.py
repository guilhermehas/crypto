from pickle import dumps, loads
import pickle
from base64 import b64encode, b64decode
from blockchain import *

class ServerUtils():
    def __init__(self):
        self.blockchain =  Blockchain()
    
    def receive_block_array(self, blockArray):
        self.blockchain.substitute(blockArray)
    
    def to_str(self, obj):
        return str(b64encode(dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)), 'utf8')
    
    def to_obj(self, string):
        return loads(b64decode(string))