import numpy as np
import random
import hashlib
import matplotlib.pyplot as plt
import pandas as pd

class CountMinSketch:
    def __init__(self, width, depth, seed=42):
        self.width = width
        self.depth = depth
        self.count = np.zeros((depth, width), dtype=int)
        random.seed(seed)
        self.seeds = [random.randint(0, 10000) for _ in range(depth)]
    
    def _hash(self, x, i):
        h = hashlib.md5((str(self.seeds[i]) + str(x)).encode()).hexdigest()
        return int(h, 16) % self.width

    def add(self, x, count=1):
        for i in range(self.depth):
            idx = self._hash(x, i)
            self.count[i][idx] += count

    def estimate(self, x):
        return min(self.count[i][self._hash(x, i)] for i in range(self.depth))

def false_positive_rate(cms, added_items, test_items):
    false_positives = 0
    for item in test_items:
        if item not in added_items and cms.estimate(item) > 0:
            false_positives += 1
    return false_positives / len(test_items)

def test_fp_vs_params():
    results = []
    added_items = [f"item_{i}" for i in range(1000)]
    test_items = [f"test_{i}" for i in range(1000)]

    for w in [100, 200, 500, 1000, 5000]:
        for d in [3, 5, 10, 15, 20]:
            cms = CountMinSketch(width=w, depth=d)
            for item in added_items:
                cms.add(item)

            fp_rate = false_positive_rate(cms, set(added_items), test_items)
            results.append({'width': w, 'depth': d, 'false_positive_rate': fp_rate})
    
    df = pd.DataFrame(results)
    
    # Таблица
    print("=== False Positive Rate Table ===")
    print(df.pivot(index='depth', columns='width', values='false_positive_rate'))
    
    # График
    for d in sorted(df['depth'].unique()):
        subset = df[df['depth'] == d]
        plt.plot(subset['width'], subset['false_positive_rate'], marker='o', label=f'depth={d}')
    
    plt.xlabel("Width")
    plt.ylabel("False Positive Rate")
    plt.title("False Positive Rate vs Hyperparameters")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Запуск анализа
if __name__ == "__main__":
    test_fp_vs_params()
