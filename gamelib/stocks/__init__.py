import random

from gamelib.Drug import Drug, drugs, create_drugs_list
from gamelib.objects import ObjPersonna, AllObjects

objsP = AllObjects()


class LigneObjet:
    def __init__(self, qty: int = 0, price_unit: float = 0.0):
        self.qty = qty
        self.price_unit = price_unit


class LigneDrugInventory(LigneObjet):
    def __init__(self, drug: Drug = None):
        super().__init__()
        self.drug = drug
        self.price_unit = drug.price


class LigneObjectPersonna(LigneObjet):
    def __init__(self, objetPersonna: ObjPersonna, type_objet: str):
        super().__init__()
        self.object_Personna = objetPersonna
        self.type_object: str = type_objet
        self.price_unit = objetPersonna.price


class Stock:
    def __init__(self):
        self.inventory = []

    def alter_price(self, coef: float = 2.0):
        for lo in self.inventory:
            price_ini = lo.price_unit
            lo.price_unit = round(random.random() * coef * price_ini, 2)


class Drug_Stock(Stock):
    def __init__(self):
        super().__init__()
        self._init_inventory()

    def _init_inventory(self):
        for drug in drugs:
            self.inventory.append(LigneDrugInventory(drug=drug))

    def create_stock(self, mult2: int = 10):
        for lo in self.inventory:
            lo.qty = int(random.random() * lo.drug.mult * mult2 )

    def print_stock_datas(self):
        n = 0
        for lo in self.inventory:
            print(str(n) + " : " + lo.drug.name + "\tstock : " + str(lo.qty) + " " + lo.drug.unit + "\tprice unit : $"
                  + str(lo.price_unit))
        n += 1

class Obj_Stock(Stock):
    def __init__(self):
        super().__init__()
        self.name_offensif = "offensif"
        self.name_defensif = "defensif"
        self.name_capacitif = "capacitif"
        self._init_inventory()
        self.alter_price()

    def _init_inventory(self):
        for obo in objsP.offensifs:
            self.inventory.append(
                LigneObjectPersonna(obo, self.name_offensif)
            )
        for obd in objsP.defensifs:
            self.inventory.append(
                LigneObjectPersonna(obd, self.name_defensif)
            )
        for obc in objsP.capacitifs:
            self.inventory.append(
                LigneObjectPersonna(obc, self.name_capacitif)
            )

    def create_stock(self, mult: int = 10):
        for lo in self.inventory:
            lo.qty = int(random.random() * mult)

    def print_stock_datas(self):
        n = 0
        for lo in self.inventory:
            print(str(n) + " : " + lo.object_Personna.name + "\tstock : " + str(lo.qty) + "\tprice unit : $"
                  + str(lo.price_unit))
            n += 1
