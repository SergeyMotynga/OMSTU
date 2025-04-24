import hashlib
import random
import matplotlib.pyplot as plt
import pandas as pd


class Slot:
    def __init__(self):
        self.is_occupied = False
        self.is_continuation = False
        self.is_shifted = False
        self.remainder = None

    def empty(self):
        return self.remainder is None


class QuotientFilter:
    def __init__(self, q, r):
        self.q = q
        self.r = r
        self.size = 1 << q
        self.slots = [Slot() for _ in range(self.size)]

    def _hash(self, value):
        h = hashlib.sha256(str(value).encode()).hexdigest()
        h_int = int(h, 16)
        return h_int & ((1 << (self.q + self.r)) - 1)

    def _get_qr(self, h):
        quotient = h >> self.r
        remainder = h & ((1 << self.r) - 1)
        return quotient, remainder

    def _increment(self, idx):
        return (idx + 1) % self.size

    def insert(self, value):
        h = self._hash(value)
        q, r = self._get_qr(h)

        idx = q
        slot = self.slots[idx]

        if slot.empty():
            slot.is_occupied = True
            slot.remainder = r
            return

        if not slot.is_occupied:
            slot.is_occupied = True

        # Найдём, куда вставить с пробированием
        insert_idx = idx
        while not self.slots[insert_idx].empty():
            insert_idx = self._increment(insert_idx)
            if insert_idx == idx:
                raise Exception("Quotient filter is full")

        # Сдвигаем элементы вправо
        while insert_idx != idx:
            prev = (insert_idx - 1) % self.size
            self.slots[insert_idx] = self.slots[prev]
            self.slots[insert_idx].is_shifted = True
            insert_idx = prev

        self.slots[idx].remainder = r
        self.slots[idx].is_shifted = (idx != q)
        self.slots[idx].is_continuation = False  # зависит от места вставки
        self.slots[idx].is_occupied = True

    def query(self, value):
        h = self._hash(value)
        q, r = self._get_qr(h)

        idx = q
        slot = self.slots[idx]

        if not slot.is_occupied:
            return False

        # Перебор кластера
        while True:
            if self.slots[idx].remainder == r:
                return True
            idx = self._increment(idx)
            if not self.slots[idx].is_shifted:
                break
        return False



def calculate_false_positive_rate(qf, true_values, false_values):
    false_positive_count = 0

    for value in false_values:
        if qf.query(value):
            false_positive_count += 1

    false_positive_rate = false_positive_count / len(false_values) * 100
    return false_positive_rate


def evaluate_false_positive_dependency(true_values, false_values, q_values, r_values):
    results = []

    for q in q_values:
        for r in r_values:
            qf = QuotientFilter(q, r)
            try:
                for value in true_values:
                    qf.insert(value)
                fpr = calculate_false_positive_rate(qf, true_values, false_values)
                results.append((q, r, fpr))
            except Exception as e:
                print(f"Ошибка при q={q}, r={r}: {e}")
                results.append((q, r, None))

    return results


true_values = [f"user_{i}" for i in range(1000)]
false_values = [f"not_user_{i}" for i in range(1000, 2000)]

q_values = list(range(6, 17))
r_values = list(range(4, 13, 2)) 

results = evaluate_false_positive_dependency(true_values, false_values, q_values, r_values)

df = pd.DataFrame(results, columns=["q", "r", "False Positive Rate"])
print(df)

plt.figure(figsize=(10, 5))
for r in r_values:
    subset = df[df["r"] == r].dropna()
    plt.plot(subset["q"], subset["False Positive Rate"], marker="o", label=f"r={r}")

plt.xlabel("q (log2 числа слотов)")
plt.ylabel("False Positive Rate (%)")
plt.title("Зависимость ложноположительных срабатываний от параметров q и r")
plt.legend()
plt.grid(True)
plt.show()