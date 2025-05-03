import os
import numpy as np
import matplotlib.pyplot as plt

# Путь к файлу с наградами (в корне game)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REWARDS_FILE = os.path.join(BASE_DIR, 'episode_rewards.npy')

def main():
    # Проверяем наличие файла с наградами
    if not os.path.exists(REWARDS_FILE):
        print(f"Файл {REWARDS_FILE} не найден. Сначала запустите train.py для генерации данных.")
        return

    # Загружаем награды
    rewards = np.load(REWARDS_FILE)
    episodes = np.arange(1, len(rewards) + 1)

    # Рисуем график
    plt.figure()
    plt.plot(episodes, rewards)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Training Progress: Episode Reward')
    plt.grid(True)

    # Сохраняем рисунок
    output_path = os.path.join(BASE_DIR, 'training_rewards.png')
    plt.savefig(output_path)
    print(f"График сохранён в {output_path}")
    plt.show()

if __name__ == '__main__':
    main()
