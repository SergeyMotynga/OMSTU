import numpy as np
from collections import Counter
import pandas as pd

# Класс узла дерева
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, value=None):
        self.feature = feature      # Индекс признака для разделения
        self.threshold = threshold  # Порог для разделения
        self.left = left           # Левый потомок
        self.right = right         # Правый потомок
        self.value = value         # Значение для листового узла (класс или число)

# Класс CART
class CART:
    def __init__(self, task_type="classification", max_depth=None, min_samples_split=2):
        self.task_type = task_type                # Тип задачи: "classification" или "regression"
        self.max_depth = max_depth                # Максимальная глубина дерева
        self.min_samples_split = min_samples_split # Минимальное число образцов для разделения
        self.root = None

    # Метрика Gini для классификации
    def _gini(self, y):
        counter = Counter(y)
        impurity = 1.0
        for count in counter.values():
            prob = count / len(y)
            impurity -= prob ** 2
        return impurity

    # MSE для регрессии
    def _mse(self, y):
        if len(y) == 0:
            return 0
        mean = np.mean(y)
        return np.mean((y - mean) ** 2)

    # Вычисление качества разделения
    def _split_score(self, left_y, right_y):
        if self.task_type == "classification":
            score = (len(left_y) * self._gini(left_y) + len(right_y) * self._gini(right_y)) / (len(left_y) + len(right_y))
        else:
            score = (len(left_y) * self._mse(left_y) + len(right_y) * self._mse(right_y)) / (len(left_y) + len(right_y))
        return score

    # Поиск лучшего разделения
    def _best_split(self, X, y):
        best_feature, best_threshold, best_score = None, None, float('inf')
        n_features = X.shape[1]

        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask

                left_y, right_y = y[left_mask], y[right_mask]

                if len(left_y) < self.min_samples_split or len(right_y) < self.min_samples_split:
                    continue

                score = self._split_score(left_y, right_y)
                if score < best_score:
                    best_score = score
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold, best_score

    # Построение дерева
    def _build_tree(self, X, y, depth=0):
        n_samples = len(y)

        # Условия остановки
        if (self.max_depth is not None and depth >= self.max_depth) or n_samples < self.min_samples_split:
            if self.task_type == "classification":
                value = Counter(y).most_common(1)[0][0]
            else:
                value = np.mean(y)
            return Node(value=value)

        # Поиск лучшего разделения
        feature, threshold, score = self._best_split(X, y)
        if feature is None:
            if self.task_type == "classification":
                value = Counter(y).most_common(1)[0][0]
            else:
                value = np.mean(y)
            return Node(value=value)

        # Разделение данных
        left_mask = X[:, feature] <= threshold
        right_mask = ~left_mask
        left_X, left_y = X[left_mask], y[left_mask]
        right_X, right_y = X[right_mask], y[right_mask]

        # Рекурсивное построение потомков
        left_node = self._build_tree(left_X, left_y, depth + 1)
        right_node = self._build_tree(right_X, right_y, depth + 1)

        return Node(feature=feature, threshold=threshold, left=left_node, right=right_node)

    # Обучение модели
    def fit(self, X, y):
        # Конвертация входных данных в NumPy массивы
        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        if isinstance(y, (pd.Series, pd.DataFrame)):
            y = y.to_numpy()
        self.root = self._build_tree(X, y)
        return self

    # Предсказание для одного примера
    def _predict_one(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self._predict_one(x, node.left)
        return self._predict_one(x, node.right)

    # Предсказание для набора данных
    def predict(self, X):
        # Конвертация входных данных в NumPy массив
        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        return np.array([self._predict_one(x, self.root) for x in X])