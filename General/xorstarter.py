"""Thực hiện phép XOR cơ bản giữa từng ký tự trong chuỗi và giá trị hằng số để tạo flag."""
data = "label"
flag = "".join(chr(ord(c) ^ 13) for c in data)
print(f"crypto{{{flag}}}")
