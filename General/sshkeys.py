"""Đọc thông tin từ tệp khóa công khai để trích xuất giá trị Modulus cần thiết cho các bước tính toán sau."""
from Crypto.PublicKey import RSA
with open('bruce_rsa.pub', 'r') as f:
    key = RSA.importKey(f.read())
print(key.n)
