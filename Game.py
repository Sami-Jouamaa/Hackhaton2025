import pygame
from Planet import PlanetRenderer, SolarSystem, COLORS, PlanetManager
from Button import Button
from Company import CompanyMenu
from ListPlanets import planetList
from PlanetInfo import PlanetInfo
from CompanyLogic import company
import math
import shared

pygame.init()
pygame.font.init()
game_font = pygame.font.SysFont('Comic Sans MS', 24)
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
renderer = PlanetRenderer(screen)
solarSystem = SolarSystem((screen.get_width() / 2, screen.get_height() / 2))
running = True
dt = 0
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
planet_button_hidden = True
selected_planet = None


RESOURCE_EXTRACTION_EVENT = pygame.USEREVENT + 1  
pygame.time.set_timer(RESOURCE_EXTRACTION_EVENT, 5000)  # 5000ms = 5s

def showPlanetInfo():
    i = 0
    for elements in planetList[str(index)]:
        text = str(elements)
        text_surface = game_font.render(text, False, (255, 255, 255))
        screen.blit(text_surface, (960, 540))
        i += 1
    planet_info = planetList[str(index)]
    planet = solarSystem.planets[index]
    ui = PlanetInfo(planet_info)
    ui.run(screen, planet, solarSystem, background_draw_func=lambda: renderer.draw(solarSystem))


def quit_game():
    global running
    running = False


def open_company_menu():
    menu = CompanyMenu(company)
    menu.run(screen, solarSystem, background_draw_func=lambda: renderer.draw(solarSystem))


quit_button = Button("Quitter", 1520, 125, 200, 60, RED, BLACK, quit_game)
company_button = Button("Compagnie", 200, 900, 200, 60, WHITE, BLACK, open_company_menu)
planet_button = Button(f"{'Planete'}", 1520, 900, 200, 60, WHITE, BLACK, showPlanetInfo)


def draw_overlay():
    overlay = pygame.Surface((1920, 1080))
    overlay.set_alpha(0)
    screen.blit(overlay, (0, 0))
    quit_button.draw(screen)
    company_button.draw(screen)
    if not planet_button_hidden:
        planet_button.draw(screen)

def extract_resources_periodically(solar_system):
    for planet in solar_system.planets:
        if "extractor" in planet.buildings:
            for resource, num_extractors in planet.buildings["extractor"].items():
                if num_extractors > 0:
                    planet.inventory[resource] = planet.inventory.get(resource, 0) + num_extractors
                    print(f"✅ Added {num_extractors} {resource} to {planet.name}. New total: {planet.inventory[resource]}")
 
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == RESOURCE_EXTRACTION_EVENT:
            extract_resources_periodically(solarSystem)

        if not shared.export_done:
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_BACKSPACE:
                    shared.qty_input = shared.qty_input[:-1]
                elif event.key == pygame.K_RETURN:
                    shared.export_done = True
                elif pygame.K_0 <= event.key <= pygame.K_9:
                    shared.qty_input += event.unicode
                elif pygame.K_a <= event.key <= pygame.K_z:
                    shared.resType_input += event.unicode
        quit_button.is_clicked(event)
        company_button.is_clicked(event)
        planet_button.is_clicked(event)

    # Handle button hover to change cursor
    hovered = (quit_button.is_hovered() or
               company_button.is_hovered() or
               (not planet_button_hidden and planet_button.is_hovered()))

    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if hovered else pygame.SYSTEM_CURSOR_ARROW)

    # Handle planet selection
    if pygame.mouse.get_pressed()[0]:
        mouseX, mouseY = pygame.mouse.get_pos()
        global index
        index = 0
        for planets in solarSystem.planets:
            distX = (mouseX - planets.pos[0]) ** 2
            distY = (mouseY - planets.pos[1]) ** 2
            if math.sqrt(distX + distY) < 100 or planet_button.rect.collidepoint(mouseX, mouseY):
                selected_planet = planets
                planet_button_hidden = False
                break
            else:
                planet_button_hidden = True
                selected_planet = None
            index += 1

    solarSystem.update(dt)

    image = pygame.image.load("background.jpg")
    background_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    scaled_image = pygame.transform.scale(image, (screen.get_width(), screen.get_height()))
    background_surface.blit(scaled_image, (0, 0))

    mask = pygame.Surface((1920, 1080), pygame.SRCALPHA)
    pygame.draw.circle(mask, (255, 255, 255), (960, 540), screen.get_width())
    background_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(background_surface, (0, 0))

    renderer.draw(solarSystem)
    draw_overlay()
    pygame.display.flip()
    
    dt = clock.tick(60) / 1000

pygame.quit()
