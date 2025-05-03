import numpy as np
import random

class QLearningAgent:
    """
    Q-Learning агент для дискретных состояний и действий.
    Хранит Q-таблицу, реализует ε-жадную стратегию.
    """
    def __init__(self, actions, alpha=0.1, gamma=0.99,
                 epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995):
        """
        Args:
            actions (list): список возможных действий
            alpha (float): скорость обучения
            gamma (float): дисконт-фактор
            epsilon_start (float): начальное значение ε
            epsilon_end (float): минимальное значение ε
            epsilon_decay (float): множитель для экспоненциального затухания ε
        """
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        # Q-таблица: обычный словарь state -> np.array Q(s,a)
        self.Q = {}

    def discretize(self, state):
        """
        Переводит непрерывное состояние в дискретное представление (ключ для Q-таблицы).
        """
        return (
            round(state['x'], 1),
            round(state['y'], 1),
            round(state['angle'] / 10) * 10,
            round(state['distance_to_goal'] / 10) * 10,
            round(state['angle_to_goal'] / 10) * 10,
        )

    def _get_q_values(self, s_key):
        """
        Возвращает Q-значения для заданного состояния, создавая массив если нужно.
        """
        if s_key not in self.Q:
            self.Q[s_key] = np.zeros(len(self.actions))
        return self.Q[s_key]

    def choose_action(self, state):
        """
        Возвращает действие по ε-жадной стратегии.
        """
        s_key = self.discretize(state)
        # ε-жадный выбор
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        q_values = self._get_q_values(s_key)
        return int(np.argmax(q_values))

    def update(self, state, action, reward, next_state, done):
        """
        Обновляет Q-значение по формуле Q-learning.
        """
        s_key = self.discretize(state)
        ns_key = self.discretize(next_state)
        q_values = self._get_q_values(s_key)
        if done:
            q_target = reward
        else:
            next_q = self._get_q_values(ns_key)
            q_target = reward + self.gamma * np.max(next_q)
        # Обновление Q
        q_values[action] += self.alpha * (q_target - q_values[action])

        # Затухание ε после завершения эпизода
        if done:
            self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
