import json

import pygame
import os
from pygame.sprite import Group

from ...components import info, sound
from ... import tools, setup, functions
from ... import constants as c

from ...components import player


class BossW:
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
        self.background = setup.graphics['map_boss_w']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * 1.21),
                                                                   int(rect.height * 1.33)))
        self.background_rect = self.background.get_rect()

        self.viewport = setup.screen.get_rect()

    def load_map_info(self):
        file_name = 'boss_w.json'
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
            self.player = functions.setup_player(500, 600)
            self.ranged_weapons = Group()
            self.enemies = Group()
            self.drop_items = Group()
            self.enemies_pos = [(200, 550), (200, 600), (200, 650)]
            functions.setup_enemy(3, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos)
            functions.load_blood_stored(2, self.player)
            # Set Boss4
            self.b4ws = Group()
            self.boss = functions.setup_boss(4, 480, 100)
            self.start_set = False
            self.bgm.play(-1)

        if self.start_over:
            functions.start_over_set(self.enemies, self.drop_items, self.ranged_weapons)
            for b4w in self.b4ws:
                self.b4ws.remove(b4w)
            self.player = functions.setup_player(500, 600)
            self.boss.health_point = self.boss.origin_health_point
            functions.load_blood_stored(2, self.player)
            self.start_over = False
            functions.setup_enemy(3, 'LAB_robot_B', self.player, self.enemies, self.enemies_pos)
            self.bgm.play(-1)

        surface.blit(self.background, self.viewport)

        functions.update_enemies(self.enemies, self.obstacles_ranges, surface)

        # Set Boss4
        self.boss.update()
        surface.blit(self.boss.image, (self.boss.pos_x, self.boss.pos_y))
        self.boss.draw_blood_bar(surface)
        if len(self.b4ws) < 8:
            functions.setup_boss4_weapon_pos(self.b4ws, self.boss.rect.centerx, self.boss.rect.centery)
        for b4w in self.b4ws.sprites():
            b4w.update()
            functions.update_boss4_weapon_pos(b4w)
            surface.blit(b4w.image, (b4w.rect.x, b4w.rect.y))
        functions.boss4_reborn(self.boss, self.ranged_weapons)
        if self.boss.health_point <= 0 and self.boss.life >= 8:
            self.bgm.fadeout(100)
            functions.update_state_now('tip8w')
            self.finished = True
            self.next = 'tip8w'

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
        # Set Boss4
        functions.b4w_player_or_edge_collision(self.b4ws, self.player)
        functions.player_boss_collision(self.boss, self.player)
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

