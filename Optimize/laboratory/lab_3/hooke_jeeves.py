import numpy as np

# Метод Хукса и Дживса
def hooke_jeeves(f, x0, delta=0.5, alpha=2.0, eps=1e-6, max_iter=500):
    x_prev = np.array(x0, dtype=float)
    n = x_prev.size

    # Инициализация векторов шагов
    if np.isscalar(delta):
        deltas = np.full(n, delta, dtype=float)
    else:
        deltas = np.array(delta, dtype=float)

    def exploratory_move(x_base, deltas):
        # Исследовательский шаг: перебор координатных смещений.
        x = x_base.copy()
        f_base = f(x)
        for i in range(n):
            for sign in (+1, -1):
                trial = x.copy()
                trial[i] += sign * deltas[i]
                f_trial = f(trial)
                if f_trial < f_base:
                    x[i] = trial[i]
                    f_base = f_trial
                    break
        return x, f_base

    f_prev = f(x_prev)
    it = 0

    while np.any(deltas > eps) and it < max_iter:
        # 1) Исследуем окрестность текущей точки
        x_expl, f_expl = exploratory_move(x_prev, deltas)

        if f_expl < f_prev:
            # 2) Шаблонный шаг экспоненциального движения
            x_pattern = x_expl + (x_expl - x_prev)
            f_pattern = f(x_pattern)

            # После шаблонного шага — снова исследуем
            x_new, f_new = exploratory_move(x_pattern, deltas)

            # Выбираем лучшее
            if f_new < f_expl:
                x_prev, f_prev = x_new, f_new
            else:
                x_prev, f_prev = x_expl, f_expl
        else:
            # 3) Нет улучшения — уменьшаем масштаб поиска
            deltas /= alpha

        it += 1

    return x_prev, f_prev