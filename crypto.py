from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, Encoding, PublicFormat


def get_private_key(n):
    if isinstance(n,int):
        return ec.derive_private_key(n, ec.SECP384R1(), default_backend())
    elif isinstance(n,bytes):
        return serialization.load_pem_private_key(
            n,
            password=None,
            backend=default_backend()
        )

def private_to_pub_bytes(n):
    return pub_to_bytes(get_private_key(n).public_key())

def get_signature(private_key, data):
    return private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )

def get_public_key(data):
    return load_pem_public_key(data,
        backend=default_backend())


def pub_to_bytes(public_key):
    pem = public_key.public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo
    )
    return pem

def is_signed_correctly(signature, message, public_key):
    try:
        public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
        return True
    except:
        return False
