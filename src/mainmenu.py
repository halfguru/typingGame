import pygame


class Menu():

    def __init__(self, game):

        self.mode = "menu"
        self.index = 0
        self.game = game
        self.bg = pygame.image.load("../img/bgGame.jpg")
        self.ingamebg = pygame.image.load("../img/ingamebg.jpg")
        self.display = True

        self.game.SCREEN.blit(self.bg, (0, 0))

        self.MENUFONT = pygame.font.Font('../utils/coders_crux.ttf', 40)
        self.TITLEFONT = pygame.font.Font('../utils/coders_crux.ttf', 90)
        self.SELECTEDFONT = pygame.font.Font('../utils/coders_crux.ttf', 50)

        self.game_name = self.TITLEFONT.render("TYPING MANIAC", 1, (game.BRIGHTBLUE))

        self.menu_items = [
            self.MENUFONT.render("PLAY", 1, (game.WHITE)),
            self.MENUFONT.render("OPTIONS", 1, (game.WHITE)),
            self.MENUFONT.render("CREDITS", 1, (game.WHITE)),
            self.MENUFONT.render("QUIT", 1, (game.WHITE))]
        self.menu_items_selected = [
            self.MENUFONT.render("PLAY", 1, (game.RED)),
            self.MENUFONT.render("OPTIONS", 1, (game.RED)),
            self.MENUFONT.render("CREDITS", 1, (game.RED)),
            self.MENUFONT.render("QUIT", 1, (game.RED))]

    def run(self):
        clock = pygame.time.Clock()
        self.game.DISPLAYSURF.blit(self.bg, (0, 0))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.mode == "menu":
                            running = False
                        else:
                            self.mode = "menu"
                            self.index = 0
                            print(self.index)
                    elif event.key == pygame.K_UP:
                        self.index = (self.index - 1) % 4
                        print(self.index)
                    elif event.key == pygame.K_DOWN:
                        self.index = (self.index + 1) % 4
                        print(self.index)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:

                        # quit
                        if self.mode == "menu" and self.index == 3: 
                            running = False
                        # play -> select map
                        elif self.mode == "menu" and self.index == 0: 
                            print("play now")
                            self.game.run()
                            running = False
                        # options
                        elif self.mode == "menu" and self.index == 1: 
                            pass
                        elif self.mode == "menu" and self.index == 2: 
                            print("credits top kek")
            if running:
                self.draw()

    def draw(self):
        self.game.SCREEN.blit(self.game_name, (450, 200))

        if self.mode == "menu":
            for ind in range(4):
                self.game.SCREEN.blit(self.menu_items[ind], (500, 304 + ind * 80))

                self.game.SCREEN.blit(self.menu_items_selected[self.index], (500, 304 + self.index * 80))
        elif self.mode == "map":
            pass
        elif self.mode == "options":
            pass


        self.game.DISPLAYSURF.blit(self.game.SCREEN, (0, 0))
        pygame.display.flip()

    def pause(self):

        self.game_name_lost = self.TITLEFONT.render("PAUSE", 1, (self.game.BRIGHTBLUE))
        self.display = not self.display
        if self.display is False:
            self.game_name_lost = self.TITLEFONT.render("PAUSE", 1, (self.game.WHITE))

        self.game.SCREEN.blit(self.game_name_lost, (self.game.WINDOWWIDTH / 2 - 100, 300))
        self.game.DISPLAYSURF.blit(self.game.SCREEN, (0, 0))
        pygame.display.flip()
        pygame.time.wait(250)
