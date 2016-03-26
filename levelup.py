import pygame, sys
from pygame.locals import *
from scoreboard import Scoreboard
from sound import Sound
from scoreboard import Scoreboard

class Level:

	index = 0
	mode = "menu"

	def __init__(self, game):

		self.game = game
		self.scoreboard = Scoreboard(pygame.display.set_mode((1280, 720)))
		self.bg = pygame.image.load("sprites/bgGame.jpg")
		self.ingamebg = pygame.image.load("sprites/ingamebg.jpg")
		#self.surf_ind = pygame.Surface([game.WINDOWWIDTH, 80])
		#self.surf_ind.set_alpha(128)
		#self.surf_ind.fill((game.BLACK))

		self.MENUFONT = pygame.font.Font('coders_crux.ttf', 40)
		self.TITLEFONT = pygame.font.Font('coders_crux.ttf', 90)
		self.SELECTEDFONT = pygame.font.Font('coders_crux.ttf', 50)

		self.game_name = self.TITLEFONT.render("LEVEL " + str(self.scoreboard.level) + " COMPLETE", 1, (game.BRIGHTBLUE))
		self.game_name_lost = self.TITLEFONT.render("GAME OVER", 1, (game.RED))

		self.menu_items = [
			self.MENUFONT.render("Accuracy: ", 1, (game.WHITE)),
			self.MENUFONT.render("Bonus: ", 1, (game.WHITE)),
			self.MENUFONT.render("Error Free: ", 1, (game.WHITE)),
			self.MENUFONT.render("Total: ", 1, (game.WHITE)),
			self.MENUFONT.render("Press <ENTER> to continue: ", 1, (game.WHITE))
			]
		self.menu_items_lost = [
			self.MENUFONT.render("Level Incomplete", 1, (game.WHITE)),
			self.MENUFONT.render("Accuracy: ", 1, (game.WHITE)),
			self.MENUFONT.render("Bonus: ", 1, (game.WHITE)),
			self.MENUFONT.render("Error Free: ", 1, (game.WHITE)),
			self.MENUFONT.render("Total: ", 1, (game.WHITE)),
			self.MENUFONT.render("Press <ENTER> to continue: ", 1, (game.WHITE))
			]

	def run(self,state):

		global index

		self.game.DISPLAYSURF.blit(self.bg, (0,0))
		running = True

		sound = Sound()
		if state == "levelup":
			sound.playsound("levelup")
		if state == "gameover":
			sound.playsound("gameover")

		while running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()
					sys.exit() 

				if event.type == pygame.KEYDOWN:
					
					if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
						print "next level mate"
						running = False
						break

	 
					if event.key == K_ESCAPE:
						pygame.quit() 
						sys.exit() 

			if state == "levelup":
				self.draw()
			if state == "gameover":
				self.draw_lost()


	def draw(self):

		self.game.screen.blit(self.game_name, (450, 100))

		if self.mode == "menu":
		  #  self.game.screen.blit(self.surf_ind, (0, self.index * 80 + 100))
			for ind in range(len(self.menu_items)):
				self.game.screen.blit(self.menu_items[ind], (500, 250 + ind * 80))

		self.game.DISPLAYSURF.blit(self.game.screen, (0, 0))
		pygame.display.flip()


	def draw_lost(self):

		self.game.screen.blit(self.game_name_lost, (450, 100))

		if self.mode == "menu":
		  #  self.game.screen.blit(self.surf_ind, (0, self.index * 80 + 100))
			for ind in range(len(self.menu_items_lost)):
				self.game.screen.blit(self.menu_items_lost[ind], (500, 250 + ind * 80))

		self.game.DISPLAYSURF.blit(self.game.screen, (0, 0))
		pygame.display.flip()







