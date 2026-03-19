# Hybrid Steganographic Security Model using RSA and AES

This project implements a multi-layered security system combining:

• AES encryption for file protection
• RSA encryption for AES key security
• Steganography (metadata + LSB) for covert data hiding

Encryption Flow

File
↓
AES Encryption
↓
AES Key Encrypted using RSA
↓
Encrypted Data Embedded using Steganography

Decryption Flow

Stego File
↓
Extract Hidden Data
↓
RSA Decrypt AES Key
↓
AES Decrypt File
