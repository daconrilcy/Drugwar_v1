from pygame import Surface, draw, Color
from tools.draw.dashed_line import DashedLine
from tools.draw.draw_figure import DrawFigure


class DrawBox(DrawFigure):
    def __init__(self, surface: Surface, color_base: tuple = (255, 255, 255), x: int = 0, y: int = 0, type_line: int = 0):
        super().__init__(surface=surface, x=x, y=y, color_base=color_base)
        self.origine = self.mouse_pos
        self.end = self.mouse_pos
        self.width = 0
        self.height = 0
        self.cotes = []
        self.case = 0
        self.typeline = type_line
        self.pt_2 = self.origine
        self.pt_3 = self.end
        self.lines = []
        print(color_base)
        for n in range(4):
            self.lines.append(DashedLine(surface=surface, color=self.color_ini,
                                         start_pos=self.mouse_pos, end_pos=self.mouse_pos))

    def update_points(self):
        if self.case == 0:
            self.origine = self.points[0]
            self.end = self.points[1]
        elif self.case == 1:
            self.origine = self.points[0][0], self.points[1][1]
            self.end = self.points[1][0], self.points[0][1]
        elif self.case == 2:
            self.origine = self.points[1][0], self.points[1][1]
            self.end = self.points[0][0], self.points[0][1]
        elif self.case == 3:
            self.origine = self.points[1][0], self.points[0][1]
            self.end = self.points[0][0], self.points[1][1]
        self.pt_2 = self.end[0], self.origine[1]
        self.pt_3 = self.origine[0], self.end[1]
        self._update_dash()

    def _update_dash(self):
        self.lines[0].change_points(start_pos=self.origine, end_pos=self.pt_2)
        self.lines[1].change_points(start_pos=self.pt_2, end_pos=self.end)
        self.lines[2].change_points(start_pos=self.end, end_pos=self.pt_3)
        self.lines[3].change_points(start_pos=self.pt_3, end_pos=self.origine)

    def update_case(self):
        self.case = 0
        if self.points[0][1] > self.points[1][1]:
            if self.points[0][0] < self.points[1][0]:
                self.case = 1
            else:
                self.case = 2
        else:
            if self.points[0][0] > self.points[1][0]:
                self.case = 3

    def update_dim(self):
        self.width = abs(self.points[1][0] - self.points[0][0])
        self.height = abs(self.points[0][1] - self.points[1][1])

    def draw_box(self):
        if self.typeline == 0:
            draw.rect(self.surface, self.color, (self.origine[0], self.origine[1], self.width, self.height), self._ep)

        if self.typeline == 1:
            for n in range(4):
                self.lines[n].draw()
                self.lines[n].color = self.color

        draw.rect(self.surface, self.color, (0, 0, 50, 50))

    def update_formula(self):
        self.update_case()
        self.update_points()
        self.update_dim()
        self._update_dash()
        self.define_min_max()

    def draw(self):
        self.draw_box()

    def get_pt2(self):
        return self.mouse_pos

