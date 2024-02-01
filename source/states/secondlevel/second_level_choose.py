import json
from time import sleep

import pygame
import os
from pygame.sprite import Group

from ...components import info, sound
from ... import tools, setup, functions
from ... import constants as c

from ...components import player


class SecondLevelChoose:
    def __init__(self):
        self.finished = False
        self.next = None
        self.start_set = True
        self.info = info.Info('second_level_1.json')
        self.setup_background()
        self.load_map_info()
        self.start_over = False

    def setup_background(self):
        self.background = setup.graphics['map_2_choose']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * 0.84),
                                                                   int(rect.height * 0.88)))
        self.background_rect = self.background.get_rect()

        self.viewport = setup.screen.get_rect()

    def load_map_info(self):
        file_name = 'second_level_choose.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

        self.information = self.map_data['information']

        self.obstacles = self.information['obstacles']
        self.obstacles_ranges = []
        for obstacle in self.obstacles:
            self.obstacles_ranges.append([obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']])

        self.passageways = self.information['passageways']
        self.passageways_ranges = []
        for passageway in self.passageways:
            self.passageways_ranges.append(
                [passageway['x'], passageway['y'], passageway['width'], passageway['height']])

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
            self.enemies_pos_1 = [(400, 300), (500, 300), (600, 300)]
            self.enemies_pos_2 = [(450, 600), (550, 600)]
            functions.setup_enemy(3, 'PA_robot', self.player, self.enemies, self.enemies_pos_1)
            functions.setup_enemy(2, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos_2)
            functions.update_blood_stored(2, self.player)
            self.start_set = False

        if self.start_over:
            functions.start_over_set(self.enemies, self.drop_items, self.ranged_weapons)
            self.player = functions.setup_player(500, 400)
            functions.load_blood_stored(2, self.player)
            self.start_over = False
            functions.setup_enemy(3, 'PA_robot', self.player, self.enemies, self.enemies_pos_1)
            functions.setup_enemy(2, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos_2)

        surface.blit(self.background, self.viewport)

        functions.update_enemies(self.enemies, self.obstacles_ranges, surface)

        # update ranged weapons
        functions.update_ranged_weapons(functions.load_weapon_name(), self.ranged_weapons, self.player, self.enemies,
                                        self.obstacles_ranges, self.drop_items, surface, keys, press)

        # update drop items
        functions.check_pick_up(keys, press, self.player, self.drop_items)
        for drop_item in self.drop_items.sprites():
            drop_item.update(surface)

        # update parameters
        functions.set_blood_bar(surface, self.player)
        functions.show_gear_num(surface)
        functions.supply_effect(self.player)
        # print(self.player.origin_health_point)

        # if the player die?
        functions.check_player_enemy_collisions(self.player, self.enemies)
        finish_life = functions.if_player_die(self.player, surface)
        if finish_life:
            self.start_over = True
            self.finished = True
            self.next = 'game_over'

        # update player
        player_passageway_type = functions.check_player_passageways_edge(self.passageways_ranges, self.player)
        player_obstacle_type = functions.check_player_obstacle_edge(self.obstacles_ranges, self.player)
        if not player_obstacle_type and not player_passageway_type:
            self.player.update(keys, press)
            functions.update_player_pos(self.player)
            surface.blit(self.player.image, self.player.rect)
        else:
            if len(self.enemies) == 0 and self.player.health_point > 0 and len(self.drop_items) == 0 and\
                    player_passageway_type:
                player_passageway_type_1 = functions.check_boss_passageways_edge(self.passageways_ranges[0],
                                                                                   self.player)
                if player_passageway_type_1 == 'go_up':
                    functions.update_blood_stored(2, self.player)
                    functions.update_state_now('tip7h')
                    self.finished = True
                    self.next = 'tip7h'
                player_passageway_type_2 = functions.check_boss_passageways_edge(self.passageways_ranges[1],
                                                                                   self.player)
                if player_passageway_type_2 == 'go_up':
                    functions.update_blood_stored(2, self.player)
                    functions.update_state_now('tip7s')
                    self.finished = True
                    self.next = 'tip7s'
                player_passageway_type_3 = functions.check_boss_passageways_edge(self.passageways_ranges[2],
                                                                                   self.player)
                if player_passageway_type_3 == 'go_up':
                    functions.update_blood_stored(2, self.player)
                    functions.update_state_now('tip7w')
                    self.finished = True
                    self.next = 'tip7w'

            elif player_obstacle_type:
                self.player.update(keys, press)
                functions.obstacle_stop_player(player_obstacle_type, self.player)
                functions.update_player_pos(self.player)
                surface.blit(self.player.image, self.player.rect)

            else:
                self.player.update(keys, press)
                functions.passageway_stop_player(player_passageway_type, self.player)
                functions.update_player_pos(self.player)
                surface.blit(self.player.image, self.player.rect)