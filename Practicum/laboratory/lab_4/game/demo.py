import pygame
from simulation.tank_env import TankEnv

# Сопоставление клавиш и действий среды
KEY_ACTIONS = {
    pygame.K_UP: 0,    # вперёд
    pygame.K_DOWN: 1,  # назад
    pygame.K_LEFT: 2,  # поворот влево
    pygame.K_RIGHT: 3, # поворот вправо
}
SHOOT_KEY = pygame.K_SPACE  # действие стрельбы (4)

def main():
    pygame.init()
    env = TankEnv(width=640, height=480, cell_size=40)
    state = env.reset()

    running = True
    while running:
        shot = False  # флаг, что в этом кадре был выстрел
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Стрельба по событию KEYDOWN (один выстрел за нажатие)
            elif event.type == pygame.KEYDOWN and event.key == SHOOT_KEY:
                state, reward, done, _ = env.step(4)
                shot = True
                if done:
                    state = env.reset()
        # Если не было выстрела, обрабатываем движение или обновляем только пули
        if not shot:
            keys = pygame.key.get_pressed()
            action = None
            for key, act in KEY_ACTIONS.items():
                if keys[key]:
                    action = act
                    break
            state, reward, done, _ = env.step(action)
            if done:
                state = env.reset()

        # Рендеринг среды
        env.render()

    env.close()
    pygame.quit()

if __name__ == '__main__':
    main()
