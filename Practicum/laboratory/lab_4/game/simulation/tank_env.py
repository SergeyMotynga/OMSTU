import pygame
import math
from .tank import Tank

class TankEnv:
    """
    Среда для танка с препятствиями, несколькими целями и стрельбой.
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
        self.bullets = []  # список пуль

    def _build_map(self):
        # Препятствия
        self.obstacles = []
        rows = self.height // self.cell_size
        cols = self.width // self.cell_size
        # Центральная стена
        center_row = rows // 2
        for i in range(5):
            rect = pygame.Rect(
                (cols // 2 + i - 2) * self.cell_size,
                center_row * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            self.obstacles.append(rect)
        # Доп. препятствия
        extra = [(2,2),(cols-3,rows//3),(cols//3,rows-3)]
        for cx, cy in extra:
            self.obstacles.append(pygame.Rect(cx*self.cell_size, cy*self.cell_size, self.cell_size, self.cell_size))
        # Границы
        self.obstacles += [
            pygame.Rect(0,0,self.width,self.cell_size),
            pygame.Rect(0,self.height-self.cell_size,self.width,self.cell_size),
            pygame.Rect(0,0,self.cell_size,self.height),
            pygame.Rect(self.width-self.cell_size,0,self.cell_size,self.height)
        ]
        # Цели
        self.goals = []
        goal_cells = [(cols-2,rows-2),(1,rows-3),(cols-3,1)]
        for gx_i, gy_i in goal_cells:
            pos = (gx_i*self.cell_size + self.cell_size/2, gy_i*self.cell_size + self.cell_size/2)
            radius = int(self.cell_size*0.4)
            self.goals.append({'pos':pos,'radius':radius})

    def reset(self, start_pos=None, start_angle: float = 0.0):
        # Сброс среды
        if start_pos is None:
            start_pos = (self.cell_size*1.5, self.cell_size*1.5)
        x,y = start_pos
        self.tank = Tank(x,y,start_angle)
        self.bullets = []
        return self._get_state()

    def _get_sensor_distances(self):
        # Расстояния до ближайшего препятствия в 4 направлениях
        dirs = [0,90,180,270]
        dists = []
        step = self.cell_size/4
        for angle in dirs:
            rad = math.radians(angle)
            dist = 0.0
            x,y = self.tank.x, self.tank.y
            while True:
                x += math.cos(rad)*step
                y -= math.sin(rad)*step
                dist += step
                # за пределами
                if not (0<=x<=self.width and 0<=y<=self.height): break
                # столкновение с препятствием
                pt = pygame.Rect(x,y,1,1)
                if any(pt.colliderect(obs) for obs in self.obstacles): break
            dists.append(dist)
        return dists

    def _get_state(self):
        # Состояние: x,y,angle, расстояние и угол до ближайшей цели, сенсоры
        # Поиск ближайшей цели
        da = []
        for goal in self.goals:
            gx,gy = goal['pos']
            dx,dy = gx-self.tank.x, gy-self.tank.y
            dist = math.hypot(dx,dy)
            goal_ang = math.degrees(math.atan2(-dy,dx))%360
            rel = (goal_ang-self.tank.angle)%360
            da.append((dist,rel))
        if da:
            distance, rel_angle = min(da, key=lambda x:x[0])
        else:
            distance, rel_angle = 0.0, 0.0
        sensors = self._get_sensor_distances()
        return {
            'x': self.tank.x,
            'y': self.tank.y,
            'angle': self.tank.angle,
            'distance_to_goal': distance,
            'angle_to_goal': rel_angle,
            'obs_distances': sensors
        }

    def step(self, action: int):
        prev = self._get_state()
        reward = -1  # штраф за шаг
        done = False
        # Действия
        if action==0: self.tank.move_forward()
        elif action==1: self.tank.move_backward()
        elif action==2: self.tank.turn_left()
        elif action==3: self.tank.turn_right()
        elif action==4:
            # стрельба
            rad = math.radians(self.tank.angle)
            bx = self.tank.x + math.cos(rad)*self.tank.size/2
            by = self.tank.y - math.sin(rad)*self.tank.size/2
            self.bullets.append({'pos':[bx,by],'angle':self.tank.angle})
        # Ограничение положения
        self.tank.x = max(self.cell_size, min(self.tank.x, self.width-self.cell_size))
        self.tank.y = max(self.cell_size, min(self.tank.y, self.height-self.cell_size))
        # Обновление пуль
        new_bullets = []
        for b in self.bullets:
            rad = math.radians(b['angle'])
            b['pos'][0] += math.cos(rad)*10
            b['pos'][1] -= math.sin(rad)*10
            # проверка попадания в цель
            hit = False
            for goal in list(self.goals):
                gx,gy = goal['pos']
                if math.hypot(b['pos'][0]-gx,b['pos'][1]-gy)<=goal['radius']:
                    reward += 100
                    self.goals.remove(goal)
                    hit=True
            # проверка столкновения с преградой или границей
            if hit: continue
            pt = pygame.Rect(b['pos'][0],b['pos'][1],2,2)
            if any(pt.colliderect(obs) for obs in self.obstacles) or not (0<=b['pos'][0]<=self.width and 0<=b['pos'][1]<=self.height):
                continue
            new_bullets.append(b)
        self.bullets = new_bullets
        # Проверка столкновения танка
        tank_rect = pygame.Rect(0,0,self.tank.size,self.tank.size)
        tank_rect.center=(self.tank.x,self.tank.y)
        if any(tank_rect.colliderect(obs) for obs in self.obstacles):
            reward-=10
            done=True
        # Подсчёт вознаграждения за приближение
        curr = self._get_state()
        if prev['distance_to_goal']>curr['distance_to_goal']:
            reward+=10
        else:
            reward-=5
        # Эпизод окончен, если нет целей или танк разбит
        if not self.goals:
            done=True
        return curr, reward, done, {}

    def render(self):
        self.screen.fill((30,30,30))
        for obs in self.obstacles:
            pygame.draw.rect(self.screen,(100,100,100),obs)
        for goal in self.goals:
            gx,gy=goal['pos']
            pygame.draw.circle(self.screen,(0,200,0),(int(gx),int(gy)),goal['radius'])
        # отрисовка пуль
        for b in self.bullets:
            pygame.draw.circle(self.screen,(255,255,0),(int(b['pos'][0]),int(b['pos'][1])),2)
        if self.tank:
            self.tank.draw(self.screen)
        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        pygame.quit()
