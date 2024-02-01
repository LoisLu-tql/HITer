# Basic functions/classes
import os
import sys

import pygame
from . import constants as c
from .components import shop


# Load all the graphics in a list
def load_graphics(path, accept=('.jpg', '.png', '.bmp')):
    graphics = {}
    for img in os.listdir(path):
        name, extend = os.path.splitext(img)
        if extend.lower() in accept:
            graphic = pygame.image.load(os.path.join(path, img))
            if graphic.get_alpha():
                graphic = graphic.convert_alpha()  # speed up the rendering for pics with transparent bg
            else:
                graphic = graphic.convert()
            graphics[name] = graphic
    return graphics


# the graphic/ left top x/ left top y/ needed width/ needed height/ delete the bg color/ transform scale
def get_graphic(sheet, x, y, width, height, color_key, scale):
    graphic = pygame.Surface((width, height))
    graphic.blit(sheet, (0, 0), (x, y, width, height))  # x,y,w,h from sheet part
    graphic.set_colorkey(color_key)
    graphic = pygame.transform.scale(graphic, (int(width*scale), int(height*scale)))
    return graphic


class CircleQueue:
    def __init__(self, size):
        self.size = size
        self.queue = [0] * size
        self.head = 0
        self.tail = 0
        self.flag = False

    def full_or_not(self):
        return self.head == self.tail and self.flag

    def empty_or_not(self):
        return self.head == self.tail and not self.flag

    def enter_queue(self, element):
        if self.full_or_not():
            sys.exit()
        else:
            self.queue[self.tail] = element
            if self.tail == self.size - 1:
                self.tail = 0
            else:
                self.tail += 1
            self.flag = True

    def out_queue(self):
        if self.empty_or_not():
            sys.exit()

        else:
            element = self.queue[self.head]
            self.queue[self.head] = None
            if self.head == self.size - 1:
                self.head = 0
            else:
                self.head += 1
            self.flag = False
            return element


class Graph:
    def __init__(self, n, directed=False):
        self.n = n  # number of vertex
        self.m = 0  # number of edge
        self.directed = directed
        self.matrix = []

    def creatMatrix(self):
        self.matrix.clear()
        for i in range(self.n):
            self.matrix.append([])
            self.matrix[i].clear()
            for j in range(self.n):
                self.matrix[i].append(0)

    # def __str__(self):
    #     for line in self.matrix:
    #         print(str(line))
    #     return ''  # must return string

    def getNumberOfEdge(self):
        return self.m

    def getNumberOfVertex(self):
        return self.n

    def hasEdge(self, v, w):
        if 0 <= v <= self.n and 0 <= w <= self.n and self.matrix[v][w] == 1:
            return True
        else:
            return False

    def addEdge(self, v, w):
        if 0 <= v <= self.n and 0 <= w <= self.n:
            if self.hasEdge(v, w):
                return
            self.matrix[v][w] = 1
            if self.directed is False:
                self.matrix[w][v] = 1
            self.m += 1
        else:
            return


class Node:
    def __init__(self, sub_num, info_list):
        self.sub_num = sub_num
        self.info_list = info_list
        self.sub_node = []


class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, parent, sub_num, info_list):
        new_node = Node(sub_num, info_list)
        parent.sub_node.append(new_node)
        