from tools.draw.draw_box import DrawBox
from tools.draw.draw_figure import DrawFigure
from tools.editor_path.forms import Forms

from pygame import Surface


class Selector:
    def __init__(self, surface: Surface):
        self.surface = surface
        self.drawingBox = DrawBox(self.surface, x=0, y=0)
        self.mouse_pos = 0, 0
        self.mouse_bt = None
        self.forms = None
        self.under_selection = False
        self.selection_to_get = False
        self.selected = []

    def select(self, forms: Forms):
        self.forms = forms
        self.drawingBox = DrawBox(surface=self.surface, x=self.mouse_pos[0], y=self.mouse_pos[1], type_line=1)
        self.drawingBox.create()
        self.under_selection = True

    def update(self, mouse_pos, mouse_bt):
        self.mouse_pos = mouse_pos
        self.mouse_bt = mouse_bt
        if self.drawingBox is not None:
            self.drawingBox.update(mouse_pos, mouse_bt)
        if self.is_drawb_created():
            print("done")
            self.plots_selected()
            self.drawingBox = None

    def is_drawb_created(self):
        if self.drawingBox is not None:
            return self.drawingBox.created
        else:
            return False

    def plots_selected(self):
        self.selected = []
        self.selection_to_get = False
        if self.drawingBox is not None:
            if self.forms is not None:
                n_fig = len(self.forms.figures)
                if n_fig > 0:
                    for n_f in range(n_fig):
                        n_points = len(self.forms.figures[n_f].points)
                        for n_p in range(n_points):
                            if self.drawingBox.pt_is_in_zone(self.forms.figures[n_f].points[n_p]):
                                self.forms.figures[n_f].pt_selected = n_p
                                self.selected.append([n_f, n_p])
                                self.selection_to_get = True

    def get_selected(self):
        self.selection_to_get = False
        return self.selected
