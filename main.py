# Import all need modules
import pygame
import random
import sys
import time
import threading
from clock import Clock

# Importing the pieces
from Displayer import Displayer
from Pawn import Pawn
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Queen import Queen
from King import King

# Initialization
pygame.init()

# Permanent variables: Scale, each block size, width, height, dimensions
WIDTH = 800
HEIGHT = 600

DIMENSIONS = (WIDTH, HEIGHT)
SCL = 8
PCESIZE = int(HEIGHT / SCL)

# Setting up pygame
screen = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption('Chess Game!')

# Colors
DGREEN = (1, 49, 31)
LGREEN = (2, 78, 50)
DGRAY = (45, 45, 45)
GRAY = (100, 100, 100)

# Global variables
gameRunning = True
snappedIn = False
mouseID = ""
turn = 1
oneSelected = False
selectedPos = ()
timeOver = False
checkMate = False

# String for winner
winnerMate = ''
# when you promote a pawn and you use the undo button this boolean is
# used because in the way my board was programmed, I its like moving the pawn
# THEN i change the piece so the number of moves goes twice, so this variable
# allows it to go back twice if it is true
justChanged = False

displayer = Displayer()

# How will the board look like:
# piece in board (Array): {attributes shown in the piece's class}
# The board will be an array of these dictionaries
entireGameStates = []
tempBoard = []

# array that is used to determine which screen is being displayed
screenDisplayed = ['Main Menu']
pawnPromotingPos = (-1, -1)

# global check for if either king is in check
mainCheck = False

# Clock or timer for the game
clock = Clock(displayer.gameTime[0])

# Maybe this is enifficient but for some reason when making a copy of an 2d array
# the inner arrays are pointing at the same thing, so this makes a complete
# new instance of the given 2d array (current game instance or state)
def makeCopy(b):
    answer = []
    for y in range(SCL):
        answer.append([])
        for x in range(SCL):
            answer[y].append(b[y][x])

    return answer

# This methods resets the time of the game that is going on, it is called when
# The player either chooses a new time from the setting or when you restart the
# game from the button next to the chess board
def resetTime():
    global turn

    clock.whiteTime = displayer.gameTime[0]
    clock.blackTime = displayer.gameTime[0]

    clock.curerntTime = 0

    clock.secondPassed = False
    clock.firstTimePassed = False

    clock.whiteTimeDisplayed = clock.secondsToClock(clock.whiteTime)
    clock.blackTimeDisplayed = clock.secondsToClock(clock.blackTime)

    turn = 1

# Initialization method for board
def initializeBoard():
    # Make everything none first
    for y in range(SCL):
        tempBoard.append([])
        for x in range(SCL):
            tempBoard[y].append(None)

    # Add all the rooks
    tempBoard[0][0] = Rook(0, 0, 'black', 0, False)
    tempBoard[0][7] = Rook(0, 7, 'black', 0, False)
    tempBoard[7][0] = Rook(7, 0, 'white', 0, False)
    tempBoard[7][7] = Rook(7, 7, 'white', 0, False)

    # Add all the knights
    tempBoard[0][1] = Knight(0, 1, 'black', 0, False)
    tempBoard[0][6] = Knight(0, 6, 'black', 0, False)
    tempBoard[7][1] = Knight(7, 1, 'white', 0, False)
    tempBoard[7][6] = Knight(7, 6, 'white', 0, False)

    # Add all the bishops
    tempBoard[0][2] = Bishop(0, 2, 'black', 0, False)
    tempBoard[0][5] = Bishop(0, 5, 'black', 0, False)
    tempBoard[7][2] = Bishop(7, 2, 'white', 0, False)
    tempBoard[7][5] = Bishop(7, 5, 'white', 0, False)

    # Add the Queens
    tempBoard[0][3] = Queen(0, 3, 'black', 0, False)
    tempBoard[7][3] = Queen(7, 3, 'white', 0, False)

    # Add the Kings
    tempBoard[0][4] = King(0, 4, 'black', 0, False, screen)
    tempBoard[7][4] = King(7, 4, 'white', 0, False, screen)

    # Add in all the pawns
    for x in range(SCL):
        tempBoard[1][x] = Pawn(1, x, 'black', 0, False, screen)

    for x in range(SCL):
        tempBoard[6][x] = Pawn(6, x, 'white', 0, False, screen)


    # Add it in as the first state of the board
    entireGameStates.append(makeCopy(tempBoard))

initializeBoard()

# After a piece is moved I use this method to call the move method from
# the piece's object and then update the position that the piece was
# at by reseting it (setting it equal to None)
def resetAfterNewMove(y, x):
    global turn
    global justChanged

    tempBoard[y][x].moveToNextPosition(y, x, tempBoard, turn, entireGameStates, screen)
    entireGameStates[-1][y][x].held = False
    entireGameStates[-1][y][x].selected = False
    oneSelected = False
    turn *= -1
    selectedPos = ()
    entireGameStates.append(makeCopy(tempBoard))

    justChanged = False

# This method removes the last selected thing, which occurs when you ar selecting
# the same color but different pieces, it resets the previous pieces that was
# selected so that it is only focused on one current selected piece
def removePreviousSelection(board, py, px):
    for y in range(SCL):
        for x in range(SCL):
            if board[y][x] != None:
                board[y][x].selected = False
    board[py][px].selected = True

# Draws board background only
# I want to have an implimentation later where the user
# can change the theme of the board.....maybe ill add it
def drawBoard(theme) -> None:
    count = 0
    for y in range(SCL):
        for x in range(SCL):
            tempRect = pygame.Rect(x*PCESIZE, y*PCESIZE, PCESIZE, PCESIZE)
            if(count % 2 == 0):
                pygame.draw.rect(screen, theme[1], tempRect)
            else:
                pygame.draw.rect(screen, theme[0], tempRect)

            count += 1
        count += 1

# Check if when I click the mouse there is an object underneath,
# not none. If there is an object, return the boolean and also the
# mouse position which will be used to figure out the specific piece at that
# position on the grid.
def mouseOnObj(pos) -> (bool, str):
    if pos[0] < 600:
        xID = int(pos[0] / PCESIZE)
        yID = int(pos[1] / PCESIZE)

        if tempBoard[yID][xID] != None:
            if (turn == 1 and tempBoard[yID][xID].color == 'white') or (turn == -1 and tempBoard[yID][xID].color == 'black'):
                return True, "{}{}".format(yID, xID)

    return False, None

def positionInCheck() -> (bool, str):

    # Get the current position of the king that is in check
    for y in range(SCL):
        for x in range(SCL):
            if tempBoard[y][x] != None and (tempBoard[y][x].reference == 'white king' or tempBoard[y][x].reference == 'black king'):
                tempBoard[y][x].checkCurrentPosition(tempBoard, y, x, tempBoard[y][x].color, screen, turn, entireGameStates)
                if tempBoard[y][x].inCheck and not((tempBoard[y][x].color == 'white' and turn == 1) or (tempBoard[y][x].color == 'black' and turn == -1)):
                    return True, tempBoard[y][x].color
    return False, ''


# Game loop
while gameRunning:
    # Get all the events in the beginning of everyloop so I dont need to
    # make one every single time in a forloop
    ev = pygame.event.get()

    # Menu Background picture
    screen.blit(displayer.background, (0, 0))

    # For all the screenDisplayed[-1], I check which screen I should be displaying
    if screenDisplayed[-1] == 'Main Menu':

        # Looking at any key events
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()

        displayer.displayMainMenu(screen, screenDisplayed, ev)

    elif screenDisplayed[-1] == 'Playing':

        # check if the time is over for any side
        if clock.whiteTime <= 0:
            timeOver = True
        if clock.blackTime <= 0:
            timeOver = True

        #screen.fill(displayer.theme)
        # Check for all events occuring
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del screenDisplayed[-1]


            # When i click the mouse I check for all of these things:
            # object exisits, nothing is snapped in (being dragged around)
            # IMPLEMENT: when the object is selected, next time you select an object
            # to be taken, take it instead of selecting it again....
            if not timeOver and not checkMate and event.type == pygame.MOUSEBUTTONDOWN and mouseOnObj(pygame.mouse.get_pos())[0]:
                mouseID = mouseOnObj(pygame.mouse.get_pos())[1]
                if tempBoard[int(mouseID[0])][int(mouseID[1])] != None:
                    if (turn == 1 and tempBoard[int(mouseID[0])][int(mouseID[1])].color == 'white') or (turn == -1 and tempBoard[int(mouseID[0])][int(mouseID[1])].color == 'black'):
                        tempBoard[int(mouseID[0])][int(mouseID[1])].held = True
                        tempBoard[int(mouseID[0])][int(mouseID[1])].selected = True
                        oneSelected = True
                        selectedPos = (int(mouseID[0]), int(mouseID[1]))
                        removePreviousSelection(tempBoard, int(mouseID[0]), int(mouseID[1]))
                        snappedIn = True

            # When I let go of the mouse I check if it is a legal move and if so move it
            # and then update the board and the entireGameStates
            if not timeOver and not checkMate and len(mouseID) > 0 and event.type == pygame.MOUSEBUTTONUP:
                if tempBoard[int(mouseID[0])][int(mouseID[1])] != None:
                    if tempBoard[int(mouseID[0])][int(mouseID[1])].legalMove(int(mouseID[0]), int(mouseID[1]), tempBoard, turn, entireGameStates):
                        resetAfterNewMove(int(mouseID[0]), int(mouseID[1]))
                        if positionInCheck()[0] and (positionInCheck()[1] == 'white' and turn == -1) or (positionInCheck()[1] == 'black' and turn == 1):
                            del entireGameStates[-1]
                            tempBoard = makeCopy(entireGameStates[-1])
                            turn *= -1
                            oneSelected = False
                            selectedPos = ()

                    # I realized there was problem that when I clicked the second time,
                    # I made a new mouse position and that is why i dont move the piece to that position
                    # this is why I had to save in tuple the (y, x) for where the selected piece
                    # exists and follow with that
                    elif oneSelected and tempBoard[selectedPos[0]][selectedPos[1]] != None and tempBoard[selectedPos[0]][selectedPos[1]].legalMove(selectedPos[0], selectedPos[1], tempBoard, turn, entireGameStates):
                        resetAfterNewMove(selectedPos[0], selectedPos[1])
                        if positionInCheck()[0] and (positionInCheck()[1] == 'white' and turn == -1) or (positionInCheck()[1] == 'black' and turn == 1):
                            del entireGameStates[-1]
                            tempBoard = makeCopy(entireGameStates[-1])
                            turn *= -1
                            oneSelected = False
                            selectedPos = ()
                    else:
                        tempBoard[int(mouseID[0])][int(mouseID[1])].held = False
                snappedIn = False

            # Using the backspace key, i added this to implement an undo function
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and len(entireGameStates) > 1:
                    if justChanged:
                        del entireGameStates[-1]
                        justChanged = False
                    del entireGameStates[-1]
                    tempBoard = makeCopy(entireGameStates[-1])
                    turn *= -1
                    oneSelected = False
                    selectedPos = ()
                    positionInCheck()
                    for x in range(SCL):
                        if entireGameStates[-1][0][x] != None and entireGameStates[-1][0][x].reference[-4:] == 'pawn':
                            turn *= -1

                        if entireGameStates[-1][7][x] != None and entireGameStates[-1][7][x].reference[-4:] == 'pawn':
                            turn *= -1
                    displayer.pawnPromoting = False

        # Draw board background
        drawBoard(displayer.theme)

        # The order is for these nested for loops is essential for the presentation of
        # the game and how it looks, other wise the pieces or the block of the board will
        # be jumbled toggether and unorganized, not good visuals

        if not timeOver:
            # This code serves many essential functions as it goes through the  board:
            # firstly it goes shows all the possible moves for all the pieces and stores them,
            # it checks if the king is being attacked, draws all the pieces, if they are held it is
            # drawn at where the mouse is instead, and checks for it the pawns are promoting.
            for y in range(SCL):
                for x in range(SCL):
                    if entireGameStates[-1][y][x] != None:
                        entireGameStates[-1][y][x].showPossibleMoves(y, x, tempBoard, turn, entireGameStates, screen, True)
                        if entireGameStates[-1][y][x].reference[-4:] == 'king':
                            entireGameStates[-1][y][x].checkCurrentPosition(tempBoard, y, x, tempBoard[y][x].color, screen, turn, entireGameStates)
                            if entireGameStates[-1][y][x].inCheck:
                                pygame.draw.rect(screen, (200, 0, 0), (x * PCESIZE, y * PCESIZE, PCESIZE, PCESIZE))
                        if not entireGameStates[-1][y][x].held:
                            entireGameStates[-1][y][x].drawPiece(screen)
                        if entireGameStates[-1][y][x].held:
                            screen.blit(entireGameStates[-1][int(mouseID[0])][int(mouseID[1])].image, (int(pygame.mouse.get_pos()[0] - PCESIZE / 2 + entireGameStates[-1][int(mouseID[0])][int(mouseID[1])].displacement), int(pygame.mouse.get_pos()[1] - PCESIZE / 2 + entireGameStates[-1][int(mouseID[0])][int(mouseID[1])].displacement)))
                        if entireGameStates[-1][y][x].reference == 'white pawn' and y == 0:
                            displayer.pawnPromoting = True
                            pawnPromotingPos = (y, x)
                        if entireGameStates[-1][y][x].reference == 'black pawn' and y == 7:
                            displayer.pawnPromoting = True
                            pawnPromotingPos = (y, x)

        # Here it pretty much checks for checkmates and if the king is in check.
        for y in range(SCL):
            for x in range(SCL):
                if entireGameStates[-1][y][x] != None:
                    if entireGameStates[-1][y][x].reference[-4:] == 'king':
                        entireGameStates[-1][y][x].checkCurrentPosition(tempBoard, y, x, tempBoard[y][x].color, screen, turn, entireGameStates)
                    if (entireGameStates[-1][y][x].reference == 'black king' or entireGameStates[-1][y][x].reference == 'white king') and entireGameStates[-1][y][x].inCheck:
                        mainCheck = True
                        mate = entireGameStates[-1][y][x].inCheckMate(tempBoard, screen, turn, entireGameStates)
                        if mate[0]:
                            checkMate = True
                            winnerMate = 'Black' if mate[1] == 'white' else 'White'

        # Here the possible moves that are the little red dots that indicate
        # Where the piece can move are displayed.
        for y in range(SCL):
            for x in range(SCL):
                if entireGameStates[-1][y][x] != None:
                    if entireGameStates[-1][y][x].selected:
                        entireGameStates[-1][y][x].showPossibleMoves(int(mouseID[0]), int(mouseID[1]), tempBoard, turn, entireGameStates, screen, False)
                        pygame.draw.rect(screen, (100, 0, 100), (x*PCESIZE, y*PCESIZE, PCESIZE, PCESIZE), 2)
                    entireGameStates[-1][y][x].highlightedAttacks = []


        # The side panel that has the options you can click during the game when it is on
        displayer.displayGameSidePanel(screen, screenDisplayed, entireGameStates, tempBoard)

        # Check if the player presses the undo button and go back a move.
        # There are many things that need to accounted for here such as changing
        # some of the global variables if needed, check some conditions for if a pawn
        # just promoted and if so you must go back twice so the turns dont mess up.
        if displayer.displayUndoButton(screen, ev) and len(entireGameStates) > 1:
            if justChanged:
                del entireGameStates[-1]
                justChanged = False
            del entireGameStates[-1]
            tempBoard = makeCopy(entireGameStates[-1])
            turn *= -1
            oneSelected = False
            selectedPos = ()
            positionInCheck()
            for x in range(SCL):
                if entireGameStates[-1][0][x] != None and entireGameStates[-1][0][x].reference[-4:] == 'pawn':
                    turn *= -1

                if entireGameStates[-1][7][x] != None and entireGameStates[-1][7][x].reference[-4:] == 'pawn':
                    turn *= -1
            displayer.pawnPromoting = False

        # display the home button on the side panel
        displayer.displayHomeButton(screen, screenDisplayed, ev)

        # When there is a pawn promoting, display the options and promote it by picking.
        if not timeOver and not checkMate and displayer.pawnPromoting:
            newPiece = displayer.displayPawnPromotingOptions(turn, screen, ev)
            if newPiece != None:
                if newPiece == 'rook':
                    tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]] = Rook(pawnPromotingPos[0], pawnPromotingPos[1], tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].color, tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].totalMoves + 1, False)

                elif newPiece == 'knight':
                    tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]] = Knight(pawnPromotingPos[0], pawnPromotingPos[1], tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].color, tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].totalMoves + 1, False)

                elif newPiece == 'queen':
                    tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]] = Queen(pawnPromotingPos[0], pawnPromotingPos[1], tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].color, tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].totalMoves + 1, False)

                elif newPiece == 'bishop':
                    tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]] = Bishop(pawnPromotingPos[0], pawnPromotingPos[1], tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].color, tempBoard[pawnPromotingPos[0]][pawnPromotingPos[1]].totalMoves + 1, False)

                displayer.pawnPromoting = False
                justChanged = True
                oneSelected = False
                selectedPos = ()
                entireGameStates.append(makeCopy(tempBoard))


        # Update and draw the clock
        if not timeOver and not checkMate:
            clock.update(turn)
            clock.drawClocks(screen)

        # check if the player clicked the reset the game button and reset it
        if  displayer.resetGame(screen, ev):
            entireGameStates = []
            tempBoard = []
            turn = 1
            initializeBoard()
            resetTime()
            timeOver = False
            checkMate = False

        # If the time is over display the time over screen and winner
        if timeOver:
            winner = 'White' if clock.whiteTime > clock.blackTime else 'Black'
            f = pygame.font.Font('freesansbold.ttf', 48)
            rendered = f.render(winner + ' wins on time!', True, (255, 255, 255), False)
            pygame.draw.rect(screen, (0, 0, 0), (PCESIZE - 25, 250, 6 * PCESIZE + 50, 100))
            screen.blit(rendered, (PCESIZE - 10, 275))

        # If a side wins by checkmate, display the color that won.
        if checkMate:
            f = pygame.font.Font('freesansbold.ttf', 48)
            rendered = f.render(winnerMate + ' wins by mate!', True, (255, 255, 255), False)
            pygame.draw.rect(screen, (0, 0, 0), (PCESIZE - 25, 250, 6 * PCESIZE + 50, 100))
            screen.blit(rendered, (PCESIZE - 10, 275))


    # Displaying the info page as the screen
    elif screenDisplayed[-1] == 'Info Page':
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del screenDisplayed[-1]

        displayer.displayInfoPage(screen, screenDisplayed, ev)

    # Displaying the setting page as the screen
    elif screenDisplayed[-1] == 'Setting':
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del screenDisplayed[-1]

        displayer.displaySettingPage(screen, screenDisplayed, ev)

    # Displaying the time page as the screen
    elif screenDisplayed[-1] == 'Time':
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del screenDisplayed[-1]

        if displayer.displayTimePage(screen, screenDisplayed, ev):
            clock.whiteTime = displayer.gameTime[0]
            clock.blackTime = displayer.gameTime[0]
            entireGameStates = []
            tempBoard = []
            turn = 1
            initializeBoard()
            resetTime()

    # Displaying the Themes page as the screen
    elif screenDisplayed[-1] == 'Themes':
        for event in ev:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    del screenDisplayed[-1]

        displayer.displayThemes(screen, screenDisplayed, ev)

    # Update pygame
    pygame.display.update()
