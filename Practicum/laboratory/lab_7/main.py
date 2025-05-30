from world.time import Time
from world.world import World
from visualization.render import Renderer

if __name__ == "__main__":
    time = Time()
    world = World(width=15, height=10)
    renderer = Renderer(width=15, height=10)

    running = True
    while running:
        current_time = time.get_time()
        print(f"\n=== {current_time.upper()} ===")
        world.update(current_time)
        renderer.render(world.grid)

        running = renderer.handle_events()

        time.advance()

    renderer.quit()
