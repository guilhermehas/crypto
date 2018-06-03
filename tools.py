def mapv(f,vec):
    return list(map(f,vec))

def zipv(*vec):
    return list(zip(*vec))

def chash(n):
    return abs(hash(n))

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat

def get_private_key(integer):
    return ec.derive_private_key(1,
    ec.SECP384R1(), default_backend())


def get_signature(private_key, data):
    return private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )

def get_public_key_from_bytes(data):
    return load_pem_public_key(data, backend=default_backend())


def pub_to_bytes(public_key):
    pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )
    return pem


#public_key = private_key.public_key()
#public_key.verify(signature, data, ec.ECDSA(hashes.SHA256()))