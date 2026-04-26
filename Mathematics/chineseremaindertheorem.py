def solve_crt():
    """Giải hệ phương trình đồng dư bằng cách tổng hợp các tích số dư với nghịch đảo modulo tương ứng."""
    a = [2, 3, 5]
    n = [5, 11, 17]
    N = 5 * 11 * 17
    x = sum(a_i * (N // n_i) * pow(N // n_i, -1, n_i) for a_i, n_i in zip(a, n))
    print(x % N)

solve_crt()
