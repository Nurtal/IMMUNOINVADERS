#!/usr/bin/python3
from classes.gameobject import GameObject

"""
A variant of invader
the hepatite virus
"""

class Invader2(GameObject):

    def __init__(self, pos):

        super(Invader2, self).__init__("./resources/images/hepatite.png")
        self.init_pos(pos)
        self.hp = 2
        self.speed = 1
