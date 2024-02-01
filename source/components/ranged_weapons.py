import pygame
from pygame.sprite import Sprite
from source import setup
from source import tools
import json
import os


class RangedWeapons(Sprite):
    def __init__(self, name, player):
        super().__init__()
        self.name = name
        self.player = player
        self.load_data()
        self.start_fire = True

    # Load basic data from json file
    # You can add other ranged weapons info in the file named ranged_weapon.json
    # PLUS: the format of data must be rigour same
    def load_data(self):
        file_name = 'ranged_weapons.json'
        file_path = os.path.join('source/data/chars', file_name)
        with open(file_path) as f:
            self.weapons_data = json.load(f)

        self.weapon = self.weapons_data[self.name]
        self.damage = self.weapon['damage']
        self.sheet = setup.graphics[self.weapon['image_source']]
        self.pos = self.weapon['pos']
        self.image = tools.get_graphic(self.sheet, self.pos['x'], self.pos['y'],
                                       self.pos['width'], self.pos['height'], (0, 0, 0), self.weapon['scale'])
        self.show_image = tools.get_graphic(setup.graphics['Weapons'], 0, 0, 1, 1, (0, 0, 0), 1)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery
        self.vel = self.weapon['vel']
        self.cartridge = self.weapon['cartridge']  # the top num can coexist in the screen
        self.rotate_to_left = self.weapon['rotate_to_left']  # how many 45 degree to rotate to face left
        self.x_vel = 0
        self.y_vel = 0

    def update(self, keys, press):
        # show the weapons and make them flyyyy~
        if self.start_fire:
            if self.player.face == 'right':
                self.show_image = pygame.transform.rotate(self.image,
                                                          45 * ((4 + int(self.rotate_to_left)) % 8))
                self.x_vel = self.vel
                self.y_vel = 0
            elif self.player.face == 'left':
                self.show_image = pygame.transform.rotate(self.image, 45 * int(self.rotate_to_left))
                self.x_vel = -1 * self.vel
                self.y_vel = 0
            elif self.player.face == 'up':
                self.show_image = pygame.transform.rotate(self.image,
                                                          45 * ((6 + int(self.rotate_to_left)) % 8))
                self.x_vel = 0
                self.y_vel = -1 * self.vel
            elif self.player.face == 'down':
                self.show_image = pygame.transform.rotate(self.image,
                                                          45 * ((2 + int(self.rotate_to_left)) % 8))
                self.x_vel = 0
                self.y_vel = self.vel
            self.start_fire = False

