import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding

def print_banner(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50 + "\n")

# --- 1. AES ENCRYPTION (Symmetric) ---
def aes_demo(message):
    print("\n--- ALGORITHM: AES-256 (SYMMETRIC) ---")
    key = os.urandom(32)  # 256-bit key
    iv = os.urandom(16)   # 128-bit IV
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode('utf-8')) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    enc_b64 = base64.b64encode(iv + ct).decode('utf-8')
    print(f"ENCRYPTED (BASE64): {enc_b64}")
    
    # Decryption
    raw_data = base64.b64decode(enc_b64)
    iv_dec, ct_dec = raw_data[:16], raw_data[16:]
    cipher_dec = Cipher(algorithms.AES(key), modes.CBC(iv_dec))
    decryptor = cipher_dec.decryptor()
    padded_pt = decryptor.update(ct_dec) + decryptor.finalize()
    
    unpadder = padding.PKCS7(128).unpadder()
    pt = unpadder.update(padded_pt) + unpadder.finalize()
    print(f"DECRYPTED TEXT:    {pt.decode('utf-8')}\n")

# --- 2. TRIPLE DES / 3DES ENCRYPTION (Symmetric - Legacy) ---
def des_demo(message):
    print("\n--- ALGORITHM: TRIPLE DES / 3DES (SYMMETRIC) ---")
    key = os.urandom(24)  # 192-bit key for 3DES
    iv = os.urandom(8)    # 64-bit IV
    
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(message.encode('utf-8')) + padder.finalize()
    
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    enc_b64 = base64.b64encode(iv + ct).decode('utf-8')
    print(f"ENCRYPTED (BASE64): {enc_b64}")
    
    # Decryption
    raw_data = base64.b64decode(enc_b64)
    iv_dec, ct_dec = raw_data[:8], raw_data[8:]
    cipher_dec = Cipher(algorithms.TripleDES(key), modes.CBC(iv_dec))
    decryptor = cipher_dec.decryptor()
    padded_pt = decryptor.update(ct_dec) + decryptor.finalize()
    
    unpadder = padding.PKCS7(64).unpadder()
    pt = unpadder.update(padded_pt) + unpadder.finalize()
    print(f"DECRYPTED TEXT:    {pt.decode('utf-8')}\n")

# --- 3. RSA ENCRYPTION (Asymmetric Public/Private) ---
def rsa_demo(message):
    print("\n--- ALGORITHM: RSA-2048 (ASYMMETRIC) ---")
    print("Generating RSA Public & Private Keys...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    
    # Encrypt with Public Key
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    enc_b64 = base64.b64encode(ciphertext).decode('utf-8')
    print(f"ENCRYPTED WITH PUBLIC KEY:  {enc_b64[:60]}...")
    
    # Decrypt with Private Key
    plaintext = private_key.decrypt(
        base64.b64decode(enc_b64),
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(f"DECRYPTED WITH PRIVATE KEY: {plaintext.decode('utf-8')}\n")

def main():
    print_banner("*** MULTI-ALGORITHM TEXT ENCRYPTION ***")
    msg = input("ENTER MESSAGE TO ENCRYPT: ")
    
    print("\nSELECT ENCRYPTION ALGORITHM:")
    print("1. AES   (Modern Symmetric Cipher)")
    print("2. 3DES  (Legacy Symmetric Cipher)")
    print("3. RSA   (Asymmetric Public/Private Key Cipher)")
    
    choice = input("\nENTER CHOICE (1-3): ").strip()
    
    if choice == '1':
        aes_demo(msg)
    elif choice == '2':
        des_demo(msg)
    elif choice == '3':
        rsa_demo(msg)
    else:
        print("\n[ERROR]: INVALID CHOICE SELECTED.")

if __name__ == "__main__":
    main()