import json
from Crypto.Util.number import long_to_bytes
from pwn import *

p1 = 211578328037
p2 = 2173767566209

conn = remote('socket.cryptohack.org', 13376, level='error')
conn.recvline()

conn.sendline(json.dumps({'option': 'get_pubkey'}).encode())
N = int(json.loads(conn.recvline())['N'], 16)

conn.sendline(json.dumps({'option': 'sign', 'msg': long_to_bytes(p1).hex()}).encode())
s1 = int(json.loads(conn.recvline())['signature'], 16)

conn.sendline(json.dumps({'option': 'sign', 'msg': long_to_bytes(p2).hex()}).encode())
s2 = int(json.loads(conn.recvline())['signature'], 16)

signature = (s1 * s2) % N

conn.sendline(json.dumps({'option': 'verify', 'msg': b'admin=True'.hex(), 'signature': hex(signature)}).encode())
print(json.loads(conn.recvline())['response'])