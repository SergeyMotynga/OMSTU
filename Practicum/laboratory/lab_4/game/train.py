import os
import pickle
import numpy as np
from simulation.tank_env import TankEnv
from agent.q_learning_agent import QLearningAgent

# Каталог проекта (где лежит train.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Папка для контрольных точек
CHECKPOINT_DIR = os.path.join(BASE_DIR, 'checkpoints')
# Файл для сохранения наград
REWARDS_FILE = os.path.join(BASE_DIR, 'episode_rewards.npy')

# Параметры обучения
NUM_EPISODES = 1000
MAX_STEPS_PER_EPISODE = 2000

os.makedirs(CHECKPOINT_DIR, exist_ok=True)

# Инициализация среды и агента
env = TankEnv(width=640, height=480, cell_size=40)
agent = QLearningAgent(actions=[0,1,2,3,4], alpha=0.1, gamma=0.99,
                       epsilon_start=1.0, epsilon_end=0.01, epsilon_decay=0.995)

# Лог накопленных вознаграждений
episode_rewards = []

for episode in range(1, NUM_EPISODES + 1):
    state = env.reset()
    total_reward = 0.0
    for step in range(MAX_STEPS_PER_EPISODE):
        # Выбираем действие
        action = agent.choose_action(state)
        # Выполняем шаг среды
        next_state, reward, done, _ = env.step(action)
        # Обновляем Q-таблицу
        agent.update(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
        if done:
            break
    # Логируем эпизод
    episode_rewards.append(total_reward)
    print(f"Episode {episode:03d}: Reward = {total_reward:.2f}, Epsilon = {agent.epsilon:.4f}")
    # Сохраняем агент каждые 50 эпизодов
    if episode % 50 == 0:
        fname = os.path.join(CHECKPOINT_DIR, f'q_table_ep{episode:03d}.pkl')
        with open(fname, 'wb') as f:
            pickle.dump(agent.Q, f)
        print(f"Saved Q-table to {fname}")

# Финальная сохранение
final_fname = os.path.join(CHECKPOINT_DIR, 'q_table_final.pkl')
with open(final_fname, 'wb') as f:
    pickle.dump(agent.Q, f)
print("Training completed.")

# Сохраняем rewards в файл для последующего анализа
np.save(REWARDS_FILE, np.array(episode_rewards))
print(f"Saved episode rewards to {REWARDS_FILE}")
