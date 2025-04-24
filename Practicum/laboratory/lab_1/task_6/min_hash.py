import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

class MinHash:
    def __init__(self, num_hashes=100, seed=42):
        self.num_hashes = num_hashes
        self.seed = seed
        self.hash_funcs = self._generate_hash_functions()

    def _generate_hash_functions(self):
        random.seed(self.seed)
        max_hash = (1 << 32) - 1
        return [
            (random.randint(1, max_hash), random.randint(0, max_hash))
            for _ in range(self.num_hashes)
        ]

    def _hash(self, x, a, b):
        return (a * hash(x) + b) % (1 << 32)

    def signature(self, input_set):
        sig = []
        for a, b in self.hash_funcs:
            min_hash = min(self._hash(el, a, b) for el in input_set)
            sig.append(min_hash)
        return sig

    @staticmethod
    def estimate_jaccard(sig1, sig2):
        assert len(sig1) == len(sig2)
        matches = sum(1 for x, y in zip(sig1, sig2) if x == y)
        return matches / len(sig1)

# Генерация непересекающихся множеств
def generate_disjoint_sets(n, set_size=50, universe_size=100000):
    sets = []
    for _ in range(n):
        set_a = set(random.sample(range(universe_size), set_size))
        set_b = set(random.sample(range(universe_size, universe_size * 2), set_size))
        sets.append((set_a, set_b))
    return sets

# Расчёт FPR для общего теста
def false_positive_rate_minhash(mh, disjoint_sets, threshold=0.5):
    false_positives = 0
    total = len(disjoint_sets)

    for setA, setB in disjoint_sets:   
        sigA = mh.signature(setA)
        sigB = mh.signature(setB)
        est_sim = mh.estimate_jaccard(sigA, sigB)
        if est_sim > threshold:
            false_positives += 1

    return false_positives / total

# Проверка FPR конкретной реализации MinHash
def evaluate_single_minhash_fpr(mh, disjoint_sets, threshold=0.5):
    false_positives = 0
    total = len(disjoint_sets)

    for setA, setB in disjoint_sets:
        sigA = mh.signature(setA)
        sigB = mh.signature(setB)
        est_sim = mh.estimate_jaccard(sigA, sigB)
        if est_sim > threshold:
            false_positives += 1

    fpr = false_positives / total
    print(f"\nОценка конкретной реализации: num_hashes={mh.num_hashes}, threshold={threshold} → FPR = {fpr:.4f}")
    return fpr

def main():
    hash_sizes = [5, 10, 20, 50, 100, 200]
    sets = generate_disjoint_sets(500, set_size=50)
    results = []

    for h in hash_sizes:
        mh = MinHash(num_hashes=h)
        fpr = false_positive_rate_minhash(mh, sets, threshold=0.5)
        results.append((h, fpr))
        print(f"Hashes={h}, False Positive Rate={fpr:.4f}")

    df = pd.DataFrame(results, columns=["NumHashes", "FalsePositiveRate"])
    print("\nТаблица ложноположительных:\n")
    print(df)

    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df, x="NumHashes", y="FalsePositiveRate", marker="o")
    plt.title("Зависимость FPR от количества хешей (MinHash)")
    plt.xlabel("Количество хеш-функций")
    plt.ylabel("False Positive Rate")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    mh_50 = MinHash(num_hashes=50)
    evaluate_single_minhash_fpr(mh_50, sets, threshold=0.5)

# Запуск
if __name__ == "__main__":
    main()
