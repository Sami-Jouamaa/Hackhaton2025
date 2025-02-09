class Company:
    def __init__(self):
        self.bank = 1000
        self.employees = 100
        self.resources = {'Fer': 100}
        self.contrats = []
        self.equipement = []
        self.technologies = []
        self.trade_routes = []

class Contrat:
    def __init__(self, payout, price, time, condition, condition_text):
        self.payout = payout
        self.price = price
        self.time = time
        self.condition = condition
        self.condition_text = condition_text


company = Company()