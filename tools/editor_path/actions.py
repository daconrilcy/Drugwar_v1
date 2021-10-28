from pygame import Surface, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYUP, K_l, K_a, K_c, K_DELETE, K_g, K_s, mouse
from tools.editor_path.grid import GridPlot
from tools.editor_path.selector import Selector

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
        self.grid = GridPlot(surface)
        self.selector = Selector(surface)

    def update(self, ev):
        self.mouse_pos = mouse.get_pos()
        self.grid.update(self.mouse_bt)
        if ev != self.last_ev:
            if ev.type == KEYUP:
                if ev.key == K_l:
                    self.forms.add("line", self.grid.pas)
                elif ev.key == K_a:
                    self.forms.add("arc", self.grid.pas)
                elif ev.key == K_c:
                    self.forms.edit("invert curve")
                elif ev.key == K_DELETE:
                    self.forms.delete()
                elif ev.key == K_g:
                    self.grid.active_desactive()
                elif ev.key == K_s:
                    self.selector.select(self.forms)

            elif (ev.type == MOUSEBUTTONUP) | (ev.type == MOUSEBUTTONDOWN):
                self.mouse_bt = ev.type

            self.last_ev = ev

        self.forms.update(mouse_pos=self.mouse_pos, mouse_bt=self.mouse_bt)
        self.forms.grided = self.grid.active
        self.selector.update(self.mouse_pos, self.mouse_bt)
        if self.selector.selection_to_get:
            print(self.selector.get_selected())
