#from cryptography.hazmat.primitives import serialization
#from cryptography.hazmat.primitives.asymmetric import ec
#from cryptography.hazmat.backends import default_backend
#from cryptography.hazmat.primitives import hashes
#from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat
#from pickle import load


class PrivateKey:
    def __init__(self, n):
        self.n = n
    
    def public_key(self):
        return PublicKey(self.n)
    
    def sign(self, message):
        return str(message)+str(self.n)

class PublicKey:
    def __init__(self, n):
        if isinstance(n, int):
            self.n = n
        else:
            self.n = int(n.decode('utf8'))
    
    def to_bytes(self):
        return bytes(str(self.n), encoding='utf8')
    
    def verify(self, signature, message):
        return str(message)+str(self.n) == signature 
    
    
def get_private_key(n):
    #if isinstance(n,int):
    #    return ec.derive_private_key(n, ec.SECP384R1(), default_backend())
    #elif isinstance(n,bytes):
    #with open('keys.pickle', 'rb') as f:
    #    private_keys = load(f)
    return PrivateKey(n)
    #print(type(private_keys))
    #assert type(private_keys) == list
    #return serialization.load_pem_private_key(
    #    private_keys[n],
    #    password=b'123',
    #    backend=default_backend()
    #)


def private_to_pub_bytes(n):
    return PublicKey(n).to_bytes() #pub_to_bytes(get_private_key(n).public_key())

def get_signature(private_key, data):
    return private_key.sign(data)
    #private_key.sign(
    #    data,
    #    ec.ECDSA(hashes.SHA256())
    #)

def get_public_key(data):
    return PublicKey(data)#load_pem_public_key(data,
        #backend=default_backend())


def pub_to_bytes(public_key):
    #pem = public_key.public_bytes(
    #    encoding=Encoding.PEM,
    #    format=PublicFormat.SubjectPublicKeyInfo
    #)
    return public_key.to_bytes()#pem

def is_signed_correctly(signature, message, public_key):
    return public_key.verify(signature, message)
    #try:
    #    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    #    return True
    #except:
    #    return False
