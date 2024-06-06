from numpy import linspace, sin, pi

def f(x):
    return x * sin(x)

a = 0
b = pi
n = 8
h = (b - a) / n
x = linspace(a, b, n + 1)
I = (f(a) + f(b))
for j in range(1, n):
    if j % 2 == 0:
        I += 2 * f(x[j])
    else:
        I += 4 * f(x[j])

I = (h / 3) * I
print('Approximate Solution is', I)
print('Hardhik-10990')
