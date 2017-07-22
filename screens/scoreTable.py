#!/usr/bin/python3
import sys
import pygame


class ScoreTable:

	def __init__(self, screen):

		bg_color=(0, 0, 0)
		font=None
		font_size=50
		font_color=(255, 255, 255)

		self.screen = screen
		self.scr_width = self.screen.get_rect().width
		self.scr_height = self.screen.get_rect().height
		self.font = pygame.font.SysFont(font, font_size)

		# Background Game
		self.bg = pygame.image.load('resources/images/menubackground.jpg')
		self.bg_rect = self.bg.get_rect()
		self.escape_selected = False

		## Get the top 10 scores
		player_to_score = {}
		scores_data= open("resources/scores.csv", "r")
		for line in scores_data:
			line = line.replace("\n", "")
			line_in_array = line.split(",")

			if(len(line_in_array) > 1):
				player_to_score[line_in_array[0]] = line_in_array[1]

		scores_data.close()

		players_to_display = []
		for x in range(0,10):
			max_player = max(player_to_score, key=player_to_score.get)
			couple = str(max_player)+"   "+str(player_to_score[max_player])
			players_to_display.append(couple)
			del player_to_score[max_player]

		items = tuple(players_to_display)
		self.score_items = []

		# Position menu titles on the menu screen
		for index, item in enumerate(items):
			label = self.font.render(item, 1, font_color)

			width = label.get_rect().width
			height = label.get_rect().height

			posx = (self.scr_width / 2) - (width / 2)

			# t_h: total height of text block
			t_h = len(items) * height

			posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
			self.score_items.append([item, label, (width, height), (posx, posy)])

	def run(self):

		mainloop = True
		while mainloop:

			# Redraw the background
			self.screen.fill((0, 0, 0))
			self.screen.blit(self.bg, self.bg_rect)

			for name, label, (width, height), (posx, posy) in self.score_items:
				self.screen.blit(label, (posx, posy))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

			keys = pygame.key.get_pressed()

			if keys[pygame.K_ESCAPE]:
				mainloop = False
				self.escape_selected = True

			pygame.display.flip()
