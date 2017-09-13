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
		self.bg = pygame.image.load('resources/images/game_bg_origin.jpeg')
		self.bg_rect = self.bg.get_rect()
		self.escape_selected = False

		## Get the top scores
		def scoregame(fname,x):
			"""
			@Author:Tiphaine
			x est le nombre de valeur que l'on veut afficher
			fonction permettant d'organiser un dictionnaire des valeurs : name, score
			"""
			name_to_score = {}
			data_in_file = open(fname, "r")
			cmpt = 0
			for line in data_in_file:
				if cmpt != 0:
					line = line.replace("\n", "")
					line_in_array = line.split(",")
					name = line_in_array[0]
					score = int(line_in_array[1])
					name_to_score[name] = score
				cmpt += 1
			data_in_file.close()
			sorted_scores = sorted(name_to_score.items(), key=lambda t:t[1], reverse = True)
	
			#return sorted_scores
			return sorted_scores[:x]

		top_scores = scoregame("resources/scores.csv", 10)
		players_to_display = []
		for couple in top_scores:
			line = str(couple[0])+"   "+str(couple[1])
			players_to_display.append(line)

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
