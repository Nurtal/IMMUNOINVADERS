#!/usr/bin/python3
import pygame
from screens.game import Game
from screens.survival import Survival
from screens.menu import GameMenu
from screens.settings import GameSettings
from screens.scoreTable import ScoreTable

pygame.init()

# set_mode(resolution=(width, height), flags=0, depth=0)
# flags : collection of qdditional options
# depth : number of bits use for colors
screen = pygame.display.set_mode((640, 780), 0, 32)
bg_color = (0, 0, 0)

# Game Menu
pygame.display.set_caption('Game Menu')
menu_items = ('Jouer','Survie','Scores','Quitter')

# Views initialization
gm = GameMenu(screen, menu_items)
gs = GameSettings(screen)
g = None

menu_selected = True
mainloop = True
while mainloop:

	screen.fill(bg_color)
	if menu_selected or g.escape_selected:
		gm.run()
		if g is not None:
			g.escape_selected = False
		#gs.escape_selected = False

	if gm.start_selected:
		pygame.display.set_caption('Game')
		g = Game(screen)
		g.run()
		gm.start_selected = False
		gm.survival_selected = False
		gm.scores_selcted = False
		gm.quit_select = False

	if gm.survival_selected:
		pygame.display.set_caption('Survival')
		gsu = Survival(screen)
		gsu.run()
		gm.start_selected = False
		gm.survival_selected = False
		gm.scores_selected = False
		gm.quit_select = False

	if gm.scores_selected:
		gs = ScoreTable(screen)
		gs.run()
		gm.start_selected = False
		gm.survival_selected = False
		gm.settings_selected = False
		gm.scores_selected = False

	

	if gm.quit_select is True:
		mainloop = False

	pygame.display.flip()
