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
		self.WORD = random.choice(self.WORDS)

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
		self.screen = pygame.Surface([self.WINDOWWIDTH, self.WINDOWHEIGHT])
		self.DISPLAYSURF = pygame.display.set_mode((self.WINDOWWIDTH, self.WINDOWHEIGHT))
		self.BASICFONT = pygame.font.Font('coders_crux.ttf', 40)
		self.BASICFONT1 = pygame.font.Font('coders_crux.ttf', 32)



	def run(self):

		global frame_count, start_time

		# Initialize
		pygame.display.set_caption('Typing Maniac')
		frame_count = 0
		start_time = 0
		oldLevel = 1

		# Music initialization
		sound = Sound()
		sound.playmusic("Play")

		# Scoreboard initialization
		scoreboard = Scoreboard(self.DISPLAYSURF)

		#Level up initialization
		level = Level(self)

		#Fonts and game instructions
		infoSurf = self.BASICFONT1.render('Type the characters as fast as possible', 1, self.DARKGRAY)
		infoRect = infoSurf.get_rect()
		infoRect.topleft = (45, self.WINDOWHEIGHT - 50)
		pauseSurf = self.BASICFONT.render('Press F1 to pause', 1, self.DARKGRAY)
		pauseRect = infoSurf.get_rect()
		pauseRect.topleft = (self.WINDOWWIDTH/2 - 70, 20)


		# letter height generator
		wordY = 650
		wordX = randint(100,950)
		wordLength = 3
		#randomLetter = ''.join(random.choice(string.uppercase) for x in range(wordLength)) #random letter generator  #random letter generator
		randomLetter = self.generateWord(wordLength)
		newWord = False
		incrementSpeed = 1
		letterAttempt = 0


		# Initialize some variables for a new game
		score = 0
		error = 0
		highlightColor = (self.WHITE)
		plusOneCheck = False
		self.last = pygame.time.get_ticks()
		self.cooldown = 300 

		# Glowing settings
		self._glowing = True 
		self.alpha = 1
		self.blink_spd = 3
		self.gamestate = ""


		while True: # Main game loop

			self.screen.blit(menu.ingamebg, (0,0))
			self.DISPLAYSURF.blit(self.screen, (0, 0))

			# Display scoreboard
			scoreboard.blitme()

			# Display timer
			self.timer()

			# Display line and progress bar
			pygame.draw.line(self.DISPLAYSURF, self.BLUE, (50, 635), (1080, 635), 4)
			pygame.draw.line(self.DISPLAYSURF, self.BLUE, (50, 635), (50, 0), 4)
			pygame.draw.line(self.DISPLAYSURF, self.BLUE, (1080, 635), (1080, 0), 4)
			pygame.draw.rect(self.DISPLAYSURF, self.WHITE, pygame.Rect(450 + 100,650,550,50))
			pygame.draw.rect(self.DISPLAYSURF, self.GREEN, pygame.Rect(450 + 100 ,650,550*scoreboard.progress_percent,50))
			pygame.draw.rect(self.DISPLAYSURF, self.DARKGRAY, pygame.Rect(1010 + 100,650,70,50))

			# Display scoreboard
			scoreboard.blitme()

			# Display score and pause

			self.DISPLAYSURF.blit(infoSurf, infoRect)
			self.DISPLAYSURF.blit(pauseSurf, pauseRect)


			# New word generates when a user types correctly a word
			if newWord == True:
				scoreboard.score += 1
				# For each multiple of 20, level up
				if scoreboard.score%20 == 0 and scoreboard.score != 0: 
					scoreboard.progress_percent = 0
					incrementSpeed = incrementSpeed*1.1
					scoreboard.speed *= 1.1
					scoreboard.level += 1
					scoreboard.error = 0

					sound.playmusic("Stop")
					level.run("levelup")

				# For each 2 levels, the word length increases by 1
				if scoreboard.level%2 == 0 and oldLevel != scoreboard.level:
					wordLength = wordLength + 1
					oldLevel = scoreboard.level


				plusOneCheck = True

				randomLetter = self.generateWord(wordLength) #random letter generator 
				wordX = randint(100,950)
				wordY = 650
				letterAttempt = 0
				newWord = False
			
			now = pygame.time.get_ticks()
			if (now - self.last >= self.cooldown):
				plusOneCheck = False
			if plusOneCheck:
				self.DISPLAYSURF.blit(plusOne,wordRect) # + 1 score text


			wordY = wordY - incrementSpeed  
			wordRect = infoSurf.get_rect()
			wordRect.topleft = (wordX, self.WINDOWHEIGHT - wordY)

			"""
			self.glowing()
			self.rect = pygame.Surface((100, 100))
			self.rect.fill(self.GREEN)
			self.rect.set_alpha(self.alpha)
			self.DISPLAYSURF.blit(self.rect,(250,250))

			"""

			# List of words to be blitted on screen
			wordSurf = []
			highlightSurf = []
			wordList = wordSurf.append(self.BASICFONT.render(randomLetter, 1, self.WHITE))
			plusOne = self.BASICFONT.render("+ 1", 1, self.WHITE)
			highlightList = highlightSurf.append(self.BASICFONT.render(randomLetter[:letterAttempt], 1, highlightColor ))

			# Blit the info, words, highlight and pause instructions
			for x in range (0,len(wordSurf)):
				self.DISPLAYSURF.blit(wordSurf[x],wordRect)
				self.DISPLAYSURF.blit(highlightSurf[x],wordRect)

			self.checkForQuit()

			for event in pygame.event.get(): # event handling loop
				if event.type == KEYDOWN:

					if pygame.key.name(event.key) == randomLetter[letterAttempt].lower():
						print randomLetter[letterAttempt] ,
						highlightColor = self.YELLOW
						letterAttempt = letterAttempt + 1
						if letterAttempt == len(randomLetter):
							newWord = True
							scoreboard.progress_percent += 0.05
							print "\nnew word"
							sound.playsound("word")

					elif event.key == pygame.K_BACKSPACE:
						if letterAttempt > 0:
							letterAttempt = letterAttempt - 1

					#elif event.key ==pygame.K_SPACE:
					#	incrementSpeed = incrementSpeed * 3

					# Pause menu

					elif event.key == pygame.K_F1:
						pause = True
						menu.mode = "pause"
						print menu.mode
						while pause:
							for event in pygame.event.get(): # event handling loop
								if event.type == KEYDOWN:
									if event.key == pygame.K_F1:
										pause = False
							menu.pause()
							self.checkForQuit()
							pygame.display.update()

					elif event.key == pygame.K_1:
						print  wordLength
						wordLength += 1
					elif event.key == pygame.K_2:
						print  wordLength
						wordLength -= 1

					elif pygame.key.name(event.key) != randomLetter[letterAttempt].lower():
						print "error"
						highlightColor = self.RED
						scoreboard.error = scoreboard.error + 1 
						sound.playsound("miss")

						 
				 
			if wordY < 100:
				newWord = True

			#GAME OVER
			if scoreboard.error == 20:
				print "game over"
				sound.playmusic("Stop")
				level.run("gameover")
				scoreboard.speed = 1 
				scoreboard.level = 1
				scoreboard.error = 0
				scoreboard.score = 0
				wordLength = 3
				frame_count = 0
				scoreboard.progress_percent = 0

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
			newRandomLetter = random.choice(self.WORDS).upper()
			if len(newRandomLetter) == wordLength:
			#newRandomLetter = ''.join(random.choice(string.uppercase) for x in range(wordLength)) #random letter generator
				return newRandomLetter

	def timer(self):
		# --- Timer going up ---
		# Calculate total seconds
		total_seconds = frame_count // self.FPS
	 
		# Divide by 60 to get total minutes
		minutes = total_seconds // 60
	 
		# Use modulus (remainder) to get seconds
		seconds = total_seconds % 60
	 
		# Use python string formatting to format in leading zeros
		output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
	 
		# Blit to the screen
		text = self.BASICFONT.render(output_string, True, self.WHITE)
		self.DISPLAYSURF.blit(text, [1100, 100])

	def glowing(self):
		if self._glowing:
			self.alpha += self.blink_spd
			if self.alpha >= 200:#if all the way up go down
				self._glowing = False
		#Check if alpha is going down        
		elif self._glowing == False:
			self.alpha += -self.blink_spd
			if self.alpha <= 170: #if all the way down go up
				self._glowing = True




if __name__ == '__main__':
	game = Game()
	menu = Menu(game)
	menu.run()