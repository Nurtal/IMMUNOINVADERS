#!/usr/bin/python3
from classes.gameobject import GameObject


class Player(GameObject):

    def __init__(self, screen_size):

        super(Player, self).__init__("./resources/images/player.png")
        pos = (
            screen_size[0] / 2 - self.sprite.width / 2,
            screen_size[1] - self.sprite.height
        )
        self.init_pos(pos)

        self.exploding = False
        self.shoot = False
        self.shooting = False
