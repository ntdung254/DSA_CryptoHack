# Challenge 68: Private Keys
# Calculating d from p, q, and e

from Crypto.Util.number import inverse

p = 857504083339712752489993810777 # from challenge
q = 1029224947942998075080348647219 # from challenge
e = 65537

n = p * q
phi = (p - 1) * (q - 1)
d = inverse(e, phi)
print(f"Private Key d: {d}")