from Crypto.Util.number import *
from pkcs1 import emsa_pkcs1_v15
from pwn import remote
import json

HOST, PORT = "socket.cryptohack.org", 13394
BIT_LENGTH = 768
TARGET_SIZE = 1 << 900

def get_smooth_prime(size):
    """Tạo số nguyên tố p sao cho p-1 là số smooth (tích các số nhỏ)"""
    i = 2
    smooth_p = 1
    while smooth_p < size or not isPrime(smooth_p + 1):
        smooth_p *= i
        i += 1
    return smooth_p + 1

def solve_discrete_log(m, s, n):
    """
    Tính e sao cho s^e = m (mod n)
    _m = mod(m, n)
    _s = mod(s, n)
    # Trong SageMath, discrete_log(target, base)
    return int(discrete_log(_m, _s))

def xor_bytes(*args):
    """XOR nhiều chuỗi bytes cùng lúc"""
    from functools import reduce
    return bytes(reduce(lambda x, y: [a ^ b for a, b in zip(x, y)], args))

io = remote(HOST, PORT)
print(io.recvline().decode())

#Lấy chữ ký mẫu từ server
io.sendline(json.dumps({"option": "get_signature"}).encode())
s = int(json.loads(io.readline())["signature"], 16)

#Thiết lập Public Key (n) tùy chỉnh để làm yếu hệ thống
p = get_smooth_prime(TARGET_SIZE)
n = p**2
io.sendline(json.dumps({'option': 'set_pubkey', 'pubkey': hex(n)}).encode())
suffix = json.loads(io.readline())["suffix"]

messages = [
    "This is a test for a fake signature.",
    "My name is 4nh H4v3rtz and I own CryptoHack.org",
    "Please send all my money to 1BvBMSEYasfaswoqppsAu4m4GFg7xJaNVN2"
]

secrets = []

for i, msg_text in enumerate(messages):
    full_msg = msg_text + suffix
    # Encode tin nhắn theo chuẩn PKCS1 v1.5
    m_encoded = bytes_to_long(emsa_pkcs1_v15.encode(full_msg.encode(), BIT_LENGTH // 8))
    
    print(f"[*] Solving discrete log for message {i}...")
    e = solve_discrete_log(m_encoded, s, n)
    
    # Gửi yêu cầu claim
    io.sendline(json.dumps({
        'option': 'claim',
        'msg': full_msg,
        'e': hex(e),
        'index': i
    }).encode())
    
    resp = json.loads(io.readline().decode())
    secrets.append(bytes.fromhex(resp['secret']))

flag = xor_bytes(*secrets)
print(f" {flag.decode()}")
