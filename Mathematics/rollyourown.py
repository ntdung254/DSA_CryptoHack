from pwn import remote
import json

def get_flag():
    """ Kết nối tới server và giải mã logarit rời rạc trong một nốt nhạc """
    io = remote('socket.cryptohack.org', 13403)
    
    """ Bóc tách q từ mớ JSON server gửi về """
    io.recvuntil(b": ")
    q = int(io.recvline().strip().decode().strip('"'), 16)
    
    """ Ép server dùng tham số yếu bằng cách chọn n = q^2 và g = 1 + q """
    io.sendlineafter(b": ", json.dumps({"g": hex(1 + q), "n": hex(q * q)}).encode())
    
    """ Tính toán x dựa trên khai triển nhị thức Newton từ public key h """
    io.recvuntil(b": ")
    h = int(io.recvline().strip().decode().strip('"'), 16)
    x = (h - 1) // q
    
    """ Gửi x dưới dạng JSON và chỉ in ra đúng chuỗi flag """
    io.sendlineafter(b": ", json.dumps({"x": hex(x)}).encode())
    
    """ Lọc dữ liệu để lấy đúng dòng chứa flag cuối cùng """
    raw_res = io.recvall().decode().strip().split('\n')[-1]
    print(json.loads(raw_res)['flag'])

get_flag()
