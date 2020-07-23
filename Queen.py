# Important imports
import pygame

# Copying important variables form main
WIDTH = HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
SCL = 8
PCESIZE = int(WIDTH / SCL)

# Rook class with all its atributes and methods, all peices will have the same structure
class Queen:

    # Constructor or initializer method
    def __init__(self, yID, xID, color, totalMoves, held):
        self.yID = yID
        self.xID = xID
        self.color = color
        self.totalMoves = totalMoves
        self.held = held
        self.selected = False

        self.displacement = 7

        self.highlightedAttacks = []

        # Find out which color is being delt with
        if self.color == 'black':
            self.image = pygame.image.load('AllChessPieces/BlackQueen.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-15, PCESIZE-15))
            self.reference = 'black queen'
        else:
            self.image = pygame.image.load('AllChessPieces/WhiteQueen.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-15, PCESIZE-15))
            self.reference = 'white queen'


    # Draw the piece
    def drawPiece(self, screen) -> bool:
        screen.blit(self.image, (self.xID * PCESIZE+7, self.yID * PCESIZE+7))

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

        # Basic movement
        if (turn == 1 and self.color == 'white') or (turn == -1 and self.color == 'black'):

            if currentXID > prevX:
                slope = (currentYID - prevY) / (currentXID - prevX)
                if slope == -1:
                    for i in range(1, currentXID - prevX):
                        if not(board[prevY - i][prevX + i] == None):
                            return False
                    if board[currentYID][currentXID] == None or not(board[currentYID][currentXID].color == board[prevY][prevX].color):
                        return True
                elif slope == 1:
                    for i in range(1, currentXID - prevX):
                        if not(board[prevY + i][prevX + i] == None):
                            return False
                    if board[currentYID][currentXID] == None or not(board[currentYID][currentXID].color == board[prevY][prevX].color):
                        return True
                else:
                    return False

            elif currentXID < prevX:
                slope = (currentYID - prevY) / (currentXID - prevX)
                if slope == -1:
                    for i in range(1, currentXID - prevX):
                        if not(board[prevY - i][prevX - i] == None):
                            return False
                    if board[currentYID][currentXID] == None or not(board[currentYID][currentXID].color == board[prevY][prevX].color):
                        return True
                elif slope == 1:
                    for i in range(1, currentXID - prevX):
                        if not(board[prevY + i][prevX - i] == None):
                            return False
                    if board[currentYID][currentXID] == None or not(board[currentYID][currentXID].color == board[prevY][prevX].color):
                        return True

        return False

    # When legal moves is checked and returns true, this method is called to
    # perform the action and move the piece
    def moveToNextPosition(self, prevY, prevX, board, turn, entireGameStates, screen) -> None:
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        board[currentYID][currentXID] = Queen(currentYID, currentXID, board[prevY][prevX].color, board[prevY][prevX].totalMoves + 1, False)
        board[prevY][prevX] = None

    # Maybe this method is redundant and could've been implemented with legalMove,
    # but I wanted to have it seperately so it is easier to debug.
    # This method highlights the possible moves the queen can do (whic is a combination of rook and bishop)
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

        # Going Up Right
        if prevX < 7 and prevY > 0:
            smaller = min(7 - prevX, prevY)
            for i in range(1, smaller + 1):
                if board[prevY - i][prevX + i] == None:
                    if store:
                        self.highlightedAttacks.append((prevX + i, prevY - i))
                    else:
                        self.drawHighlighted(screen, prevX + i, prevY - i, 2)
                else:
                    if not (board[prevY - i][prevX + i].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((prevX + i, prevY - i))
                        else:
                            self.drawHighlighted(screen, prevX + i, prevY - i, 2)
                    break

        # Going Down Right
        if prevX < 7 and prevY < 7:
            smaller = min(7 - prevX, 7 - prevY)
            for i in range(1, smaller + 1):
                if board[prevY + i][prevX + i] == None:
                    if store:
                        self.highlightedAttacks.append((prevX + i, prevY + i))
                    else:
                        self.drawHighlighted(screen, prevX + i, prevY + i, 2)
                else:
                    if not (board[prevY + i][prevX + i].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((prevX + i, prevY + i))
                        else:
                            self.drawHighlighted(screen, prevX + i, prevY + i, 2)
                    break

        # Going Up Left
        if prevX > 0 and prevY > 0:
            smaller = min(prevX, prevY)
            for i in range(1, smaller + 1):
                if board[prevY - i][prevX - i] == None:
                    if store:
                        self.highlightedAttacks.append((prevX - i, prevY - i))
                    else:
                        self.drawHighlighted(screen, prevX - i, prevY - i, 2)
                else:
                    if not (board[prevY - i][prevX - i].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((prevX - i, prevY - i))
                        else:
                            self.drawHighlighted(screen, prevX - i, prevY - i, 2)
                    break

        # Going Down Left
        if prevX > 0 and prevY < 7:
            smaller = min(prevX, 7 - prevY)
            for i in range(1, smaller + 1):
                if board[prevY + i][prevX - i] == None:
                    if store:
                        self.highlightedAttacks.append((prevX - i, prevY + i))
                    else:
                        self.drawHighlighted(screen, prevX - i, prevY + i, 2)
                else:
                    if not (board[prevY + i][prevX - i].color == board[prevY][prevX].color):
                        if store:
                            self.highlightedAttacks.append((prevX - i, prevY + i))
                        else:
                            self.drawHighlighted(screen, prevX - i, prevY + i, 2)
                    break

    # To reduce some redundancy, this method draws the highlighted square when it is
    # checked if it is possible through the method showPossibleMoves
    def drawHighlighted(self, screen, x, y, r):
        pygame.draw.circle(screen, (150, 0, 0), (x*PCESIZE + r*20-3, y*PCESIZE + r*20-3), r*3)
