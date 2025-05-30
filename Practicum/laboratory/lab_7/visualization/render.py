import pygame

COLORS = {
    "empty": (220, 220, 220),
    "Lumiere": (255, 255, 0),
    "Obscurite": (0, 0, 100),
    "Demi": (150, 150, 150),
    "Pauvre": (0, 255, 0),
    "Malheureux": (255, 0, 0),
}

CELL_SIZE = 40

class Renderer:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width * CELL_SIZE, height * CELL_SIZE + 100))  # Добавим место снизу для легенды
        pygame.display.set_caption("Ecosystem Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)

    def render(self, grid):
        self.screen.fill(COLORS["empty"])
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, COLORS["empty"], rect)

                if cell.plant:
                    if cell.plant.symbol == "L":
                        color = COLORS["Lumiere"]
                    elif cell.plant.symbol == "O":
                        color = COLORS["Obscurite"]
                    elif cell.plant.symbol == "D":
                        color = COLORS["Demi"]
                    pygame.draw.circle(self.screen, color, rect.center, CELL_SIZE // 3)

                if cell.animal:
                    if cell.animal.symbol == "P":
                        color = COLORS["Pauvre"]
                    elif cell.animal.symbol == "M":
                        color = COLORS["Malheureux"]
                    pygame.draw.rect(self.screen, color, rect.inflate(-10, -10))

                pygame.draw.rect(self.screen, (180, 180, 180), rect, 1)

        self.draw_legend()
        pygame.display.flip()
        self.clock.tick(3)  # FPS 3 для медленного обновления

    def draw_legend(self):
        legend_x = 10
        legend_y = self.height * CELL_SIZE + 10  # чуть ниже поля
        box_size = 20
        spacing = 30

        items = [
            ("Lumiere (Растение)", COLORS["Lumiere"]),
            ("Obscurite (Растение)", COLORS["Obscurite"]),
            ("Demi (Растение)", COLORS["Demi"]),
            ("Pauvre (Травоядные)", COLORS["Pauvre"]),
            ("Malheureux (Хищники)", COLORS["Malheureux"]),
        ]

        for i, (label, color) in enumerate(items):
            rect = pygame.Rect(legend_x, legend_y + i * spacing, box_size, box_size)
            pygame.draw.rect(self.screen, color, rect)
            text_surface = self.font.render(label, True, (0, 0, 0))
            self.screen.blit(text_surface, (legend_x + box_size + 10, legend_y + i * spacing))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def quit(self):
        pygame.quit()
