from pickle import dumps, loads
import pickle
from zlib import decompress
from base64 import b64encode, b64decode

class ServerUtils():
    def __init__(self):
        pass
    
    def to_str(self, obj):
        return str(b64encode(dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)), 'utf8')
    
    def to_obj(self, string):
        return loads(b64decode(string))