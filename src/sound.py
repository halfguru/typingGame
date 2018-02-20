
import pygame
from pygame.locals import*


# Play Game Sound and Music

class Sound():

    musicPlaying = False
    """
        Class Constructor for the sound class. This method creates the instance
        of the object itself.
    """
    def __init__(self):
        self.sound1 = pygame.mixer.Sound('../sound/music.ogg')
        self.chan1 = pygame.mixer.find_channel()

        # Initialize mixer
        pygame.mixer.init()

    """
        This method define 2 states (play and stop).
    """
    def playmusic(self, type):
        if type == "Play":
            self.chan1.queue(self.sound1)
        elif type == "Stop":
            self.chan1.stop()
    """
        The method plays the sounds of explosion or power-up
    """
    def playsound(self, type):
        if type == "word":
            pygame.mixer.music.load('../sound/coin_sound.ogg')
            pygame.mixer.music.play(1)

        if type == "miss":
            pygame.mixer.music.load('../sound/miss.ogg')
            pygame.mixer.music.play(1)

        if type == "levelup":
            pygame.mixer.music.load('../sound/levelup.ogg')
            pygame.mixer.music.play(1)

        if type == "gameover":
            pygame.mixer.music.load('../sound/gameover.ogg')
            pygame.mixer.music.play(1)
    """
        This method allows to play the sound
    """
    def playSound(self):
        pygame.mixer.music.load()
