import random
import pandas as pd
import numpy as np
from itertools import combinations

class CarDatasetGenerator:
    CAR_FEATURES = [
        ('двигатель_включен', 'binary'),
        ('ручной_тормоз', 'binary'),
        ('фары_включены', 'binary'),
        ('тип_кузова', 'nominal'),
        ('привод', 'nominal'),
        ('топливо', 'nominal'),
        ('уровень_топлива', 'ordinal'),
        ('скоростной_режим', 'ordinal'),
        ('скорость', 'quantitative'),
        ('угол_поворота', 'quantitative'),
        ('дистанция_до_объекта', 'quantitative'),
        ('температура_двигателя', 'quantitative'),
        ('пробег', 'quantitative'),
        ('напряжение_аккумулятора', 'quantitative')
    ]

    def __init__(self, n_features: int, threshold: int = 50, random_state: int = None):
        """
        n_features — количество признаков на объект.
        threshold — процент совпадающих признаков для коллизии [0, 100].
        random_state — база случайности для воспроизводимости.
        """
        self.n_features = n_features
        self.threshold = threshold / 100  # переводим в долю
        self.random_state = random_state

    def _generate_objects(self, n_samples: int) -> pd.DataFrame:
        if self.random_state is not None:
            random.seed(self.random_state)
            np.random.seed(self.random_state)

        data = {}
        used_features = self.CAR_FEATURES.copy()
        while len(used_features) < self.n_features:
            used_features += self.CAR_FEATURES
        used_features = used_features[:self.n_features]

        for name, f_type in used_features:
            if f_type == 'binary':
                data[name] = np.random.randint(0, 2, size=n_samples)
            elif f_type == 'nominal':
                if name == 'тип_кузова':
                    data[name] = np.random.choice(['седан', 'внедорожник', 'грузовик', 'хэтчбек'], size=n_samples)
                elif name == 'привод':
                    data[name] = np.random.choice(['передний', 'задний', 'полный'], size=n_samples)
                elif name == 'топливо':
                    data[name] = np.random.choice(['бензин', 'дизель', 'электро', 'гибрид'], size=n_samples)
            elif f_type == 'ordinal':
                if name == 'уровень_топлива':
                    levels = ['низкий', 'средний', 'высокий']
                elif name == 'скоростной_режим':
                    levels = ['медленно', 'нормально', 'быстро']
                data[name] = pd.Categorical(np.random.choice(levels, size=n_samples), categories=levels, ordered=True)
            elif f_type == 'quantitative':
                if name == 'угол_поворота':
                    data[name] = np.random.uniform(-180, 180, size=n_samples)
                elif name == 'скорость':
                    data[name] = np.random.uniform(0, 200, size=n_samples)
                elif name == 'дистанция_до_объекта':
                    data[name] = np.random.exponential(scale=50, size=n_samples)
                elif name == 'температура_двигателя':
                    data[name] = np.random.normal(loc=90, scale=10, size=n_samples)
                elif name == 'пробег':
                    data[name] = np.random.normal(loc=50000, scale=15000, size=n_samples)
                elif name == 'напряжение_аккумулятора':
                    data[name] = np.random.normal(loc=12.5, scale=0.5, size=n_samples)

        return pd.DataFrame(data)

    def _calculate_required_objects(self, pairs_required: int) -> int:
        '''
        Формула сочетаний без повторений
        '''
        n = 2
        while n * (n - 1) // 2 < pairs_required:
            n += 1
        return n

    def generate_pairs_dataset(self, pairs_required: int) -> pd.DataFrame:
        """
        pairs_required — количество строк (пар объектов) в итоговом датасете.
        """
        n_objects = self._calculate_required_objects(pairs_required)
        df = self._generate_objects(n_objects)

        all_pairs = list(combinations(df.index, 2))
        random.seed(self.random_state)
        selected_pairs = random.sample(all_pairs, pairs_required)

        pairs_data = []
        for idx1, idx2 in selected_pairs:
            obj1 = df.loc[idx1].to_dict()
            obj2 = df.loc[idx2].to_dict()
            match_count = sum(obj1[k] == obj2[k] for k in obj1) / self.n_features
            collision = 'да' if match_count >= self.threshold else 'нет'
            pair_row = {f"1_{k}": obj1[k] for k in obj1}
            pair_row.update({f"2_{k}": obj2[k] for k in obj2})
            pair_row["collision"] = collision
            pairs_data.append(pair_row)

        return pd.DataFrame(pairs_data)
