def solve_qr(p, targets):
    """Duyệt từ 0 đến p-1 để tìm số nào khi bình phương lên sẽ khớp với danh sách đề cho."""
    for x in range(p):
        if pow(x, 2, p) in targets:
            return x
        
p = 29
arr =[14,6,11]

print(solve_qr(p, arr))
