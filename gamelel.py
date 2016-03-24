

import random, sys, time, pygame, string
from random import randint
from pygame.locals import *

FPS = 60
WINDOWWIDTH = 1280
WINDOWHEIGHT = 720  
FLASHSPEED = 500 # in milliseconds
FLASHDELAY = 200 # in milliseconds
BUTTONSIZE = 300
BUTTONGAPSIZE = 20
TIMEOUT = 4 # seconds before game over if no button is pushed.


#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)


class Textsprite(pygame.sprite.Sprite):
    def __init__(self, text):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.pos = 0
        self.update()
    def update(self):
        self.image = pygame.font.Font(None, 36).render(self.text, 1, WHITE)
        self.highlight = pygame.font.Font(None, 36).render(self.text[:self.pos], 1, BLUE)
        self.image.blit(self.highlight, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.display.get_surface().get_rect().center
    def keyin(self, key):
        if key == self.text[self.pos]:
            self.pos = self.pos + 1
        if len(self.text) == self.pos:
            self.pos = 0

        """
        wordSurf = BASICFONT.render(randomLetter, 1, wordColor)
        wordRect = infoSurf.get_rect()
        wordRect.topleft = (WORDX, WINDOWHEIGHT - WORDY)
        DISPLAYSURF.blit(wordSurf,wordRect)

        """

def main():

    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Typing Maniac')

    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)
    infoSurf = BASICFONT.render('Type the characters as fast as possible', 1, DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (100, WINDOWHEIGHT - 30)

    # load the sound files
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    # letter height generator
    WORDY = 650
    WORDX = randint(100,500)
    wordColor = WHITE
    wordLength = 3
    randomLetter = ''.join(random.choice(string.lowercase) for x in range(wordLength)) #random letter generator  #random letter generator
    newWord = False
    incrementSpeed = 1
    letterAttempt = 0
  

    # keep track of sprites
    all = pygame.sprite.RenderUpdates()
    textsprite = Textsprite('I''M SO EDGY LOLOLOLL')
    all.add(textsprite)

    # Initialize some variables for a new game
    pattern = [] # stores the pattern of colors
    currentStep = 0 # the color the player must push next
    lastClickTime = 0 # timestamp of the player's last button push
    score = 0
    error = 0
    # when False, the pattern is playing. when True, waiting for the player to click a colored button:
    waitingForInput = False

    while True: # main game loop

        clickedButton = None # button that was clicked (set to YELLOW, RED, GREEN, or BLUE)
        DISPLAYSURF.fill(bgColor)


        # Display current score and errors
        scoreSurf = BASICFONT.render('Score: ' + str(score), 1, WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 200, 50) 
        errorSurf = BASICFONT.render('Error: ' + str(error), 1, WHITE)
        errorRect = scoreSurf.get_rect()
        errorRect.topleft = (WINDOWWIDTH - 200, 70)  
        DISPLAYSURF.blit(scoreSurf, scoreRect)
        DISPLAYSURF.blit(errorSurf, errorRect)
        pygame.draw.line(DISPLAYSURF, BLUE, (100, 635), (1000, 635), 4)


        if newWord == True:
            if score%10 == 0: 
                incrementSpeed = incrementSpeed*1.3
                wordLength = wordLength + 1
            score = score + 1
            randomLetter = generateWord(wordLength) #random letter generator 
            WORDX = randint(100,500)
            WORDY = 650
            wordColor = WHITE
            letterAttempt = 0
            newWord = False
 
        WORDY = WORDY - incrementSpeed        
        
        for a in randomLetter:
            wordSurf = BASICFONT.render(randomLetter, 1, wordColor)
        wordRect = infoSurf.get_rect()
        wordRect.topleft = (WORDX, WINDOWHEIGHT - WORDY)
        DISPLAYSURF.blit(wordSurf,wordRect)

        DISPLAYSURF.blit(infoSurf, infoRect)

        checkForQuit()
        for event in pygame.event.get(): # event handling loop
            if event.type == KEYDOWN:
                if pygame.key.name(event.key) == randomLetter[letterAttempt].lower():
                    print randomLetter[letterAttempt]
                    wordColor = YELLOW
                    letterAttempt = letterAttempt + 1
                    if letterAttempt == len(randomLetter):
                        newWord = True
                        print "new word"
                elif pygame.key.name(event.key) != randomLetter[letterAttempt].lower():
                    print "error"
                    error = error + 1 
             
        if WORDY == 100:
            GameOver()
            newWord = True
        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(50)
            waitingForInput = True
        else:
            # wait for the player to enter buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                # pushed the correct button
                currentStep += 1
                lastClickTime = time.time()

                if currentStep == len(pattern):
                    # pushed the last button in the pattern
                    score += 1
                    waitingForInput = False
                    currentStep = 0 # reset back to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.time() - TIMEOUT > lastClickTime):

                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(1000)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        pygame.quit()
        sys.exit() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            pygame.quit() # terminate if the KEYUP event was for the Esc key
            sys.exit() 
        pygame.event.post(event) # put the other KEYUP event objects back

def generateWord(wordLength):

    newRandomLetter = ''.join(random.choice(string.lowercase) for x in range(wordLength)) #random letter generator
    return newRandomLetter

def GameOver():
    print "game over"

def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    return None

if __name__ == '__main__':
    main()