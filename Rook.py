# Important imports
import pygame

# Copying important variables form main
WIDTH = HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
SCL = 8
PCESIZE = int(WIDTH / SCL)

# Rook class with all its atributes and methods, all peices will have the same structure
class Rook:

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
            self.image = pygame.image.load('AllChessPieces/BlackRook.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-26, PCESIZE-26))
            self.reference = 'black rook'
        else:
            self.image = pygame.image.load('AllChessPieces/WhiteRook.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-26, PCESIZE-26))
            self.reference = 'white rook'


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
        if (turn == 1 and self.color == 'white') or (turn == -1 and self.color == 'black'):
            if currentXID == prevX:
                increment = 1 if currentYID > prevY else -1
                for y in range(prevY+increment, currentYID, increment):
                    if not board[y][prevX] == None:
                        return False
                if board[currentYID][currentXID] == None or not(board[currentYID][currentXID].color == board[prevY][prevX].color):
                    return True
            elif currentYID == prevY:
                increment = 1 if currentXID > prevX else -1
                for x in range(prevX+increment, currentXID, increment):
                    if not board[prevY][x] == None:
                        return False
                if board[currentYID][currentXID] == None or not(board[currentYID][currentXID].color == board[prevY][prevX].color):
                    return True
            else:
                return False

        return False

    # When legal moves is checked and returns true, this method is called to
    # perform the action and move the piece
    def moveToNextPosition(self, prevY, prevX, board, turn, entireGameStates, screen) -> None:
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        board[currentYID][currentXID] = Rook(currentYID, currentXID, board[prevY][prevX].color, board[prevY][prevX].totalMoves + 1, False)
        board[prevY][prevX] = None


    # Maybe this method is redundant and could've been implemented with legalMove,
    # but I wanted to have it seperately so it is easier to debug.
    # This method highlights the possible moves the rooks can do
    def showPossibleMoves(self, prevY, prevX, board, turn, entireGameStates, screen, store):
        # Check for horizontal:
        # Left
        self.highlightedAttacks = []

        if prevX > 0:
            for x in range(prevX-1, -1, -1):
                if board[prevY][x] == None:
                    if store:
                        self.highlightedAttacks.append((x, prevY))
                    else:
                        self.drawHighlighted(screen, x, prevY, 2)
                else:
                    if not (board[prevY][x].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((x, prevY))
                        else:
                            self.drawHighlighted(screen, x, prevY, 2)
                    break

        # Right
        if prevX < 7:
            for x in range(prevX+1, 8, 1):
                if board[prevY][x] == None:
                    if store:
                        self.highlightedAttacks.append((x, prevY))
                    else:
                        self.drawHighlighted(screen, x, prevY, 2)
                else:
                    if not (board[prevY][x].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((x, prevY))
                        else:
                            self.drawHighlighted(screen, x, prevY, 2)
                    break

        # Check for veritcle:
        # down
        if prevY > 0:
            for y in range(prevY-1, -1, -1):
                if board[y][prevX] == None:
                    if store:
                        self.highlightedAttacks.append((prevX, y))
                    else:
                        self.drawHighlighted(screen, prevX, y, 2)
                else:
                    if not (board[y][prevX].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((prevX, y))
                        else:
                            self.drawHighlighted(screen, prevX, y, 2)
                    break

        # Right
        if prevY < 7:
            for y in range(prevY+1, 8, 1):
                if board[y][prevX] == None:
                    if store:
                        self.highlightedAttacks.append((prevX, y))
                    else:
                        self.drawHighlighted(screen, prevX, y, 2)
                else:
                    if not (board[y][prevX].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((prevX, y))
                        else:
                            self.drawHighlighted(screen, prevX, y, 2)
                    break

    # To reduce some redundancy, this method draws the highlighted square when it is
    # checked if it is possible through the method showPossibleMoves
    def drawHighlighted(self, screen, x, y, r):
        pygame.draw.circle(screen, (150, 0, 0), (x*PCESIZE + r*20-3, y*PCESIZE + r*20-3), r*3)
