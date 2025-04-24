import hashlib
import math
import pandas as pd
import matplotlib.pyplot as plt

class HyperLogLog:
    def __init__(self, b=4):
        self.b = b  # количество битов для выбора "корзины"
        self.m = 1 << b  # всего корзин
        self.registers = [0] * self.m

    def _hash(self, value):
        # Возвращает хэш в виде числа
        h = hashlib.sha1(str(value).encode()).hexdigest()
        return int(h, 16)

    def _get_register_index_and_rho(self, hashed_value):
        # Разделим хэш: первые b бит — номер корзины
        bin_value = bin(hashed_value)[2:].zfill(160)
        index = int(bin_value[:self.b], 2)
        rest = bin_value[self.b:]
        # rho — количество ведущих нулей в оставшейся части + 1
        leading_zeros = len(rest) - len(rest.lstrip('0')) + 1
        return index, leading_zeros

    def add(self, value):
        # Добавление элемента в фильтр
        h = self._hash(value)
        index, rho = self._get_register_index_and_rho(h)
        self.registers[index] = max(self.registers[index], rho)

    def count(self):
        # Оценка кардинальности множества
        Z = sum([2 ** -r for r in self.registers])
        E = (0.7213 / (1 + 1.079 / self.m)) * (self.m ** 2) / Z
        return int(E)

if __name__ == "__main__":
    # Пример с небольшим набором значений
    hll = HyperLogLog(b=4)
    values = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'apple', 'banana']
    for v in values:
        hll.add(v)

    estimated = hll.count()
    actual = len(set(values))

    print(f"Значения: {values}")
    print(f"Реальное число уникальных значений: {actual}")
    print(f"Оценка HyperLogLog: {estimated}")
    print(f"Состояние регистров: {hll.registers}")

    # График зависимости погрешности при большем объёме
    true_n = 100_000
    b_values = list(range(4, 17))
    results = []
    for b in b_values:
        hll_test = HyperLogLog(b)
        for i in range(true_n):
            hll_test.add(f"user_{i}")
        estimate = hll_test.count()
        error = abs(estimate - true_n) / true_n * 100
        results.append({
            "b": b,
            "error_pct": round(error, 2)
        })
    df = pd.DataFrame(results)

    plt.figure(figsize=(10, 5))
    plt.plot(df["b"], df["error_pct"], marker='o')
    plt.title("Погрешность (%) от параметра b")
    plt.xlabel("b (лог2 кол-ва регистров)")
    plt.ylabel("Погрешность (%)")
    plt.grid(True)
    plt.xticks(b_values)
    plt.show()
    
    print("\nТаблица погрешностей по параметру b:")
    print(df)