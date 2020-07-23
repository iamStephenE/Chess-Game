# Important imports
import pygame

# Copying important variables form main
WIDTH = HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
SCL = 8
PCESIZE = int(WIDTH / SCL)

# Rook class with all its atributes and methods, all peices will have the same structure
class Bishop:

    # Constructor or initializer method
    def __init__(self, yID, xID, color, totalMoves, held):
        self.yID = yID
        self.xID = xID
        self.color = color
        self.totalMoves = totalMoves
        self.held = held
        self.selected = False

        self.displacement = 10

        self.highlightedAttacks = []

        # Find out which color is being delt with
        if self.color == 'black':
            self.image = pygame.image.load('AllChessPieces/BlackBishop.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-20, PCESIZE-20))
            self.reference = 'black bishop'
        else:
            self.image = pygame.image.load('AllChessPieces/WhiteBishop.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-20, PCESIZE-20))
            self.reference = 'white bishop'


    # Draw the piece
    def drawPiece(self, screen) -> bool:
        screen.blit(self.image, (self.xID * PCESIZE+10, self.yID * PCESIZE+10))

    # Here is the main method for checking all the possible moves that the rook can move.
    def legalMove(self, prevY, prevX, board, turn, entireGameStates):
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        if currentXID >= 8:
            return False

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

        board[currentYID][currentXID] = Bishop(currentYID, currentXID, board[prevY][prevX].color, board[prevY][prevX].totalMoves + 1, False)
        board[prevY][prevX] = None

    # Maybe this method is redundant and could've been implemented with legalMove,
    # but I wanted to have it seperately so it is easier to debug.
    # This method highlights the possible moves the bishop can do
    def showPossibleMoves(self, prevY, prevX, board, turn, entireGameStates, screen, store):
        self.highlightedAttacks = []

        # Basically this goes in all diagonals to the bishops
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
