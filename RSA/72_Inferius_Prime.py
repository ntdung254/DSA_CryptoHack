import requests
from Crypto.Util.number import long_to_bytes, inverse

# Thông số của bạn
n = 984994081290620368062168960884976209711107645166770780785733
e = 65537
ct = 948553474947320504624302879933619818331484350431616834086273

print("[*] Đang tự động tra cứu n trên factordb.com...")
# Gọi API của factordb để lấy thừa số
res = requests.get(f"http://factordb.com/api?query={n}").json()

factors = []
for factor_str, count in res['factors']:
    for _ in range(count):
        factors.append(int(factor_str))

p = factors[0]
q = factors[1]

print(f"[+] Đã tìm thấy p = {p}")
print(f"[+] Đã tìm thấy q = {q}")

# Kiểm tra lại (đảm bảo không bao giờ bị AssertionError nữa)
assert p * q == n, "Lỗi: p và q lấy về không đúng!"

print("[*] Đang tiến hành giải mã...")
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
pt = pow(ct, d, n)

print("\n[!] BINGOOO! FLAG:")
print(long_to_bytes(pt).decode())