from urllib.request import urlopen
import json

BASE_URL = 'https://aes.cryptohack.org/flipping_cookie/'

def fetch_data(endpoint):
    response = urlopen(BASE_URL + endpoint)
    return json.loads(response.read())

def retrieve_cookie():
    data = fetch_data('get_cookie/')
    raw = bytes.fromhex(data['cookie'])
    iv_part = raw[:16]
    cipher_part = raw[16:]
    return iv_part, cipher_part

def verify_admin(mod_iv, cipher):
    endpoint = f'check_admin/{cipher.hex()}/{mod_iv.hex()}/'
    return fetch_data(endpoint)

def xor_three(a, b, c):
    return bytes(i ^ j ^ k for i, j, k in zip(a, b, c))

# Lấy IV và ciphertext từ server
initial_iv, encrypted_cookie = retrieve_cookie()

original_text = b"admin=False;expi"
desired_text  = b"admin=True;;expi"

# Tạo IV mới
modified_iv = xor_three(initial_iv, original_text, desired_text)

# Gửi lên server kiểm tra
result = verify_admin(modified_iv, encrypted_cookie)

if result.get('flag'):
    print(result['flag'])
else:
    print("Không thành công:", result)
