from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

# 1. Hàm giải mã đã được cung cấp
def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')

# 2. Tương tác với server
# Kết nối tới server của CryptoHack
io = remote('socket.cryptohack.org', 13371)

# --- BƯỚC 1: Bắt tin nhắn Alice gửi Bob ---
alice_msg = json.loads(io.recvline().decode().split('from Alice: ')[1])
p = int(alice_msg['p'], 16)

print("[+] Intercepted Alice's message")
# Tạo tin nhắn giả mạo gửi Bob: Thay A = p
fake_msg_to_bob = {
    "p": alice_msg['p'],
    "g": alice_msg['g'],
    "A": hex(p)
}
io.sendline(json.dumps(fake_msg_to_bob).encode())
print("[+] Sent malicious A to Bob")

# --- BƯỚC 2: Bắt tin nhắn Bob gửi Alice ---
bob_msg = json.loads(io.recvline().decode().split('from Bob: ')[1])

print("[+] Intercepted Bob's message")
# Tạo tin nhắn giả mạo gửi Alice: Thay B = p
fake_msg_to_alice = {
    "B": hex(p)
}
io.sendline(json.dumps(fake_msg_to_alice).encode())
print("[+] Sent malicious B to Alice")

# --- BƯỚC 3: Bắt tin nhắn chứa cờ ---
alice_flag_msg = json.loads(io.recvline().decode().split('from Alice: ')[1])
iv = alice_flag_msg['iv']
encrypted_flag = alice_flag_msg['encrypted_flag']

print("[+] Intercepted Encrypted Flag")

# --- BƯỚC 4: Giải mã ---
# Vì ta đã ép A = p và B = p, nên shared_secret = p^x mod p = 0
shared_secret = 0 
flag = decrypt_flag(shared_secret, iv, encrypted_flag)

print(f"\n[!] FLAG RECOVERED: {flag}")

io.close()