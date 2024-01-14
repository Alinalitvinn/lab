# Імпортуємо необхідні бібліотеки
import numpy as np
import matplotlib.pyplot as plt

# 1. Генеруємо випадкові дані навколо прямої y = 3x + 4
true_k = 3  # Задаємо справжній нахил прямої
true_b = 4  # Задаємо справжній зсув прямої

num_points = 50  # Кількість точок для генерації
x = np.random.uniform(0, 10, size=num_points)  # Генеруємо випадкові x з рівномірним розподілом
y = true_k * x + true_b + np.random.normal(0, 3, size=num_points)  # Обчислюємо y з додаванням шуму


# 2. Функція МНК
def least_squares(x, y):
    # Обчислюємо середні
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    # За формулою МНК
    num = np.sum((x - x_mean) * (y - y_mean))
    den = np.sum((x - x_mean) ** 2)

    # Обчислюємо параметри
    k = num / den
    b = y_mean - k * x_mean

    return k, b


# 3. Порівнюємо з np.polyfit
k_ls, b_ls = least_squares(x, y)
k_np, b_np = np.polyfit(x, y, 1)

print(f'МНК: k={k_ls:.3f}, b={b_ls:.3f}')
print(f'NumPy: k={k_np:.3f}, b={b_np:.3f}')
print(f'Істинні: k={true_k:.3f}, b={true_b:.3f}')

# 4. Будуємо графіки
plt.scatter(x, y)  # Розсіяний графік даних

plt.plot(x, true_k * x + true_b, c='black')  # Істинна пряма

y_pred_ls = k_ls * x + b_ls
plt.plot(x, y_pred_ls, c='blue', label='МНК')  # Пряма МНК

y_pred_np = k_np * x + b_np
plt.plot(x, y_pred_np, c='red', label='NumPy')  # Пряма NumPy

plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Порівняння МНК та NumPy')
plt.show()


