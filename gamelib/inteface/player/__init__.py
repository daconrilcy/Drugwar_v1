import pygame
from math import sqrt

_type_action = ['move', 'fire']


class ActionSprite:
    def __init__(self, speed: float, key: pygame.key, command=None, type_action: int = 0):
        self.speed: float = speed
        self.key: pygame.key = key
        self.command = command
        self.active = False
        self.type_action = type_action


class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Player, self).__init__()
        self.sprite_sheet = pygame.image.load(
            '..\gamelib\inteface\player\player_simple.png')
        self.image = self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.speed_move = 2
        self.feet_position = pygame.Rect(0, 0, self.rect.width * 0.3, 5)
        self.old_position = self.position.copy()
        self.is_moving = False
        self.target_move = None
        self.delta_x = 0
        self.delta_y = 0
        self.cos_di = 0
        self.sin_di = 0
        self.rang_image = 0
        self.n_image = 6
        self.images = {
            "down":
                [self.get_image(0, 0), self.get_image(32, 0), self.get_image(64, 0),
                 self.get_image(96, 0), self.get_image(128, 0), self.get_image(160, 0)],
            "up": [self.get_image(0, 96), self.get_image(32, 96), self.get_image(64, 96),
                   self.get_image(96, 96), self.get_image(128, 96), self.get_image(160, 96)],
            "left": [self.get_image(0, 32), self.get_image(32, 32), self.get_image(64, 32),
                     self.get_image(96, 32), self.get_image(128, 32), self.get_image(160, 32)],
            "right": [self.get_image(0, 64), self.get_image(32, 64), self.get_image(64, 64),
                      self.get_image(96, 64), self.get_image(128, 64), self.get_image(160, 64)],
        }
        self.move_up = ActionSprite(-self.speed_move, pygame.K_UP, 'up')
        self.move_down = ActionSprite(self.speed_move, pygame.K_DOWN, 'down')
        self.move_left = ActionSprite(-self.speed_move, pygame.K_LEFT, 'left')
        self.move_right = ActionSprite(self.speed_move, pygame.K_RIGHT, 'right')
        self.actions = [self.move_up, self.move_down, self.move_left, self.move_right]

        self.actions_encours = []

        self.delai_ini = 100
        self.delai = self.delai_ini

    def save_location(self):
        self.old_position = self.position.copy()

    def get_image(self, x, y):
        image = pygame.Surface([32, 32], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), pygame.Rect(x, y, 32, 32))
        return image

    def change_animation(self, name: str):
        n_im = int(self.rang_image)
        if n_im > self.n_image - 1:
            n_im = self.n_image - 1
        self.image = self.images[name][n_im]
        # self.image.set_colorkey([0, 0, 0])
        self.rang_image = self.rang_image + 24 / 60 / 2

        if self.rang_image >= self.n_image:
            self.rang_image = 0

    def move_to(self, x, y):
        self.is_moving = True
        self.target_move = (x, y)
        self.delta_x = x - self.position[0]
        self.delta_y = y - self.position[1]

        dist = sqrt(self.delta_x ** 2 + self.delta_y ** 2)
        if dist != 0:
            self.sin_di = self.delta_y / dist
            self.cos_di = self.delta_x / dist
        else:
            self.sin_di = 0
            self.cos_di = 0

    def __auto_move(self):
        delta_x = self.target_move[0] - self.position[0]
        delta_y = self.target_move[1] - self.position[1]
        if abs(delta_x) > self.speed_move:
            self.position[0] += self.speed_move * self.cos_di
            if self.position[0] < 0:
                self.position[0] = 0
        else:
            self.position[0] = self.target_move[0]

        if abs(delta_y) > self.speed_move:
            self.position[1] += self.speed_move * self.sin_di
            if self.position[1] < 0:
                self.position[1] = 0
        else:
            self.position[1] = self.target_move[1]

        if self.position == self.target_move:
            self.is_moving = False

    def action_key(self, key: pygame.key, type_event):
        action_to_do = None
        for action in self.actions:
            if key == action.key:
                action_to_do = action
                break

        is_already_in = False
        del_action = None

        if action_to_do is not None:
            for act_encours in self.actions_encours:
                if act_encours == action_to_do:
                    is_already_in = True
                    del_action = act_encours
                    break
            if not is_already_in:
                if type_event == "down":
                    self.actions_encours.append(action_to_do)
            else:
                if type_event == "up":
                    if len(self.actions_encours) > 0:
                        self.actions_encours.remove(del_action)

    def do_action(self):
        for action in self.actions_encours:
            if (action == self.move_up) | (action == self.move_down):
                self.position[1] += action.speed
            elif (action == self.move_left) | (action == self.move_right):
                self.position[0] += action.speed
            self.change_animation(action.command)

            if self.position[0] < 0:
                self.position[0] = 0
            if self.position[1] < 0:
                self.position[1] = 0

    def update(self):
        if self.is_moving:
            self.__auto_move()
        self.do_action()
        self.rect.center = self.position
        self.feet_position.midbottom = self.rect.midbottom

    def stop(self):
        self.actions_encours = []

    def move_back(self):
        self.is_moving = False
        self.position = self.old_position
        self.rect.center = self.position
        self.feet_position.midbottom = self.rect.midbottom
