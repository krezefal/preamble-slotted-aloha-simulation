import numpy as np
import matplotlib.pyplot as plt

# Параметры
N = 100  # Количество окон
M = 5  # Интенсивность (лямбда)

# Генерация массива заявок по закону Пуассона
requests = np.random.poisson(lam=M, size=N)

# Печать результатов
print("Массив заявок:", requests)

# Визуализация распределения заявок
plt.figure(figsize=(10, 6))
plt.bar(range(N), requests, color='#FF5733')
plt.xlabel('Окно')
plt.ylabel('Количество заявок')
plt.title('Распределение заявок по закону Пуассона')
plt.show()