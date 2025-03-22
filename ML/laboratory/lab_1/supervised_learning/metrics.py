import numpy as np


def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))


def mse(y_true, y_pred):
    return np.mean((y_true - y_pred) ** 2)


def r2_score_(y_true, y_pred):
    return 1 - (np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2))


def rmse(y_true, y_pred):
    return np.sqrt(mse(y_true, y_pred))


def mape(y_true, y_pred):
    return np.mean((np.abs(y_true - y_pred)) / (np.abs(y_true)))