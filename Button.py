import pygame

if not pygame.font.get_init():
    pygame.font.init()

font = pygame.font.Font(None, 40)

class Button:
    def __init__(self, text, x, y, width, height, bg_color, text_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=10)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.action:
                    self.action()

    def is_hovered(self):
        # Retourne True si la souris est au-dessus du bouton
        return self.rect.collidepoint(pygame.mouse.get_pos())
