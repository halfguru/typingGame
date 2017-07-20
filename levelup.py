import pygame, sys
from pygame.locals import *
from scoreboard import Scoreboard
from sound import Sound
from scoreboard import Scoreboard

class Level:


	def __init__(self, game):

		self.game = game
		#self.scoreboard = Scoreboard(pygame.display.set_mode((1280, 720)))
		self.bg = pygame.image.load("sprites/bgGame.jpg")
		self.ingamebg = pygame.image.load("sprites/ingamebg.jpg")
		self.display = True

		self.MENUFONT = pygame.font.Font('coders_crux.ttf', 40)
		self.TITLEFONT = pygame.font.Font('coders_crux.ttf', 90)
			
		self.menu_items_lost = [
			self.MENUFONT.render("Accuracy: ", 1, (game.WHITE)),
			self.MENUFONT.render("Bonus: ", 1, (game.WHITE)),
			self.MENUFONT.render("Error Free: ", 1, (game.WHITE)),
			self.MENUFONT.render("Total: ", 1, (game.WHITE)),
			self.MENUFONT.render("Press <ENTER> to continue: ", 1, (game.WHITE))
			]
	
	

	def run(self,state):

		global index

		running = True
		print str(Scoreboard.level) + " MENU LEVEL"

		sound = Sound()
		if state == "levelup":
			sound.playsound("levelup")
		if state == "gameover":
			sound.playsound("gameover")

		Scoreboard.errorFree = "No"
		Scoreboard.accuracy = int(float((Scoreboard.wordLength*20 - Scoreboard.error)) / float((Scoreboard.wordLength*20)) * 100)

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

		Scoreboard.score = int(float(Scoreboard.score + Scoreboard.accuracy/100*50*Scoreboard.bonus))



	def draw(self):


		self.game.DISPLAYSURF.blit(self.bg, (0,0))

		if Scoreboard.accuracy == 100.0:
			Scoreboard.errorFree = "Yes"
			Scoreboard.bonus = 1.2

		self.menu_items = [
			self.MENUFONT.render("Accuracy: " + str('%.0f' % Scoreboard.accuracy) + "%", 1, (self.game.WHITE)),
			self.MENUFONT.render("Bonus: " + str('%.0f' % (Scoreboard.accuracy/100*50)), 1, (self.game.WHITE)),
			self.MENUFONT.render("Error Free: " + Scoreboard.errorFree, 1, (self.game.WHITE)),
			self.MENUFONT.render("Total: " + str(int(float(Scoreboard.score + Scoreboard.accuracy/100*50*Scoreboard.bonus))), 1, (self.game.WHITE)),
			self.MENUFONT.render("Press <ENTER> to continue: ", 1, (self.game.WHITE))
			]

		#if n > 0:
		#	n=n-1
		self.game_name = self.TITLEFONT.render("LEVEL " + str(Scoreboard.level) + " COMPLETE", 1, self.game.BLUE)
		self.display = not self.display
		if self.display == False:
			self.game_name = self.TITLEFONT.render("LEVEL " + str(Scoreboard.level) + " COMPLETE", 1, self.game.WHITE)

		self.game.SCREEN.blit(self.game_name, (400, 100))

		for ind in range(len(self.menu_items)):
			self.game.SCREEN.blit(self.menu_items[ind], (500, 250 + ind * 80))

		self.game.DISPLAYSURF.blit(self.game.SCREEN, (0, 0))
		pygame.draw.rect(self.game.DISPLAYSURF, self.game.WHITE, pygame.Rect(450 ,200,500,450),1)
		pygame.display.flip()
		pygame.time.wait(200)


	def draw_lost(self):
		self.game.DISPLAYSURF.blit(self.bg, (0,0))

		self.game_name_lost = self.TITLEFONT.render("GAME OVER", 1, (self.game.RED))
		
		self.display = not self.display
		if self.display == False:
			self.game_name_lost = self.TITLEFONT.render("GAME OVER", 1, (self.game.WHITE))


		self.game.SCREEN.blit(self.game_name_lost, (500, 100))

		for ind in range(len(self.menu_items_lost)):
			self.game.SCREEN.blit(self.menu_items_lost[ind], (500, 250 + ind * 80))

		self.game.DISPLAYSURF.blit(self.game.SCREEN, (0, 0))
		pygame.draw.rect(self.game.DISPLAYSURF, self.game.WHITE, pygame.Rect(450 ,200,500,450),1)
		pygame.display.flip()
		pygame.time.wait(500)







