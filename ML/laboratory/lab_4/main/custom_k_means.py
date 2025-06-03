import numpy as np

class CustomKMeans:
    def __init__(self, n_clusters, max_iter=300, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.labels_ = None
        self.inertia_ = None

    def fit_predict(self, X):
        if self.random_state is not None:
            np.random.seed(self.random_state)

        # Инициализация центроидов случайными точками из данных
        n_samples, n_features = X.shape
        indices = np.random.choice(n_samples, self.n_clusters, replace=False)
        self.centroids = X[indices]

        for _ in range(self.max_iter):
            # Присвоение точек к ближайшему центроиду
            old_centroids = self.centroids.copy()
            distances = np.sqrt(((X - self.centroids[:, np.newaxis])**2).sum(axis=2))
            self.labels_ = np.argmin(distances, axis=0)

            # Обновление центроидов
            for k in range(self.n_clusters):
                if np.sum(self.labels_ == k) > 0:
                    self.centroids[k] = np.mean(X[self.labels_ == k], axis=0)

            # Проверка сходимости
            if np.all(old_centroids == self.centroids):
                break

        # Вычисление инерции (суммы квадратов расстояний)
        self.inertia_ = 0
        for k in range(self.n_clusters):
            cluster_points = X[self.labels_ == k]
            if len(cluster_points) > 0:
                self.inertia_ += np.sum((cluster_points - self.centroids[k])**2)

        return self.labels_