import os
from time import sleep

import pygame

from source import setup, tools
from .. import constants as c
from .. import functions


class Tip1:
    def __init__(self):
        self.finished = False
        self.next = 'tutorial'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['tutorial']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 1.05),
                                                                   int(self.background_rect.height * 1.05)))
        self.board = tools.get_graphic(setup.graphics['board'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('Welcome to HIT!!'), (270, 360)))
        self.show_information.append((functions.create_label('满怀憧憬的你踏入了校园，'
                                                             '开启了大一生活..', size=21), (270, 380)))
        self.show_information.append((functions.create_label('这不是机器人嘛?好可ai..哎?'
                                                             '别追着我啊!', size=22), (270, 380)))
        self.show_information.append((functions.create_label('打败机器人!'), (343, 355)))
        self.show_information.append((functions.create_label('使用 WASD 进行移动!', size=30), (348, 375)))
        self.show_information.append((functions.create_label('使用 J 进行攻击!', size=30), (375, 375)))
        self.show_information.append((functions.create_label('使用 K 进行交互!', size=30), (375, 375)))
        self.show_information.append((functions.create_label('使用 I 进入商店!', size=30), (375, 375)))
        self.show_information.append((functions.create_label('使用 I/Backspace/Esc 离开商店!', size=20), (320, 375)))
        self.show_information.append((functions.create_label('使用 Esc 返回主菜单!', size=30), (340, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 9:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('tutorial')
                self.finished = True


class Tip2:
    def __init__(self):
        self.finished = False
        self.next = 'tip3'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['tutorial']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 1.05),
                                                                   int(self.background_rect.height * 1.05)))
        self.board = tools.get_graphic(setup.graphics['board'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('终于摆脱了机器人的追逐!', size=30), (300, 370)))
        self.show_information.append((functions.create_label('接下来可以安安心心地学习了，'
                                                             '嘿嘿嘿..', size=24), (265, 380)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 1:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('tip3')
                self.finished = True


class Tip3:
    def __init__(self):
        self.finished = False
        self.next = 'first_level_1'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_1.1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 1.47),
                                                                   int(self.background_rect.height * 1.53)))
        self.board = tools.get_graphic(setup.graphics['board2'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('苦苦修炼了一年的Hiter决定'
                                                             '再次挑战自我..', size=21), (270, 380)))
        self.show_information.append((functions.create_label('大二的Hiter太有魅力，吸引了更多机器人'
                                                             '..', size=21), (267, 380)))
        self.show_information.append((functions.create_label('不仅仅是机器人...', size=30), (348, 375)))
        self.show_information.append((functions.create_label('还有更难的东西在等着Hiter..', size=30), (278, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 3:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('first_level_1')
                self.finished = True


class Tip4:
    def __init__(self):
        self.finished = False
        self.next = 'first_level_boss'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_1_boss']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.99),
                                                                   int(self.background_rect.height * 1.03)))
        self.board = tools.get_graphic(setup.graphics['board2'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('终于摆脱了机器人的追逐!哈哈...', size=26), (290, 380)))
        self.show_information.append((functions.create_label('天呐!高树!是高树!', size=40), (320, 370)))
        self.show_information.append((functions.create_label('Hiter才不会不会惧怕它喷出的习题册!', size=24), (270, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('first_level_boss')
                self.finished = True


class Tip5:
    def __init__(self):
        self.finished = False
        self.next = 'tip6'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_1_boss']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.99),
                                                                   int(self.background_rect.height * 1.03)))
        self.board = tools.get_graphic(setup.graphics['board2'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.boss_bh = tools.get_graphic(setup.graphics['Boss1_bh'], 0, 0, 340, 280, (0, 0, 0), 0.7)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('啊啊啊啊啊啊啊啊...', size=25), (420, 475)))
        self.show_information.append((functions.create_label('这就是传说中的Hiter吗!', size=25), (420, 475)))
        self.show_information.append((functions.create_label('竟然有如此强大的力量!大佬大佬!', size=25), (330, 475)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))
        surface.blit(self.boss_bh, (250, 280))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('tip6')
                self.finished = True


class Tip6:
    def __init__(self):
        self.finished = False
        self.next = 'second_level_choose'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_2_choose']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.84),
                                                                   int(self.background_rect.height * 0.88)))
        self.board = tools.get_graphic(setup.graphics['board3'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('又苦苦修炼了一年的Hiter决定'
                                                             '再次挑战自我..', size=21), (265, 380)))
        self.show_information.append((functions.create_label('大三的Hiter太有魅力，又吸引了机器人'
                                                             '..', size=23), (267, 380)))
        self.show_information.append((functions.create_label('还有前方的三条路..', size=30), (348, 375)))
        self.show_information.append((functions.create_label('貌似都看不到尽头..', size=30), (348, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 3:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('second_level_choose')
                self.finished = True


class Tip7h:
    def __init__(self):
        self.finished = False
        self.next = 'boss_h'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_boss_h']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.98),
                                                                   int(self.background_rect.height * 1.02)))
        self.board = tools.get_graphic(setup.graphics['board3'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('心魔总是善于抓住人类最大的恐惧..', size=26), (275, 380)))
        self.show_information.append((functions.create_label('别害怕扰乱视野的东西..', size=35), (295, 370)))
        self.show_information.append((functions.create_label('打败最深处的恐惧才能胜利..', size=30), (285, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('boss_h')
                self.finished = True


class Tip7s:
    def __init__(self):
        self.finished = False
        self.next = 'boss_s'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_boss_s']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.91),
                                                                   int(self.background_rect.height * 0.91)))
        self.board = tools.get_graphic(setup.graphics['board3'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('嗖!', size=35), (465, 370)))
        self.show_information.append((functions.create_label('呲呲呲----', size=35), (400, 370)))
        self.show_information.append((functions.create_label('对它施以仁慈吧..', size=30), (375, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('boss_s')
                self.finished = True


class Tip7w:
    def __init__(self):
        self.finished = False
        self.next = 'boss_w'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_boss_w']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 1.21),
                                                                   int(self.background_rect.height * 1.33)))
        self.board = tools.get_graphic(setup.graphics['board3'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('感受经典中世纪风格的恐惧吧!', size=26), (300, 370)))
        self.show_information.append((functions.create_label('有时候困难不止一次..', size=35), (310, 370)))
        self.show_information.append((functions.create_label('不断挑战与探索才能胜利..', size=30), (305, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('boss_w')
                self.finished = True


class Tip8h:
    def __init__(self):
        self.finished = False
        self.next = 'tip9'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_boss_h']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.98),
                                                                   int(self.background_rect.height * 1.02)))
        self.board = tools.get_graphic(setup.graphics['board3'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.boss_bh = tools.get_graphic(setup.graphics['Boss2_bh'], 0, 0, 254, 282, (0, 0, 0), 0.7)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('大家明明都很怕我...', size=25), (420, 475)))
        self.show_information.append((functions.create_label('为..为什么你却不害怕!', size=25), (420, 475)))
        self.show_information.append((functions.create_label('天,天哪,你太可怕了,你才是心魔!', size=25), (330, 475)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))
        surface.blit(self.boss_bh, (260, 280))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('tip9')
                self.finished = True


class Tip8s:
    def __init__(self):
        self.finished = False
        self.next = 'tip9'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_boss_s']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.91),
                                                                   int(self.background_rect.height * 0.91)))
        self.board = tools.get_graphic(setup.graphics['board3'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.boss_bh = tools.get_graphic(setup.graphics['Boss3_bh'], 0, 0, 276, 264, (0, 0, 0), 0.7)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('咕噜咕噜咕噜咕噜...', size=25), (420, 475)))
        self.show_information.append((functions.create_label('呲呲呲呲呲哔哔呲呲呲呲!', size=25), (420, 475)))
        self.show_information.append((functions.create_label('咕噜咕噜咕噜咕噜谢谢你呲呲呲!!', size=25), (330, 475)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))
        surface.blit(self.boss_bh, (260, 290))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('tip9')
                self.finished = True


class Tip8w:
    def __init__(self):
        self.finished = False
        self.next = 'tip9'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_boss_w']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 1.21),
                                                                   int(self.background_rect.height * 1.33)))
        self.board = tools.get_graphic(setup.graphics['board3'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.boss_bh = tools.get_graphic(setup.graphics['Boss4_bh'], 0, 0, 268, 268, (0, 0, 0), 0.7)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('啊啊啊啊啊啊可恶...', size=25), (420, 475)))
        self.show_information.append((functions.create_label('我们竟然也会败在你手上!', size=25), (390, 475)))
        self.show_information.append((functions.create_label('你实在是太强了!实力不能小觑!', size=25), (340, 475)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))
        surface.blit(self.boss_bh, (270, 280))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('tip9')
                self.finished = True


class Tip9:
    def __init__(self):
        self.finished = False
        self.next = 'third_level_1'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_3.1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.99),
                                                                   int(self.background_rect.height * 1.03)))
        self.board = tools.get_graphic(setup.graphics['board4'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('又又苦苦修炼一年的Hiter决定'
                                                             '再次挑战自我..', size=21), (265, 380)))
        self.show_information.append((functions.create_label('大四的Hiter吸引了更多的实验室机器人'
                                                             '..', size=23), (267, 380)))
        self.show_information.append((functions.create_label('远方传来了怒吼声..', size=30), (348, 375)))
        self.show_information.append((functions.create_label('这里的机器味很重..', size=30), (348, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 3:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('third_level_1')
                self.finished = True


class Tip10:
    def __init__(self):
        self.finished = False
        self.next = 'third_level_boss'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_3_boss']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.91),
                                                                   int(self.background_rect.height * 0.91)))
        self.board = tools.get_graphic(setup.graphics['board4'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('听到了机械齿轮的巨响以及电流'
                                                             '的声音..', size=22), (265, 380)))
        self.show_information.append((functions.create_label('大概是e-academic-wand太过于耀眼'
                                                             '..', size=23), (267, 380)))
        self.show_information.append((functions.create_label('它周围发出了圣光..', size=30), (348, 375)))
        self.show_information.append((functions.create_label('是巨大的危险......', size=30), (350, 375)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 3:
                self.count += 1
                sleep(0.1)
            else:
                functions.update_state_now('third_level_boss')
                self.finished = True


class Tip11:
    def __init__(self):
        self.finished = False
        self.next = 'win'
        self.set_background()
        self.set_info()
        self.count = 0

    def set_background(self):
        self.background = setup.graphics['map_3_boss']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * 0.91),
                                                                   int(self.background_rect.height * 0.91)))
        self.board = tools.get_graphic(setup.graphics['board5'], 0, 0, 722, 422, (0, 0, 0), 0.8)
        self.boss_bh = tools.get_graphic(setup.graphics['BossFinal_bh'], 0, 0, 538, 352, (0, 0, 0), 0.7)
        self.viewport = setup.screen.get_rect()

    def set_info(self):
        self.show_information = []
        self.show_information.append((functions.create_label('你是一名合格的Hiter。', size=25), (420, 475)))
        self.show_information.append((functions.create_label('这个e-academic-wand属于你了..', size=25), (290, 475)))
        self.show_information.append((functions.create_label('你值得拥有它。', size=30), (390, 475)))

    def update(self, surface, keys, press):
        surface.blit(self.background, self.viewport)
        surface.blit(self.board, (c.TIP_1_POS[0], c.TIP_1_POS[1]))
        surface.blit(self.boss_bh, (260, 260))

        show = self.show_information[self.count]
        surface.blit(show[0], show[1])

        if keys[pygame.K_RETURN] and press:
            if self.count < 2:
                self.count += 1
                sleep(0.1)
            else:
                self.finished = True