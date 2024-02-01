# Just for test
from time import sleep

from .. import tools, setup
from ..components import info, sound
from .. import constants as c
from .. import functions
import pygame


class ViewNote:
    def __init__(self):
        self.finished = False
        self.next = None
        self.info = info.Info('view_note')
        self.setup_background()
        self.load_note()
        self.show_note()

    def setup_background(self):
        self.bg = tools.get_graphic(setup.graphics['note_bg'], 0, 0, 1000, 840, (0, 0, 0), 1)
        self.down = tools.get_graphic(setup.graphics['down'], 0, 0, 325, 200, (0, 0, 0), 0.3)

    def load_note(self):
        self.circle_queue = tools.CircleQueue(c.BASE_NOTE_NUM)
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['PA_robot'], 0, 0, 150, 156, (0, 0, 0), 1),
                                       functions.create_label("平安银行里的智能机器人，每个新生"),
                                       functions.create_label("都会遇到。它们礼貌，可爱，敬业。"),
                                       functions.create_label("据说还有未放出的升级版本机器人。")])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['LAB_robot'], 0, 0, 94, 168, (0, 0, 0), 1),
                                       functions.create_label("LAB机器人有着工业化与军事化特质。"),
                                       functions.create_label("不同型号有着不同的能力！"),
                                       functions.create_label("小心，你可能看不见型号G。")])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['Boss1_bh'], 0, 0, 340, 280, (0, 0, 0), 1),
                                       functions.create_label("具有威慑力的高树不知道吓跑了多少"),
                                       functions.create_label("开拓者。高树不断造出练习册，定位"),
                                       functions.create_label("追踪HITER。")])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['Boss2_bh'], 0, 0, 254, 282, (0, 0, 0), 1),
                                       functions.create_label("心魔不断召唤出Shadow扰乱心灵……"),
                                       functions.create_label("只有最有勇气的HITER才能击败心魔。"),
                                       functions.create_label(" ")])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['Boss3_bh'], 0, 0, 276, 264, (0, 0, 0), 1),
                                       functions.create_label("被辐射污染的鱼类不能够控制自己……"),
                                       functions.create_label("甚至不能结束自己的生命……"),
                                       functions.create_label(" ")])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['Boss4_bh'], 0, 0, 268, 268, (0, 0, 0), 1),
                                       functions.create_label(" "),
                                       functions.create_label("大概是外来生物吧?"),
                                       functions.create_label("据说它拥有八次生命。")])
        self.circle_queue.enter_queue([tools.get_graphic(setup.graphics['BossFinal_bh'], 0, 0, 538, 352, (0, 0, 0), 1),
                                       functions.create_label(""),
                                       functions.create_label("拿到e-academic-wand的人马，"),
                                       functions.create_label("黑入所有机器人的系统并操纵了它们!")])

    def check_keys(self, keys, press):
        if keys[pygame.K_ESCAPE] and press:
            sound.click.play()
            self.finished = True
            self.next = 'main_menu'
        if keys[pygame.K_DOWN]:
            sound.click.play()
            self.show = self.circle_queue.out_queue()
            self.circle_queue.enter_queue(self.show)
            sleep(0.2)

    def show_note(self):
        self.show = self.circle_queue.out_queue()
        self.circle_queue.enter_queue(self.show)

    def update(self, surface, keys, press):
        self.check_keys(keys, press)

        surface.blit(self.bg, (0, 0))
        surface.blit(self.down, (450, 600))

        surface.blit(self.show[0], (170, 140))
        surface.blit(self.show[1], (50, 400))
        surface.blit(self.show[2], (50, 450))
        surface.blit(self.show[3], (50, 500))

        self.info.update()
        self.info.draw(surface)






