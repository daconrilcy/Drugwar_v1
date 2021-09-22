import pytmx
import pyscroll


class MyTmx:

    def __init__(self, screen):
        self.screen = screen
        self.tmx_data = pytmx.util_pygame.load_pygame("D:\Python\pythonProject\Drugwar_v1\gamelib\inteface\map\carte.tmx")
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size())
