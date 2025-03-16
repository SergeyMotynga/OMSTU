def balance_transportation_problem(supply, demand, cost):
    """
    Балансирует транспортную задачу, если она не закрытого типа.
    Если supply > demand, добавляется фиктивный потребитель (новый столбец) с нулевыми затратами.
    Если supply < demand, добавляется фиктивный поставщик (новая строка) с нулевыми затратами.
    Возвращает:
      - обновлённые supply, demand и cost
      - dummy: индикатор добавленной фиктивной строки/колонки (None, 'dummy_row' или 'dummy_column')
    """
    total_supply = sum(supply)
    total_demand = sum(demand)
    if total_supply == total_demand:
        return supply, demand, cost, None
    elif total_supply > total_demand:
        # Добавляем фиктивного потребителя: новый столбец с затратами 0
        dummy_demand = total_supply - total_demand
        for i in range(len(supply)):
            cost[i].append(0)  # или можно задать другой штраф, если нужно
        demand.append(dummy_demand)
        print(f"Добавлен фиктивный потребитель с спросом {dummy_demand}")
        return supply, demand, cost, 'dummy_column'
    else:
        # Добавляем фиктивного поставщика: новая строка с затратами 0
        dummy_supply = total_demand - total_supply
        new_row = [0] * len(demand)
        cost.append(new_row)
        supply.append(dummy_supply)
        print(f"Добавлен фиктивный поставщик с поставкой {dummy_supply}")
        return supply, demand, cost, 'dummy_row'


def minimum_cost_method(supply, demand, cost):
    """
    Находит начальное базисное решение методом минимальной стоимости.
    Параметры:
      supply  - список поставок (длина m)
      demand  - список спроса (длина n)
      cost    - матрица затрат размером m x n
    Возвращает:
      - x: матрица распределения (m x n)
      - basis: множество базисных клеток (i, j)
    """
    m, n = len(supply), len(demand)
    supply_left = supply.copy()
    demand_left = demand.copy()
    x = [[0] * n for _ in range(m)]
    basis = set()

    # Индексы всех строк и столбцов, в которых ещё не исчерпан запас/спрос
    active_rows = set(range(m))
    active_cols = set(range(n))

    while active_rows and active_cols:
        # Ищем клетку с минимальной стоимостью среди "активных" строк и столбцов
        min_val = float('inf')
        min_cell = None
        for i in active_rows:
            for j in active_cols:
                if cost[i][j] < min_val:
                    min_val = cost[i][j]
                    min_cell = (i, j)

        if min_cell is None:
            break

        i, j = min_cell
        # Выделяем возможное количество
        allocation = min(supply_left[i], demand_left[j])
        x[i][j] = allocation
        # Если распределили что-то > 0, клетка становится базисной
        if allocation > 0:
            basis.add((i, j))

        # Обновляем остатки
        supply_left[i] -= allocation
        demand_left[j] -= allocation

        # Если у поставщика запас исчерпан — убираем строку из "активных"
        if supply_left[i] == 0:
            active_rows.remove(i)
        # Если у потребителя спрос исчерпан — убираем столбец из "активных"
        if demand_left[j] == 0:
            active_cols.remove(j)

    # Обработка вырождения: если базисных клеток меньше, чем (m + n - 1),
    # добавляем нулевые клетки, чтобы размер базиса был достаточным.
    total_required = m + n - 1
    if len(basis) < total_required:
        for i in range(m):
            for j in range(n):
                if (i, j) not in basis:
                    basis.add((i, j))
                    if len(basis) == total_required:
                        break
            if len(basis) == total_required:
                break

    return x, basis


def calculate_potentials(cost, basis, m, n):
    """
    Вычисляет потенциалы u (для строк) и v (для столбцов) по базисным клеткам,
    решая систему уравнений: u[i] + v[j] = cost[i][j] для (i, j) из базиса.
    Возвращает:
    - u: список потенциалов строк
    - v: список потенциалов столбцов
    """
    u = [None] * m
    v = [None] * n
    # Произвольно зафиксируем u[0] = 0
    u[0] = 0
    changed = True
    while changed:
        changed = False
        for (i, j) in basis:
            if u[i] is not None and v[j] is None:
                v[j] = cost[i][j] - u[i]
                changed = True
            elif v[j] is not None and u[i] is None:
                u[i] = cost[i][j] - v[j]
                changed = True
    return u, v


def find_cycle(basis, start):
    """
    Находит цикл в расширенном базисе, содержащий клетку start.
    Цикл должен чередовать горизонтальные и вертикальные перемещения.
    Возвращает список клеток цикла (без повторения стартовой клетки в конце).
    """
    def dfs(current, start, path, last_direction):
        # Если длина пути >= 4 и мы вернулись в стартовую клетку — найден цикл
        if len(path) >= 4 and current == start:
            return path.copy()
        # Проходим по всем базисным клеткам
        for (i, j) in extended_basis:
            if (i, j) == current:
                continue
            # Разрешаем ход, если в той же строке или в том же столбце
            if i == current[0] or j == current[1]:
                direction = 'row' if i == current[0] else 'col'
                # Требуется чередование: нельзя дважды подряд идти по строкам или по столбцам
                if last_direction is not None and direction == last_direction:
                    continue
                # Избегаем повторного прохода по уже посещённой клетке (кроме возвращения в start)
                if (i, j) in path and (i, j) != start:
                    continue

                path.append((i, j))
                result = dfs((i, j), start, path, direction)
                if result is not None:
                    return result
                path.pop()
        return None

    # Расширяем базис, добавляя клетку start (чтобы найти цикл с ней)
    extended_basis = set(basis)
    extended_basis.add(start)
    return dfs(start, start, [start], None)


def transportation_method(cost, supply, demand):
    """
    Решает транспортную задачу закрытого типа:
      1) Балансирует задачу, если она не закрытого типа (добавление фиктивного поставщика или потребителя)
      2) Получает начальное решение методом минимальной стоимости
      3) Оптимизирует его методом потенциалов (MODI)
    Параметры:
      cost   - матрица затрат (m x n)
      supply - вектор поставок (длина m)
      demand - вектор спроса (длина n)
    Возвращает:
      - x: оптимальное распределение перевозок (матрица m x n)
      - total_cost: итоговая (минимальная) стоимость
    """
    # Балансировка задачи
    supply, demand, cost, dummy = balance_transportation_problem(supply, demand, cost)
    m, n = len(supply), len(demand)
    # Шаг 1: Начальное базисное решение методом минимальной стоимости
    x, basis = minimum_cost_method(supply, demand, cost)

    # Шаг 2: Итерационная оптимизация (метод потенциалов)
    while True:
        u, v = calculate_potentials(cost, basis, m, n)

        # Ищем не базисную клетку с наибольшим отрицательным значением дельты (оценки)
        entering = None
        min_delta = 0
        for i in range(m):
            for j in range(n):
                if (i, j) not in basis:
                    delta = cost[i][j] - (u[i] + v[j])
                    if delta < min_delta:
                        min_delta = delta
                        entering = (i, j)

        # Если нет отрицательных дельт, решение оптимально
        if entering is None:
            break

        # Находим цикл, добавляя новую клетку в базис (entering)
        cycle = find_cycle(basis, entering)
        if not cycle:
            raise ValueError("Не удалось найти цикл для улучшения. Проверьте корректность решения.")

        # Если цикл замкнулся (первая и последняя клетки совпали), убираем дублирующий хвост
        if cycle[0] == cycle[-1]:
            cycle = cycle[:-1]

        minus_cells = cycle[1::2]
        # Минимальный объём, который можно "перебросить"
        theta = min(x[i][j] for (i, j) in minus_cells)

        # Определяем клетку, покидающую базис (первая минус-клетка, где x[i][j] == theta)
        leaving = None
        for (i, j) in minus_cells:
            if x[i][j] == theta:
                leaving = (i, j)
                break

        # Корректируем распределение по циклу: +θ и -θ
        sign = 1
        for (i, j) in cycle:
            x[i][j] += sign * theta
            sign *= -1

        # Обновляем базис
        basis.add(entering)
        if leaving in basis:
            basis.remove(leaving)

    # Итоговая стоимость
    total_cost = sum(x[i][j] * cost[i][j] for i in range(m) for j in range(n))
    return x, total_cost


def main():
    cost = [
        [4,  21, 12,  8,  1],
        [20,  8, 25, 15, 23],
        [17,  1, 11,  5,  3],
        [23, 10, 24,  6,  5]
    ]
    # Запасы
    supply = [21, 21, 23, 23]
    # Спрос
    demand = [22, 22, 22, 11, 11]

    solution, total_cost = transportation_method(cost, supply, demand)

    print("\nОптимальное распределение поставок (x[i][j]):")
    for i, row in enumerate(solution):
        print(f"S{i+1}:", row)
    print(f"\nМинимальная суммарная стоимость перевозок: {total_cost}")


if __name__ == '__main__':
    main()
