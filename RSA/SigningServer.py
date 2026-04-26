from pwn import remote
import json

# Kết nối server
r = remote('socket.cryptohack.org', 13374)

def send(data):
    r.sendline(json.dumps(data).encode())

def recv():
    return json.loads(r.recvline().decode())


print(r.recvline().decode())

#Lấy secret
send({"option": "get_secret"})
secret_data = recv()
secret = secret_data["secret"]
print("Secret:", secret)

#Yêu cầu server ký chính secret đó
send({"option": "sign", "msg": secret})
sig_data = recv()

#Decode signature
signature_hex = sig_data["signature"]
signature_bytes = bytes.fromhex(signature_hex[2:])

print("Decoded:", signature_bytes.decode())

r.close()
