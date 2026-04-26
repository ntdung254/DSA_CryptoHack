from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import sha1
from sympy.ntheory import discrete_log

def solve_ellipse():
    """Giải mã Ellipse Curve bằng cách chuyển về bài toán logarit rời rạc trên trường số dư p."""
    p = 173754216895752892448109692432341061254596347285717132408796456167143559
    D_sqrt = 23 
    
    """Alice's public key và Generator G."""
    Ax = 155781055760279718382374741001148850818103179141959728567110540865590463
    Ay = 73794785561346677848810778233901832813072697504335306937799336126503714
    Gx = 29394812077144852405795385333766317269085018265469771684226884125940148
    Gy = 94108086667844986046802106544375316173742538919949485639896613738390948
    
    """Bob's public key (dùng để tính shared secret sau khi có n_a)."""
    Bx = 171226959585314864221294077932510094779925634276949970785138593200069419
    By = 54353971839516652938533335476115503436865545966356461292708042305317630

    """Ánh xạ điểm (x, y) sang giá trị z = x + sqrt(D)*y mod p."""
    """Phép cộng điểm trên curve này tương đương phép nhân z1 * z2 mod p."""
    g = (Gx + D_sqrt * Gy) % p
    target = (Ax + D_sqrt * Ay) % p

    """Giải Discrete Log để tìm private key n_a."""
    n_a = discrete_log(p, target, g)

    """Tính Shared Secret. Ánh xạ Bob's key rồi nâng lũy thừa n_a."""
    B_val = (Bx + D_sqrt * By) % p
    S_val = pow(B_val, n_a, p)
    
    """Shared secret thực tế là tọa độ x của điểm kết quả. x = (z + z^-1) / 2 mod p"""
    shared_secret = (S_val + pow(S_val, -1, p)) * pow(2, -1, p) % p

    """Giải mã AES-CBC."""
    iv = bytes.fromhex('64bc75c8b38017e1397c46f85d4e332b')
    enc_flag = bytes.fromhex('13e4d200708b786d8f7c3bd2dc5de0201f0d7879192e6603d7c5d6b963e1df2943e3ff75f7fda9c30a92171bbbc5acbf')
    
    key = sha1(str(shared_secret).encode('ascii')).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    decrypted = cipher.decrypt(enc_flag)
    flag = unpad(decrypted, 16)
    print(flag.decode())

solve_ellipse()
