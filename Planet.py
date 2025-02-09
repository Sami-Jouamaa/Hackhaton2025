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
        self.exports = {}  # {dest_planet: {resource: (amount, fuel_cost)}}
        self.imports = {}  # {source_planet: {resource: amount}}
        self.pollution = {"CO2": 0, "radiation": 0, "waste": 0}
        self.pos = (0, 0)
        self.sommaire = ""
        self.description = {}

        self.buildings = {
            "research": 0,  # Station de recherche (1-10)
            "decarbonizer": 0,  # Dépollueur CO2 (0-10)
            "fabricator": 0,  # Usine de production (0-5)
            "extractor": {}  # Dictionnaire des extracteurs {"type": quantité}
        }

        self.inventory = {}

        
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

    def export(self, dest_planet, resource, amount, fuel_cost):
        """ Adds an export from this planet to another """
        if self.resources.get(resource, 0) >= amount and self.resources.get('Fossil_Fuel', 0) > fuel_cost:
            self.resources[resource] -= amount  # Deduct from stock
            self.exports['Fossil_Fuel'] = fuel_cost
            num_dst = dest_planet.inventroy[resource].get(resource, 0)
            amount += num_dst
            dest_planet[resource] = amount



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
        planet.sommaire = "Enfer métallique. Tempêtes solaires mortelles, totalement dépourvue de vie. Recouverte de lacs de lave et de dépôts minéraux. Une base humaine souterraine exploite ses ressources, notamment le fer et les cristaux, sous la protection d’un bouclier orbital."

        self.planets.append(planet)

        
        #Planet 3
        p_type = "vie"
        orbit_r = 75 + 1 * 50
        orbit_speed = 0.32/(1 + 1)
        planet = Planet(f"Terre", p_type, orbit_r, orbit_speed)
        planet.radius = 15
        planet.color = "./planet-pic/Terre.png"
        planet.buildings['extractor']['fer'] = 1
        planet.buildings['extractor']['carbon'] = 0
        planet.buildings['extractor']['petrole'] = 0
        planet.sommaire = "Planète mère de l’humanité et une des rares planètes connues à abriter une vie complexe. Autrefois en parfait équilibre écologique, elle a subi de graves dommages environnementaux dus à l’exploitation humaine. Malgré une pollution croissante, elle reste un monde habitable avec des ressources vitales comme l’eau, l’oxygène et les terres fertiles."
        planet.description = "Abritant une biodiversité exceptionnelle et un écosystème fragile. Son atmosphère, riche en oxygène et en azote, permet le développement de formes de vie variées, des océans aux continents. Toutefois, des siècles d’industrialisation et de surexploitation des ressources ont provoqué une pollution massive, affectant la qualité de l’air, de l’eau et des sols. L’exploitation de ressources naturelles comme l’eau potable, les forêts, les métaux rares et les combustibles fossiles continue, mais sous des restrictions de plus en plus strictes pour limiter les dégâts environnementaux. Avec une gravité stable et une température modérée, la Terre reste un habitat idéal, bien que son avenir dépende désormais des efforts pour restaurer son équilibre écologique."
        self.planets.append(planet)
        
        #Planet 4
        p_type = "vie"
        orbit_r = 75 + 2 * 50
        orbit_speed = 0.32/(2 + 1)
        planet = Planet(f"Terralis Prime", p_type, orbit_r, orbit_speed)
        planet.radius = 19
        planet.color = "./planet-pic/Terralis_Prime.png"
        planet.sommaire = "Terralis Prime est une version premium de la Terre, une planète luxuriante avec un climat stable de 25°C en moyenne et une vie intelligente avancée. Riche en ressources comme l’oxygène, l’hydrogène, le fer, le cuivre et le titane, elle est surtout connue pour ses super-métaux, une matière précieuse vendue exclusivement par sa civilisation extraterrestre. L’exploitation est strictement régulée, avec une taxe de 25 % pour les entreprises terriennes et des quotas pour limiter l’extraction."
        planet.description = "Cités-arbres géantes alimentées par photosynthèse quantique et climat idéal, Terralis Prime est une planète prospère où nature et technologie coexistent parfaitement. La civilisation locale, bien plus avancée que l’humanité, contrôle rigoureusement l’exploitation des ressources pour préserver son équilibre écologique. Toute extraction nécessite une stérilisation préalable et est soumise à des quotas pour éviter la surexploitation. Terralis Prime représente une opportunité commerciale majeure, mais seuls ceux qui respectent ses lois peuvent espérer en tirer profit."
        self.planets.append(planet)

        #Planet 2
        p_type = "morte"
        orbit_r = 75 + 3 * 50
        orbit_speed = 0.32/(3 + 1)
        planet = Planet(f"Nekronia", p_type, orbit_r, orbit_speed)
        planet.radius = 15
        planet.color = "./planet-pic/Nekronia.png"
        planet.sommaire = "Désert radioactif post-guerre apocalyptique : Nekronia est une planète totalement morte. Avec une température de 400°C et une atmosphère hautement radioactive, toute vie y est impossible. Ses vastes déserts toxiques renferment des ressources précieuses comme l’uranium, le plutonium et le silicium, mais l’accès est strictement limité. Toute extraction nécessite une décontamination obligatoire et seuls des drones spécialisés peuvent y opérer."
        planet.description = " Un conflit dévastateur qui a erradiqué toute civilisation. Bombardée sans relâche pendant la cinquième Guerre Mondiale, aucune structure n’a survécu, et l’air est si toxique que même les combinaisons anti-radiations ne permettent qu’une exposition limitée. Malgré cet environnement infernal, Nekronia reste une cible d’exploitation pour ses gisements d’uranium et de plutonium, essentiels aux industries énergétiques et militaires. Cependant, en raison des niveaux extrêmes de radiation, seules des missions automatisées par drones sont autorisées. Toute tentative d’exploration humaine sans équipement ultra-protégé serait une condamnation certaine."
        self.planets.append(planet)
        
        # Planet 1
        p_type = "morte"
        orbit_r = 75 + 4 * 50
        orbit_speed = 0.32/(4 + 1)
        planet = Planet(f"Chloria", p_type, orbit_r, orbit_speed)
        planet.radius = 15
        planet.color = "./planet-pic/Chloria.png"
        planet.sommaire = "Monde toxique au chlore. Extraction risquée."
        planet.description = "Atmosphère corrosive de chlure d'hydrogène. Paysages de cristaux ionisés."
        self.planets.append(planet)
        
        #Planet 6
        p_type = "vie"
        orbit_r = 75 + 5 * 50
        orbit_speed = 0.32/(5 + 1)
        planet = Planet(f"Atlantis", p_type, orbit_r, orbit_speed)
        planet.radius = 22
        planet.color = "./planet-pic/Atlantis.png"
        planet.sommaire = "Planète océanique habitée, où une civilisation sous-marine s’est développée dans des cités. Riche en ressources biologiques et énergétiques, elle est un centre d’intérêt majeur pour la recherche scientifique. L’accès est strictement réglementé, nécessitant un équipement aquatique spécialisé et le paiement de taxes de respiration. Toute atteinte à l’environnement marin est passible de la peine de mort selon les lois locales."
        planet.description = "Recouverte par un immense océan, Atlantis abrite une civilisation avancée vivant dans des cités sous-marines. Ses habitants exploitent l’énergie géothermique, pratiquent l’extraction électrolytique de l’eau et collectent les gaz naturels présents dans l’atmosphère liquide. En raison de la rareté de l’oxygène accessible, tout visiteur doit payer une taxe de respiration pour utiliser un appareil filtrant, indispensable à la survie. La planète est un paradis pour les chercheurs en biologie marine, mais elle impose des règles strictes de préservation : tout dommage causé à l’environnement océanique est puni de la peine de mort..."
        self.planets.append(planet)
        
        #Planet 5
        p_type = "gas"
        orbit_r = 75 + 6 * 50
        orbit_speed = 0.32/7
        planet = Planet(f"Xenon Prime", p_type, orbit_r, orbit_speed)
        planet.radius = 30
        planet.color = "./planet-pic/Xenon_Prime.png"
        planet.sommaire = "Géante composée principalement de xénon ionisé et d’autres gaz nobles extrêmement précieux. Son atmosphère dense et comprimée crée un spectacle unique de nuages violets luminescents, tandis que son noyau, composé d’argon liquide ultra-compressé, génère une lueur mauve intense. Toute expédition nécessite un équipement de protection extrême contre la pression colossale et l’interdiction stricte d’apporter des éléments réactifs."
        planet.description = "Xénon Prime est un joyau cosmique où des tempêtes ionisées illuminent l’atmosphère d’éclats violet et bleu électrique. Les gaz nobles présents – xénon, néon, krypton et argon – sont d’une rareté et d’une valeur inestimables, attirant explorateurs et scientifiques. Cependant, l’exploration y est un défi colossal : seuls des vaisseaux ultra-renforcés peuvent pénétrer dans son atmosphère comprimée sans être écrasés. Toute présence humaine doit être totalement isolée, car le moindre élément réactif introduit dans cette mer gazeuse pourrait provoquer des réactions incontrôlables. Seuls les plus audacieux et technologiquement avancés peuvent espérer exploiter les trésors de Xénon Prime."
        self.planets.append(planet)
        
        #Planet 8
        p_type = "vie"
        orbit_r = 75 + 7 * 50
        orbit_speed = 0.32/8
        planet = Planet(f"Cryogenia", p_type, orbit_r, orbit_speed)
        planet.radius = 13
        planet.color = "./planet-pic/Cryogenia.png"
        planet.sommaire = "Monde glacé où la température atteint -40°C en moyenne. Bien qu’inhabitable pour les humains, elle abrite une faune non intelligente adaptée au froid et possède un écosystème équilibré. Ses ressources précieuses incluent cristaux rares, charbon, fer, cuivre, (H₂O), (O₂) et biocarburants naturels."
        planet.description = "Planète où de vastes étendues gelées s’étendent sous une atmosphère glaciale. Malgré des conditions extrêmes, certaines formes de vie microbiennes et animales ont réussi à s’adapter, jouant un rôle essentiel dans l’équilibre écologique de la planète. L’exploitation de ses minéraux et biocarburants est sous haute surveillance, avec un système de régénération naturelle 1:1, garantissant que chaque ressource prélevée doit être compensée. Toute tentative de perturber l’environnement, notamment en modifiant la température de plus de ±0,5°C, est passible d’une amende de 50 millions de dollars par personne. Avant toute installation humaine, une stérilisation complète est obligatoire pour éviter toute contamination de l’écosystème fragile. Cryogenia est une terre de richesses, mais seuls ceux qui respectent ses lois strictes peuvent espérer y prospérer."

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


    @staticmethod
    def build_structure(planet, structure, amount=1):
        """ Ajoute un bâtiment si la limite n’est pas atteinte """
        if structure in ["research", "decarbonizer", "fabricator"]:
            max_limits = {"research": 1, "decarbonizer": 10, "fabricator": 5}
            if planet.buildings[structure] + amount <= max_limits[structure]:
                planet.buildings[structure] += amount
                return True
        return False

    @staticmethod
    def add_extractor(planet, resource_type, amount=1):
        """ Ajoute des extracteurs pour un type de ressource donné (0 à 10) """
        if amount < 0 or amount > 10:
            return False
        if resource_type in planet.resources:
            current_amount = planet.buildings["extractor"].get(resource_type, 0)
            if current_amount + amount <= 10:
                planet.buildings["extractor"][resource_type] = current_amount + amount
                return True
        return False


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

