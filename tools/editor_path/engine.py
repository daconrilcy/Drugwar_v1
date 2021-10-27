import pygame.event
from pygame import Surface, mouse, MOUSEBUTTONUP, MOUSEBUTTONDOWN, event, KEYDOWN, KEYUP, K_l, key
from tools.editor_path.interface import InterfaceEditor
from tools.editor_path.actions import ActionEdithPath


class EditorPath:
    def __init__(self, surface: Surface, marge=20):
        self.surface = surface
        self.marge = marge
        self.interface = None
        self.color_bt = (125, 125, 125)
        self.actions = ActionEdithPath(surface=surface, marge=marge)
        self.create_interface()
        self.event = None

    def handle_event(self, ev):
        self.event = ev

    def update(self):
        self.actions.update(self.event)
        self.interface.update()

    def create_interface(self):
        self.interface = InterfaceEditor(self.surface)
        self.interface.add_button(0, 0, 32, heigh=None, color=self.color_bt,
                                  path_image='..\\tools\editor_path\img\\bt_courbe.png')
        self.interface.add_button(0, 32, 32, heigh=None, color=self.color_bt,
                                  path_image='..\\tools\editor_path\img\\bt_ligne.png')
        self.interface.add_button(0, 64, 32, heigh=None, color=self.color_bt,
                                  path_image='..\\tools\editor_path\img\\bt_grid.png')

        self.interface.add_button(0, 96, 32, heigh=None, color=self.color_bt,
                                  path_image='..\\tools\editor_path\img\\bt_groupe.png')
