import os
import base64
from Crypto.Util import number
def rsa_decrypt(encrypted_message, priv_key):
    n, d = priv_key
    encrypted_int = int.from_bytes(base64.b64decode(encrypted_message), 'big')
    decrypted_int = pow(encrypted_int, d, n)
    return decrypted_int.to_bytes((decrypted_int.bit_length() + 7) // 8, 'big')

def aes_decrypt(ciphertext, iv, key):
    ciphertext = base64.b64decode(ciphertext)
    plaintext = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        plain_block = bytes([block[j] ^ key[j % len(key)] for j in range(16)])
        plaintext.extend(plain_block)
    return plaintext.rstrip(b' ')  # Remove padding

def load_encrypted_data(aes_key_file, encrypted_file):
    with open(aes_key_file, 'r', encoding='utf-8') as f:
        encrypted_aes_key = f.read().strip()
    with open(encrypted_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        iv = base64.b64decode(lines[0].strip())
        ciphertext = lines[1].strip()
    return encrypted_aes_key, iv, ciphertext

def main(aes_key_file, encrypted_file):
    with open("private_key.txt", "r") as f:
        priv_key = eval(f.read())  # Load private key
    encrypted_aes_key, iv, ciphertext = load_encrypted_data(aes_key_file, encrypted_file)
    aes_key = rsa_decrypt(encrypted_aes_key, priv_key)
    decrypted_text = aes_decrypt(ciphertext, iv, aes_key)
    with open("decrypted_" + os.path.basename(encrypted_file), 'w', encoding='utf-8') as f:
        f.write(decrypted_text.decode('utf-8', errors='replace'))
    print("Decryption complete.")

if __name__ == "__main__":
    main("encrypted_aes_key.txt", "fun.txt")
