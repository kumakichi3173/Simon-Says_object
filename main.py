import pygame
import random
import time

from button import Button # By importing Button we can access methods from the Button class


clock = pygame.time.Clock()


# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BLUE = (80, 80, 155)
font = pygame.font.SysFont("Arial", 50)
text_render = font.render("Score 0", 1, BLUE)



start_ticks=pygame.time.get_ticks()

GREEN_ON = (0, 255, 0)
GREEN_OFF = (0, 200, 0)
RED_ON = (255, 0, 0)
RED_OFF = (200, 0, 0)
BLUE_ON = (0, 0, 255)
BLUE_OFF = (0, 0, 200)
YELLOW_ON = (255, 255, 0)
YELLOW_OFF = (200, 200, 0)

# Pass in respective sounds for each color
GREEN_SOUND = pygame.mixer.Sound("bell1.mp3") # bell1
RED_SOUND = pygame.mixer.Sound("bell2.mp3") # bell2
BLUE_SOUND = pygame.mixer.Sound("bell3.mp3") # bell3
YELLOW_SOUND = pygame.mixer.Sound("bell4.mp3") # bell4



class SimonSays:
    seconds = 3
    highScore = 0
    gameOver = False
    first = True # To see if it's the first round of the game
    cpu_sequence = []

    # Button Sprite Objects
    green = Button(GREEN_ON, GREEN_OFF, GREEN_SOUND, 10, 110)
    red = Button(RED_ON, RED_OFF, RED_SOUND, 260, 110)
    blue = Button(BLUE_ON, BLUE_OFF, BLUE_SOUND, 260, 360)
    yellow = Button(YELLOW_ON, YELLOW_OFF, YELLOW_SOUND, 10, 360)


    def stats(self):
        #scoreShow = pygame.Surface((230, 230))
        #scoreShow.fill("White")
        #font = pygame.font.SysFont("Arial", 50)
        text_render = font.render("Score: " + str(self.score-1), 1, "Black")
        SCREEN.blit(text_render, (10, 10))
        text_render = font.render("Score: " + str(self.score), 1, BLUE)
        SCREEN.blit(text_render, (10, 10))

        text = font.render("Timer: {}".format(self.seconds), True, (255, 255, 255), (0, 0, 0))
        SCREEN.blit(text, (230, 10))


    def resetButton(self, screen, position, text):
        font = pygame.font.SysFont("Arial", 50)
        text_render = font.render(text, 1, (255, 0, 0))
        x, y, w , h = text_render.get_rect()
        x, y = position
        pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
        pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
        pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, w , h))

        return screen.blit(text_render, (x, y))


    '''
    Draws game board
    '''
    def draw_board(self):
        # Call the draw method on all four button objects
        self.green.draw(SCREEN)
        self.red.draw(SCREEN)
        self.blue.draw(SCREEN)
        self.yellow.draw(SCREEN)

    '''
    Chooses a random color and appends to cpu_sequence.
    Illuminates randomly chosen color.
    '''
    def cpu_turn(self):
        colors = ["green", "red", "blue", "yellow"]

        choice = random.choice(colors) # pick random color
        self.cpu_sequence.append(choice) # update cpu sequence
        if choice == "green":
            self.green.update(SCREEN)

        # Check other three color options
        if choice == "blue":
            self.blue.update(SCREEN)
        if choice == "red":
            self.red.update(SCREEN)
        if choice == "yellow":
            self.yellow.update(SCREEN)

    '''
    Plays pattern sequence that is being tracked by cpu_sequence
    '''
    def repeat_cpu_sequence(self):
        if(len(self.cpu_sequence) != 0):
            for color in self.cpu_sequence:
                if color == "green":
                    self.green.update(SCREEN)
                elif color == "red":
                    self.red.update(SCREEN)
                elif color == "blue":
                    self.blue.update(SCREEN)
                else:
                    self.yellow.update(SCREEN)

                pygame.time.wait(500)

    '''
    After cpu sequence is repeated the player must attempt to copy the same
    pattern sequence.
    The player is given 3 seconds to select a color and checks if the selected
    color matches the cpu pattern sequence.
    If player is unable to select a color within 3 seconds then the game is
    over and the pygame window closes.
    '''
    def player_turn(self):
        pygame.event.clear()

        turn_time = time.time()
        players_sequence = []

        while time.time() <= turn_time + 3 and len(players_sequence) < len(self.cpu_sequence):
            text = font.render("Timer: {}".format(self.seconds), True, (0, 0, 0), (0, 0, 0))
            SCREEN.blit(text, (230, 10))

            self.seconds = int(turn_time + 3 - time.time()) + 1
            text = font.render("Timer: {}".format(self.seconds), True, (255, 255, 255), (0, 0, 0))
            SCREEN.blit(text, (230, 10))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # button click occured
                    # Grab the current position of mouse here
                    pos = pygame.mouse.get_pos()
                    if self.green.selected(pos): # green button was selected
                        self.green.update(SCREEN) # illuminate button
                        players_sequence.append("green") # add to player sequence
                        self.check_sequence(players_sequence) # check if player choice was correct
                        turn_time = time.time() # reset timer


                    # Check other three options

                    if self.red.selected(pos): # red button was selected
                        self.red.update(SCREEN) # illuminate button
                        players_sequence.append("red") # add to player sequence
                        self.check_sequence(players_sequence) # check if player choice was correct
                        turn_time = time.time() # reset timer



                    if self.blue.selected(pos): # blue button was selected
                        self.blue.update(SCREEN) # illuminate button
                        players_sequence.append("blue") # add to player sequence
                        self.check_sequence(players_sequence) # check if player choice was correct
                        turn_time = time.time() # reset timer

                
                    if self.yellow.selected(pos): # yellow button was selected
                        self.yellow.update(SCREEN) # illuminate button
                        players_sequence.append("yellow") # add to player sequence
                        self.check_sequence(players_sequence) # check if player choice was correct
                        turn_time = time.time() # reset timer


        # If player does not select a button within 3 seconds then the game closes
        if not time.time() <= turn_time + 3:
            self.game_over()

    '''
    Checks if player's move matches the cpu pattern sequence
    '''
    def check_sequence(self, players_sequence):
        if players_sequence != self.cpu_sequence[:len(players_sequence)]:
            self.game_over()


    '''
    Quits game and closes pygame window
    '''
    def game_over(self):
        pygame.event.clear()

        image = pygame.Surface((500, 600))
        image.fill("Black")
        SCREEN.blit(image, (0, 0))

        # if self.highScore < len(self.cpu_sequence):
            # self.highScore = len(self.cpu_sequence)
        if self.highScore < self.score:
            self.highScore = self.score
            font = pygame.font.SysFont("Arial", 25)
            text_render = font.render("New High Score! " + str(self.highScore), 1, "Gold")
            SCREEN.blit(text_render, (150, 150))

        else:
            font = pygame.font.SysFont("Arial", 25)
            # text_render = font.render("Score:  " + str(len(self.cpu_sequence)), 1, "Gold")
            text_render = font.render("Score:  " + str(self.score), 1, "Gold")
            SCREEN.blit(text_render, (150, 150))
            text_render = font.render("High Score:  " + str(self.highScore), 1, "Gold")
            SCREEN.blit(text_render, (150, 200))

        font = pygame.font.SysFont("Arial", 25)
        text_render = font.render("If you want to restart, ", 1, "White")
        SCREEN.blit(text_render, (150, 300))
        text_render = font.render("click on the reset button!", 1, "White")
        SCREEN.blit(text_render, (150, 325))

        reset = self.resetButton(SCREEN, (150, 400), "RESET")
        self.gameOver = True

        self.score = 0
        self.cpu_sequence = []
        self.first = True


    # Game Loop
    def gameStart(self):
        while self.gameOver == False:
            pygame.event.clear()

            self.score = len(self.cpu_sequence)

            if self.first == True:
                #pygame.display.update()
                self.draw_board() # draws buttons onto pygame screen
                self.stats() # Timer and score
                self.first = False

            #pygame.display.update()

            pygame.time.wait(1000) # waits one second before repeating cpu sequence
            self.draw_board() # draws buttons onto pygame screen

            self.stats() # Timer and score

            self.repeat_cpu_sequence() # repeats cpu sequence if it's not empty

            self.cpu_turn() # cpu randomly chooses a new color

            self.player_turn() # player tries to recreate cpu sequence
            clock.tick(60)
            if self.gameOver == True:
                break

    # This was for the timer of how long the whole game lasts
    def run(self):
        while True:
            pygame.display.update()
            if self.gameOver == False:
                self.gameStart()

            else:
                reset = self.resetButton(SCREEN, (150, 400), "RESET")
                pygame.event.clear()
                #event = pygame.event.wait()  
                while self.gameOver == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.display.quit()
                            pygame.quit()
                            quit()

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if reset.collidepoint(pygame.mouse.get_pos()):
                                self.gameOver = False
                                pygame.event.clear()
                                image = pygame.Surface((500, 600))
                                image.fill("Black")
                                SCREEN.blit(image, (0, 0))

            pygame.display.update()


# main loop
game = SimonSays()
game.run()

