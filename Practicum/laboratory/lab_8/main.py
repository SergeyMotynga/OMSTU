import PySimpleGUI as sg
from world import World
from stats import get_stats
from plants import Lumiere, Obscurite, Demi
from animals import Pauvre, Malheureux

# Настройка DPI для корректного отображения на Windows
sg.set_options(dpi_awareness=True)

# Определяем layout для окна
layout = [
    [sg.Text('Время:'),
     sg.Slider(range=(0, 23), orientation='h', size=(20, 15), key='-TIME-', enable_events=True, default_value=0),
     sg.Text('Скорость:'),
     sg.Slider(range=(1, 10), orientation='h', size=(10, 15), key='-SPEED-', default_value=5, enable_events=True),
     sg.Button('Старт/Пауза', key='-PLAY-'),
     sg.Button('Сброс', key='-RESET-')],
    [sg.Graph(canvas_size=(600, 400), graph_bottom_left=(0, 0), graph_top_right=(600, 400), key='-MAP-',
              enable_events=True, motion_events=True, background_color='white')],
    [sg.Multiline(size=(80, 10), key='-STATS-', disabled=True, autoscroll=True)]
]

window = sg.Window('Экосистема', layout, finalize=True, resizable=True)
graph = window['-MAP-']

# Инициализация мира
world = World(30, 20, plant_density=0.5)
cell_size = 20
colors = {
    'Lumiere': '#FFFF00',  # Жёлтый
    'Obscurite': '#0000FF',  # Синий
    'Demi': '#808080',  # Серый
    'Pauvre': '#FFFF00',  # Жёлтый
    'Malheureux': '#800080'  # Фиолетовый
}
running = False
tick = 0
selected_animal = None
vision_circle_id = None

# Функция для отрисовки карты
def draw_world():
    global vision_circle_id
    graph.erase()
    # Отрисовка сущностей
    for y in range(world.height):
        for x in range(world.width):
            entity = world.grid[y][x]
            if entity and entity.alive:
                if isinstance(entity, (Lumiere, Obscurite, Demi)):
                    # Рисуем квадрат для растений
                    top_left = (x * cell_size, (world.height - y - 1) * cell_size)
                    bottom_right = ((x + 1) * cell_size, (world.height - y) * cell_size)
                    graph.draw_rectangle(top_left, bottom_right,
                                       fill_color=colors[type(entity).__name__], line_color='black', line_width=1)
                elif isinstance(entity, (Pauvre, Malheureux)):
                    # Рисуем круг для животных
                    radius = 8 * entity.scale
                    center = ((x + 0.5) * cell_size, (world.height - y - 0.5) * cell_size)
                    graph.draw_circle(center, radius,
                                    fill_color=colors[type(entity).__name__], line_color='black', line_width=1)
    
    # Отрисовка радиуса обзора для выбранного животного
    if selected_animal and selected_animal.alive:
        x, y = selected_animal.x, selected_animal.y
        vision_pixel_radius = selected_animal.vision_radius * cell_size
        if vision_circle_id:
            graph.delete_figure(vision_circle_id)
        vision_circle_id = graph.draw_circle(
            ((x + 0.5) * cell_size, (world.height - y - 0.5) * cell_size),
            vision_pixel_radius, fill_color=None, line_color='#FF0000', line_width=2
        )

# Функция для обновления статистики
def update_stats():
    stats_text, get_animal_info = get_stats(world)
    animal_info = get_animal_info(selected_animal, world)
    window['-STATS-'].update(stats_text + "\n\n" + animal_info)

# Первоначальная отрисовка и обновление статистики
draw_world()
update_stats()

# Основной цикл
while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break
    
    # Обработка событий
    if event == '-PLAY-':
        running = not running
        window['-PLAY-'].update('Пауза' if running else 'Старт')
    
    if event == '-RESET-':
        world.reset()
        tick = 0
        selected_animal = None
        draw_world()
        update_stats()
    
    if event == '-TIME-':
        time_idx = int(values['-TIME-']) // 6
        world.time_manager.tick = int(values['-TIME-'])
        world.time_manager.time_of_day = world.time_manager.times_of_day[time_idx % len(world.time_manager.times_of_day)]
        world.update()
        draw_world()
        update_stats()
    
    if event == '-MAP-':
        x, y = values['-MAP-']
        grid_x = x // cell_size
        grid_y = world.height - 1 - (y // cell_size)
        if 0 <= grid_x < world.width and 0 <= grid_y < world.height:
            entity = world.grid[grid_y][grid_x]
            selected_animal = entity if isinstance(entity, (Pauvre, Malheureux)) else None
        else:
            selected_animal = None
        draw_world()
        update_stats()
    
    if running:
        speed = int(values['-SPEED-'])
        if tick % (11 - speed) == 0:
            world.update()
            draw_world()
            update_stats()
        tick += 1

window.close()