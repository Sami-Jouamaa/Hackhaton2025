import pygame
from Button import Button


FONT = pygame.font.Font(None, 32)
TITLE_FONT = pygame.font.Font(None, 40)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
NAV_ACTIVE = (135, 206, 250)  # bleu ciel
NAV_INACTIVE = LIGHT_GRAY

def wrap_text(text, font, max_width):
    lines = []

    paragraphs = text.split("\n")
    for paragraph in paragraphs:
        words = paragraph.split(" ")
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    return lines

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
        self.current_view = "description"

    def close(self):
        self.running = False

    def set_view(self, view_key):
        self.current_view = view_key

    #def export_prompt(self, target):


    def extract_resources_periodically(self, solar_system):
        """ Runs every 5 seconds: Loops through planets, adding resources based on extractors. """
        for planet in solar_system.planets:
            if "extractor" in planet.buildings:
                for resource, num_extractors in planet.buildings["extractor"].items():
                    if num_extractors > 0:
                        planet.inventory[resource] = planet.inventory.get(resource, 0) + num_extractors
                        print(
                            f"✅ Added {num_extractors} {resource} to {planet.name}. New total: {planet.inventory[resource]}")

    def run(self, screen, planet, solar_system, background_draw_func=None):
        export_buttons = []
        clock = pygame.time.Clock()
        screen_width, screen_height = screen.get_width(), screen.get_height()
        RESOURCE_EXTRACTION_EVENT = pygame.USEREVENT + 1

        modal_width = 800
        modal_height = 600
        modal_x = (screen_width - modal_width) // 2
        modal_y = (screen_height - modal_height) // 2

        left_width = int(modal_width * 0.30)
        right_width = modal_width - left_width

        image_height = int(modal_height * 0.50)
        content_height = modal_height - image_height

        close_button_size = 40
        margin = 10
        close_button = CloseButton("X",
                                     modal_x + modal_width - close_button_size - margin,
                                     modal_y + margin,
                                     close_button_size, close_button_size,
                                     RED, WHITE,
                                     action=self.close)

        data = self.planet_data
        if len(data) >= 8:
            name = str(data[0])
            type_info = str(data[4])
            summary = str(data[5])
            image_path = data[6]
            detailed_desc = str(data[7])
        else:
            name = "Unknown"
            type_info = "Unknown"
            summary = ""
            image_path = ""
            detailed_desc = ""

        extra = {}
        if len(data) >= 9 and isinstance(data[8], dict):
            extra = data[8]

        nav_options = [("Description", "description"),
                       ("Contrats", "contrats"),
                       ("Colonie", "colonie"),
                       ("Inventaire", "inventaire"),
                       ("Export", "export"),]
        if type_info.lower() == "vie":
            nav_options.insert(1, ("Lois/Taxes", "lois"))
            nav_options.append(("Marché", "marche"))


        view_contents = {}
        view_contents["description"] = detailed_desc
        view_contents["contrats"] = extra.get("contrats", "Aucun contrat disponible.")
        colonies = extra.get("colonies", [])
        if colonies:
            view_contents["colonie"] = "Colonies:\n" + "\n".join(colonies)
        else:
            view_contents["colonie"] = "Aucune colonie."
        view_contents["inventaire"] = "\n".join(f"{key}: {value} tonnes galactiques" for key, value in planet.inventory.items())
        view_contents["lois"] = extra.get("lois", "Aucune loi disponible.")
        view_contents["marché"] = extra.get("marché", "Aucun marché disponible.")
        view_contents["export"] = "Sélectionnez une planète pour exporter des ressources."

        nav_buttons = []
        left_margin = 10
        info_lines = [
            "Nom: " + name,
            "Type: " + type_info
        ]
        y_info = modal_y + 10
        for line in info_lines:
            y_info += FONT.render(line, True, BLACK).get_height() + 5
        wrap_max_width = left_width - 2 * left_margin
        wrapped_summary = wrap_text(summary, FONT, wrap_max_width)
        for line in wrapped_summary:
            y_info += FONT.render(line, True, BLACK).get_height() + 5

        y_nav = y_info + 10
        nav_button_height = 40
        nav_button_spacing = 5
        for (label, view_key) in nav_options:
            btn = Button(label, modal_x + left_margin, y_nav, left_width - 2 * left_margin, nav_button_height,
                         NAV_ACTIVE if self.current_view == view_key else NAV_INACTIVE,
                         BLACK,
                         action=lambda vk=view_key: self.set_view(vk))
            nav_buttons.append(btn)
            y_nav += nav_button_height + nav_button_spacing

        while self.running:
            for event in pygame.event.get():
                if event.type == RESOURCE_EXTRACTION_EVENT:
                    self.extract_resources_periodically(solar_system)

            if background_draw_func:
                background_draw_func()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                close_button.is_clicked(event)
                for btn in nav_buttons:
                    btn.is_clicked(event)
                for btn in export_buttons:
                    btn.is_clicked(event)

            modal_rect = pygame.Rect(modal_x, modal_y, modal_width, modal_height)
            pygame.draw.rect(screen, WHITE, modal_rect)
            pygame.draw.rect(screen, BLACK, modal_rect, 2)
            close_button.draw(screen)

            left_rect = pygame.Rect(modal_x, modal_y, left_width, modal_height)
            pygame.draw.rect(screen, LIGHT_GRAY, left_rect)
            y_draw = modal_y + 10
            for line in info_lines:
                line_surface = FONT.render(line, True, BLACK)
                screen.blit(line_surface, (modal_x + left_margin, y_draw))
                y_draw += line_surface.get_height() + 5
            for line in wrapped_summary:
                line_surface = FONT.render(line, True, BLACK)
                screen.blit(line_surface, (modal_x + left_margin, y_draw))
                y_draw += line_surface.get_height() + 5
            for btn in nav_buttons:
                btn.bg_color = NAV_ACTIVE if btn.text.lower() in self.current_view.lower() or (btn.text.lower() == "description" and self.current_view=="description") else NAV_INACTIVE
                btn.draw(screen)

            image_rect = pygame.Rect(modal_x + left_width, modal_y, right_width, image_height)
            pygame.draw.rect(screen, BLACK, image_rect, 2)
            content_rect = pygame.Rect(modal_x + left_width, modal_y + image_height, right_width, content_height)
            pygame.draw.rect(screen, BLACK, content_rect, 2)

            # Charger et afficher l'image
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

            content_text = view_contents.get(self.current_view, "")
            content_surface = pygame.Surface((right_width, content_height))
            content_surface.fill(WHITE)
            wrapped_content = wrap_text(view_contents.get(self.current_view, ""), FONT, right_width - 20)
            y_content = 10
            for line in wrapped_content:
                line_surface = FONT.render(line, True, BLACK)
                content_surface.blit(line_surface, (10, y_content))
                y_content += line_surface.get_height() + 5
            if self.current_view == "export":
                for target_planet in solar_system.planets:
                    if target_planet != planet:  # Exclude the current planet
                        btn = Button(target_planet.name, modal_x + left_width + 20, y_content + image_height,
                                     right_width - 40, 40, NAV_ACTIVE, BLACK,
                                     action=lambda p=target_planet: print(
                                         f"Selected {p.name} for export"))  # Placeholder action
                        export_buttons.append(btn)
                        y_content += 50

            screen.blit(content_surface, (modal_x + left_width, modal_y + image_height))
            if self.current_view == "export":
                for btn in export_buttons:
                    btn.draw(screen)
            pygame.display.flip()
            clock.tick(30)
