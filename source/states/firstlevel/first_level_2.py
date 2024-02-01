import json

import pygame
import os
from pygame.sprite import Group

from ...components import info, sound
from ... import tools, setup, functions
from ... import constants as c

from ...components import player


class FirstLevel2:
    def __init__(self):
        self.finished = False
        self.next = None
        self.start_set = True
        self.level = 1
        self.info = info.Info('first_level_2.json')
        self.setup_background()
        self.load_map_info()
        self.save_map()
        self.arrive_set = True
        self.start_over = False

    def setup_background(self):
        self.background = setup.graphics['map_1.2']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * 0.99),
                                                                   int(rect.height * 1.03)))
        self.background_rect = self.background.get_rect()

        self.viewport = setup.screen.get_rect()

    def load_map_info(self):
        file_name = 'first_level_2.json'
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

    def save_map(self):
        file_name = 'first_level_Graph.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.graph_nodes = json.load(f)

        self.nodes_info = self.graph_nodes['node']

        self.n = 3
        self.graph = tools.Graph(self.n)
        self.graph.creatMatrix()
        for node in self.nodes_info:
            self.graph.addEdge(node['x'], node['y'])

    def has_arrived(self):
        file_name_1 = 'arrived_2.txt'
        file_path_1 = os.path.join('source/states/firstlevel', file_name_1)
        with open(file_path_1, 'r') as file_to_read:
            reason = file_to_read.read()
            if reason == 'False':
                file_name_2 = 'first_level_memory.txt'
                file_path_2 = os.path.join('source/states/firstlevel', file_name_2)
                with open(file_path_2, 'r') as f1:
                    a = f1.read()
                    a1 = int(a)
                    a1 += 1
                    a2 = str(a1)
                with open(file_path_2, 'w') as f2:
                    f2.write(a2)
                with open(file_path_1, 'w') as f3:
                    f3.write('True')

    def die_in_level(self):
        file_name_1 = 'arrived_2.txt'
        file_path_1 = os.path.join('source/states/firstlevel', file_name_1)
        with open(file_path_1, 'r') as file_to_read:
            reason = file_to_read.read()
            if reason == 'True':
                file_name_2 = 'first_level_memory.txt'
                file_path_2 = os.path.join('source/states/firstlevel', file_name_2)
                with open(file_path_2, 'r') as f1:
                    a = f1.read()
                    a1 = int(a)
                    a1 -= 1
                    a2 = str(a1)
                with open(file_path_2, 'w') as f2:
                    f2.write(a2)
                with open(file_path_1, 'w') as f3:
                    f3.write('False')

    def update(self, surface, keys, press):
        if keys[pygame.K_ESCAPE] and press:
            sound.click.play()
            self.finished = True
            self.next = 'main_menu'
        # Initial settings
        self.has_arrived()
        if self.arrive_set:
            self.player = functions.setup_player(400, 400)
            functions.load_blood_stored(1, self.player)
            self.arrive_set = False
        if self.start_set:
            self.ranged_weapons = Group()
            self.enemies = Group()
            self.drop_items = Group()
            self.enemies_pos_1 = [(400, 200), (450, 200), (450, 250)]
            self.enemies_pos_2 = [(300, 500), (200, 500)]
            functions.setup_enemy(3, 'PA_robot_R', self.player, self.enemies, self.enemies_pos_1)
            functions.setup_enemy(2, 'PA_robot_O', self.player, self.enemies, self.enemies_pos_2)
            self.start_set = False

        if self.start_over:
            functions.start_over_set(self.enemies, self.drop_items, self.ranged_weapons)
            self.player = functions.setup_player(400, 400)
            functions.load_blood_stored(1, self.player)
            self.start_over = False
            functions.setup_enemy(3, 'PA_robot_R', self.player, self.enemies, self.enemies_pos_1)
            functions.setup_enemy(2, 'PA_robot_O', self.player, self.enemies, self.enemies_pos_2)

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

        # if the player die?
        functions.check_player_enemy_collisions(self.player, self.enemies)
        finish_life = functions.if_player_die(self.player, surface)
        if finish_life:
            self.start_over = True
            self.finished = True
            self.die_in_level()
            self.next = 'game_over'


        # update player
        player_passageway_type = functions.check_player_passageways_edge(self.passageways_ranges, self.player)
        player_obstacle_type = functions.check_player_obstacle_edge(self.obstacles_ranges, self.player)
        if not player_passageway_type and not player_obstacle_type:
            self.player.update(keys, press)
            functions.update_player_pos(self.player)
            surface.blit(self.player.image, self.player.rect)
        else:
            if len(self.enemies) == 0 and self.player.health_point > 0 and len(self.drop_items) == 0 and\
                    player_passageway_type:
                if player_passageway_type == 'go_left' and self.graph.hasEdge(self.level, self.level - 1):
                    functions.update_blood_stored(1, self.player)
                    self.arrive_set = True
                    self.finished = True
                    self.next = 'first_level_1'
                elif player_passageway_type == 'go_right' and self.graph.hasEdge(self.level, self.level + 1):
                    functions.update_blood_stored(1, self.player)
                    self.arrive_set = True
                    self.finished = True
                    self.next = 'first_level_3'
                elif player_passageway_type == 'go_up' and self.graph.hasEdge(self.level, self.level):
                    pass
                elif player_passageway_type == 'go_down' and self.graph.hasEdge(self.level, self.level):
                    pass
                else:
                    functions.obstacle_stop_player(player_obstacle_type, self.player)
                    functions.update_player_pos(self.player)
                    surface.blit(self.player.image, self.player.rect)

            elif player_obstacle_type:
                self.player.update(keys, press)
                functions.obstacle_stop_player(player_obstacle_type, self.player)
                functions.update_player_pos(self.player)
                surface.blit(self.player.image, self.player.rect)

            else:
                functions.passageway_stop_player(player_passageway_type, self.player)
                functions.update_player_pos(self.player)
                surface.blit(self.player.image, self.player.rect)