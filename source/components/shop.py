import json
import os
import sys

import pygame

from . import sound
from .. import constants as c, functions, setup, tools
from ..tools import Tree, Node


class Shop:
    def __init__(self):
        # self.coins = 100
        self.load_price_tag()

        self.bg = pygame.image.load("./resource/graphics/shop_bg.png")
        self.shop = pygame.image.load("./resource/graphics/shop.png")
        self.show = pygame.image.load("./resource/graphics/show_goods.png")
        # self.shop2 = pygame.image.load("./resource/graphics/44.png")
        self.talk = pygame.image.load("./resource/graphics/sure.png")
        self.talk_1 = pygame.image.load("./resource/graphics/get.png")
        self.talk_2 = pygame.image.load("./resource/graphics/fail.png")

        self.font = pygame.font.Font(c.FONT, 40)
        # self.text = self.font.render("coins:" + str(self.coins), True, (0, 0, 255))

        self.load_goods()


    def load_price_tag(self):
        self.cost_list = functions.get_cost_list()
        self.SHOP1_1 = int(self.cost_list[0])
        self.SHOP1_2 = int(self.cost_list[1])
        self.SHOP1_3 = int(self.cost_list[2])
        self.SHOP1_4 = int(self.cost_list[3])
        self.SHOP1_5 = int(self.cost_list[4])
        self.SHOP1_6 = int(self.cost_list[5])
        self.SHOP1_7 = int(self.cost_list[6])
        self.SHOP1_8 = int(self.cost_list[7])
        self.SHOP1_9 = int(self.cost_list[8])

        self.SHOP2_1 = 4
        self.SHOP2_2 = 4
        self.SHOP2_3 = 4
        self.SHOP2_4 = 4


    def load_goods(self):
        self.tree = Tree()
        self.tree.root = Node(2, 'root')
        self.tree.add_node(self.tree.root, 9, '武器')
        self.tree.add_node(self.tree.root, 4, '补给')
        self.weapon_root = self.tree.root.sub_node[0]
        self.supply_root = self.tree.root.sub_node[1]

        # weapons for sale
        file_name = 'ranged_weapons.json'
        file_path = os.path.join('source/data/chars', file_name)
        with open(file_path) as f:
            self.weapons_data = json.load(f)
        name_list = ['wave', 'big_wave', 'knife', 'saw', 'normal_book', 'jl_book',
                     'e_stick', 'magic_wand', 'wood_wand']
        count = 0
        while count < 9:
            weapon = self.weapons_data[name_list[count]]
            damage = weapon['damage']
            pos = weapon['pos']
            image = tools.get_graphic(setup.graphics[weapon['image_source']], pos['x'], pos['y'],
                                           pos['width'], pos['height'], (0, 0, 0), 1.4)
            vel = weapon['vel']
            cartridge = weapon['cartridge']
            cost = weapon['cost']
            self.tree.add_node(self.weapon_root, 0, [name_list[count], damage, image, vel, cartridge, cost, count+1])
            count += 1

        # supply for sale
        self.tree.add_node(self.supply_root, 0, ['red', 1, self.SHOP2_1,
                                                 functions.create_label('你的生命上限增加+10', size=15),
                                                 tools.get_graphic(setup.graphics['animation_items2'], 0, 48, 48, 48,
                                                                   (0, 0, 0), 1.5)])
        self.tree.add_node(self.supply_root, 0, ['orange', 2, self.SHOP2_2,
                                                 functions.create_label('你的生命部分恢复+30', size=15),
                                                 tools.get_graphic(setup.graphics['animation_items2'], 144, 48, 48, 48,
                                                                   (0, 0, 0), 1.5)])
        self.tree.add_node(self.supply_root, 0, ['green', 3, self.SHOP2_3,
                                                 functions.create_label('增加你的行走速度+3', size=15),
                                                 tools.get_graphic(setup.graphics['animation_items2'], 288, 48, 48, 48,
                                                                   (0, 0, 0), 1.5)])
        self.tree.add_node(self.supply_root, 0, ['blue', 4, self.SHOP2_4,
                                                 functions.create_label('可与敌人互相伤害+5', size=15),
                                                 tools.get_graphic(setup.graphics['animation_items2'], 432, 48, 48, 48,
                                                                   (0, 0, 0), 1.5)])


    def shop_open(self, screen, clock):
        # 光标
        cursor = pygame.sprite.Sprite()
        cursor.image = pygame.image.load("./resource/graphics/shop_cursor.png")
        rect = cursor.image.get_rect()
        rect.x = 345
        rect.y = 500
        cursor.rect = rect
        cursor.state = 'A'
        left = True
        pygame.display.update()

        while True:
            clock.tick(30)
            for event0 in pygame.event.get():
                if event0.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                elif event0.type == pygame.KEYDOWN:
                    sound.click.play()
                    if event0.key == pygame.K_i or event0.key == pygame.K_ESCAPE or event0.key == pygame.K_BACKSPACE:
                        return False
                    if event0.key == pygame.K_RIGHT and left:
                        cursor.rect.x += 300
                        cursor.state = 'B'
                        left = False
                    elif event0.key == pygame.K_LEFT and not left:
                        cursor.rect.x -= 300
                        cursor.state = 'A'
                        left = True
                    elif event0.key == pygame.K_RETURN:
                        if cursor.state == 'A':
                            self.buy1(screen)
                        elif cursor.state == 'B':
                            self.buy2(screen)

            screen.blit(self.bg, c.SHOP_BG_POS)
            screen.blit(self.shop, c.SHOP_POS)
            screen.blit(cursor.image, cursor.rect)
            functions.show_gear_num(screen, icon_pos=c.SHOP_GEAR_ICON_POS, num_pos=c.SHOP_GEAR_POS)
            screen.blit(functions.create_label(self.weapon_root.info_list, size=30), (325, 350))
            screen.blit(functions.create_label(self.supply_root.info_list, size=30), (620, 350))
            # screen.blit(self.text, (450, 60))
            pygame.display.update()

    def update_shop_1(self, screen):
        screen.blit(self.bg, c.SHOP_BG_POS)
        screen.blit(self.show, c.SHOP1_POS)
        functions.show_gear_num(screen, icon_pos=c.SHOP_GEAR_ICON_POS, num_pos=c.SHOP_GEAR_POS)
        screen.blit(functions.create_label('伤害', size=20), (175, 410))
        screen.blit(functions.create_label('速度', size=20), (175, 430))
        screen.blit(functions.create_label('弹匣', size=20), (175, 450))
        screen.blit(functions.create_label('价格', size=20), (175, 470))
        screen.blit(functions.create_label('商品编号', size=18), (160, 490))
        count = 0
        while count < 9:
            weapon = self.weapon_root.sub_node[count]
            screen.blit(weapon.info_list[2], (200+count*70, 310))
            screen.blit(functions.create_label(str(weapon.info_list[1]), size=20), (240+count*65, 410))
            screen.blit(functions.create_label(str(weapon.info_list[3]), size=20), (240+count*65, 430))
            screen.blit(functions.create_label(str(weapon.info_list[4]), size=20), (240+count*65, 450))
            # screen.blit(functions.create_label(str(weapon.info_list[5]), size=20), (250+count*65, 470))
            screen.blit(functions.create_label(str(weapon.info_list[6]), size=20), (240+count*65, 490))
            count += 1
        # screen.blit(self.text, (450, 60))
        screen.blit(functions.create_label(str(self.SHOP1_1), size=20), (240, 470))
        screen.blit(functions.create_label(str(self.SHOP1_2), size=20), (305, 470))
        screen.blit(functions.create_label(str(self.SHOP1_3), size=20), (370, 470))
        screen.blit(functions.create_label(str(self.SHOP1_4), size=20), (435, 470))
        screen.blit(functions.create_label(str(self.SHOP1_5), size=20), (500, 470))
        screen.blit(functions.create_label(str(self.SHOP1_6), size=20), (565, 470))
        screen.blit(functions.create_label(str(self.SHOP1_7), size=20), (630, 470))
        screen.blit(functions.create_label(str(self.SHOP1_8), size=20), (695, 470))
        screen.blit(functions.create_label(str(self.SHOP1_9), size=20), (760, 470))

        screen.blit(functions.create_label('按下相应商品编号购买或切换武器', size=22), (200, 550))
        pygame.display.update()

    def update_shop_2(self, screen):
        screen.blit(self.bg, c.SHOP_BG_POS)
        screen.blit(self.show, c.SHOP2_POS)
        functions.show_gear_num(screen, icon_pos=c.SHOP_GEAR_ICON_POS, num_pos=c.SHOP_GEAR_POS)
        screen.blit(functions.create_label('价格', size=20), (160, 440))
        screen.blit(functions.create_label('商品编号', size=18), (142, 460))
        screen.blit(functions.create_label('按下相应商品编号购买', size=22), (200, 520))
        screen.blit(functions.create_label('购买后仅在关闭商店后的游戏场景中有效,属于一次性用品!', size=22), (200, 550))
        count = 0
        while count < 4:
            supply = self.supply_root.sub_node[count]
            screen.blit(supply.info_list[4], (210+count*180, 310))
            screen.blit(supply.info_list[3], (160+count*180, 420))
            screen.blit(functions.create_label(str(supply.info_list[2]), size=20), (250+count*180, 440))
            screen.blit(functions.create_label(str(supply.info_list[1]), size=20), (250+count*180, 460))
            count += 1
        # screen.blit(self.text, (450, 60))
        pygame.display.update()

    def buy1(self, screen):
        self.update_shop_1(screen)
        while True:
            for event1 in pygame.event.get():
                if event1.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                if event1.type == pygame.KEYDOWN:
                    sound.click.play()
                    if event1.key == pygame.K_1:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_1, self.weapon_root.sub_node[0].info_list[0], 1)

                    elif event1.key == pygame.K_2:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_2, self.weapon_root.sub_node[1].info_list[0], 2)

                    elif event1.key == pygame.K_3:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_3, self.weapon_root.sub_node[2].info_list[0], 3)

                    elif event1.key == pygame.K_4:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_4, self.weapon_root.sub_node[3].info_list[0], 4)

                    elif event1.key == pygame.K_5:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_5, self.weapon_root.sub_node[4].info_list[0], 5)

                    elif event1.key == pygame.K_6:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_6, self.weapon_root.sub_node[5].info_list[0], 6)

                    elif event1.key == pygame.K_7:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_7, self.weapon_root.sub_node[6].info_list[0], 7)

                    elif event1.key == pygame.K_8:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_8, self.weapon_root.sub_node[7].info_list[0], 8)

                    elif event1.key == pygame.K_9:
                        functions.buying(self.update_shop_1, 1, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP1_9, self.weapon_root.sub_node[8].info_list[0], 9)

                    elif event1.key == pygame.K_i or event1.key == pygame.K_ESCAPE or event1.key == pygame.K_BACKSPACE:
                        return
            self.load_price_tag()
            self.update_shop_1(screen)

    def buy2(self, screen):
        self.update_shop_2(screen)
        while True:
            for event2 in pygame.event.get():
                if event2.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()

                if event2.type == pygame.KEYDOWN:
                    sound.click.play()
                    if event2.key == pygame.K_1:
                        functions.buying(self.update_shop_2, 2, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP2_1, self.supply_root.sub_node[0].info_list[0], 1)

                    elif event2.key == pygame.K_2:
                        functions.buying(self.update_shop_2, 2, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP2_2, self.supply_root.sub_node[1].info_list[0], 2)

                    elif event2.key == pygame.K_3:
                        functions.buying(self.update_shop_2, 2, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP2_3, self.supply_root.sub_node[2].info_list[0], 3)

                    elif event2.key == pygame.K_4:
                        functions.buying(self.update_shop_2, 2, screen, self.talk, self.talk_1, self.talk_2,
                                         self.SHOP2_4, self.supply_root.sub_node[3].info_list[0], 4)

                    elif event2.key == pygame.K_i or event2.key == pygame.K_ESCAPE or event2.key == pygame.K_BACKSPACE:
                        return

            self.update_shop_2(screen)
