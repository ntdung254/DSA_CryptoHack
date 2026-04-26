from sage.all import *
from decimal import *

getcontext().prec = 100

# Dữ liệu từ ảnh chụp code
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103]
ct = 1350995397927355657956786955603012410260017344805998076702828160316695004588429433

n = len(PRIMES)
scale = Decimal(16 ** 64)

# Tính lại chính xác các giá trị S_i như lúc server mã hóa
S = [int(Decimal(p).sqrt() * scale) for p in PRIMES]

# Khởi tạo ma trận LLL kích thước (n+1) x (n+1)
M = Matrix(ZZ, n + 1, n + 1)

# Trọng số W để cân bằng giữa độ lớn của mã ASCII (~100) và sai số làm tròn thập phân
W = 1000

for i in range(n):
    M[i, i] = W
    M[i, n] = S[i]

# Hàng cuối cùng chứa giá trị đích cần đạt được
M[n, n] = -ct

print("[*] Đang chạy thuật toán LLL...")
reduced = M.LLL()

for row in reduced:
    # Trích xuất lại các hệ số (chia lại cho trọng số W)
    chars = [int(x / W) for x in row[:n]]

    # Do LLL có thể tìm ra vector ngược chiều, ta lấy trị tuyệt đối
    chars = [abs(c) for c in chars]

    # Lọc ra vector hợp lệ chứa Flag (Bắt đầu bằng 'crypto{')
    # Ký tự 'c' có mã ASCII là 99, 'r' là 114
    if chars[0] == 99 and chars[1] == 114:
        flag = "".join(chr(c) for c in chars)
        print("[+] BINGOOO! Flag tìm thấy:")
        print(flag)
        break