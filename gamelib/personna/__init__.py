from gamelib.stocks import Drug_Stock, Obj_Stock


class Personna:
    def __init__(self, name: str = "", force: int = 10, capacity: int = 100, health: int = 100, protection: int = 1,
                 monnaie: float = 0
                 ):
        self.name = name
        self.force = force
        self.capacity = capacity
        self.occuped_capacity = 0
        self.health = health
        self.protection = protection
        self.obj_inventory = Obj_Stock()
        self.drug_inventory = Drug_Stock()
        self.monnaie = monnaie
        self.alive = True

        self.drug_inventory.alter_price(0)



