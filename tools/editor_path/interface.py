from pygame import Surface
import pygame
from tools.editor_path.button import ButtonInterface


class InterfaceEditor:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.buttons = []
        self.is_visible = True
        self.image = pygame.image.load('C:\\Users\86010478\PycharmProjects\pythonProject\Drugwar_v1\\tools\editor_path\img\\bt_courbe.png')
        self.surf_image = Surface([0,0])

    def update(self):
        if self.is_visible:
            self.update_buttons()
        self.surf_image.blit(self.image, (100, 100),pygame.Rect(0,0, 64, 64))

    def add_button(self, left, top, width, heigh=None, color=(125, 125, 125), path_image: str = None):
        if heigh is None:
            heigh = width
        self.buttons.append(ButtonInterface(self.surface, left, top, width, heigh, color, img_path=path_image))

    def update_buttons(self):
        for button in self.buttons:
            button.update()
