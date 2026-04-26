p = 28151
p_minus_1 = p - 1

prime_factors = [2, 5, 563]

for g in range(2, p):
    is_primitive = True
    for q in prime_factors:
        if pow(g, p_minus_1 // q, p) == 1:
            is_primitive = False
            break
            
    if is_primitive:
        print(g)
        break