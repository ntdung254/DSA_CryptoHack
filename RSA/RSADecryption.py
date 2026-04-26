from Crypto.Util.number import inverse

# Public key
e = 65537

p = 857504083339712752489993810777
q = 1029224947942998075080348647219
n = p * q
phi = (p - 1) * (q - 1)

#Pprivate key d
d = inverse(e, phi)

# Ciphertext
c = 77578995801157823671636298847186723593814843845525223303932

m = pow(c, d, n)

print("Plaintext:", m)
