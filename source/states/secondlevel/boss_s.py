import json

import pygame
import os
from pygame.sprite import Group

from ...components import info, sound
from ... import tools, setup, functions
from ... import constants as c

from ...components import player


class BossS:
    def __init__(self):
        self.finished = False
        self.next = None
        self.start_set = True
        self.info = info.Info('first_level_boss.json')
        self.setup_background()
        self.load_map_info()
        self.start_over = False
        self.bgm = sound.boss

    def setup_background(self):
        self.background = setup.graphics['map_boss_s']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * 0.91),
                                                                   int(rect.height * 0.91)))
        self.background_rect = self.background.get_rect()

        self.viewport = setup.screen.get_rect()

    def load_map_info(self):
        file_name = 'boss_s.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

        self.information = self.map_data['information']

        self.obstacles = self.information['obstacles']
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
            self.enemies_pos = [(200, 350), (200, 400), (200, 450)]
            functions.setup_enemy(3, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos)
            functions.load_blood_stored(2, self.player)
            # Set Boss3
            self.boss = functions.setup_boss(3, 350, 350)
            self.start_set = False
            self.bgm.play(-1)

        if self.start_over:
            functions.start_over_set(self.enemies, self.drop_items, self.ranged_weapons)
            self.player = functions.setup_player(500, 400)
            self.boss.health_point = self.boss.origin_health_point
            functions.load_blood_stored(2, self.player)
            self.start_over = False
            functions.setup_enemy(3, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos)
            self.bgm.play(-1)

        surface.blit(self.background, self.viewport)

        functions.update_enemies(self.enemies, self.obstacles_ranges, surface)

        # Set Boss3
        self.boss.update()
        functions.update_boss3_pos(self.boss)
        surface.blit(self.boss.image, (self.boss.rect.x, self.boss.rect.y))
        self.boss.draw_blood_bar(surface)
        if functions.ranged_weapon_boss_collision(self.ranged_weapons, self.boss):
            self.bgm.fadeout(100)
            functions.update_state_now('tip8s')
            self.finished = True
            self.next = 'tip8s'

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
        # Set Boss3
        functions.boss3_hurt_player(self.boss, self.player)
        finish_life = functions.if_player_die(self.player, surface)
        if finish_life:
            self.bgm.fadeout(100)
            self.start_over = True
            self.finished = True
            self.next = 'game_over'

        player_obstacle_type = functions.check_player_obstacle_edge(self.obstacles_ranges, self.player)
        if not player_obstacle_type:
            self.player.update(keys, press)
            functions.update_player_pos(self.player)
            surface.blit(self.player.image, self.player.rect)
        else:
            if player_obstacle_type:
                surface.blit(self.background, self.viewport)
                functions.obstacle_stop_player(player_obstacle_type, self.player)
                functions.update_player_pos(self.player)
                surface.blit(self.player.image, self.player.rect)

