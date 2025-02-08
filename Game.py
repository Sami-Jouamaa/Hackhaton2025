import pygame
from Planet import PlanetRenderer, SolarSystem, COLORS, PlanetManager
from Button import Button
from Company import CompanyMenu

pygame.init()
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


def quit_game():
    global running
    running = False


def open_company_menu():
    menu = CompanyMenu(company_data)
    menu.run(screen)


quit_button = Button("Quitter", 1520, 125, 200, 60, RED, BLACK, quit_game)
company_button = Button("Compagnie", 200, 900, 200, 60, WHITE, BLACK, open_company_menu)
company_data = {
    "profit": 100000,
    "employes" : 10,
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

def open_company_menu():
    menu = CompanyMenu(company_data)
    menu.run(screen, background_draw_func=lambda: renderer.draw(solarSystem))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        quit_button.is_clicked(event)
        company_button.is_clicked(event)

    solarSystem.update(dt)
    screen.fill(COLORS["background"])
    renderer.draw(solarSystem)
    draw_overlay()
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
