from pygame import Surface
import pygame
from tools.editor_path.button import ButtonInterface


class InterfaceEditor:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.buttons = []
        self.is_visible = True

    def update(self):
        if self.is_visible:
            self.update_buttons()

    def add_button(self, left, top, width, heigh=None, color=(125, 125, 125), path_image: str = None):
        if heigh is None:
            heigh = width
        self.buttons.append(ButtonInterface(self.surface, left, top, width, heigh, color, img_path=path_image))

    def update_buttons(self):
        for button in self.buttons:
            button.update()
