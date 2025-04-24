import numpy as np


class ridge:
    def __init__(self, alpha=1, n_iter=10000, learning_rate=0.001):
        self.alpha = alpha
        self.n_iter = n_iter
        self.learning_rate = learning_rate
        self.tol = 1e-6
        self.weights = None
        self.bias = None


    def __gradient(self, X_train, y_train):
        for i in range(self.n_iter):
            y_pred = np.dot(X_train, self.weights) + self.bias
            errors = y_pred - y_train

            dw = (2 / self.n_samples) * np.dot(X_train.T, errors) + self.alpha * self.weights
            db = (2 / self.n_samples) * np.sum(errors)

            if np.linalg.norm(dw) < self.tol and abs(db) < self.tol:
                print(f'Остановка на итерации {i}, ||dw||: {np.linalg.norm(dw):.6f}, |db|: {abs(db):.6f}')
                break

            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db



    def fit(self, X_train, y_train):
        self.n_samples, self.n_features = X_train.shape
        self.weights = np.zeros(self.n_features)
        self.bias = 0.0
        self.__gradient(X_train, y_train)


    def predict(self, X_test):
        return np.dot(X_test, self.weights) + self.bias
    

    def coef_(self):
        return self.weights
