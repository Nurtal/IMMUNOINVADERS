#!/usr/bin/python3
from classes.gameobject import GameObject


class EnnemyBullet(GameObject):

	def __init__(self, pos):

		super(EnnemyBullet, self).__init__("./resources/images/ennemy_bullet.png")
		self.init_pos(pos)
