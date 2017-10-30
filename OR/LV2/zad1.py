import math

def newton_raphson(f, df, ddf, x0, max_iter, eps):
    iters = 0
    cur_x = x0
    next_x = 0
    while iters < max_iter:
        next_x = cur_x - df(cur_x) / ddf(cur_x)
        if abs(next_x - cur_x) < eps:
            break
        cur_x = next_x
        iters += 1
    cur_x = next_x
    return (cur_x, f(cur_x))

f = lambda x: math.cos(x)
df = lambda x: -math.sin(x)
ddf = lambda x: -math.cos(x)
print(newton_raphson(f, df, ddf, -0.3, 200, 0.01))

f = lambda x: x ** 3 - x + 1
df = lambda x: 3 * (x ** 2) - 1
ddf = lambda x: 6 * x
print(newton_raphson(f, df, ddf, 10, 200, 0.01))
