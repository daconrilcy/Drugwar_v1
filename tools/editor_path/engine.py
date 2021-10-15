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

    def handle_event(self, ev: event):
        self.actions.handle(ev)

    def update(self):
        self.actions.update()
        self.interface.update()

    def create_interface(self):
        self.interface = InterfaceEditor(self.surface)
        self.interface.add_button(0, 0, 32, heigh=None, color=self.color_bt,
                                  path_image='C:\\Users\86010478\PycharmProjects\pythonProject\Drugwar_v1'
                                             '\\tools\editor_path\img\\bt_courbe.png')
        self.interface.add_button(0, 32, 32, heigh=None, color=self.color_bt,
                                  path_image='C:\\Users\86010478\PycharmProjects\pythonProject\Drugwar_v1'
                                             '\\tools\editor_path\img\\bt_ligne.png')
        self.interface.add_button(0, 64, 32, heigh=None, color=self.color_bt,
                                  path_image='C:\\Users\86010478\PycharmProjects\pythonProject\Drugwar_v1'
                                             '\\tools\editor_path\img\\bt_grid.png')
        self.interface.add_button(0, 96, 32, heigh=None, color=self.color_bt,
                                  path_image='C:\\Users\86010478\PycharmProjects\pythonProject\Drugwar_v1'
                                             '\\tools\editor_path\img\\bt_groupe.png')
