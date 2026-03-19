import os
import base64
from Crypto.Util import number

def generate_prime(bits=2048):
    return number.getPrime(bits)

def mod_inverse(e, phi):
    """ Compute modular inverse using Extended Euclidean Algorithm """
    a, b, x0, x1 = phi, e, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
    return x0 % phi

def generate_rsa_keys():
    p, q = generate_prime(), generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537  # Common public exponent
    d = mod_inverse(e, phi)
    return ((n, e), (n, d))  # Public and private keys

def rsa_encrypt(message, pub_key):
    n, e = pub_key
    message_int = int.from_bytes(message, 'big')
    encrypted_int = pow(message_int, e, n)
    return base64.b64encode(encrypted_int.to_bytes((n.bit_length() + 7) // 8, 'big'))

def generate_aes_key():
    return os.urandom(32)  # AES-256

def encrypt_file(file_path, aes_key):
    iv = os.urandom(16)  # AES block size is 16 bytes
    plaintext = open(file_path, 'rb').read()
    ciphertext = bytearray()
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i + 16].ljust(16, b' ')
        cipher_block = bytes([block[j] ^ aes_key[j % len(aes_key)] for j in range(16)])
        ciphertext.extend(cipher_block)
    return iv, ciphertext

def save_encrypted_data_to_txt(encrypted_aes_key, iv, ciphertext, aes_key_file, encrypted_file):
    encoded_aes_key = encrypted_aes_key.decode('utf-8')
    encoded_iv = base64.b64encode(iv).decode('utf-8')
    encoded_ciphertext = base64.b64encode(ciphertext).decode('utf-8')
    with open(aes_key_file, 'w') as f:
        f.write(encoded_aes_key)
    with open(encrypted_file, 'w') as f:
        f.write(encoded_iv + '\n' + encoded_ciphertext)

def main(file_path, aes_key_file, encrypted_file):
    pub_key, priv_key = generate_rsa_keys()
    aes_key = generate_aes_key()
    encrypted_aes_key = rsa_encrypt(aes_key, pub_key)
    iv, ciphertext = encrypt_file(file_path, aes_key)
    save_encrypted_data_to_txt(encrypted_aes_key, iv, ciphertext, aes_key_file, encrypted_file)
    with open("private_key.txt", "w") as f:
        f.write(str(priv_key))  # Save private key as a string
    print("Encryption complete. Encrypted data saved to files.")

if __name__ == "__main__":
    main("text.txt", "encrypted_aes_key.txt", "encrypted_file.txt")
