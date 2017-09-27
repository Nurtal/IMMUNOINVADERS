#!/usr/bin/python3
import sys
import pygame
from random import randint
from classes.player import Player
from classes.bullet import Bullet
from classes.ennemybullet import EnnemyBullet
from classes.invader import Invader
from classes.invader2 import Invader2
from classes.boss import Boss
from classes.life import Life

pygame.init()


class Game:

	def __init__(self, screen):

		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
		self.screen_size = self.scr_width, self.scr_height

		## Level
		self.game_level = 1
		self.game_level_max = 5

		# Background Game
		self.bg = pygame.image.load("resources/images/game_bg_origin.jpeg")
		self.bg_rect = self.bg.get_rect()

		# Sound Game
		self.audio_activate = True
		try:
			self.victory_sound = pygame.mixer.Sound('resources/sounds/victory.wav')
			self.laser_sound = pygame.mixer.Sound('resources/sounds/laser_shot.wav')
			self.laser_sound.set_volume(0.2)
		except:
			self.audio_activate = False


		# Labels
		self.font = pygame.font.SysFont(None, 100)
		self.label_game_over = self.font.render("Game Over", 1, (255, 255, 255))
		self.label_victory = self.font.render("Victoire !", 1, (255, 255, 255))
		self.label_next_level = self.font.render("Niveau "+str(self.game_level+1)+" !", 1, (255, 255, 255))

		# Life Bar
		self.lifes = []
		self.lifes_number = 3

		# Invaders
		self.invaders = []
		self.invaders_number = 5

		# Spaceship and bullets
		self.player = Player(self.screen_size)
		self.init_pos_bullet = (
			self.player.sprite.x + self.player.sprite.width / 2, self.player.sprite.y
		)

		self.bullet = Bullet(self.init_pos_bullet)
		

		## Multiple bullets [TEST]
		self.bullets_fired = []
		self.max_bullets = 10
		
		

		self.game_over = False
		self.victory = False
		self.escape_selected = False

		# Objects initialisation
		self.randinvader = ()
		self.ennemybullet = ()
		self.ennemybullet_2 = ()
		self.ennemybullet_3 = ()
		self.boss_deplacement_vector = []
		self.position_in_deplacement_vector = 0

		# Invaders
		self.has_already_chosen = False
		# Go down every second
		self.nasty_move_time = 10
		# Invader shoot duration
		self.nasty_shoot_time = 3000
		self.boss_lateral_move = 1

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

		# Init Invaders
		self.init_x = 75
		for i in range(self.invaders_number):
			self.invaders.append(Invader((self.init_x, 10)))
			self.init_x += 100


		# Init life bar
		self.init_life_x = self.scr_width - 120

		for i in range(self.lifes_number):
			self.lifes.append(Life((self.init_life_x, 0)))
			self.init_life_x += 40

	def run(self):
		mainloop = True
		while mainloop:
			self.clock.tick(60)
			self.screen.fill([0, 0, 0])
			self.screen.blit(self.bg, self.bg_rect)

			# Close the game when the red cross is clicked
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			# Keyboard Events
			keys = pygame.key.get_pressed()

			if keys[pygame.K_LEFT]:
				if self.player.sprite.x -10 > 0:
					self.player.sprite.x -= 10
					if self.player.shooting is False:
						self.bullet.sprite.x -= 10
			elif keys[pygame.K_RIGHT]:
				if self.player.sprite.x + 10 < self.scr_width - 55:
					self.player.sprite.x += 10
					if self.player.shooting is False:
						self.bullet.sprite.x += 10
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

				"""
				## Multiple bullets [TEST]
				if(len(self.bullets_fired) <= self.max_bullets):
					print("tardis")
					self.init_pos_bullet = (self.player.sprite.x + self.player.sprite.width / 2, self.player.sprite.y)
					self.bullets_fired.append(Bullet(self.init_pos_bullet))
				for ac in self.bullets_fired:
					self.player.shooting = True
					ac.sprite = ac.sprite.move([0, -14])
				"""

				if self.bullet.sprite.y > 0 and self.invader_exploding is False:
					self.player.shooting = True
					if self.current_weapon == "slow":
						self.bullet.sprite = self.bullet.sprite.move([0, -5])
					elif self.current_weapon == "fast":
						self.bullet.sprite = self.bullet.sprite.move([0, -18])

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
						invader.hp -= 1
						if(invader.hp <= 0):
							item_to_remove = i
						
						self.invader_exploding = True	
					else:
						if self.invaders_moving and not self.game_over:
							invader.sprite.y += invader.speed

							## Add a special move for the Boss
							if self.game_level == self.game_level_max:

								## Check if deplacement vector is empty, and if index in vector
								## is not larger than the len of vector (i.e test if vector is initialized and
								## if we already use all position in vector)
								## create one if true, use coordinates if false
								if(len(self.boss_deplacement_vector) > 0 and self.position_in_deplacement_vector < len(self.boss_deplacement_vector)):
									deplacement_instruction = self.boss_deplacement_vector[self.position_in_deplacement_vector]
									if(deplacement_instruction == "right"):
										invader.sprite.x += self.boss_lateral_move
									else:
										invader.sprite.x += -self.boss_lateral_move

									self.position_in_deplacement_vector += 1

								## Create a new vector
								else:
									vector_len = randint(15,45)
									direction = randint(0,100)
									boss_position = invader.sprite.x
									self.boss_deplacement_vector = []
									self.position_in_deplacement_vector = 0
									
									## Go right if possible
									if(direction > 50):
										for x in range(0, vector_len):
											if boss_position + self.boss_lateral_move < self.scr_width:
												self.boss_deplacement_vector.append("right")
												boss_position += self.boss_lateral_move
											else:
												self.boss_position.append("left")
									## Go left if possible
									else:
										for x in range(0, vector_len):
											if boss_position - self.boss_lateral_move > 60:
												self.boss_deplacement_vector.append("left")
												boss_position += - self.boss_lateral_move
											else:
												self.boss_position.append("right")

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

					if self.game_level != self.game_level_max:
						self.ennemybullet =EnnemyBullet((posx + width / 2, posy + height))
					else:
						self.ennemybullet =EnnemyBullet((posx + width / 2, posy + height))
						self.ennemybullet_2 =EnnemyBullet((posx + width , posy + height))
						self.ennemybullet_3 =EnnemyBullet((posx , posy + height))

				else:
					self.victory = True



			self.timecount += self.clock.get_time()

			# Handle the bullet shot by the random invader

			if self.timecount > self.nasty_shoot_time and self.has_already_chosen:
				self.timecount = 0
				self.has_already_chosen = False

			elif self.timecount < self.nasty_shoot_time and self.has_already_chosen:
				if self.ennemybullet.sprite.y <= self.scr_height:
					
					## Multiple ennemy fire for the Boss
					if self.game_level == self.game_level_max:
						self.ennemybullet.sprite = self.ennemybullet.sprite.move([0, 6])
						self.ennemybullet_2.sprite = self.ennemybullet_2.sprite.move([2, 6])
						self.ennemybullet_3.sprite = self.ennemybullet_3.sprite.move([-2, 6])
						self.screen.blit(self.ennemybullet.image, self.ennemybullet.sprite)
						self.screen.blit(self.ennemybullet_2.image, self.ennemybullet_2.sprite)
						self.screen.blit(self.ennemybullet_3.image, self.ennemybullet_3.sprite)
					else:
						self.ennemybullet.sprite = self.ennemybullet.sprite.move([0, 6])
						self.screen.blit(self.ennemybullet.image, self.ennemybullet.sprite)



			## Collision ad display srpites
			if self.game_level != self.game_level_max:

				if self.player.sprite.collidepoint(self.ennemybullet.sprite.x, self.ennemybullet.sprite.y) and self.player.exploding is False:
					self.timecount = self.nasty_shoot_time
					self.has_already_chosen = False
					self.player.exploding = True
				else:
					self.screen.blit(self.bullet.image, self.bullet.sprite)
					self.screen.blit(self.player.image, self.player.sprite)
			else:

				if self.player.sprite.collidepoint(self.ennemybullet.sprite.x, self.ennemybullet.sprite.y) and self.player.exploding is False:
					self.timecount = self.nasty_shoot_time
					self.has_already_chosen = False
					self.player.exploding = True

				elif self.player.sprite.collidepoint(self.ennemybullet_2.sprite.x, self.ennemybullet_2.sprite.y) and self.player.exploding is False:
					self.timecount = self.nasty_shoot_time
					self.has_already_chosen = False
					self.player.exploding = True

				elif self.player.sprite.collidepoint(self.ennemybullet_3.sprite.x, self.ennemybullet_3.sprite.y) and self.player.exploding is False:
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

				## Victory music
				if self.audio_activate:
					self.victory_sound.play()

				self.game_level += 1
				self.label_next_level = self.font.render("Niveau "+str(self.game_level)+" !", 1, (255, 255, 255))
				if(self.game_level <= self.game_level_max):
					self.screen.blit(self.label_next_level,
						(
						self.scr_width / 2 - self.label_victory.get_rect().width / 2,
						self.scr_height / 2 - self.label_victory.get_rect().height / 2
						)
					)
				else:
					self.screen.blit(
						self.label_victory,
							(
							self.scr_width / 2 - self.label_victory.get_rect().width / 2,
							self.scr_height / 2 - self.label_victory.get_rect().height / 2
							)
					)

				pygame.display.flip()
				pygame.time.delay(1000)
				

				##-------------------------------------------##
				## Instanciate the new level (init Invaders) ##
				##-------------------------------------------##

				## Level 2
				if(self.game_level == 2):
					self.init_x = 10
					self.number_of_ennemy = 8

					for i in range(0, 3):
						self.invaders.append(Invader((self.init_x, 10)))
						self.init_x += 55
					
					self.invaders.append(Invader2((self.init_x , 10)))
					self.init_x += 70

					for i in range(6, 7):
						self.invaders.append(Invader((self.init_x, 10)))
						self.init_x += 55

					self.invaders.append(Invader2((self.init_x , 10)))
					self.init_x += 70

					self.invaders.append(Invader((self.init_x, 10)))
					self.init_x += 55
					self.invaders.append(Invader((self.init_x, 10)))
					self.init_x += 55
					self.invaders.append(Invader((self.init_x, 10)))
					self.init_x += 55

					## Stay in the loop
					self.victory = False

				## Level 3
				if(self.game_level == 3):
					self.init_x = 10
					self.number_of_ennemy = 10

					for i in range(0, 4):
						self.invaders.append(Invader((self.init_x, 10)))
						self.init_x += 50
					
					self.invaders.append(Invader2((self.init_x , 10)))
					self.init_x += 70

					for i in range(6, 7):
						self.invaders.append(Invader((self.init_x, 10)))
						self.init_x += 50

					self.invaders.append(Invader2((self.init_x , 10)))
					self.init_x += 70

					self.invaders.append(Invader((self.init_x, 10)))
					self.init_x += 50
					self.invaders.append(Invader((self.init_x, 10)))
					self.init_x += 50
					self.invaders.append(Invader((self.init_x, 10)))
					self.init_x += 50

					self.invaders.append(Invader2((self.init_x , 10)))
					self.init_x += 70

					## Stay in the loop
					self.victory = False

				## Level 4
				if(self.game_level == 4):
					self.init_x = 10
					self.number_of_ennemy = 10

					for i in range(0, self.number_of_ennemy):
						if(i in [0,2,4,6,8,10]):
							self.invaders.append(Invader((self.init_x, 10)))
							self.init_x += 50
						else:
							self.invaders.append(Invader2((self.init_x , 10)))
							self.init_x += 70

					## Stay in the loop
					self.victory = False

				
				## Level 5
				if(self.game_level == 5):
					self.init_x = self.scr_width/2
					self.invaders.append(Boss((self.init_x , 10)))

					## Stay in the loop
					self.victory = False


				## Finish the game
				elif(self.game_level == 6):
					self.victory = True

				


			if self.game_over:
				self.screen.blit(
					self.label_game_over,
					(
						self.scr_width / 2 - self.label_game_over.get_rect().width / 2,
						self.scr_height / 2 - self.label_game_over.get_rect().height / 2
					)
				)


			pygame.display.flip()

			if self.game_over or self.victory:
				pygame.time.delay(2000)
				mainloop = False
