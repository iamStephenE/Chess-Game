import pygame
import sys

# Load all the necessary pictures
wbishop = pygame.image.load('AllChessPieces/WhiteBishop.png')
wbishop = pygame.transform.scale(wbishop, (70, 70))

wknight = pygame.image.load('AllChessPieces/WhiteKnight.png')
wknight = pygame.transform.scale(wknight, (70, 70))

wqueen = pygame.image.load('AllChessPieces/WhiteQueen.png')
wqueen = pygame.transform.scale(wqueen, (73, 73))

wrook = pygame.image.load('AllChessPieces/WhiteRook.png')
wrook = pygame.transform.scale(wrook, (70, 70))

bbishop = pygame.image.load('AllChessPieces/BlackBishop.png')
bbishop = pygame.transform.scale(bbishop, (70, 70))

bknight = pygame.image.load('AllChessPieces/BlackKnight.png')
bknight = pygame.transform.scale(bknight, (70, 70))

bqueen = pygame.image.load('AllChessPieces/BlackQueen.png')
bqueen = pygame.transform.scale(bqueen, (73, 73))

brook = pygame.image.load('AllChessPieces/BlackRook.png')
brook = pygame.transform.scale(brook, (70, 70))

background1 = pygame.image.load('ImagesAndComponents/ChessBackground.jpg')
background1 = pygame.transform.scale(background1, (800, 600))

backArrow = pygame.image.load('ImagesAndComponents/BackArrow.png')
backArrow = pygame.transform.scale(backArrow, (40, 40))

checkMark = pygame.image.load('ImagesAndComponents/CheckMark.png')
checkMark = pygame.transform.scale(checkMark, (40, 40))

restartGameButton = pygame.image.load('ImagesAndComponents/RestartGameButton.png')
restartGameButton = pygame.transform.scale(restartGameButton, (150, 150))

restartGameButtonHighlighted = pygame.image.load('ImagesAndComponents/RestartGameButtonHighlighted.png')
restartGameButtonHighlighted = pygame.transform.scale(restartGameButtonHighlighted, (155, 155))

undo = pygame.image.load('ImagesAndComponents/Undo.png')
undo = pygame.transform.scale(undo, (95, 95))

undoHighlighted = pygame.image.load('ImagesAndComponents/UndoHighlighted.png')
undoHighlighted = pygame.transform.scale(undoHighlighted, (97, 97))

homeButton = pygame.image.load('ImagesAndComponents/HomeButton.png')
homeButton = pygame.transform.scale(homeButton, (95, 95))

homeButtonHighlighted = pygame.image.load('ImagesAndComponents/HomeButtonHighlighted.png')
homeButtonHighlighted = pygame.transform.scale(homeButtonHighlighted, (97, 97))

# Colors:
DGREEN = (1, 49, 31)
LGREEN = (50, 100, 50)

BROWN = (215, 200, 160)
YELLOW = (212, 180, 74)

DGRAY = (35, 35, 35)
GRAY = (150, 150, 150)

DBLUE = (0, 57, 76)
LBLUE = (51, 184, 229)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# The displayer class will pretty much take care of everything displayed on the screen.
# It basically acts like a manager for what is being displayed via the array screenDisplayed
class Displayer:

    # The displayer class is initialized with the basic settings
    def __init__(self):
        self.theme = (DGRAY, GRAY)
        self.themeID = 'dg/g'
        self.themeIDPos = (290, 240)
        self.gameTime = (600, (275, 350))

        self.inThemes = False
        self.inAbout = False
        self.inGame = False

        self.pawnPromoting = False
        self.background = background1

    # Displays the main menue
    def displayMainMenu(self, screen, screenDisplayed, ev):
        f = pygame.font.Font('freesansbold.ttf', 90)
        mainRendered = f.render('Main Menu', True, WHITE)
        screen.blit(mainRendered, (165, 65))

        f = pygame.font.Font('freesansbold.ttf', 40)

        self.displayButton(screen, screenDisplayed, 210, 230, f, 'Play Game / Resume', 'Playing', ev)
        self.displayButton(screen, screenDisplayed, 335, 320, f, 'Setting', 'Setting', ev)
        self.displayButton(screen, screenDisplayed, 295, 410, f, 'Info / About', 'Info Page', ev)
        self.displayButton(screen, screenDisplayed, 360, 500, f, 'Quit', 'Quit', ev)

    # Displays the setting page
    def displaySettingPage(self, screen, screenDisplayed, ev):
        f = pygame.font.Font('freesansbold.ttf', 90)
        mainRendered = f.render('Setting', True, WHITE)
        screen.blit(mainRendered, (245, 65))

        f = pygame.font.Font('freesansbold.ttf', 40)

        self.displayButton(screen, screenDisplayed, 260, 230, f, 'Board Themes', 'Themes', ev)
        self.displayButton(screen, screenDisplayed, 285, 320, f, 'Adjust Time', 'Time', ev)

        self.goBack(screen, screenDisplayed, ev)

    # Displays buttons
    def displayButton(self, screen, screenDisplayed, x, y, font, title, action, ev):
        rendered = font.render(title, True, WHITE, False)

        if pygame.mouse.get_pos()[1] > y - 5 and pygame.mouse.get_pos()[1] < y + rendered.get_height() + 5:
            if pygame.mouse.get_pos()[0] > x - 5 and pygame.mouse.get_pos()[0] < x + rendered.get_width() + 5:
                pygame.draw.rect(screen, (0, 80, 0), (x - 5, y - 5, rendered.get_width() + 10, rendered.get_height() + 10), 4)
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if action == 'Quit':
                            sys.exit()
                        else:
                            screenDisplayed.append(action)

        screen.blit(rendered, (x, y))

    # Here there is a little displayer for when a pawn is about to promote, it shows the options
    def displayPawnPromotingOptions(self, turn, screen, ev) -> str:

        currentMousePos = pygame.mouse.get_pos()

        selectionBox_x = 200
        selectionBox_y = 300-37
        pygame.draw.rect(screen, BLACK, (selectionBox_x, selectionBox_y, 75*4+15, 75+6))

        if currentMousePos[1] > selectionBox_y and currentMousePos[1] < selectionBox_y+75+3:
            if currentMousePos[0] > selectionBox_x + 3 and currentMousePos[0] < selectionBox_x+75+3:
                pygame.draw.rect(screen, (0, 100, 0), (selectionBox_x+3, selectionBox_y+3, 75, 75))
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return 'queen'
                        self.pawnPromoting = False
            elif currentMousePos[0] > selectionBox_x + 6 + 75 and currentMousePos[0] < selectionBox_x+75*2+6:
                pygame.draw.rect(screen, (0, 100, 0), (selectionBox_x + 6 + 75, selectionBox_y+3, 75, 75))
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return 'rook'
                        self.pawnPromoting = False
            elif currentMousePos[0] > selectionBox_x + 9 + 150 and currentMousePos[0] < selectionBox_x+75*3+9:
                pygame.draw.rect(screen, (0, 100, 0), (selectionBox_x + 9 + 150, selectionBox_y+3, 75, 75))
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return 'bishop'
                        self.pawnPromoting = False
            elif currentMousePos[0] > selectionBox_x + 12 + 225 and currentMousePos[0] < selectionBox_x+75*4+12:
                pygame.draw.rect(screen, (0, 100, 0), (selectionBox_x + 12 + 225, selectionBox_y+3, 75, 75))
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return 'knight'
                        self.pawnPromoting = False

        if turn == -1:
            screen.blit(wqueen, (selectionBox_x+3, selectionBox_y+3))
            screen.blit(wrook, (selectionBox_x + 6 + 75, selectionBox_y+5))
            screen.blit(wbishop, (selectionBox_x + 9 + 150, selectionBox_y+5))
            screen.blit(wknight, (selectionBox_x + 12 + 225, selectionBox_y+5))
        else:
            screen.blit(bqueen, (selectionBox_x+3, selectionBox_y+3))
            screen.blit(brook, (selectionBox_x + 6 + 75, selectionBox_y+5))
            screen.blit(bbishop, (selectionBox_x + 9 + 150, selectionBox_y+5))
            screen.blit(bknight, (selectionBox_x + 12 + 225, selectionBox_y+5))

    # Displays the themes
    def displayThemes(self, screen, screenDisplayed, ev):
        f = pygame.font.Font('freesansbold.ttf', 48)
        topTitle = f.render('Select From Displayed', True, WHITE)
        botTitle = f.render('Themes!', True, WHITE)

        screen.blit(topTitle, (130, 60))
        screen.blit(botTitle, (300, 120))

        f = pygame.font.Font('freesansbold.ttf', 30)


        self.displayThemeOptions(screen, screenDisplayed, 290, 240, f, 'Classic', DGRAY, GRAY, 'dg/g', ev)
        self.displayThemeOptions(screen, screenDisplayed, 295, 330, f, 'Sandy', BROWN, YELLOW, 'b/y', ev)
        self.displayThemeOptions(screen, screenDisplayed, 320, 420, f, 'Icy', DBLUE, LBLUE, 'db/lb', ev)
        self.displayThemeOptions(screen, screenDisplayed, 290, 510, f, 'Grassy', DGREEN, LGREEN, 'dg/lg', ev)

        screen.blit(checkMark, (525, self.themeIDPos[1] - 5))
        self.goBack(screen, screenDisplayed, ev)

    # Display all the theme options
    def displayThemeOptions(self, screen, screenDisplayed, x, y, font, string, c1, c2, id, ev):
        rendered = font.render(string, True, WHITE, False)
        pygame.draw.rect(screen, c1, (x + rendered.get_width() + 10, y - 10, 50, 50))
        pygame.draw.rect(screen, c2, (x + rendered.get_width() + 60, y - 10, 50, 50))

        if pygame.mouse.get_pos()[1] > y - 10 and pygame.mouse.get_pos()[1] < y + rendered.get_height() + 15:
            if pygame.mouse.get_pos()[0] > x - 10 and pygame.mouse.get_pos()[0] < x + rendered.get_width() + 130:
                pygame.draw.rect(screen, (0, 80, 0), (x - 10, y - 15, rendered.get_width() + 130, rendered.get_height() + 30), 4)
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.theme = (c1, c2)
                        self.themeID == id
                        self.themeIDPos = (x, y)

        screen.blit(rendered, (x, y))

    # Displays the time page
    def displayTimePage(self, screen, screenDisplayed, ev):
        f = pygame.font.Font('freesansbold.ttf', 90)
        mainRendered = f.render('Game Duration', True, WHITE)
        screen.blit(mainRendered, (60, 70))

        f = pygame.font.Font('freesansbold.ttf', 30)

        if (self.displayAndPickTime(screen, screenDisplayed, 350, 230, f, '1 Hour', 3600, ev) or \
        self.displayAndPickTime(screen, screenDisplayed, 325, 290, f, '30 Minutes', 1800, ev) or \
        self.displayAndPickTime(screen, screenDisplayed, 325, 350, f, '10 Minutes', 600, ev) or \
        self.displayAndPickTime(screen, screenDisplayed, 335, 410, f, '5 Minutes', 300, ev) or \
        self.displayAndPickTime(screen, screenDisplayed, 335, 470, f, '3 Minutes', 180, ev) or \
        self.displayAndPickTime(screen, screenDisplayed, 335, 530, f, '1 Minute', 60, ev)):
            return True

        screen.blit(checkMark, (500, self.gameTime[1][1] - 5))

        self.goBack(screen, screenDisplayed, ev)

    # Displays the options on the time page and also sets it when one is picked
    def displayAndPickTime(self, screen, screenDisplayed, x, y, font, string, time, ev) -> bool:
        rendered = font.render(string, True, WHITE, False)

        if pygame.mouse.get_pos()[1] > y - 5 and pygame.mouse.get_pos()[1] < y + rendered.get_height() + 5:
            if pygame.mouse.get_pos()[0] > x - 5 and pygame.mouse.get_pos()[0] < x + rendered.get_width() + 5:
                pygame.draw.rect(screen, (0, 80, 0), (x - 5, y - 5, rendered.get_width() + 10, rendered.get_height() + 10), 4)
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.gameTime = (time, (x, y))
                        return True

        screen.blit(rendered, (x, y))
        return False

    # Displays the black side panel when the game is playing
    def displayGameSidePanel(self, screen, screenDisplayed, entireGameStates, tempBoard):
        pygame.draw.rect(screen, BLACK, (600, 0, 200, 600))

        f = pygame.font.Font('freesansbold.ttf', 18)

    # When the reset button is pressed it returns true and in the main class I reset
    # the board
    def resetGame(self, screen, ev) -> bool:
        x = 625
        y = 200

        screen.blit(restartGameButton, (x, y))

        f = pygame.font.Font('freesansbold.ttf', 36)
        rendered1 = f.render('Restart', True, BLACK, False)
        rendered2 = f.render('Game', True, BLACK, False)

        if pygame.mouse.get_pos()[1] > y - 5 and pygame.mouse.get_pos()[1] < y + restartGameButton.get_height() + 5:
            if pygame.mouse.get_pos()[0] > x - 5 and pygame.mouse.get_pos()[0] < x + restartGameButton.get_width() + 5:
                #pygame.draw.rect(screen, (0, 80, 0), (x - 5, y - 5, restartGameButton.get_width() + 10, restartGameButton.get_height() + 10), 4)
                screen.blit(restartGameButtonHighlighted, (x - 2, y - 2))
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return True

        screen.blit(rendered1, (x + 12, y + 35))
        screen.blit(rendered2, (x + 22, y + 85))

        return False

    # Displays the home button
    def displayHomeButton(self, screen, screenDisplayed, ev):
        x = 610
        y = 355

        screen.blit(homeButton, (x, y))

        if pygame.mouse.get_pos()[1] > y - 2 and pygame.mouse.get_pos()[1] < y + homeButton.get_height() + 2:
            if pygame.mouse.get_pos()[0] > x - 2 and pygame.mouse.get_pos()[0] < x + homeButton.get_width() + 2:
                screen.blit(homeButtonHighlighted, (x - 1, y - 1))
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        del screenDisplayed[-1]

    # Displays the undo button
    def displayUndoButton(self, screen, ev):
        x = 695
        y = 355

        screen.blit(undo, (x, y))

        if pygame.mouse.get_pos()[1] > y - 2 and pygame.mouse.get_pos()[1] < y + undo.get_height() + 2:
            if pygame.mouse.get_pos()[0] > x - 2 and pygame.mouse.get_pos()[0] < x + undo.get_width() + 2:
                screen.blit(undoHighlighted, (x - 1, y - 1))
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        return True

        return False

    # Displays the information page
    def displayInfoPage(self, screen, screenDisplayed, ev):
        f = pygame.font.Font('freesansbold.ttf', 48)
        topTitle = f.render('Information About Game', True, WHITE)
        botTitle = f.render('And Me!', True, WHITE)

        screen.blit(topTitle, (110, 55))
        screen.blit(botTitle, (300, 115))

        f = pygame.font.Font('freesansbold.ttf', 36)

        gameInfoTitle = f.render('Game Information: ', True, WHITE)
        screen.blit(gameInfoTitle, (15, 185))

        aboutMeTitle = f.render('About me: ', True, WHITE)
        screen.blit(aboutMeTitle, (15, 400))

        f = pygame.font.Font('freesansbold.ttf', 16)

        # Paragraphs for basic information
        gameInfoParagraph = ['This is a chess game that was created with my basic knowledge of python', \
                            'and pygame. It has all the rules of chess implemented, however there are ', \
                            'some functionalities that would be nice if they are added such as: flipping ', \
                            'the board, etc. The things implemented are: board themes, undo functions, and ', \
                            'resetting the game. Maybe I\'ll come back to this game one day in the future ', \
                            'and make it better and more efficient! :)']

        aboutMeParagraph = ['Hello my name is Stephen and at the time of creating this game I am 17', \
                            'years old. This is the first game that I made where I had to put thought', \
                            'into the design, interface, friendliness, and flow of the project. Although ', \
                            'it is not a very complicated project, it is a stepping stone to build my', \
                            'foundation about python and designing structures in general. Plus I really ', \
                            'enjoyed programing it! Thank you for playing and I hope you enjoy!']

        for index in range(len(gameInfoParagraph)):
            screen.blit(f.render(gameInfoParagraph[index], True, WHITE), (15, 238 + 25 * index))
            screen.blit(f.render(aboutMeParagraph[index], True, WHITE), (15, 450 + 25 * index))

        self.goBack(screen, screenDisplayed, ev)


    # This is the go back function at the top left of the pages
    def goBack(self, screen, screenDisplayed, ev):
        circleX = 10
        circleY = 10
        diameter = backArrow.get_width()
        radius = int(diameter / 2)

        if pygame.mouse.get_pos()[1] > circleY and pygame.mouse.get_pos()[1] < circleY + diameter:
            if pygame.mouse.get_pos()[0] > circleX and pygame.mouse.get_pos()[0] < circleX + diameter:
                pygame.draw.circle(screen, WHITE, (circleX + radius, circleY + radius), radius)
                for event in ev:
                    if event.type == pygame.MOUSEBUTTONUP:
                        del screenDisplayed[-1]

        screen.blit(backArrow, (circleX, circleY))
