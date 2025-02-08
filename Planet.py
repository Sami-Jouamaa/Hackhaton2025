import pygame
import math
import random
import pygame.gfxdraw
from pygame.locals import *

# --- Couleurs ---
# COLORS = {
#     "life": "lifeTexture.jpg",
#     "gas": "lifeTexture.jpg",
#     "dead": "lifeTexture.jpg",
#     "star": "lifeTexture.jpg",
#     "background": (0, 0, 40)
# }
COLORS = {
    "life": (34, 139, 34),
    "gas": (255, 165, 0),
    "dead": (139, 137, 137),
    "star": (255, 255, 0),
    "background": (0, 0, 40)
}


# --- Classe de Base Planète ---
class Planet:
    def __init__(self, name, planet_type, orbit_radius, orbit_speed):
        self.name = name
        self.type = planet_type
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.angle = random.uniform(0, 2*math.pi)
        self.resources = {}
        self.pollution = {"CO2": 0, "radiation": 0, "waste": 0}
        self.pos = (0, 0)
        
        # Définition des ressources par type
        if self.type == "life":
            self.resources = {
                "water": random.randint(500, 1000),
                "oxygen": random.randint(800, 1200),
                "petrol": random.randint(200, 500),
                "wood": random.randint(300, 700)
            }
            self.color = COLORS["life"]
            self.radius = 20
            
        elif self.type == "gas":
            self.resources = {
                "hydrogen": random.randint(1000, 2000),
                "methane": random.randint(500, 1500),
                "helium": random.randint(300, 800)
            }
            self.color = COLORS["gas"]
            self.radius = 27
            
        elif self.type == "dead":
            self.resources = {
                "iron": random.randint(1000, 3000),
                "copper": random.randint(500, 1000),
                "gold": random.randint(100, 300),
                "plutonium": random.randint(50, 150)
            }
            self.color = COLORS["dead"]
            self.radius = 16

    def update_orbit(self, center, dt):
        self.angle += self.orbit_speed * dt
        x = center[0] + math.cos(self.angle) * self.orbit_radius
        y = center[1] + math.sin(self.angle) * self.orbit_radius
        self.pos = (int(x), int(y))

# --- Système Solaire ---
class SolarSystem:
    def __init__(self, center, num_planets):
        self.center = center
        self.planets = []
        self.star_radius = 32
                
        # Génération procédurale de planètes
        planet_types = ["life", "gas", "dead"]
        for i in range(num_planets):
            p_type = random.choice(planet_types)
            orbit_r = 75 + i*50  # Distance orbitale
            orbit_speed = 0.32 / (i+1)  # Plus lent avec la distance
            planet = Planet(f"Planet {i+1}", p_type, orbit_r, orbit_speed)
            self.planets.append(planet)

    def update(self, dt):
        for planet in self.planets:
            planet.update_orbit(self.center, dt)

# --- Gestion des Ressources et Pollution ---
class PlanetManager:
    @staticmethod
    def extract_resources(planet, resource_type, amount):
        if planet.resources.get(resource_type, 0) >= amount:
            planet.resources[resource_type] -= amount
            # Génère pollution
            if resource_type in ["petrol", "plutonium"]:
                planet.pollution["CO2"] += amount * 0.1
                planet.pollution["radiation"] += amount * 0.05
            return amount
        return 0

    @staticmethod
    def simulate_pollution(planet):
        # Simulation simplifiée de la diffusion
        if planet.type == "life":
            planet.pollution["CO2"] *= 0.95  # Absorption naturelle
        elif planet.type == "dead":
            planet.pollution["radiation"] *= 1.05  # Accumulation

# --- Affichage Pygame ---
class PlanetRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)

    def draw(self, solar_system):
        # Dessiner l'étoile
        pygame.gfxdraw.filled_circle(
            self.screen,  
            int(solar_system.center[0]),
            int(solar_system.center[1]), 
            int(solar_system.star_radius),
            COLORS["star"]
            )
        # pygame.draw.circle(self.screen, COLORS["star"], 
        #                   solar_system.center, solar_system.star_radius)
        
        # Dessiner les orbites
        for planet in solar_system.planets:
            rect = (solar_system.center[0] - planet.orbit_radius,
                    solar_system.center[1] - planet.orbit_radius,
                    planet.orbit_radius*2, planet.orbit_radius*2)
            pygame.draw.ellipse(self.screen, (80, 80, 80), rect, 1)
        
        # Dessiner les planètes
        for planet in solar_system.planets:
            # pygame.gfxdraw.filled_circle(self.screen, planet.pos.x, planet.pos.y, planet.radius, texture, 0, 0)
            pygame.draw.circle(self.screen, planet.color, planet.pos, planet.radius)
            
            # Info-bulle
            text = self.font.render(f"{planet.name} ({planet.type})", True, (255, 255, 255))
            self.screen.blit(text, (planet.pos[0]+20, planet.pos[1]-10))