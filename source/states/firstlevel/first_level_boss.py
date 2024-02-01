import json

import pygame
import os
from pygame.sprite import Group

from ...components import info, sound
from ... import tools, setup, functions
from ... import constants as c

from ...components import player


class FirstLevel:
    def __init__(self):
        self.finished = False
        self.next = None
        self.start_set = True
        self.info = info.Info('first_level_boss.json')
        self.setup_background()
        self.load_map_info()
        # self.save_map()
        self.change_memory()
        self.start_over = False
        self.bgm = sound.boss

    def setup_background(self):
        self.background = setup.graphics['map_1_boss']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * 0.99),
                                                                   int(rect.height * 1.03)))
        self.background_rect = self.background.get_rect()

        self.viewport = setup.screen.get_rect()

    def load_map_info(self):
        file_name = 'first_level_boss.json'
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
        file_path_1 = os.path.join('source/states/firstlevel', file_name_1)
        with open(file_path_1, 'w') as f1:
            f1.write('False')
        file_name_2 = 'arrived_2.txt'
        file_path_2 = os.path.join('source/states/firstlevel', file_name_2)
        with open(file_path_2, 'w') as f2:
            f2.write('False')
        file_name_3 = 'arrived_3.txt'
        file_path_3 = os.path.join('source/states/firstlevel', file_name_3)
        with open(file_path_3, 'w') as f3:
            f3.write('False')

        file_name_4 = 'first_level_memory.txt'
        file_path_4 = os.path.join('source/states/firstlevel', file_name_4)
        with open(file_path_4, 'w') as f4:
            f4.write('0')

    def update(self, surface, keys, press):
        if keys[pygame.K_ESCAPE] and press:
            sound.click.play()
            self.finished = True
            self.next = 'main_menu'
        # Initial settings
        self.change_memory()

        if self.start_set:
            self.player = functions.setup_player(550, 400)
            self.ranged_weapons = Group()
            self.enemies = Group()
            self.drop_items = Group()
            self.enemies_pos = [(550, 150), (550, 200), (550, 250)]
            functions.setup_enemy(3, 'PA_robot_G', self.player, self.enemies, self.enemies_pos)
            functions.load_blood_stored(1, self.player)
            # Set Boss1
            self.b1ws = Group()
            self.boss = functions.setup_boss(1, 120, 200)
            self.start_set = False
            self.bgm.play(-1)

        if self.start_over:
            functions.start_over_set(self.enemies, self.drop_items, self.ranged_weapons)
            for b1w in self.b1ws:
                self.b1ws.remove(b1w)
            self.player = functions.setup_player(550, 400)
            self.boss.health_point = self.boss.origin_health_point
            functions.load_blood_stored(1, self.player)
            self.start_over = False
            functions.setup_enemy(3, 'PA_robot_G', self.player, self.enemies, self.enemies_pos)
            self.bgm.play(-1)

        surface.blit(self.background, self.viewport)

        functions.update_enemies(self.enemies, self.obstacles_ranges, surface)

        # Set Boss1
        self.boss.update()
        surface.blit(self.boss.image, (self.boss.pos_x, self.boss.pos_y))
        self.boss.draw_blood_bar(surface)
        if len(self.b1ws) < 6:
            functions.setup_boss1_weapon_pos(self.b1ws, self.player, self.boss.rect.centerx, self.boss.rect.centery)
        for b1w in self.b1ws.sprites():
            b1w.update()
            functions.update_boss1_weapon_pos(b1w)
            surface.blit(b1w.image, (b1w.rect.x, b1w.rect.y))
        if functions.ranged_weapon_boss_collision(self.ranged_weapons, self.boss):
            self.bgm.fadeout(100)
            functions.update_state_now('tip5')
            self.finished = True
            self.next = 'tip5'

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
        # Set Boss1
        functions.b1w_player_collision(self.b1ws, self.player)
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

