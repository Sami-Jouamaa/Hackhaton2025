import pygame
from Button import Button

FONT = pygame.font.Font(None, 32)
TITLE_FONT = pygame.font.Font(None, 40)


class CompanyMenu:
    def __init__(self, company_data):
        self.company_data = company_data
        self.running = True
        self.selected_section = "informations"

    def set_section(self, section):
        self.selected_section = section

    def close(self):
        self.running = False

    def run(self, screen):
        clock = pygame.time.Clock()
        screen_width, screen_height = screen.get_width(), screen.get_height()

        panel_width = 1000
        panel_height = 700
        panel_x = (screen_width - panel_width) // 2
        panel_y = (screen_height - panel_height) // 2

        border_thickness = 10

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
                           (100, 100, 100), (255, 255, 255),
                           action=lambda: self.set_section("informations"))
        sidebar_buttons.append(btn_infos)
        btn_y += btn_height + btn_spacing

        btn_contrats = Button("Contrats", btn_x, btn_y, sidebar_width - 40, btn_height,
                              (100, 100, 100), (255, 255, 255),
                              action=lambda: self.set_section("contrats"))
        sidebar_buttons.append(btn_contrats)
        btn_y += btn_height + btn_spacing

        btn_inventaire = Button("Inventaire", btn_x, btn_y, sidebar_width - 40, btn_height,
                                (100, 100, 100), (255, 255, 255),
                                action=lambda: self.set_section("inventaire"))
        sidebar_buttons.append(btn_inventaire)
        btn_y += btn_height + btn_spacing

        btn_trade_routes = Button("Trade Routes", btn_x, btn_y, sidebar_width - 40, btn_height,
                                  (100, 100, 100), (255, 255, 255),
                                  action=lambda: self.set_section("trade_routes"))
        sidebar_buttons.append(btn_trade_routes)
        btn_y += btn_height + btn_spacing

        btn_technologies = Button("Technologies", btn_x, btn_y, sidebar_width - 40, btn_height,
                                  (100, 100, 100), (255, 255, 255),
                                  action=lambda: self.set_section("technologies"))
        sidebar_buttons.append(btn_technologies)
        btn_y += btn_height + btn_spacing

        close_button = Button("X",
                              panel_x + panel_width - border_thickness,
                              panel_y,
                              border_thickness, border_thickness,
                              (255, 0, 0), (255, 255, 255),
                              action=self.close)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                for button in sidebar_buttons:
                    button.is_clicked(event)
                close_button.is_clicked(event)

            overlay = pygame.Surface((screen_width, screen_height))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
            pygame.draw.rect(screen, (50, 50, 50), panel_rect)
            pygame.draw.rect(screen, (255, 255, 255), panel_rect, border_thickness)

            close_button.draw(screen)

            profit_text = TITLE_FONT.render(f"Profit: {self.company_data.get('profit', 0)} GLD", True, (255, 215, 0))
            profit_rect = profit_text.get_rect(center=(panel_x + panel_width // 2, panel_y + 30))
            screen.blit(profit_text, profit_rect)

            sidebar_rect = pygame.Rect(sidebar_x, sidebar_y, sidebar_width, sidebar_height)
            pygame.draw.rect(screen, (70, 70, 70), sidebar_rect)

            for button in sidebar_buttons:
                button.draw(screen)

            content_rect = pygame.Rect(content_x, content_y, content_width, content_height)
            pygame.draw.rect(screen, (80, 80, 80), content_rect)

            content_surface = pygame.Surface((content_width, content_height))
            content_surface.fill((80, 80, 80))
            content_margin = 20
            text_y = content_margin

            if self.selected_section == "informations":
                title = FONT.render("Informations Générales", True, (255, 255, 255))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                profit_line = FONT.render(f"Profit: {self.company_data.get('profit', 0)} GLD", True, (200, 200, 200))
                content_surface.blit(profit_line, (content_margin, text_y))
                text_y += profit_line.get_height() + 5
                employes = self.company_data.get("employes", "N/A")
                employes_line = FONT.render(f"Employés: {employes}", True, (200, 200, 200))
                content_surface.blit(employes_line, (content_margin, text_y))
                text_y += employes_line.get_height() + 5
                resources = self.company_data.get("resources", {})
                for res, qty in resources.items():
                    res_line = FONT.render(f"{res}: {qty} tonnes galactiques", True, (200, 200, 200))
                    content_surface.blit(res_line, (content_margin, text_y))
                    text_y += res_line.get_height() + 5

            elif self.selected_section == "contrats":
                title = FONT.render("Contrats", True, (255, 255, 255))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                for contrat in self.company_data.get("contrats", []):
                    line = FONT.render(f"- {contrat}", True, (200, 200, 200))
                    content_surface.blit(line, (content_margin, text_y))
                    text_y += line.get_height() + 5

            elif self.selected_section == "inventaire":
                title = FONT.render("Inventaire", True, (255, 255, 255))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                ressources_title = FONT.render("Ressources:", True, (255, 255, 255))
                content_surface.blit(ressources_title, (content_margin, text_y))
                text_y += ressources_title.get_height() + 5
                for res in self.company_data.get("inventaire", {}).get("ressources", []):
                    line = FONT.render(f"- {res}", True, (200, 200, 200))
                    content_surface.blit(line, (content_margin + 20, text_y))
                    text_y += line.get_height() + 5
                text_y += 10
                equipement_title = FONT.render("Équipement:", True, (255, 255, 255))
                content_surface.blit(equipement_title, (content_margin, text_y))
                text_y += equipement_title.get_height() + 5
                for eq in self.company_data.get("inventaire", {}).get("equipement", []):
                    line = FONT.render(f"- {eq}", True, (200, 200, 200))
                    content_surface.blit(line, (content_margin + 20, text_y))
                    text_y += line.get_height() + 5

            elif self.selected_section == "trade_routes":
                title = FONT.render("Trade Routes", True, (255, 255, 255))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                for route in self.company_data.get("trade_routes", []):
                    line = FONT.render(f"- {route}", True, (200, 200, 200))
                    content_surface.blit(line, (content_margin, text_y))
                    text_y += line.get_height() + 5

            elif self.selected_section == "technologies":
                title = FONT.render("Technologies", True, (255, 255, 255))
                content_surface.blit(title, (content_margin, text_y))
                text_y += title.get_height() + 10
                for tech in self.company_data.get("technologies", []):
                    line = FONT.render(f"- {tech}", True, (200, 200, 200))
                    content_surface.blit(line, (content_margin, text_y))
                    text_y += line.get_height() + 5

            screen.blit(content_surface, (content_x, content_y))

            pygame.display.flip()
            clock.tick(30)

