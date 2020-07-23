# Important imports
import pygame

# Copying important variables form main
WIDTH = HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
SCL = 8
PCESIZE = int(WIDTH / SCL)

# Rook class with all its atributes and methods, all peices will have the same structure
class Knight:

    # Constructor or initializer method
    def __init__(self, yID, xID, color, totalMoves, held):
        self.yID = yID
        self.xID = xID
        self.color = color
        self.totalMoves = totalMoves
        self.held = held
        self.selected = False

        self.highlightedAttacks = []

        self.displacement = 13

        # Find out which color is being delt with
        if self.color == 'black':
            self.image = pygame.image.load('AllChessPieces/BlackKnight.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-26, PCESIZE-26))
            self.reference = 'black knight'

        else:
            self.image = pygame.image.load('AllChessPieces/WhiteKnight.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-26, PCESIZE-26))
            self.reference = 'white knight'

    # Draw the piece
    def drawPiece(self, screen) -> bool:
        screen.blit(self.image, (self.xID * PCESIZE+13, self.yID * PCESIZE+13))

    # Here is the main method for checking all the possible moves that the rook can move.
    def legalMove(self, prevY, prevX, board, turn, entireGameStates):
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        if currentXID >= 8:
            return False

        # Basic movement
        if (board[currentYID][currentXID] == None or not(board[currentYID][currentXID].color == board[prevY][prevX].color)):
            if currentYID == prevY + 2 and (currentXID == prevX + 1 or currentXID == prevX - 1):
                return True
            elif currentYID == prevY - 2 and (currentXID == prevX + 1 or currentXID == prevX - 1):
                return True
            elif currentXID == prevX + 2 and (currentYID == prevY + 1 or currentYID == prevY - 1):
                return True
            elif currentXID == prevX - 2 and (currentYID == prevY + 1 or currentYID == prevY - 1):
                return True

        return False

    # When legal moves is checked and returns true, this method is called to
    # perform the action and move the piece
    def moveToNextPosition(self, prevY, prevX, board, turn, entireGameStates, screen) -> None:
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        board[currentYID][currentXID] = Knight(currentYID, currentXID, board[prevY][prevX].color, board[prevY][prevX].totalMoves + 1, False)
        board[prevY][prevX] = None

        self.showPossibleMoves(currentYID, currentXID, board, turn, entireGameStates, screen, True)

    # Maybe this method is redundant and could've been implemented with legalMove,
    # but I wanted to have it seperately so it is easier to debug.
    # This method highlights the possible moves the Knight can do (all the 'L's around it)
    def showPossibleMoves(self, prevY, prevX, board, turn, entireGameStates, screen, store):

        self.highlightedAttacks = []

        # Up and down area
        if prevX <= 6 and prevY >= 2 and (board[prevY - 2][prevX + 1] == None or not(board[prevY][prevX].color == board[prevY - 2][prevX + 1].color)):
            if store:
                self.highlightedAttacks.append((prevX + 1, prevY - 2))
            else:
                self.drawHighlighted(screen, prevX + 1, prevY - 2, 2)
        if prevX >= 1 and prevY >= 2 and (board[prevY - 2][prevX - 1] == None or not(board[prevY][prevX].color == board[prevY - 2][prevX - 1].color)):
            if store:
                self.highlightedAttacks.append((prevX - 1, prevY - 2))
            else:
                self.drawHighlighted(screen, prevX - 1, prevY - 2, 2)
        if prevX <= 6 and prevY <= 5 and (board[prevY + 2][prevX + 1] == None or not(board[prevY][prevX].color == board[prevY + 2][prevX + 1].color)):
            if store:
                self.highlightedAttacks.append((prevX + 1, prevY + 2))
            else:
                self.drawHighlighted(screen, prevX + 1, prevY + 2, 2)
        if prevX >= 1 and prevY <= 5 and (board[prevY + 2][prevX - 1] == None or not(board[prevY][prevX].color == board[prevY + 2][prevX - 1].color)):
            if store:
                self.highlightedAttacks.append((prevX - 1, prevY + 2))
            else:
                self.drawHighlighted(screen, prevX - 1, prevY + 2, 2)

        # Left and right area
        if prevX >= 2 and prevY >= 1 and (board[prevY - 1][prevX - 2] == None or not(board[prevY][prevX].color == board[prevY - 1][prevX - 2].color)):
            if store:
                self.highlightedAttacks.append((prevX - 2, prevY - 1))
            else:
                self.drawHighlighted(screen, prevX - 2, prevY - 1, 2)
        if prevX >= 2 and prevY <= 6 and (board[prevY + 1][prevX - 2] == None or not(board[prevY][prevX].color == board[prevY + 1][prevX - 2].color)):
            if store:
                self.highlightedAttacks.append((prevX - 2, prevY + 1))
            else:
                self.drawHighlighted(screen, prevX - 2, prevY + 1, 2)
        if prevX <= 5 and prevY >= 1 and (board[prevY - 1][prevX + 2] == None or not(board[prevY][prevX].color == board[prevY - 1][prevX + 2].color)):
            if store:
                self.highlightedAttacks.append((prevX + 2, prevY - 1))
            else:
                self.drawHighlighted(screen, prevX + 2, prevY - 1, 2)
        if prevX <= 5 and prevY <= 6 and (board[prevY + 1][prevX + 2] == None or not(board[prevY][prevX].color == board[prevY + 1][prevX + 2].color)):
            if store:
                self.highlightedAttacks.append((prevX + 2, prevY + 1))
            else:
                self.drawHighlighted(screen, prevX + 2, prevY + 1, 2)


    # To reduce some redundancy, this method draws the highlighted square when it is
    # checked if it is possible through the method showPossibleMoves
    def drawHighlighted(self, screen, x, y, r):
        pygame.draw.circle(screen, (150, 0, 0), (x*PCESIZE + r*20-3, y*PCESIZE + r*20-3), r*3)
