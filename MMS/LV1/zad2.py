import math

def max_na_intervalu(f, a, b, step):
    cur_max = f(a)
    a += step
    while a <= b:
        cur_max = max(cur_max, f(a))
        a += step
    return cur_max


print(max_na_intervalu(lambda x: x**2, -8, 9, 1))
print(max_na_intervalu(math.sin, -math.pi, math.pi, 0.001))
