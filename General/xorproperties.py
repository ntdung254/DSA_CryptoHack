"""Vận dụng các tính chất của phép toán XOR trên chuỗi Hex để tìm kiếm phần dữ liệu bị ẩn."""
from Crypto.Util.number import long_to_bytes

KEY1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
KEY23 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
ALL = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"

def hex_to_int(h): 
    return int(h, 16)

res = hex_to_int(KEY1) ^ hex_to_int(KEY23) ^ hex_to_int(ALL)

print(long_to_bytes(res).decode())
