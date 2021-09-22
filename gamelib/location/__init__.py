from gamelib.stocks import Drug_Stock, Obj_Stock
locations_raw = [
    {"name": "New York", "country": "USA", "latitude": "40.7127281", "longitude": "-74.0060152"},
    {"name": "Los Angeles", "country": "USA", "latitude": "34.02574317244863", "longitude": "-118.37860840837958"},
    {"name": "Miami", "country": "USA", "latitude": "25.7741728", "longitude": "-80.19362"},
    {"name": "Dallas", "country": "USA", "latitude": "32.7762719", "longitude": "-96.7968559"},
    {"name": "Las Vegas", "country": "USA", "latitude": "36.1672559", "longitude": "-115.148516"},
    {"name": "Chicago", "country": "USA", "latitude": "41.8755616", "longitude": "-87.6244212"},
    {"name": "San Fransisco", "country": "USA", "latitude": "37.797297585844376", "longitude": "-122.57000139765626"}
]

locations = []
actual_location = None


class Location:
    def __init__(self, name: str, country: str, gps_x: str, gps_y: str):
        self.country = country
        self.name = name
        self.gps_x = gps_x
        self.gps_y = gps_y
        self.drugs = Drug_Stock()
        self.objects = Obj_Stock()

        self.alter_stocks_prices()

    def alter_stocks_prices(self):
        self.drugs.create_stock()
        self.drugs.alter_price()
        self.objects.create_stock()
        self.objects.alter_price()


def create_location():
    for location in locations_raw:
        tmp = Location(name=location['name'], country=location['country'],
                       gps_x=location['latitude'], gps_y=location['longitude'])
        locations.append(tmp)