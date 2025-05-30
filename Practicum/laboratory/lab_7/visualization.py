import pygame
import platform
import asyncio
from world import World

async def main():
    pygame.init()
    cell_size = 20
    width, height = 40, 20
    screen_width = cell_size * width
    screen_height = cell_size * height + 100  # Extra space for legend
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Ecosystem Simulation")
    
    world = World(width, height)
    colors = {
        'Lumiere': (0, 255, 0),    # Green
        'Obscurite': (0, 0, 255),  # Blue
        'Demi': (128, 0, 128),     # Purple
        'Pauvre': (255, 255, 0),   # Yellow
        'Malheureux': (255, 0, 0), # Red
        'Background': (255, 255, 255)  # White
    }
    
    font = pygame.font.SysFont('arial', 16)
    clock = pygame.time.Clock()
    FPS = 100
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        world.update()
        screen.fill(colors['Background'])
        
        for y in range(world.height):
            for x in range(world.width):
                entity = world.grid[y][x]
                if entity:
                    color = colors[type(entity).__name__]
                    pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))
        
        legend_y = world.height * cell_size + 20
        legend_items = [
            ("Lumiere (Sun)", colors['Lumiere']),
            ("Obscurite (Moon)", colors['Obscurite']),
            ("Demi (Dawn/Dusk)", colors['Demi']),
            ("Pauvre (Herbivore)", colors['Pauvre']),
            ("Malheureux (Omnivore)", colors['Malheureux'])
        ]
        for i, (text, color) in enumerate(legend_items):
            pygame.draw.rect(screen, color, (10 + i * 120, legend_y, 20, 20))
            label = font.render(text, True, (0, 0, 0))
            screen.blit(label, (40 + i * 120, legend_y))
        
        time_text = font.render(f"Time: {world.time_manager.time_of_day}", True, (0, 0, 0))
        screen.blit(time_text, (10, legend_y + 40))
        
        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)
    
    pygame.quit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())