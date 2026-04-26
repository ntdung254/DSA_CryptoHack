import requests

url = "https://aes.cryptohack.org/ecbcbcwtf"
ct = bytes.fromhex(requests.get(f"{url}/encrypt_flag/").json()["ciphertext"])
blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]

flag = b""
for i in range(1, len(blocks)):
    dec = bytes.fromhex(requests.get(f"{url}/decrypt/{blocks[i].hex()}/").json()["plaintext"])
    flag += bytes([a ^ b for a, b in zip(dec, blocks[i-1])])

print(flag.decode())