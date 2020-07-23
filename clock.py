import time
import pygame

# Initialize pygame
pygame.init()

# Load in the images that is/are needed in this file, which is only the clock
clockImage = pygame.image.load('ImagesAndComponents/clock.png')

class Clock:

    # In the Initialize method there are a lot that has to be done:
    # first I must take in the time that will be displayed as the time for the clock,
    # then since there will be two clocks, there will be 2 different position but
    # both will have the same dimensions. The images must be loaded. After have a
    # paused variable for when the user is not playing the game, a current time,
    # a boolean for if a second is passed which will determine the new update of the
    # the displayed, firstTimePassed - for when the game starts and finally render the
    # strings (or the time on the clock)
    def __init__(self, time):
        self.blackX = 625
        self.blackY = 30
        self.whiteX = 625
        self.whiteY = 500

        self.width = 150
        self.height = 75
        self.whiteTime = time
        self.blackTime = time

        self.whiteClockImage = pygame.transform.scale(clockImage, (self.width, self.height))
        self.blackClockImage = pygame.transform.scale(clockImage, (self.width, self.height))

        self.paused = True

        self.curerntTime = 0

        self.secondPassed = False
        self.firstTimePassed = False

        self.whiteTimeDisplayed = self.secondsToClock(self.whiteTime)
        self.blackTimeDisplayed = self.secondsToClock(self.blackTime)

        self.f = pygame.font.Font('ImagesAndComponents/DS-DIGIT.ttf', 36)

        self.whiteTextColor = (255, 255, 255)
        self.blackTextColor = (0, 0, 0)

        self.whiteRendered = self.f.render(self.whiteTimeDisplayed, True, self.whiteTextColor, False)
        self.blackRendered = self.f.render(self.blackTimeDisplayed, True, self.blackTextColor, False)


    # Draws both clocks
    def drawClocks(self, screen):

        self.whiteRendered = self.f.render(self.whiteTimeDisplayed, True, self.whiteTextColor, False)
        self.blackRendered = self.f.render(self.blackTimeDisplayed, True, self.blackTextColor, False)

        screen.blit(self.whiteClockImage, (self.whiteX, self.whiteY))
        screen.blit(self.whiteRendered, (self.whiteX + 35, self.whiteY + 19))

        screen.blit(self.blackClockImage, (self.blackX, self.blackY))
        screen.blit(self.blackRendered, (self.blackX + 35, self.blackY + 19))

    # Update the time whenever a second passes, pass in the turn to know which to update
    def update(self, turn):
        if not self.firstTimePassed:
            self.currentTime = int(time.time())
            self.firstTimePassed = True

        if self.currentTime < int(time.time()):
            self.secondPassed = True
            self.currentTime = int(time.time())

        if self.secondPassed:
            if turn == 1:
                self.whiteTime -= 1
                self.whiteTimeDisplayed = self.secondsToClock(self.whiteTime)
            else:
                self.blackTime -= 1
                self.blackTimeDisplayed = self.secondsToClock(self.blackTime)

        self.secondPassed = False

    # Quick methods that converts the amound of seconds remaining to a regular digital time.
    # Future: Since I made the higehst time as an house, there isnt a place for the hours position
    # in other words it is only minutes:seconds
    def secondsToClock(self, t) -> str:
        minutes = int(t / 60)
        seconds = t % 60

        return "{}:{}".format(minutes, seconds) if seconds >= 10 else "{}:0{}".format(minutes, seconds)
