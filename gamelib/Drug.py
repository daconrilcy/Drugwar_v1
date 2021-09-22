drugnames = [
    {"name": "Cocaine", "unit": "g", "mult": 1, "av_price": 70.0},
    {"name": "Heroine", "unit": "g", "mult": 1, "av_price": 40.0},
    {"name": "Crack", "unit": "g", "mult": 1, "av_price": 60.0},
    {"name": "Weed", "unit": "g", "mult": 100, "av_price": 10.0},
    {"name": "Hashish", "unit": "g", "mult": 10, "av_price": 7.0},
    {"name": "Speed", "unit": "pils", "mult": 1, "av_price": 60.0},
    {"name": "MDMA", "unit": "pils", "mult": 1, "av_price": 10.0},
]

drugs = []


class Drug:
    def __init__(self, price: float = 0.0, drugname = None):
        if drugname is None:
            drugname = drugnames[0]
        self.name = drugname["name"]
        self.unit = drugname['unit']
        self.price = drugname['av_price']
        self.mult = drugname['mult']


def create_drugs_list():
    for dr in drugnames:
        tmp = Drug(drugname=dr)
        drugs.append(tmp)