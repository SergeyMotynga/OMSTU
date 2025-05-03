import pygame
import math
from simulation.tank import Tank

class TankEnv:
    """
    Простая среда для танка с препятствиями и целью.
    """
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 40):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tank RL Environment")
        self.clock = pygame.time.Clock()
        self._build_map()
        self.tank = None

    def _build_map(self):
        # Строим несколько препятствий в виде блоков
        self.obstacles = []
        rows = self.height // self.cell_size
        cols = self.width // self.cell_size
        # Пример: стенка из 5 блоков по центру
        center_row = rows // 2
        for i in range(5):
            rect = pygame.Rect(
                (cols // 2 + i - 2) * self.cell_size,
                center_row * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            self.obstacles.append(rect)
        # Цель как круг в правом нижнем углу
        gx = self.width - self.cell_size
        gy = self.height - self.cell_size
        self.goal_pos = (gx + self.cell_size / 2, gy + self.cell_size / 2)
        self.goal_radius = (self.cell_size // 2) * 0.8

    def reset(self, start_pos=None, start_angle: float = 0.0):
        # Сброс среды: новый танк
        if start_pos is None:
            start_pos = (self.cell_size / 2, self.cell_size / 2)
        x, y = start_pos
        self.tank = Tank(x, y, start_angle)
        return self._get_state()

    def _get_state(self):
        # Состояние: координаты, угол, расстояние и угол до цели
        dx = self.goal_pos[0] - self.tank.x
        dy = self.goal_pos[1] - self.tank.y
        distance = math.hypot(dx, dy)
        goal_angle = math.degrees(math.atan2(-dy, dx)) % 360
        rel_angle = (goal_angle - self.tank.angle) % 360
        # TODO: добавить датчики препятствий
        return {
            'x': self.tank.x,
            'y': self.tank.y,
            'angle': self.tank.angle,
            'distance_to_goal': distance,
            'angle_to_goal': rel_angle
        }

    def step(self, action: int):
        # Действия: 0=вперёд, 1=назад, 2=поворот влево, 3=поворот вправо
        # Сохраняем предыдущее состояние для расчёта вознаграждения
        prev_state = self._get_state()

        if action == 0:
            self.tank.move_forward()
        elif action == 1:
            self.tank.move_backward()
        elif action == 2:
            self.tank.turn_left()
        elif action == 3:
            self.tank.turn_right()

        # Проверка столкновений
        tank_rect = pygame.Rect(0, 0, self.tank.size, self.tank.size)
        tank_rect.center = (self.tank.x, self.tank.y)
        collision = any(tank_rect.colliderect(obs) for obs in self.obstacles)

        state = self._get_state()
        reward = -1  # штраф за шаг
        done = False

        if collision:
            reward -= 10
            done = True

        # Приближение/удаление
        if prev_state['distance_to_goal'] > state['distance_to_goal']:
            reward += 10
        else:
            reward -= 5

        # Достижение цели
        gx, gy = self.goal_pos
        if math.hypot(self.tank.x - gx, self.tank.y - gy) <= self.goal_radius:
            reward += 100
            done = True

        return state, reward, done, {}

    def render(self):
        self.screen.fill((30, 30, 30))
        # Рисуем препятствия
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, (100, 100, 100), obs)
        # Рисуем цель
        pygame.draw.circle(
            self.screen,
            (0, 200, 0),
            (int(self.goal_pos[0]), int(self.goal_pos[1])),
            int(self.goal_radius)
        )
        # Рисуем танк
        if self.tank:
            self.tank.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        pygame.quit()
