# Example file showing a circle moving on screen
import pygame
from Planet import PlanetRenderer, SolarSystem, COLORS,PlanetManager

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
renderer = PlanetRenderer(screen)
solarSystem = SolarSystem((screen.get_width()/2, screen.get_height()/2), 8)
running = True
dt = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    solarSystem.update(dt)

    screen.fill(COLORS["background"])
    renderer.draw(solarSystem)
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
