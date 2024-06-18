import numpy as np


def f(G, N=100):
    sum_value = 0
    for i in range(1, N+1):
        term = (1/np.math.factorial(i)) * ((1 - 1/i)**(i-1)) * (np.exp(G)) * (G**(i-1)) * (i - G)
        sum_value += term
    return sum_value


def f_prime(G, N=100):
    sum_value = 0
    for i in range(1, N+1):
        term = (1/np.math.factorial(i)) * ((1 - 1/i)**(i-1)) * (np.exp(G)) * (G**(i-2)) * (i*(i - 1 - G))
        sum_value += term
    return sum_value


def newton_raphson(G0, tol=1e-6, max_iter=1000):
    G = G0
    for _ in range(max_iter):
        fG = f(G)
        f_primeG = f_prime(G)
        if abs(f_primeG) < 1e-10:  # избегаем деления на очень малое число
            print("Производная близка к нулю.")
            break
        G_new = G - fG / f_primeG
        if abs(G_new - G) < tol:
            return G_new
        G = G_new
    return G


G0 = 1.0
solution = newton_raphson(G0)
print("Найденное значение G:", solution)
