from pygame import Surface, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, KEYDOWN, K_l, K_a, K_c, event, mouse, draw
from tools.editor_path.forms import Forms


class ActionEdithPath:
    def __init__(self, surface: Surface, marge):
        self.surface = surface
        self.marge = marge
        self.last_ev = None
        self.under_creation = False
        self.forms = Forms(self.surface)
        self.mouse_pos = None
        self.mouse_bt = None
        self.last_key = None
        self.last_bt = None
        self.clic = False

    def update(self, ev):
        self.mouse_pos = mouse.get_pos()
        if ev != self.last_ev:
            if ev.type == KEYUP:
                if ev.key == K_l:
                    self.create_form("line")
                elif ev.key == K_a:
                    self.create_form("arc")
            elif (ev.type == MOUSEBUTTONUP) | (ev.type == MOUSEBUTTONDOWN):
                self.mouse_bt = ev.type

            self.last_ev = ev

        self.forms.update(mouse_pos=self.mouse_pos, mouse_bt=self.mouse_bt)

    def create_form(self, type_ev: str = "line"):
        self.forms.add(type_ev)
