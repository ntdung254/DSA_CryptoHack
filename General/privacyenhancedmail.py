"""Mở tệp khóa định dạng PEM để lấy ra thành phần số mũ phục vụ cho việc giải mã dữ liệu."""
from Crypto.PublicKey import RSA
with open('privacy_enhanced_mail.pem', 'r') as f:
    key = RSA.importKey(f.read())
print(key.d)
