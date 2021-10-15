import pygame.draw
import pytmx
import pyscroll
from gamelib.poly_interact import pytmx_obp_poly_to_shapely_poly_2d


class City_Obj(pygame.Rect):
    def __init__(self, name: str, left: float, top: float, width: float, height: float):
        super(City_Obj, self).__init__(left=left, top=top, width=width, height=height)
        self._name = name

    def get_name(self):
        return self._name


class MyTmx:

    def __init__(self, screen):
        self.screen = screen
        path_carte = "..\gamelib\inteface\map\carte.tmx"
        print(path_carte)
        self.tmx_data = pytmx.util_pygame.load_pygame(
            path_carte)
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())

        # dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

        # zones interdites
        self.walls_poly = []

        #cities
        self.city_obj = []
        self.city_name = []

        for obj in self.tmx_data.objects:
            if obj.type == "map_limit":
                self.walls_poly.append(pytmx_obp_poly_to_shapely_poly_2d(obj))
            if obj.type == "city_obj":
                self.city_obj.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                self.city_name.append(obj.name)


