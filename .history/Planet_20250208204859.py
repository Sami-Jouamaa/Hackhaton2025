import pygame
import math
import random
import pygame.gfxdraw
from pygame.locals import *

# --- Couleurs ---
COLORS = {
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
            self.radius = 20
            
        elif self.type == "gas":
            self.resources = {
                "hydrogen": random.randint(1000, 2000),
                "methane": random.randint(500, 1500),
                "helium": random.randint(300, 800)
            }
            self.radius = 27
            
        elif self.type == "dead":
            self.resources = {
                "iron": random.randint(1000, 3000),
                "copper": random.randint(500, 1000),
                "gold": random.randint(100, 300),
                "plutonium": random.randint(50, 150)
            }
            self.radius = 16

    def update_orbit(self, center, dt):
        self.angle += self.orbit_speed * dt
        x = center[0] + math.cos(self.angle) * self.orbit_radius
        y = center[1] + math.sin(self.angle) * self.orbit_radius
        self.pos = (int(x), int(y))

# --- Système Solaire ---
class SolarSystem:
    def __init__(self, center):
        self.center = center
        self.planets = []
        self.star_radius = 32
                
        #Planet  6
        p_type = "morte"
        orbit_r = 75 + 0 * 50
        orbit_speed = 0.32/(0 + 1)
        planet = Planet(f"Infernis", p_type, orbit_r, orbit_speed)
        planet.radius = 19
        planet.color = "./planet-pic/Infernis.png"
        self.planets.append(planet)
        
        #Planet 3
        p_type = "vie"
        orbit_r = 75 + 1 * 50
        orbit_speed = 0.32/(1 + 1)
        planet = Planet(f"Terre", p_type, orbit_r, orbit_speed)
        planet.radius = 15
        planet.color = "./planet-pic/Terre.png"
        self.planets.append(planet)
        
        #Planet 4
        p_type = "vie"
        orbit_r = 75 + 2 * 50
        orbit_speed = 0.32/(2 + 1)
        planet = Planet(f"Terralis Prime", p_type, orbit_r, orbit_speed)
        planet.radius = 19
        planet.color = "./planet-pic/Terralis_Prime.png"
        self.planets.append(planet)

        #Planet 2
        p_type = "morte"
        orbit_r = 75 + 3 * 50
        orbit_speed = 0.32/(3 + 1)
        planet = Planet(f"Nekronia", p_type, orbit_r, orbit_speed)
        planet.radius = 15
        planet.color = "./planet-pic/Nekronia.png"
        self.planets.append(planet)
        
        # Planet 1
        p_type = "morte"
        orbit_r = 75 + 4 * 50
        orbit_speed = 0.32/(4 + 1)
        planet = Planet(f"Chloria", p_type, orbit_r, orbit_speed)
        planet.radius = 15
        planet.color = "./planet-pic/Chloria.png"
        self.planets.append(planet)
        
        #Planet 6
        p_type = "vie"
        orbit_r = 75 + 5 * 50
        orbit_speed = 0.32/(5 + 1)
        planet = Planet(f"Atlantis", p_type, orbit_r, orbit_speed)
        planet.radius = 22
        planet.color = "./planet-pic/Atlantis.png"
        self.planets.append(planet)
        
        #Planet 5
        p_type = "gas"
        orbit_r = 75 + 6 * 50
        orbit_speed = 0.32/7
        planet = Planet(f"Xenon Prime", p_type, orbit_r, orbit_speed)
        planet.radius = 30
        planet.color = "./planet-pic/Xenon_Prime.png"
        self.planets.append(planet)
        
        #Planet 8
        p_type = "vie"
        orbit_r = 75 + 7 * 50
        orbit_speed = 0.32/8
        planet = Planet(f"Cryogenia", p_type, orbit_r, orbit_speed)
        planet.radius = 13
        planet.color = "./planet-pic/Cryogenia.png"
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
        image = pygame.image.load("./planet-pic/sunTexture.jpg")
        star_surface = pygame.Surface((solar_system.star_radius * 2, solar_system.star_radius*2), pygame.SRCALPHA)
        scaled_image = pygame.transform.scale(image, (solar_system.star_radius*2, solar_system.star_radius*2))
        star_surface.blit(scaled_image, (0,0))
        
        mask = pygame.Surface((solar_system.star_radius*2, solar_system.star_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255), (solar_system.star_radius, solar_system.star_radius), solar_system.star_radius)
        star_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        self.screen.blit(star_surface, (solar_system.center[0] - solar_system.star_radius, solar_system.center[1] - solar_system.star_radius))
        
        # Dessiner les orbites
        for planet in solar_system.planets:
            rect = (solar_system.center[0] - planet.orbit_radius,
                    solar_system.center[1] - planet.orbit_radius,
                    planet.orbit_radius*2, planet.orbit_radius*2)
            pygame.draw.ellipse(self.screen, (80, 80, 80), rect, 1)
        
        # Dessiner les planètes
        for planet in solar_system.planets:
            image = pygame.image.load(planet.color)
            planet_surface = pygame.Surface((planet.radius * 2, planet.radius*2), pygame.SRCALPHA)
            scaled_image = pygame.transform.scale(image, (planet.radius * 2, planet.radius*2))
            planet_surface.blit(scaled_image, (0, 0))
            
            mask = pygame.Surface((planet.radius * 2, planet.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(mask, (255, 255, 255), (planet.radius, planet.radius), planet.radius)
            planet_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            self.screen.blit(planet_surface, (planet.pos[0] - planet.radius, planet.pos[1] - planet.radius))
            
            # pygame.draw.circle(self.screen, planet.color, planet.pos, planet.radius)
            # Info-bulle
            text = self.font.render(f"{planet.name} ({planet.type})", True, (255, 255, 255))
            self.screen.blit(text, (planet.pos[0]+20, planet.pos[1]-10))