"""
Utility file for GUI implementation. Contains multiple classes for proper
GUI implementation as well as testing via Mocks.
"""
import pygame

#Color constants in RGB
PINK = (255, 105, 180)
BLUE = (5, 255, 161)
WHITE = (255, 255, 255)
PURPLE =  (140, 30, 255)

#Window size constants
WIDTH, HEIGHT = 1000, 1000

class ScrollingBackground:
    """
    A class storing ScrollingBackground objects and helper functions used to
    create the rolling background that can be seen while playing the Game of
    Checkers.
    """
    def __init__(self, height, filename):
        """
        A function to initialize the ScrollingBackground objects.

        Inputs:
            height : int : the height of the window
            filename : str : the name and path, if necessary, of the image file.
        
        Outputs:
            Does not return anything.
        """
        self.img = pygame.image.load(filename)
        self.coord = [0, 0]
        self.coord2 = [0, - height]
        self.y_original = self.coord[1]
        self.y2_original = self.coord2[1]

    def show(self, surface):
        """
        Function used to draw the same image twice, right next to each other.
        """
        surface.blit(self.img, self.coord)
        surface.blit(self.img, self.coord2)

    def update_coords(self, speed_y, time):
        """
        A function used to update coordinates and change location of the images,
        creating the rolling background effect.

        Inputs:
            speed_y : int : equal to the FPS, 60.
            time : int : milliseconds that have passed since the last
                clock.tick().
        """
        distance_y = speed_y * time
        self.coord[1] += distance_y
        self.coord2[1] += distance_y

        if self.coord2[1] >= 0:
            self.coord[1] = self.y_original
            self.coord2[1] = self.y2_original

class Piece:
    """
    A mock class that stores Piece objects and functions.
    """
    def __init__(self, row, col, color, king = False):
        """
        A function to initialize a Piece object.
        """
        self.row = row
        self.col = col
        self.color = color
        self.moving = False
        self.king = king
        self.moves = None

    def make_king(self):
        """
        A function to king a piece.
        """
        self.king = True

    def move(self, row, col):
        """
        A function to change the location of a piece.
        """
        self.row = row
        self.col = col

    def find_possible_moves(self, board):
        """
        A mocked function to find possible valid moves for a piece.

        Inputs:
            Self : Piece Object
        
        Outputs:
            mockß_list : None or list of tuples of possible moves
        """
        mock_list = []

        rowc = self.row + 1
        colc = self.col + 1
        mock_list.append((colc, rowc))

        north_east = (colc + 1, rowc - 1)
        south_east = (colc + 1, rowc + 1)
        south_west = (colc - 1, rowc + 1)
        north_west = (colc - 1, rowc - 1)
        jump_north_east = (colc + 2, rowc - 2)
        jump_south_east = (colc + 2, rowc + 2)
        jump_south_west = (colc - 2, rowc + 2)
        jump_north_west = (colc - 2, rowc - 2)

        if not self.king:
            if self.color == PINK:
                #Check for south east jumps
                if jump_south_east[0] <= board.rows and jump_south_east[1] <= board.columns:
                    p = board.board[south_east[1] - 1][south_east[0] - 1]
                    if p != 0 and p.color == BLUE:
                        if board.board[jump_south_east[1] - 1][jump_south_east[0] - 1] == 0:
                            mock_list.append(jump_south_east)
                #Check for south east moves
                if south_east[0] <= board.rows and south_east[1] <= board.columns:
                    if board.board[south_east[1] - 1][south_east[0] - 1] == 0:
                        mock_list.append(south_east)
                #Check for south west jumps
                if jump_south_west[0] >= 1 and jump_south_west[1] <= board.columns:
                    p = board.board[south_west[1] - 1][south_west[0] - 1]
                    if p != 0 and p.color == BLUE:
                        if board.board[jump_south_west[1] - 1][jump_south_west[0] - 1] == 0:
                            mock_list.append(jump_south_west)
                #Check for south west moves
                if south_west[0] <= board.rows and south_west[1] <= board.columns:
                    if board.board[south_west[1] - 1][south_west[0] - 1] == 0:
                        mock_list.append(south_west)
                
            if self.color == BLUE:
                #Check for north east jumps
                if jump_north_east[0] <= board.columns and jump_north_east[1] >= 1:
                    p = board.board[north_east[1] - 1][north_east[0] - 1]
                    if p != 0 and p.color == PINK:
                        if board.board[jump_north_east[1] - 1][jump_north_east[0] - 1] == 0:
                            mock_list.append(jump_north_east)
                #Check for north east moves
                if north_east[0] <= board.columns and north_east[1] >= 1:
                    if board.board[north_east[1] - 1][north_east[0] - 1] == 0:
                        mock_list.append(north_east)
                #Check for north west jumps
                if jump_north_west[0] >= 1 and jump_north_west[1] >= 1:
                    p = board.board[north_west[1] - 1][north_west[0] - 1]
                    if p != 0 and p.color == PINK:
                        if board.board[jump_north_west[1] - 1][jump_north_west[0] - 1] == 0:
                            mock_list.append(jump_north_west)
                #Check for north west moves
                if north_west[0] >= 1 and north_west[1] >= 1:
                    if board.board[north_west[1] - 1][north_west[0] - 1] == 0:
                        mock_list.append(north_west)
                
        else:
            if self.color == PINK:
                #Check for south east jumps
                if jump_south_east[0] <= board.rows and jump_south_east[1] <= board.columns:
                    p = board.board[south_east[1] - 1][south_east[0] - 1]
                    if p != 0 and p.color == BLUE:
                        if board.board[jump_south_east[1] - 1][jump_south_east[0] - 1] == 0:
                            mock_list.append(jump_south_east)
                #Check for south east moves
                if south_east[0] <= board.rows and south_east[1] <= board.columns:
                    if board.board[south_east[1] - 1][south_east[0] - 1] == 0:
                        mock_list.append(south_east)
                #Check for south west jumps
                if jump_south_west[0] >= 1 and jump_south_west[1] <= board.columns:
                    p = board.board[south_west[1] - 1][south_west[0] - 1]
                    if p != 0 and p.color == BLUE:
                        if board.board[jump_south_west[1] - 1][jump_south_west[0] - 1] == 0:
                            mock_list.append(jump_south_west)
                #Check for south west moves
                if south_west[0] <= board.rows and south_west[1] <= board.columns:
                    if board.board[south_west[1] - 1][south_west[0] - 1] == 0:
                        mock_list.append(south_west)
                #Check for north east jumps
                if jump_north_east[0] <= board.columns and jump_north_east[1] >= 1:
                    p = board.board[north_east[1] - 1][north_east[0] - 1]
                    if p != 0 and p.color == BLUE:
                        if board.board[jump_north_east[1] - 1][jump_north_east[0] - 1] == 0:
                            mock_list.append(jump_north_east)
                #Check for north east moves
                if north_east[0] <= board.columns and north_east[1] >= 1:
                    if board.board[north_east[1] - 1][north_east[0] - 1] == 0:
                        mock_list.append(north_east)
                #Check for north west jumps
                if jump_north_west[0] >= 1 and jump_north_west[1] >= 1:
                    p = board.board[north_west[1] - 1][north_west[0] - 1]
                    if p != 0 and p.color == BLUE:
                        if board.board[jump_north_west[1] - 1][jump_north_west[0] - 1] == 0:
                            mock_list.append(jump_north_west)
                #Check for north west moves
                if north_west[0] >= 1 and north_west[1] >= 1:
                    if board.board[north_west[1] - 1][north_west[0] - 1] == 0:
                        mock_list.append(north_west)
            if self.color == BLUE:
                #Check for south east jumps
                if jump_south_east[0] <= board.rows and jump_south_east[1] <= board.columns:
                    p = board.board[south_east[1] - 1][south_east[0] - 1]
                    if p != 0 and p.color == PINK:
                        if board.board[jump_south_east[1] - 1][jump_south_east[0] - 1] == 0:
                            mock_list.append(jump_south_east)
                #Check for south east moves
                if south_east[0] <= board.rows and south_east[1] <= board.columns:
                    if board.board[south_east[1] - 1][south_east[0] - 1] == 0:
                        mock_list.append(south_east)
                #Check for south west jumps
                if jump_south_west[0] >= 1 and jump_south_west[1] <= board.columns:
                    p = board.board[south_west[1] - 1][south_west[0] - 1]
                    if p != 0 and p.color == PINK:
                        if board.board[jump_south_west[1] - 1][jump_south_west[0] - 1] == 0:
                            mock_list.append(jump_south_west)
                #Check for south west moves
                if south_west[0] <= board.rows and south_west[1] <= board.columns:
                    if board.board[south_west[1] - 1][south_west[0] - 1] == 0:
                        mock_list.append(south_west)
                #Check for north east jumps
                if jump_north_east[0] <= board.columns and jump_north_east[1] >= 1:
                    p = board.board[north_east[1] - 1][north_east[0] - 1]
                    if p != 0 and p.color == PINK:
                        if board.board[jump_north_east[1] - 1][jump_north_east[0] - 1] == 0:
                            mock_list.append(jump_north_east)
                #Check for north east moves
                if north_east[0] <= board.columns and north_east[1] >= 1:
                    if board.board[north_east[1] - 1][north_east[0] - 1] == 0:
                        mock_list.append(north_east)
                #Check for north west jumps
                if jump_north_west[0] >= 1 and jump_north_west[1] >= 1:
                    p = board.board[north_west[1] - 1][north_west[0] - 1]
                    if p != 0 and p.color == PINK:
                        if board.board[jump_north_west[1] - 1][jump_north_west[0] - 1] == 0:
                            mock_list.append(jump_north_west)
                #Check for north west moves
                if north_west[0] >= 1 and north_west[1] >= 1:
                    if board.board[north_west[1] - 1][north_west[0] - 1] == 0:
                        mock_list.append(north_west)

        if len(mock_list) == 0:
            return None
        else:
            return mock_list

class Board:
    """
    A mock class that stores Board objects and functions.
    """
    def __init__(self, ROWS, COLUMNS):
        """
        A function to initialize a Board object.
        """
        self.board = []
        self.rows = ROWS
        self.columns = COLUMNS
        self.r = None
        self.c = None
        self.middle_row = None
        self.middle_col = None
        self.pinks = 0
        self.blues = 0
        self.winner = False

        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if col % 2 == ((row + 1) % 2):
                    if row < (ROWS - 2) / 2:
                        self.board[row].append(Piece(row, col, PINK))
                        self.pinks += 1
                    elif row > ROWS - ((ROWS - 2) / 2 + 1):
                        self.board[row].append(Piece(row, col, BLUE))
                        self.blues += 1
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def check_winner(self):
        """
        A mock function that checks if there is a winner on the board.
        """
        if self.pinks == 0:
            self.winner = True
            return "BLUE"
        
        if self.blues == 0:
            self.winner = True
            return "PINK"

        else:
            pink = 0
            blue = 0
            pink_list = []
            blue_list = []
            for rs in self.board:
                for c in rs:
                    if c == 0:
                        continue
                    else:
                        if c.color == PINK:
                            pink_list = pink_list + c.find_possible_moves(self)
                            pink += 1
                        if c.color == BLUE:
                            blue_list = blue_list + c.find_possible_moves(self)
                            blue += 1
            if len(pink_list) == pink:
                self.winner = True
                return "BLUE"
            if len(blue_list) == blue:
                self.winner = True
                return "PINK"

    def move(self, piece, row, col):
        """
        A function to change the location of a piece on the board.
        """
        #Check if move takes a piece
        if abs(piece.row - row) == 2 and abs(piece.col - col) == 2:
            self.remove_piece(piece.row, piece.col, row, col)
        #Move piece to empty spot on board
        self.board[piece.row][piece.col] = 0
        self.board[row][col] = Piece(row, col, piece.color, piece.king)
        self.board[self.r][self.c] = 0
        #Reset Board
        self.r = None
        self.c = None
        #Make piece a king
        if row == self.rows - 1 or row == 0:
            self.board[row][col].make_king()

    def remove_piece(self, start_row, start_col, end_row, end_col):
        """
        A function used to remove a piece from the board.
        """
        #Find piece to be removed
        if start_row > end_row:
            self.middle_row = start_row - 1
        if start_row < end_row:
            self.middle_row = start_row + 1
        if start_col > end_col:
            self.middle_col = start_col - 1
        if start_col < end_col:
            self.middle_col = start_col + 1
        #Remove the piece
        if self.board[self.middle_row][self.middle_col] != 0:
            if self.board[self.middle_row][self.middle_col].color == PINK:
                self.pinks = self.pinks - 1
            elif self.board[self.middle_row][self.middle_col].color == BLUE:
                self.blues = self.blues - 1
        self.board[self.middle_row][self.middle_col] = 0

        #Reset Board
        self.middle_row = None
        self.middle_col = None

        # self.board = [[p, None, b, None, None, None],
        #                 [None, None, None, None, None, p],
        #                 [p, None, b, None, None, None],
        #                 [None, None, None, b, None, p],
        #                 [None, None, b, None, None, None],
        #                 [None, None, None, None, None, p]]
