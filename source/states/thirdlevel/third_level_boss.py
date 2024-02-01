import json

import pygame
import os
from pygame.sprite import Group

from ...components import info, sound
from ... import tools, setup, functions
from ... import constants as c

from ...components import player


class ThirdLevel:
    def __init__(self):
        self.finished = False
        self.next = None
        self.start_set = True
        self.setup_background()
        self.load_map_info()
        self.change_memory()
        self.start_over = False
        self.bgm = sound.boss_final

    def setup_background(self):
        self.background = setup.graphics['map_3_boss']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * 0.91),
                                                                   int(rect.height * 0.91)))
        self.background_rect = self.background.get_rect()

        self.viewport = setup.screen.get_rect()

    def load_map_info(self):
        file_name = 'third_level_boss.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

        self.information = self.map_data['information']

        self.obstacles = self.information['obstacles']
        self.obstacles_ranges = []
        for obstacle in self.obstacles:
            self.obstacles_ranges.append([obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']])

    def change_memory(self):
        file_name_1 = 'arrived_1.txt'
        file_path_1 = os.path.join('source/states/thirdlevel', file_name_1)
        with open(file_path_1, 'w') as f1:
            f1.write('False')
        file_name_2 = 'arrived_2.txt'
        file_path_2 = os.path.join('source/states/thirdlevel', file_name_2)
        with open(file_path_2, 'w') as f2:
            f2.write('False')
        file_name_3 = 'arrived_3.txt'
        file_path_3 = os.path.join('source/states/thirdlevel', file_name_3)
        with open(file_path_3, 'w') as f3:
            f3.write('False')
        file_name_4 = 'arrived_4.txt'
        file_path_4 = os.path.join('source/states/thirdlevel', file_name_4)
        with open(file_path_4, 'w') as f4:
            f4.write('False')

        file_name_5 = 'third_level_memory.txt'
        file_path_5 = os.path.join('source/states/thirdlevel', file_name_5)
        with open(file_path_5, 'w') as f5:
            f5.write('0')

    def update(self, surface, keys, press):
        if keys[pygame.K_ESCAPE] and press:
            sound.click.play()
            self.finished = True
            self.next = 'main_menu'
        # Initial settings
        self.change_memory()
        if self.start_set:
            self.player = functions.setup_player(500, 700)
            self.ranged_weapons = Group()
            self.enemies = Group()
            self.drop_items = Group()
            self.enemies_pos = []
            functions.setup_enemy(0, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos)
            functions.load_blood_stored(3, self.player)
            # Set BossFinal
            self.boss = functions.setup_boss(5, 440, 340)
            self.start_set = False
            self.bgm.play(-1)
        if self.start_over:
            functions.start_over_set(self.enemies, self.drop_items, self.ranged_weapons)
            self.player = functions.setup_player(500, 700)
            self.boss.health_point = self.boss.origin_health_point
            functions.load_blood_stored(3, self.player)
            self.start_over = False
            functions.setup_enemy(0, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos)
            self.bgm.play(-1)


        surface.blit(self.background, self.viewport)

        functions.update_enemies(self.enemies, self.obstacles_ranges, surface)

        # Set BossFinal
        self.boss.update()
        surface.blit(self.boss.image, (self.boss.pos_x, self.boss.pos_y))
        self.boss.draw_blood_bar(surface)
        if len(self.enemies) < 6:
            functions.summon_robots(self.player, self.enemies, [(430, 500), (480, 500), (530, 500)])
        if functions.ranged_weapon_boss_collision(self.ranged_weapons, self.boss):
            self.bgm.fadeout(100)
            self.start_over = True
            self.finished = True
            self.next = 'tip11'

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

        # if the player die?
        functions.check_player_enemy_collisions(self.player, self.enemies)
        functions.player_boss_collision(self.boss, self.player)
        finish_life = functions.if_player_die(self.player, surface)
        if finish_life:
            self.bgm.fadeout(100)
            self.start_over = True
            self.finished = True
            self.next = 'game_over'

        # update player
        player_obstacle_type = functions.check_player_obstacle_edge(self.obstacles_ranges, self.player)
        if not player_obstacle_type:
            self.player.update(keys, press)
        else:
            functions.obstacle_stop_player(player_obstacle_type, self.player)
        functions.update_player_pos(self.player)
        surface.blit(self.player.image, self.player.rect)