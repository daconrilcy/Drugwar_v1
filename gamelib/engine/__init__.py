from gamelib.location import create_location, locations, actual_location
from gamelib.Drug import create_drugs_list, drugs
from gamelib.personna import Personna
import pygame
import gamelib.inteface.windows as game_win
import gamelib.inteface.map as game_map
from gamelib.inteface.player import Player
from gamelib.poly_interact import is_collide_spr_poly


class Game:
    def __init__(self):
        # creation de la fenetre principale
        self.main_win = game_win.MainWindow()

        # chargement de la carte(tmx)
        self.game_map = game_map.MyTmx(self.main_win.screen)

        # generer un joueur
        self.player_position = self.game_map.tmx_data.get_object_by_name('player')
        self.player = Player(self.player_position.x, self.player_position.y)

        # attacher le joueur au groupe
        self.game_map.group.add(self.player)

        self.previous_city = -1
        self.mouse_pos = None

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move(0)
        elif pressed[pygame.K_DOWN]:
            self.player.move(1)
        elif pressed[pygame.K_LEFT]:
            self.player.move(2)
        elif pressed[pygame.K_RIGHT]:
            self.player.move(3)

        self.verify_check_click()

    def check_collision(self):
        for sprite in self.game_map.group.sprites():
            for wall in self.game_map.walls_poly:
                if is_collide_spr_poly(sprite.feet_position, wall):
                    sprite.move_back()
            city_n = sprite.feet_position.collidelist(self.game_map.city_obj)
            if city_n > -1:
                if self.previous_city != city_n:
                    print("georges est à " + self.game_map.city_name[city_n])
                    self.previous_city = city_n
            else:
                if self.previous_city != city_n:
                    print("georges est sortie de " + self.game_map.city_name[self.previous_city])
                    self.previous_city = city_n

    def verify_check_click(self):
        click = pygame.mouse.get_pressed(3)[0]
        if click:
            self.mouse_pos = pygame.mouse.get_pos()
            r = self.is_in_cities(self.mouse_pos[0], self.mouse_pos[1])
            self.player.move_to(self.game_map.city_obj[r].center[0], self.game_map.city_obj[r].center[1])

    def is_in_cities(self, x, y):
        n = 0
        for city in self.game_map.city_obj:
            if (x >= city.x) & (x <= city.x + city.width):
                if (y >= city.y) & (y <= city.y + city.height):
                    return n
            n += 1

        return -1

    def update(self):
        self.game_map.group.update()
        self.check_collision()


    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.game_map.group.draw(self.main_win.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()


# first Engine
"""
def main_engine():
    create_drugs_list()
    create_location()
    actual_location = locations[0]
    to_exit = False

    georges = Personna(name='George')

    print ('Bonjour Georges, bienvenue dans Dope War !')
    print_actual_situation(actual_location)
    while not to_exit:
        rep = input()
        if (rep == 'x') | (rep == 'X'):
            to_exit = True
        elif (rep == 'm') | (rep == 'M'):
            actual_location = mouvement()
            print_actual_situation(actual_location)
        elif (rep == 'b') | (rep == 'B'):
            buy(actual_location)
        elif (rep == 's') | (rep == 'S'):
            sell()
    print('Tchao')


def print_actual_situation(loc):
    print(str(loc.name).upper())
    print('Objets à vendre :')
    print(loc.objects.print_stock_datas())
    print('******************')
    print('Drogues en vente :')
    print(loc.drugs.print_stock_datas())
    print('Quel action veux tu mener ?')
    print("'x' : exit, 'm' : mouvement, 'b': buy, 's': sell")


def mouvement():
    n = 0
    for loc in locations:
        print(str(n) + " : " + loc.name)
        n += 1

    print("tapez le numero de destination")
    new_loc = input()
    if int(new_loc) >= 0 & (int(new_loc) < len(locations)):
        return locations[int(new_loc)]
    else:
        mouvement()


def buy(loc):
    print("buy drug(1) or object(2) ?")
    drop = input()
    if drop == "1":
        "Which drug do you want to buy ?"
        loc.drugs.print_stock_datas()
    if drop == "2":
        "Which object do you want to buy ?"
        loc.objects.print_stock_datas()

    pass


def sell():
    pass
"""