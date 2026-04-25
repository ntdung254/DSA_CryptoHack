"""Brute-force XOR với từng giá trị từ 0-255 để tìm byte chìa khóa và giải mã flag."""
hex_str = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
data = bytes.fromhex(hex_str)

for i in range(256):
    """XOR từng byte trong data với i."""
    decoded = "".join(chr(b ^ i) for b in data)
    if "crypto{" in decoded:
        print(decoded)
        break
