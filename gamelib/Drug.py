from gamelib.location import Location

drugType = {1: "Cocaine", 2: "Marijuana", 3: "Heroine", 4: "LSD"}


class Drug:
    def __init__(self, name: str, prod_location: Location = None, price: float = 0.0, qty: int = 0, drugtype: int = 1):
        self.name = name
        self.price = price
        self.qty = qty
        self.type = drugtype
        if prod_location is not None:
            self.prod_location = prod_location
        else:
            self.prod_location = None
