"""Script tự động hóa việc kết nối Socket và giải quyết 100 thử thách encoding với các định dạng: Base64, Hex, ROT13, BigInt và UTF-8."""
from pwn import *
import json
import base64
import codecs
from Crypto.Util.number import long_to_bytes

"""Kết nối đến server."""
r = remote('socket.cryptohack.org', 13377)

def json_recv():
    """Nhận và giải mã dữ liệu JSON từ server."""
    line = r.recvline()
    return json.loads(line.decode())

def json_send(hsh):
    """Đóng gói dữ liệu vào JSON và gửi phản hồi cho server."""
    request = json.dumps(hsh).encode()
    r.sendline(request)

"""Lặp 100 lần để lấy Flag."""
for i in range(101):
    received = json_recv()
    
    """Nếu nhận được flag thì dừng và in ra."""
    if "flag" in received:
        print(received["flag"])
        break

    print(f"{i+1}: {received['type']}")
    
    encoding_type = received["type"]
    encoded_value = received["encoded"]
    decoded = ""

    """Xử lý từng loại."""
    if encoding_type == "base64":
        decoded = base64.b64decode(encoded_value).decode()
    elif encoding_type == "hex":
        decoded = bytes.fromhex(encoded_value).decode()
    elif encoding_type == "rot13":
        decoded = codecs.decode(encoded_value, 'rot_13')
    elif encoding_type == "bigint":
        decoded = long_to_bytes(int(encoded_value, 16)).decode()
    elif encoding_type == "utf-8":
        decoded = "".join(chr(b) for b in encoded_value)

    """Gửi lại kết quả."""
    json_send({"decoded": decoded})
