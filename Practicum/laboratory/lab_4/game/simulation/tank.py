import pygame
import math

class Tank:
    """
    Класс Tank представляет агент-танк в среде.
    Хранит положение, угол поворота и отвечает за отрисовку и выстрелы.
    """
    def __init__(self, x: float, y: float, angle: float = 0.0,
                 size: int = 30, color: tuple = (200, 0, 0)):
        """
        Args:
            x (float): начальная x-координата центра танка
            y (float): начальная y-координата центра танка
            angle (float): угол поворота в градусах (0 = вправо, 90 = вверх)
            size (int): размер квадрата, описывающего танк
            color (tuple): цвет танка в формате RGB
        """
        self.x = x
        self.y = y
        self.angle = angle  # в градусах, по часовой стрелке
        self.size = size
        self.color = color
        self.speed = 5.0      # пикселей за шаг
        self.turn_speed = 5.0 # градусов за шаг

    def move_forward(self):
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y -= math.sin(rad) * self.speed

    def move_backward(self):
        rad = math.radians(self.angle)
        self.x -= math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

    def turn_left(self):
        self.angle = (self.angle + self.turn_speed) % 360

    def turn_right(self):
        self.angle = (self.angle - self.turn_speed) % 360

    def shoot(self):
        """
        Создает снаряд, вылетающий из передней части танка.
        Возвращает словарь с начальными координатами и углом полёта.
        """
        rad = math.radians(self.angle)
        bx = self.x + math.cos(rad) * (self.size / 2)
        by = self.y - math.sin(rad) * (self.size / 2)
        return {'pos': [bx, by], 'angle': self.angle}

    def draw(self, surface: pygame.Surface):
        """
        Рисует танк на заданной поверхности.
        Прямоугольник корпуса и ориентирующее направление.
        """
        # Прямоугольник танка
        rect = pygame.Rect(0, 0, self.size, self.size)
        rect.center = (self.x, self.y)
        pygame.draw.rect(surface, self.color, rect)
        # Линия направления
        rad = math.radians(self.angle)
        end_x = self.x + math.cos(rad) * (self.size / 2)
        end_y = self.y - math.sin(rad) * (self.size / 2)
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (end_x, end_y), 2)
