def solve_successive_powers():
    """Duyệt các số nguyên tố 3 chữ số để tìm cặp (p, x) thỏa mãn quy luật nhân lũy thừa liên tiếp của dãy số."""
    data = [588, 665, 216, 113, 642, 4, 836, 114, 851, 492, 819, 237]
    
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    """Tạo danh sách các số nguyên tố có 3 chữ số."""
    primes = [p for p in range(100, 1000) if is_prime(p)]
    
    for p in primes:
        try:
            """Tính x giả định từ u1 = u0 * x mod p."""
            u0, u1 = data[0], data[1]
            x = (u1 * pow(u0, -1, p)) % p
            
            """Kiểm tra xem x này có khớp với toàn bộ dãy không."""
            if all((data[i] * x) % p == data[i+1] for i in range(len(data) - 1)):
                print(f"crypto{{{p},{x}}}")
                return
        except ValueError:
            """Bỏ qua nếu không tồn tại nghịch đảo modulo (gcd(u0, p) != 1)."""
            continue

solve_successive_powers()
