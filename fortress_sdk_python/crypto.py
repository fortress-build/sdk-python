from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import hashlib
import hmac
import base64


def decrypt(private_key, ciphertext):
    """Decrypt a ciphertext using the provided private key"""

    # Load the private key
    private_key = serialization.load_pem_private_key(
        f"-----BEGIN EC PRIVATE KEY-----\n{private_key}\n-----END EC PRIVATE KEY-----".encode(),
        password=None,
        backend=default_backend(),
    )

    # Decode the ciphertext
    ciphertext = base64.b64decode(ciphertext)

    # Extract the ephemeral public key
    ephemeral_size = int(ciphertext[0])
    ephemeral_public_key = ciphertext[1 : 1 + ephemeral_size]

    # Extract the MAC and AES-GCM ciphertext
    sha1_size = 20
    aes_size = 16
    ciphertext = ciphertext[1 + ephemeral_size :]

    # Verify the ciphertext length
    if len(ciphertext) < sha1_size + aes_size:
        raise ValueError("Invalid ciphertext")

    # Derive the public key
    eph_pub = ec.EllipticCurvePublicKey.from_encoded_point(
        ec.SECP256R1(), ephemeral_public_key
    )

    # Perform the ECDH key exchange
    shared_key = private_key.exchange(ec.ECDH(), eph_pub)

    # Derive the shared key
    shared = hashlib.sha256(shared_key).digest()

    # Verify the MAC
    tagStart = len(ciphertext) - sha1_size
    h = hmac.new(shared[16:], digestmod=hashlib.sha1)
    h.update(ciphertext[:tagStart])
    mac = h.digest()

    if not hmac.compare_digest(mac, ciphertext[tagStart:]):
        raise ValueError("Invalid MAC")

    # Decrypt the ciphertext using AES-GCM
    decryptor = Cipher(
        algorithms.AES(shared[:16]),
        modes.CBC(
            ciphertext[:aes_size],
        ),
        backend=default_backend(),
    ).decryptor()

    plaintext = decryptor.update(ciphertext[aes_size:tagStart]) + decryptor.finalize()

    # Remove padding
    plaintext = plaintext[: -plaintext[-1]]
    return plaintext.decode()
