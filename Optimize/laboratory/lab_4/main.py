import numpy as np
import matplotlib.pyplot as plt

def projected_gradient_descent(f, grad_f, projector, x0, alpha=0.1, tol=1e-6, max_iter=100):
    x = projector(x0)
    trajectory = [x.copy()]

    for _ in range(max_iter):
        grad = grad_f(x)
        x_new = x - alpha * grad
        x_new = projector(x_new)
        trajectory.append(x_new.copy())
        if np.linalg.norm(x_new - x) < tol:
            break
        x = x_new

    return np.array(trajectory), x, f(x)

def f(x):
    return x[0] - x[1]

def grad_f(x):
    return np.array([1.0, -1.0])

R = np.sqrt(2)
def projector_circle(x):
    return R * x / np.linalg.norm(x)

# стартовая точка
x0 = np.array([1.0, 1.0])

# Запуск алгоритма
trajectory, x_opt, f_opt = projected_gradient_descent(
    f=f,
    grad_f=grad_f,
    projector=projector_circle,
    x0=x0,
    alpha=0.1,
    tol=1e-6,
    max_iter=100
)

print("Найденная точка:", x_opt)
print("Значение функции в точке:", f_opt)

# Визуализация
theta = np.linspace(0, 2*np.pi, 200)
circle = np.vstack((R*np.cos(theta), R*np.sin(theta))).T

plt.figure(figsize=(6,6))
plt.plot(circle[:,0], circle[:,1], 'k--', label='Ограничение')
plt.plot(trajectory[:,0], trajectory[:,1], 'x-', label='Траектория ПГС')
plt.scatter(*x_opt, c='red', label='Решение')
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.title('Проецируемый градиентный спуск')
plt.legend()
plt.axis('equal')
plt.show()
