#!/usr/bin/python3
from classes.gameobject import GameObject

"""
A variant of invader
the hepatite virus
"""

class Boss(GameObject):

    def __init__(self, pos):

        super(Boss, self).__init__("./resources/images/Boss.png")
        self.init_pos(pos)
        self.hp = 8
        self.speed = 2
