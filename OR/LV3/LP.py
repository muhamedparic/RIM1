from __future__ import print_function, division

import random
import math

def okolina(x, delta_x):
    tren_x = list(x)
    for i in range(len(delta_x)):
        tren_x[i] += delta_x[i]
        yield tren_x[:]
        tren_x[i] -= 2 * delta_x[i]
        yield tren_x[:]
        tren_x[i] += delta_x[i]

def LP(f, x0, max_iter, eps, delta_x):
    cur_iter = 0
    tren_x = x0
    while cur_iter < max_iter:
        tren_vr = f(tren_x)
        prosli_x = tren_x
        for okolni_x in okolina(tren_x, delta_x):
            okolni_vr = f(okolni_x)
            if okolni_vr < tren_vr:
                tren_x = okolni_x
                tren_vr = f(tren_x)
        if abs(f(prosli_x) - f(tren_x)) < eps:
            break
    cur_iter += 1
    return (tren_x, f(tren_x))

print(LP(lambda x: x[0] ** 2 + x[1] ** 2, [10, 5], 500, 1e-4, (0.01, 0.01)))
print(LP(lambda x: (x[0] + x[1]) ** 2, [10, 5], 500, 1e-4, (0.01, 0.01)))
print(LP(lambda x: x[0] ** 2 + x[1] ** 2 + 4 * math.exp(-(x[0] ** 2 + x[1] ** 2)), [10, 5], 500, 1e-4, (0.01, 0.01)))
print(LP(lambda x: -math.exp(-(x[0] ** 2 + x[1] ** 2)) - 2 * math.exp(-((x[0] - 1) ** 2 + (x[1] - 1.2) ** 2)), [10, 5], 500, 1e-4, (0.01, 0.01)))
