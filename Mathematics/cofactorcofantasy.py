import time
import json
from pwn import *

HOST = 'socket.cryptohack.org'
PORT = 13398

def solve():
    context.log_level = 'error' 
    r = remote(HOST, PORT)
    r.recvline()
    
    def measure_time(index, samples=7):
        total_time = 0
        for _ in range(samples):
            payload = json.dumps({"option": "get_bit", "i": index}).encode()
            start = time.time()
            r.sendline(payload)
            r.recvline() 
            total_time += (time.time() - start)
        return total_time / samples

    """Đo mốc thời gian chuẩn dựa vào chữ 'c'."""
    time_1 = measure_time(0, samples=15)
    time_0 = measure_time(7, samples=15)
    
    """Tính ngưỡng phân định."""
    threshold = time_0 + (time_1 - time_0) * 0.4
    
    flag_bits = ""
    flag = ""
    
    """Quét 43 ký tự (43 * 8 bits)."""
    for i in range(344):
        t = measure_time(i, samples=5) 
        flag_bits += "1" if t > threshold else "0"
            
        if len(flag_bits) == 8:
            flag += chr(int(flag_bits[::-1], 2)) 
            flag_bits = "" 
                
    """In ra flag cuối cùng."""
    print(flag)
    r.close()

  solve()
