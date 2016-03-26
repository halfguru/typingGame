import pygame, pygame.font
from pygame.sprite import Sprite
 
class Scoreboard(Sprite):
 
    def __init__(self, screen):
 
        Sprite.__init__(self)
        self.screen = screen
 
        # Game attributes to track for scoring
        self.score = 0
        self.error = 0
        self.speed = 1
        self.level = 1
        self.progress_percent = 0
 
        # Set dimensions and properties of scoreboard
        self.sb_height, self.sb_width = 50, self.screen.get_width()
        self.rect = pygame.Rect(0,0, self.sb_width, self.sb_height)
        self.bg_color=(100,100,100)
        self.text_color = (225,225,225)
        self.font = pygame.font.SysFont('coders_crux.ttf', 30)
 
        # Set positions of individual scoring elements on the scoreboard
        self.x_popped_position, self.y_popped_position = 20.0, 10.0
        self.x_missed_position, self.y_missed_position = 150.0, 10.0
        self.x_speed_position, self.y_speed_position = 1010.0, 10.0
        self.x_level_position, self.y_level_position = 1130.0, 10.0
        self.x_progress_position, self.y_progress_position = 1015.0 + 100, 665.0


    def prep_scores(self):
        self.popped_string = "Score: " + str(self.score)
        self.popped_image = self.font.render(self.popped_string, True, self.text_color)
 
        self.missed_string = "Missed: " + str(self.error)
        self.missed_image = self.font.render(self.missed_string, True, self.text_color)

        self.speed_string = "Speed: " + str('%.1f' % self.speed)
        self.speed_image = self.font.render(self.speed_string, True, self.text_color)

        self.level_string = "Level: " + str(self.level)
        self.level_image = self.font.render(self.level_string, True, self.text_color)

        self.progress_string = str(self.progress_percent*100) + " %"
        self.progress_image = self.font.render(self.progress_string, True, self.text_color)
 
 
    def blitme(self):
        # Turn individual scoring elements into images that can be drawn
        self.prep_scores()
        # Draw blank scoreboard
        self.screen.fill(self.bg_color, self.rect)
        # Draw individual scoring elements
        self.screen.blit(self.popped_image, (self.x_popped_position, self.y_popped_position))
        self.screen.blit(self.missed_image, (self.x_missed_position, self.y_missed_position))
        self.screen.blit(self.speed_image, (self.x_speed_position, self.y_speed_position))
        self.screen.blit(self.level_image, (self.x_level_position, self.y_level_position))
        self.screen.blit(self.progress_image, (self.x_progress_position, self.y_progress_position))
