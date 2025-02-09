import pygame
from Button import Button

FONT = pygame.font.Font(None, 32)
TITLE_FONT = pygame.font.Font(None, 40)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class CloseButton(Button):
    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)
        text_surface = FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

class PlanetInfo:
    def __init__(self, planet_data):

        self.planet_data = planet_data
        self.running = True

    def close(self):
        self.running = False

    def run(self, screen, background_draw_func=None):
        clock = pygame.time.Clock()
        screen_width, screen_height = screen.get_width(), screen.get_height()

        modal_width = 800
        modal_height = 600
        modal_x = (screen_width - modal_width) // 2
        modal_y = (screen_height - modal_height) // 2

        left_width = int(modal_width * 0.30)
        right_width = modal_width - left_width

        image_height = int(modal_height * 0.50)
        desc_height = modal_height - image_height

        close_button_size = 40
        margin = 10
        close_button = CloseButton("X",
                                     modal_x + modal_width - close_button_size - margin,
                                     modal_y + margin,
                                     close_button_size, close_button_size,
                                     RED, WHITE,
                                     action=self.close)

        data = self.planet_data
        if len(data) >= 7:
            name = str(data[0])
            type_info = str(data[4])
            description = str(data[5])
            image_path = data[6]
        elif len(data) >= 4:
            name = str(data[0])
            type_info = str(data[1])
            description = str(data[2])
            image_path = data[3]
        else:
            name = "Unknown"
            type_info = "Unknown"
            description = ""
            image_path = ""

        while self.running:

            if background_draw_func:
                background_draw_func()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                close_button.is_clicked(event)

            modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
            pygame.draw.rect(screen, WHITE, modal_rect)
            pygame.draw.rect(screen, BLACK, modal_rect, 2)

            close_button.draw(screen)

            left_rect = pygame.Rect(modal_x, modal_y, left_width, modal_height)
            pygame.draw.rect(screen, LIGHT_GRAY, left_rect)
            info_lines = [
                "Nom: " + name,
                "Type: " + type_info
            ]
            left_margin = 10
            y_offset = modal_y + 10
            for line in info_lines:
                line_surface = FONT.render(line, True, BLACK)
                screen.blit(line_surface, (modal_x + left_margin, y_offset))
                y_offset += line_surface.get_height() + 5

            right_rect = pygame.Rect(modal_x + left_width, modal_y, right_width, modal_height)
            image_rect = pygame.Rect(modal_x + left_width, modal_y, right_width, image_height)
            pygame.draw.rect(screen, BLACK, image_rect, 2)
            desc_rect = pygame.Rect(modal_x + left_width, modal_y + image_height, right_width, desc_height)
            pygame.draw.rect(screen, BLACK, desc_rect, 2)

            image = None
            if image_path:
                try:
                    image = pygame.image.load(image_path)
                except Exception as e:
                    image = None

            if image:
                image = pygame.transform.scale(image, (right_width, image_height))
                screen.blit(image, image_rect.topleft)
            else:
                pygame.draw.rect(screen, LIGHT_GRAY, image_rect)
                placeholder = FONT.render("No Image", True, BLACK)
                placeholder_rect = placeholder.get_rect(center=image_rect.center)
                screen.blit(placeholder, placeholder_rect)

            desc_surface = FONT.render(description, True, BLACK)
            screen.blit(desc_surface, (desc_rect.x + 10, desc_rect.y + 10))

            pygame.display.flip()
            clock.tick(30)
