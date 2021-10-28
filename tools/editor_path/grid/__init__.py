from pygame import Surface, draw, mouse,MOUSEBUTTONDOWN


class _Plot:
    def __init__(self, surface: Surface, color: tuple = (50, 50, 50), center: tuple = (0, 0), rayon: int = 1):
        self.surface = surface
        self.color = color
        self.center = center
        self.rayon = rayon

    def draw(self):
        draw.circle(self.surface, self.color, center=self.center, radius=self.rayon )


class _PictureGrid:
    def __init__(self, surface: Surface, pas: int = 32, color: tuple = (50, 50, 50), rayon: int = 1):
        self.suface: Surface = surface
        self.pas: int = pas
        self.color: tuple = color
        self.show: bool = False
        self.rayon = rayon
        self.width = 0
        self.height = 0
        self.plots = []
        self.create_plot()

    def create_plot(self):
        self.width = self.suface.get_width()
        self.height = self.suface.get_height()
        n_ho = int(self.width/self.pas) + 1
        n_ve = int(self.height/self.pas) + 1
        for nh in range(n_ho):
            for nv in range(n_ve):
                x = self.pas*nh
                y = self.pas * nv
                self.plots.append(
                    self.plotter(x, y)
                )

    def plotter(self, x, y):
        return _Plot(self.suface, self.color, (x, y), self.rayon)

    def draw(self):
        if self.show:
            for plot in self.plots:
                plot.draw()


class GridPlot:
    def __init__(self, surface: Surface, pas: int = 16, color: tuple = (50, 50, 50), rayon: int = 1):
        self.suface: Surface = surface
        self.pas: int = pas
        self.picture_grid = _PictureGrid(surface, pas, color, rayon)
        self.active = False
        self.delai_mouse_up_ini = 5
        self.delai_mouse_up = self.delai_mouse_up_ini
        self.last_mouse_pos = mouse.get_pos()

    def active_desactive(self):
        if self.active:
            self.active = False
        else:
            self.active = True

        self.picture_grid.show = self.active

    def update_mouse_pos(self, ev):
        if self.active:
            x, y = mouse.get_pos()
            if ev == MOUSEBUTTONDOWN:
                mouse.set_pos(
                    round(x/self.pas, 0)*self.pas,
                    round(y/self.pas, 0)*self.pas
                )

    def update(self, ev):
        #self.update_mouse_pos(ev)
        self.picture_grid.draw()
