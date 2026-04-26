import json
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib

HOST = "socket.cryptohack.org"
PORT = 13371

def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(len(padding)))

def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
    plaintext = cipher.decrypt(bytes.fromhex(ciphertext))

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode()
    else:
        return plaintext.decode()

def recv_json(conn):
    line = b""
    while not line.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            break
        line += chunk
    line = line.decode()
    return json.loads(line[line.find("{"):])

def send_json(conn, data):
    conn.sendall((json.dumps(data) + "\n").encode())

s = socket.socket()
s.connect((HOST, PORT))

# Step 1: intercept Alice
alice_msg = recv_json(s)
p = int(alice_msg["p"], 16)

# Step 2: MITM A -> Bob (force A = p)
send_json(s, {
    "p": hex(p),
    "g": alice_msg["g"],
    "A": hex(p)
})

# Step 3: intercept Bob
bob_msg = recv_json(s)

# Step 4: MITM B -> Alice (force B = p)
send_json(s, {"B": hex(p)})

# Step 5: receive encrypted flag
flag_msg = recv_json(s)
iv = flag_msg["iv"]
ciphertext = flag_msg["encrypted_flag"]

# Step 6: shared secret
shared_secret = 0

print(decrypt_flag(shared_secret, iv, ciphertext))

s.close()