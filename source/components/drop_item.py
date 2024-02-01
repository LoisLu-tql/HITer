# Manage the drop items when player kills enemies
import os
import random
import pygame

from source import setup, tools
from source.components import sound


class DropItem(pygame.sprite.Sprite):
    # Initial drop item settings
    def __init__(self, pos_x, pos_y):
        super(DropItem, self).__init__()
        self.be_picked_up = False
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.center_x = pos_x + 16
        self.center_y = pos_y + 16
        self.choices = []
        self.load_choices()
        self.random_drop()

    # You can add choices here about what will fall when an enemy dies
    def load_choices(self):
        sheet = setup.graphics['items']
        self.choices.append(["none", tools.get_graphic(sheet, 0, 0, 32, 32, (0, 0, 0), 1)])
        self.choices.append(["gear", tools.get_graphic(sheet, 96, 160, 32, 32, (0, 0, 0), 1)])
        self.choices.append(["blood", tools.get_graphic(sheet, 128, 160, 32, 32, (0, 0, 0), 1)])

    # You can set the corresponding probability about the choices
    # The codes are a little bit ugly [/facepalm]
    def random_drop(self):
        random_choice = random.randint(1, 100)
        if 1 <= random_choice <= 60:
            self.choice = self.choices[1]
        elif 60 < random_choice <= 80:
            self.choice = self.choices[2]
        else:
            self.choice = self.choices[0]
        self.image = self.choice[1]

    # You can set what will happen if the player picks the item up
    def have_an_impact(self, player):
        if self.choice[0] == "none":
            pass
        elif self.choice[0] == "gear":  # Maybe we can use gear to represent money cause i cant find a money icon
            file_name = 'gear_num.txt'
            file_path = os.path.join('source/memory', file_name)
            with open(file_path, 'r') as f:
                gear_num = int(f.read())
            with open(file_path, 'w') as f:
                f.write(str(gear_num+1))
            sound.pick_up_gear.play()

        elif self.choice[0] == "blood":
            if player.health_point <= player.origin_health_point - 10:
                player.health_point += 10
            else:
                player.health_point = player.origin_health_point
            sound.pick_up_hp.play()

    # Draw the item
    def update(self, surface):
        surface.blit(self.image, (self.pos_x, self.pos_y))