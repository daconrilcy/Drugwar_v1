from pygame import Surface
from tools.draw.draw_line import DrawLine
from tools.draw.draw_arc import DrawArc


class Forms:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.figures = []
        self.mouse_pos = None
        self.mouse_bt = None
        self.act_figure = None

    def add(self, type_forms: str = "line"):
        create = False
        if type_forms == "line":
            self.figures.append(
                DrawLine(self.surface, self.mouse_pos[0], self.mouse_pos[1])
            )
            create = True
        elif type_forms == "arc":
            self.figures.append(
                DrawArc(self.surface, self.mouse_pos[0], self.mouse_pos[1])
            )
            create = True

        if create:
            self.act_figure = len(self.figures) - 1
            self.figures[self.act_figure].create()

    def update(self, mouse_pos, mouse_bt):
        self.mouse_bt = mouse_bt
        self.mouse_pos = mouse_pos
        for fig in self.figures:
            fig.update(mouse_pos, mouse_bt)
