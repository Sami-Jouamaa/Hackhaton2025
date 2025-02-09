class Company:
    def __init__(self):
        self.bank = 1000
        self.employees = 100
        self.resources = {'Fer': 100, 'Acier': 200, 'Fossil_Fuel': 500}  
        self.contrats = []
        self.equipement = []
        self.technologies = {}
        self.trade_routes = []
        self.upgrading_tech = {}

    def upgrade(self, tech, solar_system):
        valid = True
        research_planets = list(filter(lambda curr_planet: curr_planet.buildings['research'] != 0, solar_system.planets))
        for key, value in tech.resources_till_level.items():
            num = 0
            for planet in research_planets:
                num += planet.inventory.get(key, 0)
            if num < value:
                valid = False
        if valid:
            tech.level_up()
            for key, value in tech.resources_till_level.items():
                num = value
                for planet in research_planets:
                    if num > planet.inventory[key]:
                        planet.inventory[key] = 0
                        num -= planet.inventory[key]
                    else:
                        planet.inventory[key] -= num
                        break
    
    def create_export_route(self, source_planet, dest_planet, resource, amount, fuel_cost_per_unit=1):
        total_fuel_cost = fuel_cost_per_unit * amount

        # Check if company has enough fossil fuel
        if self.resources.get('Fossil_Fuel', 0) >= total_fuel_cost:
            self.resources['Fossil_Fuel'] -= total_fuel_cost  # Reduce fuel stock
            source_planet.resources[resource] -= amount  # Remove from source
            dest_planet.resources[resource] = dest_planet.resources.get(resource, 0) + amount  # Add to destination

            # Store trade route
            self.trade_routes.append({
                'source': source_planet,
                'destination': dest_planet,
                'resource': resource,
                'amount': amount,
                'fuel_cost': total_fuel_cost
            })
            return True
        
        return False  # Export fails if not enough fossil fuel




class Contrat:
    def __init__(self, payout, price, time, condition, condition_text):
        self.payout = payout
        self.price = price
        self.time = time
        self.condition = condition
        self.condition_text = condition_text

class Technology:
    def __init__(self, name, level, max_level, resources_till_level, money_till_level):
        self.name = name
        self.level = level
        self.max_level = max_level
        self.resources_till_level = resources_till_level
        self.money_till_level = money_till_level

    def level_up(self):
        if self.level != self.max_level:
            self.level += 1
            self.money_till_level *= self.level
            for res, amt in self.resources_till_level.items():
                amt *= self.level

company = Company()
company.technologies = {
    'fusee': Technology('fusee', 1, 5, {'acier': 0, 'bronze': 0},10000),
    'extracteur': Technology('extracteur', 1, 5, {'acier': 200, 'bronze': 200},10000),
    'decarbonizeur': Technology('decarbonizeur', 0, 5, {'supermetal': 200, 'Cristaux': 100, 'Titanium': 100},10000),
    'fabricateur': Technology('fabricateur', 1, 5, {'supermetal': 200, 'acier': 200, 'cuivre': 200}, 10000)
}

