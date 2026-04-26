from Crypto.Util.number import long_to_bytes

# Thông số đề bài (Không thèm quan tâm n luôn vì không cần dùng tới)
ct = 44981230718212183604274785925793145442655465025264554046028251311164494127485

print("[*] Tiến hành bẻ khóa RSA với e = 1...")

# Vì e = 1 nên Ciphertext chính là Plaintext
pt = ct

print("\n[!] BINGOOO! FLAG LÀ:")
print(long_to_bytes(pt).decode())