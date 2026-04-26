import requests
from Crypto.Util.Padding import unpad

url = "https://aes.cryptohack.org/triple_des"
key = "0101010101010101fefefefefefefefe"

ct = requests.get(f"{url}/encrypt_flag/{key}/").json()["ciphertext"]

pt_hex = requests.get(f"{url}/encrypt/{key}/{ct}/").json()["ciphertext"]

print(unpad(bytes.fromhex(pt_hex), 8).decode())