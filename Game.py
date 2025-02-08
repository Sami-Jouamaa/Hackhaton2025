import pygame
from Planet import PlanetRenderer, SolarSystem, COLORS, PlanetManager
from Button import Button
from Company import CompanyMenu
from ListPlanets import planetList
import math

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

def showPlanetInfo():
    i = 0
    for elements in planetList[str(index)]:
        text = str(elements)
        text_surface = game_font.render(text, False, (255, 255, 255))
        screen.blit(text_surface, (960, 540))
        i += 1

def quit_game():
    global running
    running = False

def nothing():
    pass

# Définition unique de open_company_menu (avec background_draw_func)
def open_company_menu():
    menu = CompanyMenu(company_data)
    menu.run(screen, background_draw_func=lambda: renderer.draw(solarSystem))

# Créez le bouton "Quitter"
quit_button = Button("Quitter", 1520, 125, 200, 60, RED, BLACK, quit_game)
# IMPORTANT : Attribuez open_company_menu au bouton "Compagnie"
company_button = Button("Compagnie", 200, 900, 200, 60, WHITE, BLACK, open_company_menu)
planet_button = Button("Planete", 1520, 900, 200, 60, WHITE, BLACK, showPlanetInfo)

company_data = {
    "profit": 100000,
    "employes": 10,
    "contrats": ["Contrat d'extraction", "Contrat de minage", "Contrat d'expedition"],
    "trade_routes": ["Terre -> Cholria", "Cryogenia -> Infernus"],
    "technologies": ["Propulseur nucleaire", "Voile spatiale"],
    "inventaire": {
        "ressources": ["Eau", "Fer", "Carburant"],
        "equipement": ["Fusée", "Satellite"]
    }
}

def draw_overlay():
    overlay = pygame.Surface((1920, 1080))
    overlay.set_alpha(0)
    screen.blit(overlay, (0, 0))
    quit_button.draw(screen)
    company_button.draw(screen)
    if not planet_button_hidden:
        planet_button.draw(screen)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        quit_button.is_clicked(event)
        company_button.is_clicked(event)
        planet_button.is_clicked(event)

    if pygame.mouse.get_pressed()[0]:
        mouseX, mouseY = pygame.mouse.get_pos()
        global index
        index = 0
        for planets in solarSystem.planets:
            distX = (mouseX - planets.pos[0]) ** 2
            distY = (mouseY - planets.pos[1]) ** 2
            if math.sqrt(distX + distY) < 100:
                planet_button_hidden = False
                break
            else:
                planet_button_hidden = True
            index += 1

    solarSystem.update(dt)
    screen.fill(COLORS["background"])
    renderer.draw(solarSystem)
    draw_overlay()
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
