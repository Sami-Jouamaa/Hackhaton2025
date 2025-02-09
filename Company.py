import pygame
from Button import Button
from CompanyLogic import company


FONT = pygame.font.Font(None, 32)
TITLE_FONT = pygame.font.Font(None, 40)

WHITE = (255, 255, 255)
LIGHT_BLUE = (135, 206, 250)  # Bleu ciel
RED = (255, 0, 0)


class CloseButton(Button):
    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text_surface = FONT.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class CompanyMenu:
    def __init__(self, company_data):
        self.company_data = company_data
        self.running = True
        self.selected_section = "informations"

    def set_section(self, section):
        self.selected_section = section

    def close(self):
        self.running = False

    def run(self, screen, background_draw_func=None):
        clock = pygame.time.Clock()
        screen_width, screen_height = screen.get_width(), screen.get_height()

        panel_width = 1000
        panel_height = 700
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2

        sidebar_width = 200
        sidebar_height = panel_height
        sidebar_x = panel_x
        sidebar_y = panel_y

        content_x = panel_x + sidebar_width
        content_y = panel_y
        content_width = panel_width - sidebar_width
        content_height = panel_height

        btn_height = 50
        btn_spacing = 10
        btn_x = sidebar_x + 20
        btn_y = sidebar_y + 60

        sidebar_buttons = []

        btn_infos = Button("Infos", btn_x, btn_y, sidebar_width - 40, btn_height,
                           LIGHT_BLUE, WHITE,
                           action=lambda: self.set_section("informations"))
        sidebar_buttons.append(btn_infos)
        btn_y += btn_height + btn_spacing

        btn_contrats = Button("Contrats", btn_x, btn_y, sidebar_width - 40, btn_height,
                              LIGHT_BLUE, WHITE,
                              action=lambda: self.set_section("contrats"))
        sidebar_buttons.append(btn_contrats)
        btn_y += btn_height + btn_spacing

        btn_inventaire = Button("Inventaire", btn_x, btn_y, sidebar_width - 40, btn_height,
                                LIGHT_BLUE, WHITE,
                                action=lambda: self.set_section("inventaire"))
        sidebar_buttons.append(btn_inventaire)
        btn_y += btn_height + btn_spacing

        btn_trade_routes = Button("Trade Routes", btn_x, btn_y, sidebar_width - 40, btn_height,
                                  LIGHT_BLUE, WHITE,
                                  action=lambda: self.set_section("trade_routes"))
        sidebar_buttons.append(btn_trade_routes)
        btn_y += btn_height + btn_spacing

        btn_technologies = Button("Technologies", btn_x, btn_y, sidebar_width - 40, btn_height,
                                  LIGHT_BLUE, WHITE,
                                  action=lambda: self.set_section("technologies"))
        sidebar_buttons.append(btn_technologies)
        btn_y += btn_height + btn_spacing

        close_button_size = 40
        margin = 10
        close_button = CloseButton("X",
                                   panel_x + panel_width - close_button_size - margin,
                                   panel_y + margin,
                                   close_button_size, close_button_size,
                                   RED, WHITE,
                                   action=self.close)

        while self.running:
            if background_draw_func:
                background_draw_func()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                for button in sidebar_buttons:
                    button.is_clicked(event)
                close_button.is_clicked(event)

            panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            pygame.draw.rect(screen, WHITE, panel_rect)

            profit_text = TITLE_FONT.render(f"Profit: {self.company_data.bank} GLD", True, (255, 215, 0))
            profit_rect = profit_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 30))
            screen.blit(profit_text, profit_rect)

            sidebar_rect = pygame.Rect(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
            pygame.draw.rect(screen, WHITE, sidebar_rect)

            for button in sidebar_buttons:
                button.draw(screen)

            content_rect = pygame.Rect(content_x, content_y, content_width, content_height)
            pygame.draw.rect(screen, WHITE, content_rect)

            content_surface = pygame.Surface((content_width, content_height))
            content_surface.fill(WHITE)
            content_margin = 20
            text_y = content_margin

            if self.selected_section == "informations":
                title = FONT.render("Informations Générales", True, (0, 0, 0))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                profit_line = FONT.render(f"Banque: {"{:,}".format(self.company_data.bank)} M GLD", True, (0, 0, 0))
                content_surface.blit(profit_line, (content_margin, text_y))
                text_y += profit_line.get_height() + 5
                employes = self.company_data.employees
                employes_line = FONT.render(f"Employés: {employes}", True, (0, 0, 0))
                content_surface.blit(employes_line, (content_margin, text_y))
                text_y += employes_line.get_height() + 5
                resources = self.company_data.resources
                for res, qty in resources.items():
                    res_line = FONT.render(f"{res}: {qty} tonnes galactiques", True, (0, 0, 0))
                    content_surface.blit(res_line, (content_margin, text_y))
                    text_y += res_line.get_height() + 5

            elif self.selected_section == "contrats":
                title = FONT.render("Contrats", True, (0, 0, 0))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                for contrat in self.company_data.contrats:
                    line = FONT.render(f"- {contrat}", True, (0, 0, 0))
                    content_surface.blit(line, (content_margin, text_y))
                    text_y += line.get_height() + 5

            elif self.selected_section == "inventaire":
                title = FONT.render("Inventaire", True, (0, 0, 0))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                ressources_title = FONT.render("Ressources:", True, (0, 0, 0))
                content_surface.blit(ressources_title, (content_margin, text_y))
                text_y += ressources_title.get_height() + 5
                for res in self.company_data.resources:
                    line = FONT.render(f"- {res}", True, (0, 0, 0))
                    content_surface.blit(line, (content_margin + 20, text_y))
                    text_y += line.get_height() + 5
                text_y += 10
                equipement_title = FONT.render("Equipement:", True, (0, 0, 0))
                content_surface.blit(equipement_title, (content_margin, text_y))
                text_y += equipement_title.get_height() + 5
                for tech in self.company_data.equipement:
                    line = FONT.render(f"- {eq}", True, (0, 0, 0))
                    content_surface.blit(line, (content_margin + 20, text_y))
                    text_y += line.get_height() + 5

            elif self.selected_section == "trade_routes":
                title = FONT.render("Trade Routes", True, (0, 0, 0))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                for route in self.company_data.trade_routes:
                    line = FONT.render(f"- {route}", True, (0, 0, 0))
                    content_surface.blit(line, (content_margin, text_y))
                    text_y += line.get_height() + 5

            elif self.selected_section == "technologies":
                title = FONT.render("Technologies", True, (0, 0, 0))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                for tech in self.company_data.technologies:
                    line = FONT.render(f"- {tech}", True, (0, 0, 0))
                    content_surface.blit(line, (content_margin, text_y))
                    text_y += line.get_height() + 5

            screen.blit(content_surface, (content_x, content_y))

            close_button.draw(screen)

            pygame.display.flip()
            clock.tick(30)
