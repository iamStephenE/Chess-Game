# Important imports
import pygame

from Rook import Rook

# Copying important variables form main
WIDTH = HEIGHT = 600
DIMENSIONS = (WIDTH, HEIGHT)
SCL = 8
PCESIZE = int(WIDTH / SCL)

# Rook class with all its atributes and methods, all peices will have the same structure
class King:

    # Constructor or initializer method
    def __init__(self, yID, xID, color, totalMoves, held, screen):
        self.yID = yID
        self.xID = xID
        self.color = color
        self.totalMoves = totalMoves
        self.held = held
        self.selected = False
        self.displacement = 2

        self.pieceAttacking = ('', ())

        self.mainScreen = screen

        self.highlightedAttacks = []

        self.inCheck = False

        # Find out which color is being delt with
        if self.color == 'black':
            self.image = pygame.image.load('AllChessPieces/BlackKing.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-5, PCESIZE-5))
            self.reference = 'black king'
        else:
            self.image = pygame.image.load('AllChessPieces/WhiteKing.png')
            self.image = pygame.transform.scale(self.image, (PCESIZE-5, PCESIZE-5))
            self.reference = 'white king'

    # Draw the piece
    def drawPiece(self, screen) -> bool:
        screen.blit(self.image, (self.xID * PCESIZE+2, self.yID * PCESIZE+2))

    # Here is the main method for checking all the possible moves that the rook can move.
    def legalMove(self, prevY, prevX, board, turn, entireGameStates):
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        if currentXID >= 8:
            return False

        # When moved, check if you can castle and if the move happens to be there then execute
        if self.canCastleLeft(prevY, prevX, board, turn, entireGameStates):
            if currentXID == 2 and prevY == currentYID:
                if self.color == 'white':
                    board[7][3] = Rook(7, 3, board[7][0].color, board[7][0].totalMoves + 1, False)
                    board[7][0] = None
                elif self.color == 'black':
                    board[0][3] = Rook(0, 3, board[0][0].color, board[0][0].totalMoves + 1, False)
                    board[0][0] = None
                return True

        # When moved, check if you can castle and if the move happens to be there then execute
        if self.canCastleRight(prevY, prevX, board, turn, entireGameStates):
            if currentXID == 6 and prevY == currentYID:
                if self.color == 'white':
                    board[7][5] = Rook(7, 5, board[7][7].color, board[7][7].totalMoves + 1, False)
                    board[7][7] = None

                elif self.color == 'black':
                    board[0][5] = Rook(0, 5, board[0][7].color, board[0][7].totalMoves + 1, False)
                    board[0][7] = None
                return True

        # Basic movement (around the king)
        if currentXID == prevX + 1 or currentXID == prevX - 1:
            # Add and not in check
            if (board[currentYID][currentXID] == None or not(board[prevY][prevX].color == board[currentYID][currentXID].color)):
                if currentYID == prevY - 1 or currentYID == prevY or currentYID == prevY + 1:
                    return True
        elif currentXID == prevX:
            if (board[currentYID][currentXID] == None or not(board[prevY][prevX].color == board[currentYID][currentXID].color)):
                if currentYID == prevY - 1 or currentYID == prevY + 1:
                    return True

        return False

    # Method for checking if it is possible to castle to the left for either side
    def canCastleLeft(self, prevY, prevX, board, turn, entireGameStates) -> bool:
        if self.color == 'white' and self.totalMoves == 0:
            if board[7][0] != None and board[7][0].totalMoves == 0:
                if board[7][1] == None and board[7][2] == None and board[7][3] == None and not self.inCheck:
                    for x in range(1, 4):
                        if self.checkInThatPosition(board, 7, x, self.color, self.mainScreen, turn, entireGameStates, board[7][x]):
                            return False
                    return True

                    return True
        elif self.color == 'black' and self.totalMoves == 0:
            if board[0][0] != None and board[0][0].totalMoves == 0:
                if board[0][1] == None and board[0][2] == None and board[0][3] == None and not self.inCheck:
                    for x in range(1, 4):
                        if self.checkInThatPosition(board, 0, x, self.color, self.mainScreen, turn, entireGameStates, board[0][x]):
                            return False
                    return True

        return False

    # Method for checking if it is possible to castle to the right for either side
    def canCastleRight(self, prevY, prevX, board, turn, entireGameStates) -> bool:
        if self.color == 'white' and self.totalMoves == 0:
            if board[7][7] != None and board[7][7].totalMoves == 0:
                if board[7][5] == None and board[7][6] == None and not self.inCheck:
                    for x in range(5, 7):
                        if self.checkInThatPosition(board, 7, x, self.color, self.mainScreen, turn, entireGameStates, board[7][x]):
                            return False
                    return True

        elif self.color == 'black' and self.totalMoves == 0:
            if board[0][7] != None and board[0][7].totalMoves == 0:
                if board[0][5] == None and board[0][6] == None and not self.inCheck:
                    for x in range(5, 7):
                        if self.checkInThatPosition(board, 0, x, self.color, self.mainScreen, turn, entireGameStates, board[0][x]):
                            return False
                    return True


        return False

    # This method checks if there is a 'check' in that position for the king.
    # It is done by saving the piece in the current move, and placing the king piece
    # in the next spot, if it works, it back tracks and resets to where you were and
    # gives the boolean that it is either a true (legal) or not.
    def checkInThatPosition(self, board, y, x, c, screen, turn, entireGameStates, piece):
        board[y][x] = King(y, x, c, 0, False, screen)
        board[y][x].checkCurrentPosition(board, y, x, c, screen, turn, entireGameStates)
        if board[y][x].inCheck:
            board[y][x] = piece
            return True
        else:
            board[y][x] = piece

        return False


    # Method to check if the king is in checkmate.
    def inCheckMate(self, board, screen, turn, entireGameStates) -> (bool, str):

        # check the surroundings of the king and if it is possible to move there
        # check below it
        if self.yID < 7:
            if self.xID > 0 and (board[self.yID + 1][self.xID - 1] == None or board[self.yID + 1][self.xID - 1].color != self.color):
                if not self.checkInThatPosition(board, self.yID + 1, self.xID - 1, self.color, screen, turn, entireGameStates, board[self.yID + 1][self.xID - 1]):
                    return (False, '')
            if board[self.yID + 1][self.xID] == None or board[self.yID + 1][self.xID].color != self.color:
                if not self.checkInThatPosition(board, self.yID + 1, self.xID, self.color, screen, turn, entireGameStates, board[self.yID + 1][self.xID]):
                    return (False, '')
            if self.xID < 7 and (board[self.yID + 1][self.xID + 1] == None or board[self.yID + 1][self.xID + 1].color != self.color):
                if not self.checkInThatPosition(board, self.yID + 1, self.xID + 1, self.color, screen, turn, entireGameStates, board[self.yID + 1][self.xID + 1]):
                    return (False, '')

        # check above it
        if self.yID > 0:
            if self.xID > 0 and (board[self.yID - 1][self.xID - 1] == None or board[self.yID - 1][self.xID - 1].color != self.color):
                if not self.checkInThatPosition(board, self.yID - 1, self.xID - 1, self.color, screen, turn, entireGameStates, board[self.yID - 1][self.xID - 1]):
                    return (False, '')
            if board[self.yID - 1][self.xID] == None or board[self.yID - 1][self.xID].color != self.color:
                if not self.checkInThatPosition(board, self.yID - 1, self.xID, self.color, screen, turn, entireGameStates, board[self.yID - 1][self.xID]):
                    return (False, '')
            if self.xID < 7 and (board[self.yID - 1][self.xID + 1] == None or board[self.yID - 1][self.xID + 1].color != self.color):
                if not self.checkInThatPosition(board, self.yID - 1, self.xID + 1, self.color, screen, turn, entireGameStates, board[self.yID - 1][self.xID + 1]):
                    return (False, '')

        # check to its left and right
        if self.xID > 0:
            if board[self.yID][self.xID - 1] == None or board[self.yID][self.xID - 1].color != self.color:
                if not self.checkInThatPosition(board, self.yID, self.xID - 1, self.color, screen, turn, entireGameStates, board[self.yID][self.xID - 1]):
                    return (False, '')
        if self.xID < 7:
            if board[self.yID][self.xID + 1] == None or board[self.yID][self.xID + 1].color != self.color:
                if not self.checkInThatPosition(board, self.yID, self.xID + 1, self.color, screen, turn, entireGameStates, board[self.yID][self.xID + 1]):
                    return (False, '')

        # After checking the surround of the king, if that all fails and the king cant move,
        # find the piece that is attacking the piece and perform some calculation which is
        # explained at self.arrayFromAttackerToKing. When the array is aquired, it checks if any
        # of the same colored piece can obstruct or take the attacking piece.
        for y in range(SCL):
            for x in range(SCL):
                if board[y][x] != None and board[y][x].color == self.color and board[y][x].reference[-4:] != 'king':
                    arr = self.arrayFromAttackerToKing()
                    for each in board[y][x].highlightedAttacks:
                        if each in arr:
                            return (False, '')


        # Return that the game is in checkmate and the color that lost (or in mate)
        return (True, self.color)

    # This method check the path of the attacker to the king. This means that it returns
    # an array that is filled with all the squares that are between it and the king, this is
    # done to check if the attackers way can be obstructed or disturbed by another piece and
    # prevent checkmate. It is important to note that if the length of the array returned is 1
    # that means the piece is right next to the king (not in the case of the knight).
    def arrayFromAttackerToKing(self):
        pce = self.pieceAttacking[0]
        pos = self.pieceAttacking[1]
        result = []

        # in the case of knight or pawn, just return the position.
        if pce == 'knight' or pce == 'pawn':
            return [pos]

        # If it is a rook check up, down, left, right, and find the one going to the king.
        if pce == 'rook':
            if self.xID == pos[0]:
                increment = 1 if pos[1] < self.yID else -1
                for y in range(pos[1], self.yID, increment):
                    result.append((self.xID, y))
                return result

            elif self.yID == pos[1]:
                increment = 1 if pos[0] < self.xID else -1
                for x in range(pos[0], self.xID, increment):
                    result.append((x, self.yID))
                return result

        # If it is a bishop then check all the diagonals and find the one going to the king
        if pce == 'bishop':
            # Going Up Right
            if pos[0] < self.xID and pos[1] > self.yID:
                smaller = min(7 - pos[0], pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] + i, pos[1] - i))
                return result
            # Going Down Right
            elif pos[0] < self.xID and pos[1] < self.yID:
                smaller = min(7 - pos[0], 7 - pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] + i, pos[1] + i))
                return result
            # Going Up Left
            elif pos[0] > self.xID and pos[1] > self.yID:
                smaller = min(pos[0], pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] - i, pos[1] - i))
                return result
            # Going Down Left
            elif pos[0] > self.xID and pos[1] < self.yID:
                smaller = min(pos[0], 7 - pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] - i, pos[1] + i))
                return result

        result = []

        # Perform the same proceder of the rook and bishop but in one.
        if pce == 'queen':
            # copying rook
            if self.xID == pos[0]:
                increment = 1 if pos[1] < self.yID else -1
                for y in range(pos[1], self.yID, increment):
                    result.append((self.xID, y))
                return result

            elif self.yID == pos[1]:
                increment = 1 if pos[0] < self.xID else -1
                for x in range(pos[0], self.xID, increment):
                    result.append((x, self.yID))
                return result

            # Going Up Right
            if pos[0] < self.xID and pos[1] > self.yID:
                smaller = min(7 - pos[0], pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] + i, pos[1] - i))
                return result
            # Going Down Right
            elif pos[0] < self.xID and pos[1] < self.yID:
                smaller = min(7 - pos[0], 7 - pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] + i, pos[1] + i))
                return result
            # Going Up Left
            elif pos[0] > self.xID and pos[1] > self.yID:
                smaller = min(pos[0], pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] - i, pos[1] - i))
                return result
            # Going Down Left
            elif pos[0] > self.xID and pos[1] < self.yID:
                smaller = min(pos[0], 7 - pos[1])
                result.append((pos[0], pos[1]))
                for i in range(1, smaller):
                    result.append((pos[0] - i, pos[1] + i))
                return result


        return []

    # Checks the current position and sees if it is in check.
    def checkCurrentPosition(self, b, y, x, c, screen, turn, entireGameStates):

        oppC = 'black' if c == 'white' else 'white'

        # Check for the pawns first
        if c == 'white' and (y > 0 and x > 0 and b[y-1][x-1] != None and b[y-1][x-1].reference == 'black pawn' or y > 0 and x < 7 and b[y-1][x+1] != None and b[y-1][x+1].reference == 'black pawn'):
            self.inCheck = True
            pos = (x-1, y-1) if b[y-1][x-1] != None and b[y-1][x-1].reference == 'black pawn' else (x+1, y-1)
            self.pieceAttacking = ('pawn', pos)
        elif c == 'black' and (y < 7 and x > 0 and b[y+1][x-1] != None and b[y+1][x-1].reference == 'white pawn' or y < 7 and x < 7 and b[y+1][x+1] != None and b[y+1][x+1].reference == 'white pawn'):
            self.inCheck = True
            pos = (x-1, y+1) if b[y+1][x-1] != None and b[y+1][x-1].reference == 'white pawn' else (x+1, y+1)
            self.pieceAttacking = ('pawn', pos)
        else:
            self.inCheck = False

        # Check for knights
        # Up and down area
        if not self.inCheck:
            if x <= 6 and y >= 2 and (not b[y - 2][x + 1] == None and not(b[y][x].color == b[y - 2][x + 1].color)) and b[y-2][x+1].reference[len(b[y-2][x+1].reference)-6 : len(b[y-2][x+1].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x+1, y-2))
            elif x >= 1 and y >= 2 and (not b[y - 2][x - 1] == None and not(b[y][x].color == b[y - 2][x - 1].color)) and b[y-2][x-1].reference[len(b[y-2][x-1].reference)-6 : len(b[y-2][x-1].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x-1, y-2))
            elif x <= 6 and y <= 5 and (not b[y + 2][x + 1] == None and not(b[y][x].color == b[y + 2][x + 1].color)) and b[y+2][x+1].reference[len(b[y+2][x+1].reference)-6 : len(b[y+2][x+1].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x+1, y+2))
            elif x >= 1 and y <= 5 and (not b[y + 2][x - 1] == None and not(b[y][x].color == b[y + 2][x - 1].color)) and b[y+2][x-1].reference[len(b[y+2][x-1].reference)-6 : len(b[y+2][x-1].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x-1, y+2))

            # Left and right area
            if x >= 2 and y >= 1 and (not b[y - 1][x - 2] == None and not(b[y][x].color == b[y - 1][x - 2].color)) and b[y-1][x-2].reference[len(b[y-1][x-2].reference)-6 : len(b[y-1][x-2].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x-2, y-1))
            elif x >= 2 and y <= 6 and (not b[y + 1][x - 2] == None and not(b[y][x].color == b[y + 1][x - 2].color)) and b[y+1][x-2].reference[len(b[y+1][x-2].reference)-6 : len(b[y+1][x-2].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x-2, y+1))
            elif x <= 5 and y >= 1 and (not b[y - 1][x + 2] == None and not(b[y][x].color == b[y - 1][x + 2].color)) and b[y-1][x+2].reference[len(b[y-1][x+2].reference)-6 : len(b[y-1][x+2].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x+2, y-1))
            elif x <= 5 and y <= 6 and (not b[y + 1][x + 2] == None and not(b[y][x].color == b[y + 1][x + 2].color)) and b[y+1][x+2].reference[len(b[y+1][x+2].reference)-6 : len(b[y+1][x+2].reference)] == 'knight':
                self.inCheck = True
                self.pieceAttacking = ('knight', (x+2, y+1))

        # Check for rooks
        if not self.inCheck:
            if c == 'white':
                for ry in range(SCL):
                    for rx in range(SCL):
                        if b[ry][rx] != None and b[ry][rx].color == 'black' and b[ry][rx].reference[len(b[ry][rx].reference)-4:len(b[ry][rx].reference)] == 'rook':
                            b[ry][rx].showPossibleMoves(ry, rx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[ry][rx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('rook', (rx, ry))

            if c == 'black':
                for ry in range(SCL):
                    for rx in range(SCL):
                        if b[ry][rx] != None and b[ry][rx].color == 'white' and b[ry][rx].reference[len(b[ry][rx].reference)-4:len(b[ry][rx].reference)] == 'rook':
                            b[ry][rx].showPossibleMoves(ry, rx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[ry][rx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('rook', (rx, ry))


        # Check for bishops
        if not self.inCheck:
            if c == 'white':
                for by in range(SCL):
                    for bx in range(SCL):
                        if b[by][bx] != None and b[by][bx].color == 'black' and b[by][bx].reference[len(b[by][bx].reference)-6:len(b[by][bx].reference)] == 'bishop':
                            b[by][bx].showPossibleMoves(by, bx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[by][bx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('bishop', (bx, by))

            if c == 'black':
                for by in range(SCL):
                    for bx in range(SCL):
                        if b[by][bx] != None and b[by][bx].color == 'white' and b[by][bx].reference[len(b[by][bx].reference)-6:len(b[by][bx].reference)] == 'bishop':
                            b[by][bx].showPossibleMoves(by, bx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[by][bx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('bishop', (bx, by))

        # Check for queens
        if not self.inCheck:
            if c == 'white':
                for qy in range(SCL):
                    for qx in range(SCL):
                        if b[qy][qx] != None and b[qy][qx].color == 'black' and b[qy][qx].reference[len(b[qy][qx].reference)-5:len(b[qy][qx].reference)] == 'queen':
                            b[qy][qx].showPossibleMoves(qy, qx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[qy][qx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('queen', (qx, qy))

            if c == 'black':
                for qy in range(SCL):
                    for qx in range(SCL):
                        if b[qy][qx] != None and b[qy][qx].color == 'white' and b[qy][qx].reference[len(b[qy][qx].reference)-5:len(b[qy][qx].reference)] == 'queen':
                            b[qy][qx].showPossibleMoves(qy, qx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[qy][qx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('queen', (qx, qy))

        # Check for the kings
        if not self.inCheck:
            if c == 'white':
                for ky in range(SCL):
                    for kx in range(SCL):
                        if b[ky][kx] != None and b[ky][kx].reference == 'black king':
                            b[ky][kx].showPossibleMoves(ky, kx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[ky][kx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('king', (kx, ky))

            if c == 'black':
                for ky in range(SCL):
                    for kx in range(SCL):
                        if b[ky][kx] != None and b[ky][kx].reference == 'white king':
                            b[ky][kx].showPossibleMoves(ky, kx, b, turn, entireGameStates, screen, True)
                            if (x, y) in b[ky][kx].highlightedAttacks:
                                self.inCheck = True
                                self.pieceAttacking = ('king', (kx, ky))



    # When legal moves is checked and returns true, this method is called to
    # perform the action and move the piece
    def moveToNextPosition(self, prevY, prevX, board, turn, entireGameStates, screen) -> None:
        currentXID = int(pygame.mouse.get_pos()[0] / PCESIZE)
        currentYID = int(pygame.mouse.get_pos()[1] / PCESIZE)

        board[currentYID][currentXID] = King(currentYID, currentXID, board[prevY][prevX].color, board[prevY][prevX].totalMoves + 1, False, self.mainScreen)
        board[prevY][prevX] = None

    # Maybe this method is redundant and could've been implemented with legalMove,
    # but I wanted to have it seperately so it is easier to debug.
    # This method highlights the possible moves the king can do.
    # This is not full correct because it shows the moves that can usually be taken,
    # it doesnt account for illegal moves when checked.
    def showPossibleMoves(self, prevY, prevX, board, turn, entireGameStates, screen, store):
        if self.canCastleLeft(prevY, prevX, board, turn, entireGameStates):
            if (self.color == 'white' and turn == 1) or (self.color == 'black' and turn == -1):
                self.drawHighlighted(screen, prevX - 2, prevY, 2)

        if self.canCastleRight(prevY, prevX, board, turn, entireGameStates):
            if (self.color == 'white' and turn == 1) or (self.color == 'black' and turn == -1):
                self.drawHighlighted(screen, prevX + 2, prevY, 2)

        if prevX < 7:
            if prevY > 0 and (board[prevY - 1][prevX + 1] == None or not(board[prevY][prevX].color == board[prevY - 1][prevX + 1].color)):
                if store:
                    self.highlightedAttacks.append((prevX + 1, prevY - 1))
                else:
                    self.drawHighlighted(screen, prevX + 1, prevY - 1, 2)

            if (board[prevY][prevX + 1] == None or not(board[prevY][prevX].color == board[prevY][prevX + 1].color)):
                if store:
                    self.highlightedAttacks.append((prevX + 1, prevY))
                else:
                    self.drawHighlighted(screen, prevX + 1, prevY, 2)

            if prevY < 7 and (board[prevY + 1][prevX + 1] == None or not(board[prevY][prevX].color == board[prevY + 1][prevX + 1].color)):
                if store:
                    self.highlightedAttacks.append((prevX + 1, prevY + 1))
                else:
                    self.drawHighlighted(screen, prevX + 1, prevY + 1, 2)

        if prevX > 0:
            if prevY > 0 and (board[prevY - 1][prevX - 1] == None or not(board[prevY][prevX].color == board[prevY - 1][prevX - 1].color)):
                if store:
                    self.highlightedAttacks.append((prevX - 1, prevY - 1))
                else:
                    self.drawHighlighted(screen, prevX - 1, prevY - 1, 2)

            if (board[prevY][prevX - 1] == None or not(board[prevY][prevX].color == board[prevY][prevX - 1].color)):
                if store:
                    self.highlightedAttacks.append((prevX - 1, prevY))
                else:
                    self.drawHighlighted(screen, prevX - 1, prevY, 2)

            if prevY < 7 and (board[prevY + 1][prevX - 1] == None or not(board[prevY][prevX].color == board[prevY + 1][prevX - 1].color)):
                if store:
                    self.highlightedAttacks.append((prevX - 1, prevY + 1))
                else:
                    self.drawHighlighted(screen, prevX - 1, prevY + 1, 2)


        if prevY > 0 and (board[prevY - 1][prevX] == None or not(board[prevY][prevX].color == board[prevY - 1][prevX].color)):
            if store:
                self.highlightedAttacks.append((prevX, prevY - 1))
            else:
                self.drawHighlighted(screen, prevX, prevY - 1, 2)

        if prevY < 7 and (board[prevY + 1][prevX] == None or not(board[prevY][prevX].color == board[prevY + 1][prevX].color)):
            if store:
                self.highlightedAttacks.append((prevX, prevY + 1))
            else:
                self.drawHighlighted(screen, prevX, prevY + 1, 2)


    # To reduce some redundancy, this method draws the highlighted square when it is
    # checked if it is possible through the method showPossibleMoves
    def drawHighlighted(self, screen, x, y, r):
        pygame.draw.circle(screen, (150, 0, 0), (x*PCESIZE + r*20-3, y*PCESIZE + r*20-3), r*3)
