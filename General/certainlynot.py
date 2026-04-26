"""Đọc tệp chứng chỉ ở định dạng nhị phân để lấy ra giá trị Modulus phục vụ cho việc tính toán[cite: 3]."""
from Crypto.PublicKey import RSA
with open('2048b-rsa-example-cert.der', 'rb') as f:
    cert = RSA.importKey(f.read())
print(cert.n)
