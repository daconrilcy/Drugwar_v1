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
        self.n_act_figure = -1
        self.n_figures = 0
        self.grided = False
        self.linked_points = []

    def add(self, type_forms: str = "line", pas: int = 32):
        create = False
        if type_forms == "line":
            self.figures.append(
                DrawLine(surface=self.surface, x=self.mouse_pos[0], y=self.mouse_pos[1], pas=pas)
            )
            create = True
        elif type_forms == "arc":
            self.figures.append(
                DrawArc(surface=self.surface, x=self.mouse_pos[0], y=self.mouse_pos[1], pas=pas)
            )
            create = True

        if create:
            self.n_figures += 1
            self.act_figure = self.n_figures - 1
            self.figures[self.act_figure].create()

    def edit(self, type_edit: str = "invert curve"):
        if type_edit == "invert curve":
            if isinstance(self.act_figure, DrawArc):
                self.act_figure.reverse_curve()

    def delete(self):
        if self.act_figure is not None:
            self.figures.pop(self.n_act_figure)
            self.n_act_figure = -1
            self.act_figure = None
            self.n_figures -= 1

    def update(self, mouse_pos, mouse_bt):
        self.mouse_bt = mouse_bt
        self.mouse_pos = mouse_pos
        self.n_act_figure = -1
        self.act_figure = None
        for n in range(self.n_figures):
            self.figures[n].update(mouse_pos, mouse_bt)
            self.figures[n].grided = self.grided
            if self.figures[n].selected:
                self.act_figure = self.figures[n]
                self.n_act_figure = n
