import random, sys, time, pygame, string
from random import randint
from pygame.locals import *
from scoreboard import Scoreboard
from sound import Sound
from mainmenu import Menu
from levelup import Level


class Game():

	def __init__(self):

		self.FPS = 60
		self.WINDOWWIDTH = 1280
		self.WINDOWHEIGHT = 720  
		self.read_wordlist("wordlist.txt")

		#                R    G    B
		self.WHITE        = (255, 255, 255)
		self.BLACK        = (  0,   0,   0)
		self.BRIGHTRED    = (255,   0,   0)
		self.RED          = (155,   0,   0)
		self.BRIGHTGREEN  = (  0, 255,   0)
		self.GREEN        = (  0, 155,   0)
		self.BRIGHTBLUE   = (  0,   0, 255)
		self.BLUE         = (  0,   0, 155)
		self.BRIGHTYELLOW = (255, 255,   0)
		self.YELLOW       = (155, 155,   0)
		self.DARKGRAY     = ( 40,  40,  40)
		self.bgColor = self.BLACK

		pygame.init()
		self.FPSCLOCK = pygame.time.Clock()
		self.SCREEN = pygame.Surface([self.WINDOWWIDTH, self.WINDOWHEIGHT])
		self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
		self.BASICFONT = pygame.font.Font('coders_crux.ttf', 40)
		self.BASICFONT1 = pygame.font.Font('coders_crux.ttf', 32)

	def run(self):

		global frame_count, start_time

		# Time
		pygame.display.set_caption('Typing Maniac')
		frame_count = 0
		self.start_time = time.time()
		clock = pygame.time.Clock()
		time_elapsed_since_last_action = 0

		# Music, Scoreboard, Level initialization
		sound = Sound()
		sound.playmusic("Play")
		scoreboard = Scoreboard(self.DISPLAYSURF)
		level = Level(self)

		# Initialize some variables for a new game
		score = 0; error = 0; oldLevel = 1; highlightColor = (self.WHITE); self.cooldown = 300; self.keypressCheck = False
		self.word_counter = 0; self.character_counter = 0; self.speed = 0; self.charspeed = 0; wordY = 650; wordX = randint(100,900)
		randomWord = self.generateWord(scoreboard.wordLength)
		newWord = False; incrementSpeed = 1; letterAttempt = 0
		#randomWord = ''.join(random.choice(string.uppercase) for x in range(wordLength)) #random letter generator  #random letter generator

		#Fonts and game instructions
		infoSurf = self.BASICFONT1.render('Type the characters as fast as possible', 1, self.DARKGRAY)
		infoRect = infoSurf.get_rect(); infoRect.topleft = (45, self.WINDOWHEIGHT - 50)
		wordRect = infoSurf.get_rect()
		pauseSurf = self.BASICFONT.render('Press F1 to pause', 1, self.DARKGRAY); pauseRect = infoSurf.get_rect()
		pauseRect.topleft = (self.WINDOWWIDTH/2 - 70, 20)


		# Main game loop
		while True: 

			# Clock tick
			dt = clock.tick()

			# Wallpaper
			self.SCREEN.blit(menu.ingamebg, (0,0))
			self.DISPLAYSURF.blit(self.SCREEN, (0, 0))

			# Display line and progress bar
			pygame.draw.line(self.DISPLAYSURF, self.BLUE, (50, 635), (1030, 635), 4)
			pygame.draw.line(self.DISPLAYSURF, self.BLUE, (50, 635), (50, 0), 4)
			pygame.draw.line(self.DISPLAYSURF, self.BLUE, (1030, 635), (1030, 0), 4)
			pygame.draw.rect(self.DISPLAYSURF, self.WHITE, pygame.Rect(450 + 100,650,550,50))
			pygame.draw.rect(self.DISPLAYSURF, self.GREEN, pygame.Rect(450 + 100 ,650,550*Scoreboard.progress_percent,50))
			pygame.draw.rect(self.DISPLAYSURF, self.DARKGRAY, pygame.Rect(1010 + 100,650,70,50))

			# Display info and pause
			self.DISPLAYSURF.blit(infoSurf, infoRect)
			self.DISPLAYSURF.blit(pauseSurf, pauseRect)

			# Display scoreboard, timer, wpm
			scoreboard.blitme()
			self.timer()
			self.wpm()

			if newWord == True:
				Scoreboard.score += 1
				# LEVEL UP AFTER 20 LEVELS
				if Scoreboard.score%20 == 0 and Scoreboard.score != 0: 

					sound.playmusic("Stop")
					level.run("levelup")

					Scoreboard.progress_percent = 0; Scoreboard.speedLevel *= 1.1; Scoreboard.level += 1; Scoreboard.error = 0
					incrementSpeed = incrementSpeed*1.1
					self.word_counter = 0; self.character_counter = 0; self.start_time = time.time()

				# WORDLENGTH INCREASES AFTER 2 LEVELS
				if Scoreboard.level%3 == 0 and oldLevel != Scoreboard.level:
					scoreboard.wordLength = scoreboard.wordLength + 1
					oldLevel = Scoreboard.level

				randomWord = self.generateWord(scoreboard.wordLength) #random letter generator 
				wordX = randint(100,950); wordY = 650; letterAttempt = 0; newWord = False

		

			wordY = wordY - incrementSpeed  
			wordRect.topleft = (wordX, self.WINDOWHEIGHT - wordY)

			# List of words to be blitted on screen
			wordSurf = []
			highlightSurf = []
			wordList = wordSurf.append(self.BASICFONT.render(randomWord, 1, self.WHITE))
			highlightList = highlightSurf.append(self.BASICFONT.render(randomWord[:letterAttempt], 1, highlightColor ))
			plusOne = self.BASICFONT.render("+ 1", 1, self.WHITE)

			# Blit the info, words, highlight and pause instructions
			for x in range (0,len(wordSurf)):
				self.DISPLAYSURF.blit(wordSurf[x],wordRect)
				self.DISPLAYSURF.blit(highlightSurf[x],wordRect)

			self.checkForQuit()

			for event in pygame.event.get(): # event handling loop

				keys = pygame.key.get_pressed()  #checking pressed keys
				if keys[pygame.K_SPACE] and self.keypressCheck == False:
					incrementSpeed = incrementSpeed + 3
					self.keypressCheck = True

				elif self.keypressCheck == True:
					incrementSpeed -= 3
					self.keypressCheck = False

				if event.type == KEYDOWN:

					if pygame.key.name(event.key) == randomWord[letterAttempt].lower():
						print (randomWord[letterAttempt])
						self.character_counter += 1
						highlightColor = self.YELLOW
						letterAttempt = letterAttempt + 1
						if letterAttempt == len(randomWord):
							self.word_counter += 1
							newWord = True
							Scoreboard.progress_percent += 0.05
							print ("\nnew word")
							sound.playsound("word")

					elif event.key == pygame.K_BACKSPACE:
						if letterAttempt > 0:
							letterAttempt = letterAttempt - 1


					# Pause menu

					elif event.key == pygame.K_F1:
						pause = True
						menu.mode = "pause"
						print (menu.mode)
						while pause:
							for event in pygame.event.get(): # event handling loop
								if event.type == KEYDOWN:
									if event.key == pygame.K_F1:
										pause = False
							menu.pause()
							self.checkForQuit()
							pygame.display.update()

					elif event.key == pygame.K_1:
						print  (scoreboard.wordLength)
						scoreboard.wordLength += 1
					elif event.key == pygame.K_2:
						print  (scoreboard.wordLength)
						scoreboard.wordLength -= 1

					elif pygame.key.name(event.key) != randomWord[letterAttempt].lower() and event.key != K_SPACE and event.key != K_RETURN:
						print ("error")
						highlightColor = self.RED
						Scoreboard.error = Scoreboard.error + 1 
						sound.playsound("miss")

						 
				 
			if wordY < 105:
				newWord = True

			#GAME OVER
			if Scoreboard.error == 20:
				print ("game over")
				sound.playmusic("Stop")
				level.run("gameover")
				newWord = True
				Scoreboard.speedLevel = 1; Scoreboard.level = 1; Scoreboard.error = 0; Scoreboard.score = 0; scoreboard.wordLength = 3;Scoreboard.progress_percent = 0
				frame_count = 0
				self.word_counter = 0; self.character_counter = 0; self.start_time = time.time()

			frame_count += 1
			pygame.display.update()
			self.FPSCLOCK.tick(self.FPS)

	def checkForQuit(self):
		for event in pygame.event.get(QUIT): # get all the QUIT events
			pygame.quit()
			sys.exit() 
		for event in pygame.event.get(KEYUP): 
			if event.key == K_ESCAPE:
				pygame.quit() 
				sys.exit() 
			pygame.event.post(event) 


	def read_wordlist(self, filename):
		f = open(filename, "r")
		lines = f.readlines()
		f.close()
		self.WORDS = []
		for line in lines:
			self.WORDS.append(line[:-1].lower())

	def generateWord(self,wordLength):
		while 1:
			newrandomWord = random.choice(self.WORDS).upper()
			if len(newrandomWord) == wordLength:
			#newrandomWord = ''.join(random.choice(string.uppercase) for x in range(wordLength)) #random letter generator
				return newrandomWord

	def timer(self):
		# --- Timer going up ---
		# Calculate total seconds
		total_seconds = frame_count // self.FPS
		minutes = total_seconds // 60
		seconds = total_seconds % 60
	 
		# Use python string formatting to format in leading zeros
		output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
	 
		# Blit to the screen
		text = self.BASICFONT.render(output_string, True, self.WHITE)
		self.DISPLAYSURF.blit(text, [1060, 100])

	def wpm(self):
		# Words per minute
		now = time.time()
		if not self.word_counter == 0:
			self.speed = self.word_counter / (now - self.start_time)
			self.speed = round(self.speed, 2)
			self.charspeed = self.character_counter* 0.2 * 60 / (now - self.start_time) 
			self.charspeed = round(self.charspeed, 2)
		wpm_counter = self.BASICFONT.render("speed (words/s): " ,1,self.WHITE); speed_counter = self.BASICFONT.render("speed (chars/m): ",1,self.WHITE)
		wpm_counter1 = self.BASICFONT.render(str(self.speed) ,1,self.WHITE); speed_counter1 = self.BASICFONT.render(str(self.charspeed),1,self.WHITE)

		self.DISPLAYSURF.blit(wpm_counter, (1040,200)); self.DISPLAYSURF.blit(speed_counter, (1040,300)); self.DISPLAYSURF.blit(wpm_counter1, (1050,250))
		self.DISPLAYSURF.blit(speed_counter1, (1050,350))



if __name__ == '__main__':
	game = Game()
	menu = Menu(game)
	menu.run()