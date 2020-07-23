# Important imports
import pygame

# Copying important variables form main
WIDTH = HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
SCL = 8
PCESIZE = int(WIDTH / SCL)

from Displayer import Displayer
from Rook import Rook
from Knight import Knight
from Queen import Queen
from Bishop import Bishop

displayer = Displayer()

# Pawn class with all its atributes and methods, all peices will have the same structure
class Pawn:

    # Constructor or initializer method
    def __init__(self, yID, xID, color, totalMoves, held, screen):
        self.yID = yID
        self.xID = xID
        self.color = color
        self.totalMoves = totalMoves
        self.held = held
        self.selected = False
        self.highlightedAttacks = []

        self.mainScreen = screen

        self.displacement = 0

        # Find out which color is being delt with
        if self.color == 'black':
            self.image = pygame.image.load('AllChessPieces/BlackPawn.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE, PCESIZE))
            self.reference = 'black pawn'
        else:
            self.image = pygame.image.load('AllChessPieces/WhitePawn.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE, PCESIZE))
            self.reference = 'white pawn'


    # Draw the piece
    def drawPiece(self, screen) -> bool:
        screen.blit(self.image, (self.xID * PCESIZE, self.yID * PCESIZE))

    # Here is the main method for checking all the possible moves that the pawn can move.
    # It calls the possible take method, and also calls the enpassent and has the basic
    # movement already implemented
    def legalMove(self, prevY, prevX, board, turn, entireGameStates):
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        if currentXID >= 8:
            return False

        # En Passant
        if(self.checkEnPassant(prevY, prevX, currentXID, currentYID, board, turn, entireGameStates)):
            return True

        # Basic movement
        if self.color == 'black' and turn == -1:
            if self.possibleTake(prevY, prevX, currentYID, currentXID, board, turn):
                return True
            if currentXID != prevX:
                return False
            else:
                if currentYID - prevY == 1:
                    if board[currentYID][currentXID] == None:
                        return True
                elif currentYID - prevY == 2 and board[prevY][prevX].totalMoves == 0:
                    if board[currentYID][currentXID] == None and board[currentYID-1][currentXID] == None:
                        return True
        elif self.color == 'white' and turn == 1:
            if self.possibleTake(prevY, prevX, currentYID, currentXID, board, turn):
                return True
            if currentXID != prevX:
                return False
            else:
                if currentYID - prevY == -1:
                    if board[currentYID][currentXID] == None:
                        return True
                elif currentYID - prevY == -2 and board[prevY][prevX].totalMoves == 0:
                    if board[currentYID][currentXID] == None and board[currentYID+1][currentXID] == None:
                        return True

        return False

    # Checks the cells diagonal to the current pieces and sees if it can be taken
    def possibleTake(self, prevY, prevX, currentYID, currentXID, board, turn) -> bool:

        if board[currentYID][currentXID] != None:
            if turn == 1:
                if prevX == 0 and prevX + 1 == currentXID and prevY - 1 == currentYID and board[currentYID][currentXID].color == 'black':
                    return True
                elif prevX == 7 and prevX - 1 == currentXID and prevY - 1 == currentYID and board[currentYID][currentXID].color == 'black':
                    return True
                elif (prevX + 1 == currentXID or prevX - 1 == currentXID) and (prevY - 1 == currentYID) and (board[currentYID][currentXID].color == 'black'):
                    return True
            elif turn == -1:
                if prevX == 0 and prevX + 1 == currentXID and prevY + 1 == currentYID and board[currentYID][currentXID].color == 'white':
                    return True
                elif prevX == 7 and prevX - 1 == currentXID and prevY + 1 == currentYID and board[currentYID][currentXID].color == 'white':
                    return True
                elif (prevX + 1 == currentXID or prevX - 1 == currentXID) and (prevY + 1 == currentYID) and (board[currentYID][currentXID].color == 'white'):
                    return True

        return False

    # When legal moves is checked and returns true, this method is called to
    # perform the action and move the piece
    def moveToNextPosition(self, prevY, prevX, board, turn, entireGameStates, screen) -> None:
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        board[currentYID][currentXID] = Pawn(currentYID, currentXID, board[prevY][prevX].color, board[prevY][prevX].totalMoves + 1, False, self.mainScreen)
        board[prevY][prevX] = None


    # En Passant check
    def checkEnPassant(self, prevY, prevX, currentXID, currentYID, board, turn, entireGameStates) -> bool:
        if self.color == 'black' and turn == -1:
            if prevY == 4 and currentYID == 5:
                if (prevX + 1 == currentXID or prevX - 1 == currentXID) and board[currentYID-1][currentXID] != None and board[currentYID-1][currentXID].totalMoves == 1:
                    if entireGameStates[len(entireGameStates)-2][6][currentXID] != None:
                        board[currentYID-1][currentXID] = None
                        return True
        elif self.color == 'white' and turn == 1:
            if prevY == 3 and currentYID == 2:
                if (prevX + 1 == currentXID or prevX - 1 == currentXID) and board[currentYID+1][currentXID] != None and board[currentYID+1][currentXID].totalMoves == 1:
                    if entireGameStates[len(entireGameStates)-2][1][currentXID] != None:
                        board[currentYID+1][currentXID] = None
                        return True
        return False

    # Maybe this method is redundant and could've been implemented with legalMove,
    # but I wanted to have it seperately so it is easier to debug.
    # This method highlights the possible moves the pawn can do
    def showPossibleMoves(self, prevY, prevX, board, turn, entireGameStates, screen, store):
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        # For WhitePawn
        if turn == 1 and self.color == 'white':
            if self.totalMoves == 0 and board[prevY-1][prevX] == None and board[prevY-2][prevX] == None:
                if store:
                    self.highlightedAttacks.append((prevX, prevY-1))
                    self.highlightedAttacks.append((prevX, prevY-2))
                else:
                    self.drawHighlighted(screen, prevX, prevY-1, 2)
                    self.drawHighlighted(screen, prevX, prevY-2, 2)
            elif self.totalMoves >= 0 and board[prevY-1][prevX] == None:
                if store:
                    self.highlightedAttacks.append((prevX, prevY-1))
                else:
                    self.drawHighlighted(screen, prevX, prevY-1, 2)

            if prevX > 0 and board[prevY-1][prevX-1] != None and board[prevY-1][prevX-1].color == 'black':
                if store:
                    self.highlightedAttacks.append((prevX - 1, prevY - 1))
                else:
                    self.drawHighlighted(screen, prevX-1, prevY-1, 2)
            elif prevX < 7 and board[prevY-1][prevX+1] != None and board[prevY-1][prevX+1].color == 'black':
                if store:
                    self.highlightedAttacks.append((prevX + 1, prevY - 1))
                else:
                    self.drawHighlighted(screen, prevX+1, prevY-1, 2)

            if prevY == 3 and not store:
                if prevX != 0 and board[prevY][prevX-1] != None and board[prevY][prevX-1].totalMoves == 1 and entireGameStates[len(entireGameStates)-2][1][prevX-1] != None:
                    self.drawHighlighted(screen, prevX-1, 2, 2)
                if prevX != 7 and board[prevY][prevX+1] != None and board[prevY][prevX+1].totalMoves == 1 and entireGameStates[len(entireGameStates)-2][1][prevX+1] != None:
                    self.drawHighlighted(screen, prevX+1, 2, 2)

        # For BlackPawn
        elif turn == -1 and self.color == 'black':
            if prevY + 2 < 8 and self.totalMoves == 0 and board[prevY+1][prevX] == None and board[prevY+2][prevX] == None:
                if store:
                    self.highlightedAttacks.append((prevX, prevY+1))
                    self.highlightedAttacks.append((prevX, prevY+2))
                else:
                    self.drawHighlighted(screen, prevX, prevY+1, 2)
                    self.drawHighlighted(screen, prevX, prevY+2, 2)
            elif self.totalMoves >= 0 and board[prevY+1][prevX] == None:
                if store:
                    self.highlightedAttacks.append((prevX, prevY+1))
                else:
                    self.drawHighlighted(screen, prevX, prevY+1, 2)

            if prevX > 0 and board[prevY+1][prevX-1] != None and board[prevY+1][prevX-1].color == 'white':
                if store:
                    self.highlightedAttacks.append((prevX - 1, prevY + 1))
                else:
                    self.drawHighlighted(screen, prevX-1, prevY+1, 2)
            elif prevX < 7 and board[prevY+1][prevX+1] != None and board[prevY+1][prevX+1].color == 'white':
                if store:
                    self.highlightedAttacks.append((prevX + 1, prevY + 1))
                else:
                    self.drawHighlighted(screen, prevX+1, prevY+1, 2)

            if prevY == 4 and not store:
                if prevX != 0 and board[prevY][prevX-1] != None and board[prevY][prevX-1].totalMoves == 1 and entireGameStates[len(entireGameStates)-2][6][prevX-1] != None:
                    self.drawHighlighted(screen, prevX-1, 5, 2)
                if prevX != 7 and board[prevY][prevX+1] != None and board[prevY][prevX+1].totalMoves == 1 and entireGameStates[len(entireGameStates)-2][6][prevX+1] != None:
                    self.drawHighlighted(screen, prevX+1, 5, 2)


    # To reduce some redundancy, this method draws the highlighted square when it is
    # checked if it is possible through the method showPossibleMoves
    def drawHighlighted(self, screen, x, y, r):
        pygame.draw.circle(screen, (150, 0, 0), (x*PCESIZE + r*20-3, y*PCESIZE + r*20-3), r*3)
