_list_obj_defs = [{"name": 'gilet pareballes', 'life_time': 50, "protection": 2, "place": 1, "price": 1000}]
_list_obj_attaques = [{"name": 'Colt Single Action Army', 'added_force_obj': 1, "place": 1, "price": 1000}]
_list_obj_inventory = [{"name": 'Manteau', 'added': 20, "price": 100}]


class ObjPersonna:
    def __init__(self, name: str = "",
                 added_force: int = 0,
                 added_protection: int = 1,
                 place_inventory: int = 1,
                 added_place: int = 0,
                 price: float = 0.0,
                 life_time: int = 100,
                 is_destructable: bool = True):
        self.name = name
        self.added_force = added_force
        self.added_protection = added_protection
        self.place_inventory = place_inventory
        self.added_place = added_place
        self.price = price
        self.lifeTime = life_time
        self.is_destructable = is_destructable


class ObjDefensePersonna(ObjPersonna):
    def __init__(self, nameObj: str = "", added_protection_obj: int = 0, place_inventory_obj: int = 0,
                 life_time_obj: int = 100, price_obj: float = 0.0):
        super().__init__(name=nameObj, added_protection=added_protection_obj, place_inventory=place_inventory_obj,
                         life_time=life_time_obj, price=price_obj,
                         added_force=0, added_place=0, is_destructable=True)


class ObjAttaquePersonna(ObjPersonna):
    def __init__(self, nameObj: str = "", added_force_obj: int = 0, place_inventory_obj: int = 0,
                 price_obj: float = 0.0):
        super().__init__(name=nameObj, added_protection=0, place_inventory=place_inventory_obj, price=price_obj,
                         added_force=added_force_obj, added_place=0, is_destructable=False)


class ObjInventoryPersonna(ObjPersonna):
    def __init__(self, nameObj: str = "", added_place_obj: int = 0, price_obj: float = 0.0):
        super().__init__(name=nameObj, added_protection=0, place_inventory=0, price=price_obj,
                         added_force=0, added_place=added_place_obj, is_destructable=False)


objets_defensifs = []
objets_offensifs = []
objects_capacitifs = []


def create_Objects():
    for ld in _list_obj_defs:
        tmp = ObjDefensePersonna(nameObj=ld['name'], added_protection_obj=ld['protection'],
                                 place_inventory_obj=ld['place'], life_time_obj=ld['life_time'], price_obj=ld['price'])
        objets_defensifs.append(tmp)
    for lo in _list_obj_attaques:
        tmp2 = ObjAttaquePersonna(nameObj=lo['name'], added_force_obj=lo['added_force_obj'],
                                  place_inventory_obj=lo['place'], price_obj=lo['price'])
        objets_offensifs.append(tmp2)
    for li in _list_obj_inventory:
        tmp3 = ObjInventoryPersonna(nameObj=li['name'], added_place_obj=li['added'], price_obj=li['price'])
        objects_capacitifs.append(tmp3)


class AllObjects:
    def __init__(self):
        self.defensifs = [ObjPersonna]
        self.offensifs = [ObjPersonna]
        self.capacitifs = [ObjPersonna]
        create_Objects()
        self.defensifs = objets_defensifs
        self.offensifs = objets_offensifs
        self.capacitifs = objects_capacitifs
