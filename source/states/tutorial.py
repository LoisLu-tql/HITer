import json
import os
import random
from time import sleep

from pygame.sprite import Group

from .. import setup, functions, tools
from ..components import info, enemy, sound
from ..components import player
import pygame
from .. import constants as c
from ..components.ranged_weapons import RangedWeapons


class Tutorial:
    def __init__(self):
        self.setup_background()
        self.finished = False
        self.next = None
        self.start_set = True
        self.load_map_info()
        self.start_over = False

    def setup_background(self):
        self.background = setup.graphics['tutorial']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 1.05),
                                                                   int(self.background_rect.height * 1.05)))
        self.viewport = setup.screen.get_rect()

    # Load the map's information from json file
    # You can set the obstacles in the json file
    def load_map_info(self):
        file_name = 'tutorial.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

        self.obstacles = self.map_data['obstacles']
        self.obstacles_ranges = []
        for obstacle in self.obstacles:
            self.obstacles_ranges.append([obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']])

    def update(self, surface, keys, press):
        if keys[pygame.K_ESCAPE] and press:
            sound.click.play()
            self.finished = True
            self.next = 'main_menu'
        # Initial settings
        if self.start_set:
            self.player = functions.setup_player(500, 400)
            self.ranged_weapons = Group()
            self.enemies = Group()
            self.drop_items = Group()
            self.enemies_pos = [(200, 400), (200, 450), (200, 500)]
            functions.setup_enemy(3, 'PA_robot', self.player, self.enemies, self.enemies_pos)
            self.start_set = False

        if self.start_over:
            functions.start_over_set(self.enemies, self.drop_items, self.ranged_weapons)
            self.player = functions.setup_player(500, 400)
            self.start_over = False
            functions.setup_enemy(3, 'PA_robot', self.player, self.enemies, self.enemies_pos)

        surface.blit(self.background, self.viewport)

        # update enemies
        functions.update_enemies(self.enemies, self.obstacles_ranges, surface)

        # update ranged weapons
        functions.update_ranged_weapons(functions.load_weapon_name(), self.ranged_weapons, self.player, self.enemies,
                                        self.obstacles_ranges, self.drop_items, surface, keys, press)

        # update drop items
        functions.check_pick_up(keys, press, self.player, self.drop_items)
        for drop_item in self.drop_items.sprites():
            drop_item.update(surface)

        # update player
        player_obstacle_type = functions.check_player_obstacle_edge(self.obstacles_ranges, self.player)
        if not player_obstacle_type:
            self.player.update(keys, press)
        else:
            functions.obstacle_stop_player(player_obstacle_type, self.player)
        functions.update_player_pos(self.player)
        surface.blit(self.player.image, self.player.rect)

        functions.set_blood_bar(surface, self.player)
        functions.show_gear_num(surface)
        functions.supply_effect(self.player)

        # if the player die?
        functions.check_player_enemy_collisions(self.player, self.enemies)

        finish_life = functions.if_player_die(self.player, surface)
        if finish_life:
            self.start_over = True
            self.finished = True
            self.next = 'game_over'

        if len(self.enemies) == 0 and self.player.health_point > 0 and len(self.drop_items) == 0:
            functions.update_state_now('tip2')
            self.start_set = True
            self.finished = True
            self.next = 'tip2'



