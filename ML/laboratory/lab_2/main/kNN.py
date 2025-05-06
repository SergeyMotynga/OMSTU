import numpy as np
from collections import Counter

class kNN():
    '''
    Модель классификации реализующая метод k-ближайших соседей

    Parameters
    ----------
    k : int, default=5
        Количество соседей для предсказания.

    metric: str, default='minkowski'
        Вычисление расстояние от точки до k-ближайших соседей.

    p : float, default=2
        Параметр степени для метрики Минковского. Когда p = 1, это эквивалентно использованию manhattan_distance (l1) и euclidean_distance (l2) для p = 2. Ожидается, что параметр будет положительный.
    '''
    def __init__(self,
                k: int=5,
                metric: str='minkowski',
                p: float=2
                ):
        self.k = k
        self.metric = self.__distance
        self.p = p
        self.__fit_X = None
        self.__fit_y = None

    def fit(self,
            X_train=None,
            y_train=None
            ):
        self.__fit_X = np.array(X_train)
        self.__fit_y = np.array(y_train)
        return self
    
    def predict(self, X_test):
        X = np.array(X_test)
        return np.array([self.__predict_one(x) for x in X])

    def __predict_one(self, x):
        distances = np.array([self.metric(x, xi) for xi in self.__fit_X])
        idxs = np.argsort(distances)[:self.k]
        labels = self.__fit_y[idxs]
        most_popular = Counter(labels).most_common(1)
        return most_popular[0][0]

    def __distance(self, x, y):
        return np.sum(np.abs(x - y) ** self.p) ** (1 / self.p)