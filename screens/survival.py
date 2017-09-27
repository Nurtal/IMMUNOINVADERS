#!/usr/bin/python3
import sys
import pygame

from pygame.locals import *

from random import randint
from classes.player import Player
from classes.bullet import Bullet
from classes.ennemybullet import EnnemyBullet
from classes.invader import Invader
from classes.invader2 import Invader2
from classes.life import Life



import eztext

pygame.init()


class Survival:

	def __init__(self, screen):

		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
		self.screen_size = self.scr_width, self.scr_height

		# Background Game
		self.bg = pygame.image.load("resources/images/game_bg_origin.jpeg")
		self.bg_rect = self.bg.get_rect()

		# Sound Game
		self.audio_activate = True
		try:
			self.victory_sound = pygame.mixer.Sound('resources/sounds/victory.wav')
			self.victory_sound.set_volume(0.2)
			self.laser_sound = pygame.mixer.Sound('resources/sounds/laser_shot.wav')
			self.laser_sound.set_volume(0.2)
		except:
			self.audio_activate = False

		# Labels
		self.font = pygame.font.SysFont(None, 100)
		self.label_game_over = self.font.render("Game Over", 1, (255, 255, 255))
		self.label_victory = self.font.render("Victory is yours", 1, (255, 255, 255))
		self.label_new_wave = self.font.render("New Wave !", 1, (255, 255, 255))

		## Score
		self.score = 0

		# Life Bar
		self.lifes = []
		self.lifes_number = 3

		## Invaders
		self.invaders = []

		# Spaceship and bullets
		self.player = Player(self.screen_size)
		self.init_pos_bullet = (
			self.player.sprite.x + self.player.sprite.width / 2, self.player.sprite.y
		)
		self.bullet = Bullet(self.init_pos_bullet)

		self.game_over = False
		self.victory = False
		self.escape_selected = False

		# Objects initialisation
		self.randinvader = ()
		self.ennemybullet = ()

		# Invaders
		self.has_already_chosen = False
		# Go down every second
		self.nasty_move_time = 1
		# Invader shoot duration
		self.nasty_shoot_time = 1000

		self.invaders_moving = False
		self.invader_exploding = False

		## Weapons
		self.weapons_list = ["slow", "fast"]
		self.current_weapon = "fast"
		self.current_weapon_index = 0

		# Time Variables
		self.clock = pygame.time.Clock()

		# Timer for invaders vertical moving
		self.timecount_m = 0

		# Time for invader bullet vertical moving
		self.timecount = 0

		## Init score count
		self.init_score_x = self.scr_width - 180

		## Init Invaders
		wave_line = []
		position_taken = []
		self.init_x = 10
		self.number_of_ennemy = 10

		for i in range(0, self.number_of_ennemy):
			flip_the_coin = randint(0,100)
			if(flip_the_coin > 50):
				self.invaders.append(Invader((self.init_x, 10)))
				self.init_x += 50
			else:
				self.invaders.append(Invader2((self.init_x , 10)))
				self.init_x += 70


		# Init life bar
		self.init_life_x = self.scr_width - 120
		for i in range(self.lifes_number):
			self.lifes.append(Life((self.init_life_x, 0)))
			self.init_life_x += 40



	def run(self):
		mainloop = True
		while mainloop:
			self.clock.tick(50)
			self.screen.fill([0, 0, 0])
			self.screen.blit(self.bg, self.bg_rect)

			# Close the game when the red cross is clicked
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			# Keyboard Events
			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT]:
				if self.player.sprite.x -20 > 0:
					self.player.sprite.x -= 20
					if self.player.shooting is False:
						self.bullet.sprite.x -= 20
			elif keys[pygame.K_RIGHT]:
				if self.player.sprite.x + 20 < self.scr_width - 55:
					self.player.sprite.x += 20
					if self.player.shooting is False:
						self.bullet.sprite.x += 20
			elif keys[pygame.K_SPACE]:
				self.player.shoot = True
			elif keys[pygame.K_RSHIFT]:
				number_of_weapon = len(self.weapons_list)
				if(self.current_weapon_index == number_of_weapon-1):
					self.current_weapon_index = 0
				else:
					self.current_weapon_index += 1				
				self.current_weapon = self.weapons_list[self.current_weapon_index]
			elif keys[pygame.K_ESCAPE]:
				# Go back to the game menu
				mainloop = False
				self.escape_selected = True
				if self.audio_activate:
					pygame.mixer.music.rewind()



			if self.player.shoot is True:
				if self.audio_activate:
					self.laser_sound.play()

				if self.bullet.sprite.y > 0 and self.invader_exploding is False:
					self.player.shooting = True
					if self.current_weapon == "slow":
						self.bullet.sprite = self.bullet.sprite.move([0, -5])
						self.bullet.power = 2
					elif self.current_weapon == "fast":
						self.bullet.sprite = self.bullet.sprite.move([0, -25])
						self.bullet.power = 1
				else:
					if self.audio_activate:
						self.laser_sound.fadeout(1000)
					self.bullet.sprite.x, self.bullet.sprite.y = (
						self.player.sprite.x + self.player.sprite.width / 2, self.player.sprite.y
					)

					self.player.shoot = False
					self.player.shooting = False
					self.invader_exploding = False



			item_to_remove = None

			# Invader Colision + Vertical Movement

			# Allow slowly vertical movement
			if self.timecount_m > self.nasty_move_time:
				self.invaders_moving = True
			else:
				self.invaders_moving = False
				self.timecount_m += self.clock.get_time()

			if len(self.invaders) > 0:
				for i, invader in enumerate(self.invaders):
					if invader.sprite.collidepoint(
						self.bullet.sprite.x, self.bullet.sprite.y
					):

						invader.hp -= self.bullet.power
						if(invader.hp <= 0):
							item_to_remove = i
						
						self.invader_exploding = True
						self.score += 1

					else:
						if self.invaders_moving and not self.game_over:
							invader.sprite.y += invader.speed
							self.timecount_m = 0

							## Game over when get out of the screen
							if invader.sprite.y > self.scr_height:
								self.game_over = True

						self.screen.blit(invader.image, invader.sprite)

			# Remove dead invaders:
			if item_to_remove is not None:
				del self.invaders[item_to_remove]


			if not self.has_already_chosen:

				# Select random invader among survivor invaders

				if len(self.invaders) > 0 and not self.game_over:
					if len(self.invaders) is not 1:
						self.randinvader = self.invaders[randint(1, len(self.invaders) - 1)]
					else:
						self.randinvader = self.invaders[0]

					self.has_already_chosen = True
					posx = self.randinvader.sprite.x
					width = self.randinvader.sprite.width
					height = self.randinvader.sprite.height
					posy = self.randinvader.sprite.y

					self.ennemybullet =EnnemyBullet((posx + width / 2, posy + height))
				else:
					self.victory = True



			self.timecount += self.clock.get_time()

			# Handle the bullet shot by the random invader
			if self.timecount > self.nasty_shoot_time and self.has_already_chosen:
				self.timecount = 0
				self.has_already_chosen = False

			elif self.timecount < self.nasty_shoot_time and self.has_already_chosen:
				if self.ennemybullet.sprite.y < self.scr_height:

					lateral_move = 0
					flip_the_coin = randint(0,100)
					if(flip_the_coin >= 45):
						if(self.ennemybullet.sprite.y + 12 < self.scr_width - 10):
							lateral_move = 12
						else:
							lateral_move = -12

					if(flip_the_coin >= 65):
						if(self.ennemybullet.sprite.y - 12 > 10):
							lateral_move = -12
						else:
							lateral_move = 12

					self.ennemybullet.sprite = self.ennemybullet.sprite.move([lateral_move, 17])
					self.screen.blit(self.ennemybullet.image, self.ennemybullet.sprite)




			# Shuttle Displaying and Colision
			if self.player.sprite.collidepoint(
				self.ennemybullet.sprite.x, self.ennemybullet.sprite.y
			) and self.player.exploding is False:
				self.timecount = self.nasty_shoot_time
				self.has_already_chosen = False
				self.player.exploding = True
			else:
				self.screen.blit(self.bullet.image, self.bullet.sprite)
				self.screen.blit(self.player.image, self.player.sprite)

			# Life Management and Displaying
			if self.player.exploding:
				self.player.exploding = False
				if len(self.lifes) > 0:
					self.lifes.pop()
				else:
					self.game_over = True
					self.player.exploding = False


			# Remaining lifes
			pygame.draw.rect(
				self.screen, (255, 255, 255), [self.scr_width - 120, 0, 120, 40], 1
			)

			for life in self.lifes:
				self.screen.blit(life.image, life.sprite)

			if self.victory:
			
				## TODO : add victory sound
				if self.audio_activate:
						self.victory_sound.play()


				# New wave messages
				self.screen.blit(
					self.label_new_wave,
					(
						self.scr_width / 2 - self.label_new_wave.get_rect().width / 2,
						self.scr_height / 2 - self.label_new_wave.get_rect().height / 2
					)	
				)

				pygame.display.flip()

				pygame.time.delay(1000)

				## Init Invaders
				self.init_x = 10
				self.number_of_ennemy = 10
				for i in range(0, self.number_of_ennemy):
					flip_the_coin = randint(0,100)
					if(flip_the_coin > 50):
						self.invaders.append(Invader((self.init_x, 10)))
						self.init_x += 50
					else:
						self.invaders.append(Invader2((self.init_x , 10)))
						self.init_x += 70

				self.victory = False


			## Display score
			self.label_score = self.font.render(str(self.score), 1, (255, 255, 255))
			self.screen.blit(self.label_score, [self.scr_width - 90, 70, 120, 40])

			if self.game_over:
				self.screen.blit(
					self.label_game_over,
					(
						self.scr_width / 2 - self.label_game_over.get_rect().width / 2,
						self.scr_height / 2 - self.label_game_over.get_rect().height / 2
					)
				)


				## Get the player name
				## TODO: embellir le truc
				clock = pygame.time.Clock()
				player_name = ""
				txtbx = eztext.Input(maxlength=45, color=(255,255,255), prompt="Enter Your Name: ")
				while 1:
					clock.tick(30)
					events = pygame.event.get()
					for event in events:

						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_RETURN:
								player_name = str(txtbx.value)
								## Write player name and score in scores file
								score_file = open("resources/scores.csv", "a")
								score_file.write(str(player_name)+","+str(self.score)+"\n")
								score_file.close()
								return
						elif event.type == QUIT:
							return
					self.screen.fill((0,76,153))
					txtbx.update(events)
					txtbx.draw(self.screen)
					pygame.display.flip()


			pygame.display.flip()

			if self.game_over or self.victory:
				pygame.time.delay(4000)
				mainloop = False
