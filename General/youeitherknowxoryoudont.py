"""Xác định khóa dựa trên phần đầu đã biết của kết quả, sau đó dùng khóa đó để xử lý toàn bộ dữ liệu."""
from pwn import xor

hex_encrypted = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
data = bytes.fromhex(hex_encrypted)

secret_key = xor(data[:7], b"crypto{")
print(f"Secret Key: {secret_key.decode()}")

secret_key = "myXORkey"
flag = xor(data, secret_key.encode())
print(flag.decode())
