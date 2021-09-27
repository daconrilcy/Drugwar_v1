import pyscroll

from gamelib.location import create_location, locations, actual_location
from gamelib.Drug import create_drugs_list, drugs
from gamelib.personna import Personna
import pygame
import pytmx
import pyscroll

import gamelib.inteface.windows as game_win
import gamelib.inteface.map as game_map
from gamelib.inteface.player import Player

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

    def update(self):
        self.game_map.group.update()

        # verification collision
        for sprite in self.game_map.group.sprites():
            if sprite.feet_position.collidelist(self.game_map.walls) > -1:
                sprite.move_back()

    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
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