# Example file showing a circle moving on screen
import pygame

from Planet import PlanetRenderer, SolarSystem, COLORS,PlanetManager

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
renderer = PlanetRenderer(screen)
solarSystem = SolarSystem((screen.get_width()/2, screen.get_height()/2))
running = True
selected_planet = None
dt = 0
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)

from Button import Button

def nothing():
    pass

def quit_game():
    global running
    running = False

quit_button = Button("Quitter", 1520, 125, 200, 60, RED, BLACK, quit_game)
company_button = Button("Compagnie", 200, 900, 200, 60, WHITE, BLACK, nothing)
#planet_button = Button(selected_planet, 200, 900, 200, 60, WHITE, BLACK, nothing)

def draw_overlay():
    overlay = pygame.Surface((1920, 1080))
    overlay.set_alpha(180)
    overlay.fill(DARK_GRAY)
    screen.blit(overlay, (0, 0))
    quit_button.draw(screen)
    company_button.draw(screen)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

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

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
