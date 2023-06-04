"""
GUI for Checkers
"""
#Imports
import pygame
from pygame.locals import *
import utils
from utils import *

#Initialize pygame
pygame.init()
pygame.mouse.set_visible(1)

#Set surface constants
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
BACKGROUND = utils.ScrollingBackground(HEIGHT, "galaxy.png")
WIN_BACKGROUND = utils.ScrollingBackground(HEIGHT, "fireworks.png")
CAT = utils.ScrollingBackground(HEIGHT, "cat.png")
BACKGROUND_SPEED = 60
#Load Crowns
PINK_CROWN = pygame.image.load('Pink_Crown.png')
BLUE_CROWN = pygame.image.load('Blue_Crown.png')

#Create class to control Music
class Music:
    """
    A class storing Music objects and functions. Allows the user to listen to a
    banger; however, they are able to turn it on and off.
    """
    def __init__(self, filename):
        """
        A funtion to initialize Music object.

        Inputs:
        
        """
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        self.playing = True

    def play(self):
        if self.playing == True:
            pygame.mixer.music.pause()
            self.playing = False
        else:
            pygame.mixer.music.play()
            self.playing = True

#Initialize Music MUSIC
MUSIC = Music('LOSINGIT.ogg')

#Create class to control Board
class Game_Board:

    def __init__(self, rows = 8, columns = 8):
        self.rows = rows
        self.columns = columns
        self.row_height = (HEIGHT // self.rows)
        self.column_width = (WIDTH // self.columns)
        self.GRID_U = utils.Board((self.rows), (self.columns))
        self.possible_moves = []

    def increase(self):
        self.rows += 2
        self.columns += 2
        self.row_height = (HEIGHT // self.rows)
        self.column_width = (WIDTH // self.columns)
        self.GRID_U = utils.Board((self.rows), (self.columns))

    def decrease(self):
        if self.rows > 4:
            self.rows -= 2
            self.columns -= 2
            self.row_height = (HEIGHT // self.rows)
            self.column_width = (WIDTH // self.columns)
            self.GRID_U = utils.Board((self.rows), (self.columns))
        else:
            pass

    def draw_board(self, grid_u):
        #set grid border thickness based on size of board
        if self.rows < 8:
            thickness = 3
        if 8 <= self.rows <= 15:
            thickness = 2
        if self.rows > 15:
            thickness = 1

        #draw grid
        for row in range(self.rows):
            for col in range(self.columns):
                rect = (col * self.column_width,
                        row * self.row_height, self.column_width,
                        self.row_height)
                if col % 2 == ((row + 1) % 2):
                    pygame.draw.rect(WINDOW, color = PURPLE, border_radius = 6,
                                rect = rect, width = thickness)
                else:
                    pygame.draw.rect(WINDOW, color = WHITE, border_radius = 6,
                                rect = rect, width = thickness)

        for row in range(self.rows):
            for col in range(self.columns):
                rect = (col * self.column_width, row * self.row_height,
                        self.column_width, self.row_height)

        #draw pieces
        for column, rows in enumerate(grid_u.board):
            for loc, piece in enumerate(rows):
                if piece == 0:
                    continue
                if piece.color == PINK:
                    color = PINK
                if piece.color == BLUE:
                    color = BLUE
                #find coordinates for center & radius length
                center = ((loc * self.column_width) + (self.column_width // 2),
                            (column * self.row_height) + (self.row_height // 2))
                radius = self.row_height // 2 - (self.row_height // 5)
                pygame.draw.circle(WINDOW, color = WHITE, center = center,
                                    radius = radius + thickness)
                pygame.draw.circle(WINDOW, color = color, center = center,
                                    radius = radius)

                #position crown at center of piece
                crown_x = center[0] - (PINK_CROWN.get_width() // 2)
                crown_y = center[1] - (PINK_CROWN.get_height() // 2)
                #draw crown
                if piece.king:
                    if piece.color == PINK:
                        WINDOW.blit(PINK_CROWN, (crown_x, crown_y))
                    if piece.color == BLUE:
                        WINDOW.blit(BLUE_CROWN, (crown_x, crown_y))

        #draw possible moves
        if len(self.possible_moves) != 0:
            self.draw_possible_moves(self.possible_moves)

    def draw_possible_moves(self, possible_moves):
        """
        A function that highlights the possible moves for a piece as well as
        the piece itself.
        """
        for coord in possible_moves:
            x_loc = coord[0]
            y_loc = coord[1]
            x_center = (self.column_width * x_loc) - (self.column_width // 2)
            y_center = (self.row_height * y_loc) - (self.row_height // 2)
            center = (x_center, y_center)
            radius = self.row_height // 3
            if possible_moves[0] == coord:
                pygame.draw.circle(WINDOW, color = PURPLE, center = center,
                               radius = radius / 2)
            else:
                pygame.draw.circle(WINDOW, color = WHITE, center = center,
                               radius = radius / 2)
#Initialize Game_Board GRID
GRID = Game_Board()

#Rescale crown image size based on size of board
PINK_CROWN = pygame.transform.scale_by(PINK_CROWN, 1/(2 * GRID.rows))
BLUE_CROWN = pygame.transform.scale_by(BLUE_CROWN, 1/(2 * GRID.rows))

clock = pygame.time.Clock()

def rolling_background(time, background):
    """
    A helper function used to create the rolling background that can be seen
    while playing the Game of Checkers.

    Inputs:
        time : int : milliseconds that have passed since the last clock.tick().

    Outputs:
        Does not return anything.
    """
    background.update_coords(BACKGROUND_SPEED, time)
    background.show(WINDOW)

def main_menu():
    """
    A function used to display the Main Menu of the Checkers game.

    Allows the user to play the game, access the options, and quit the game.
    """
    pygame.display.set_caption("Menu")
    run = True

    while run:
        #Set background
        WINDOW.blit(BACKGROUND.img, (0,0))

        #display 'MAIN MENU'
        MENU_FONT = pygame.font.SysFont(['futura', 'arial bold'], 100)
        MENU_TEXT = MENU_FONT.render("MAIN MENU", True, WHITE)
        MENU_LOC = ((WIDTH / 2) - (MENU_TEXT.get_width() / 2), HEIGHT / 8)
        WINDOW.blit(MENU_TEXT, MENU_LOC)

        #Display menu shortcut
        SHORTCUT_FONT = pygame.font.SysFont(['futura', 'arial bold'], 20)
        SHORTCUT_TEXT = SHORTCUT_FONT.render(
            "Press [m] at any time to Return to Main Menu", True, WHITE)
        SHORTCUT_LOC = ((WIDTH / 2) - SHORTCUT_TEXT.get_width() / 2,
                        (HEIGHT / 3 - 30))
        WINDOW.blit(SHORTCUT_TEXT, SHORTCUT_LOC)

        #create buttons
        BUTTON_FONT = pygame.font.SysFont(['futura', 'arial bold'], 50)
        BUTTONS = []
        TEXTS = []
        #create play button
        PLAY_TEXT = BUTTON_FONT.render("PLAY", True, PURPLE)
        PLAY_LOC = ((WIDTH/2) - (PLAY_TEXT.get_width() / 2),(HEIGHT * 2) / 5)
        PLAY_BUTTON = pygame.Rect(PLAY_LOC[0], PLAY_LOC[1],
                                    PLAY_TEXT.get_width() + 10, 60)
        BUTTONS.append(PLAY_BUTTON)
        TEXTS.append(PLAY_TEXT)

        #create options button
        OPTIONS_TEXT = BUTTON_FONT.render("OPTIONS", True, PURPLE)
        OPTIONS_LOC = ((WIDTH/2)- (OPTIONS_TEXT.get_width() / 2), (HEIGHT * 3)
                                                                         / 5)
        OPTIONS_BUTTON = pygame.Rect(OPTIONS_LOC[0], OPTIONS_LOC[1],
                                    OPTIONS_TEXT.get_width() + 10, 60)
        BUTTONS.append(OPTIONS_BUTTON)
        TEXTS.append(OPTIONS_TEXT)

        #create quit button
        QUIT_TEXT = BUTTON_FONT.render("QUIT", True, PURPLE)
        QUIT_LOC = ((WIDTH/2) - (QUIT_TEXT.get_width() / 2),(HEIGHT * 4) / 5)
        QUIT_BUTTON = pygame.Rect(QUIT_LOC[0], QUIT_LOC[1],
                                    QUIT_TEXT.get_width() + 10, 60)
        BUTTONS.append(QUIT_BUTTON)
        TEXTS.append(QUIT_TEXT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #quit button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.collidepoint(event.pos):
                    pygame.quit()

            #play button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.collidepoint(event.pos):
                    instructions()

            #option button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BUTTON.collidepoint(event.pos):
                    options()

        a, b = pygame.mouse.get_pos()
        #draw buttons and change color if hovered on
        for button in BUTTONS:
            if button.x <= a <= (
                button.x + TEXTS[BUTTONS.index(button)].get_width()) and (
                (button.y <= b <= button.y + 70)):
                pygame.draw.rect(WINDOW, WHITE, button)
            else:
                pygame.draw.rect(WINDOW, BLUE, button)
            WINDOW.blit(TEXTS[BUTTONS.index(button)], (button.x + 3, button.y))

        #Update window
        pygame.display.update()

    pygame.quit()

def options():
    """
    A function used to display the Options of the Checkers game.

    Allows the user to toggle on/off music and change board dimensions.
    """
    pygame.display.set_caption('Options')
    run = True

    while run:
        #Set background
        WINDOW.blit(BACKGROUND.img, (0,0))

        #Display 'OPTIONS'
        MENU_FONT = pygame.font.SysFont(['futura', 'arial bold'], 100)
        MENU_TEXT = MENU_FONT.render("OPTIONS", True, WHITE)
        MENU_LOC = ((WIDTH / 2) - (MENU_TEXT.get_width() / 2), HEIGHT / 8)
        WINDOW.blit(MENU_TEXT, MENU_LOC)

        #Display instructions to edit dimension
        SCALE_FONT = pygame.font.SysFont(['futura', 'arial bold'], 20)
        SCALE_DECREASE_TEXT = SCALE_FONT.render(
            "Press [j] to Decrease Board Dimensions", True, WHITE)
        SCALE_INCREASE_TEXT = SCALE_FONT.render(
            "Press [k] to Increase Board Dimensions", True, WHITE)
        SCALE_DECREASE_LOC = ((WIDTH / 2) - SCALE_DECREASE_TEXT.get_width() / 2,
                        (HEIGHT / 2 - 30))
        SCALE_INCREASE_LOC = ((WIDTH / 2) - SCALE_INCREASE_TEXT.get_width() / 2,
                        (HEIGHT / 2 + 10))
        WINDOW.blit(SCALE_DECREASE_TEXT, SCALE_DECREASE_LOC)
        WINDOW.blit(SCALE_INCREASE_TEXT, SCALE_INCREASE_LOC)

        #Create button
        BUTTON_FONT = pygame.font.SysFont(['futura', 'arial bold'], 50)
        #Create MUSIC button
        MUSIC_TEXT = BUTTON_FONT.render("TOGGLE MUSIC", True, PURPLE)
        MUSIC_LOC = ((WIDTH/2) - (MUSIC_TEXT.get_width() / 2),(HEIGHT / 3))
        MUSIC_BUTTON = pygame.Rect(MUSIC_LOC[0], MUSIC_LOC[1],
                                    MUSIC_TEXT.get_width() + 10, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #Music button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MUSIC_BUTTON.collidepoint(event.pos):
                    MUSIC.play()

            #Return to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    main_menu()
                if event.key == pygame.K_j:
                    GRID.decrease()
                if event.key == pygame.K_k:
                    GRID.increase()

        #Create Dimension Label
        DIM_TEXT = BUTTON_FONT.render("DIMENSION: {} X {}".format(GRID.rows,
                                                    GRID.columns),True, PURPLE)
        DIM_LOC = ((WIDTH/2) - (DIM_TEXT.get_width() / 2),(HEIGHT * 3 / 5))
        DIM_BUTTON = pygame.Rect(DIM_LOC[0], DIM_LOC[1],
                                 DIM_TEXT.get_width() + 10, 60)
        pygame.draw.rect(WINDOW, BLUE, DIM_BUTTON)
        WINDOW.blit(DIM_TEXT, DIM_LOC)
        a, b = pygame.mouse.get_pos()
        #Draw button and change color if hovered on
        if (MUSIC_BUTTON.x <= a <= MUSIC_BUTTON.x + MUSIC_TEXT.get_width()
            and MUSIC_BUTTON.y <= b <= MUSIC_BUTTON.y + 70):
            pygame.draw.rect(WINDOW, WHITE, MUSIC_BUTTON)
        else:
            pygame.draw.rect(WINDOW, BLUE, MUSIC_BUTTON)
        WINDOW.blit(MUSIC_TEXT, (MUSIC_BUTTON.x + 3, MUSIC_BUTTON.y))    

        #Update window
        pygame.display.update()

    pygame.quit()

def end_menu(winner):
    """
    A function used to display the End Menu of the Checkers game.

    Congratulates the winner. Allows the user quit or go back to the main menu
    after losing.
    """
    pygame.display.set_caption('Winner!')
    run = True

    while run:
        time = clock.tick(FPS)/1000
        #Set background
        WINDOW.blit(BACKGROUND.img, (0,0))

        #Display 'WINNER'
        if winner == "THE PERSON WHO DID NOT PRESS THE R KEY":
            font_size = 20
        else:
            font_size = 60
        MENU_FONT = pygame.font.SysFont(['futura', 'arial bold'], font_size)
        MENU_TEXT = MENU_FONT.render("{} IS THE WINNER!".format(winner), True, WHITE)
        MENU_LOC = ((WIDTH / 2) - (MENU_TEXT.get_width() / 2), HEIGHT / 4)
        WINDOW.blit(MENU_TEXT, MENU_LOC)

        #Display instructions to continue
        SCALE_FONT = pygame.font.SysFont(['futura', 'arial bold'], 20)
        SCALE_DECREASE_TEXT = SCALE_FONT.render(
            "Press [q] to QUIT", True, WHITE)
        SCALE_INCREASE_TEXT = SCALE_FONT.render(
            "Press [m] to Return to the Main Menu", True, WHITE)
        SCALE_DECREASE_LOC = ((WIDTH / 2) - SCALE_DECREASE_TEXT.get_width() / 2,
                        (HEIGHT / 2 - 30))
        SCALE_INCREASE_LOC = ((WIDTH / 2) - SCALE_INCREASE_TEXT.get_width() / 2,
                        (HEIGHT / 2 + 10))
        WINDOW.blit(SCALE_DECREASE_TEXT, SCALE_DECREASE_LOC)
        WINDOW.blit(SCALE_INCREASE_TEXT, SCALE_INCREASE_LOC)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #Return to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    main_menu()
                if event.key == pygame.K_q:
                    pygame.quit()

        #Update window
        rolling_background(time, WIN_BACKGROUND)
        pygame.display.update()

    pygame.quit()

def instructions():
    """
    A function used to display the Instructions of the Checkers game.

    Press any key to continue.
    """
    pygame.display.set_caption('How to Play!')
    run = True

    while run:
        time = clock.tick(FPS)/1000
        #Set background
        WINDOW.blit(BACKGROUND.img, (0,0))

        #Display 'How to Play'
        MENU_FONT = pygame.font.SysFont(['futura', 'arial bold'], 100)
        MENU_TEXT = MENU_FONT.render("How to Play", True, WHITE)
        MENU_LOC = ((WIDTH / 2) - (MENU_TEXT.get_width() / 2), HEIGHT / 8)
        WINDOW.blit(MENU_TEXT, MENU_LOC)

        #Display instructions to play
        INFO_FONT = pygame.font.SysFont(['futura', 'arial bold'], 20)
        CLICK1_TEXT = INFO_FONT.render(
            "Click on any piece to select it and reveal possible moves.",
            True, WHITE)
        CLICK2_TEXT = INFO_FONT.render(
            "Then, click on any empty space to move the piece.",
            True, WHITE)
        JUMP_TEXT = INFO_FONT.render(
            "Note: Please click each jump when taking multiple pieces.",
            True, WHITE)
        RESIGN_TEXT = INFO_FONT.render(
            "A player may Resign during the game by pressing [r]!",
            True, WHITE)
        CONTINUE_TEXT = INFO_FONT.render(
            "Press [SPACEBAR] to Continue to Game!",
            True, WHITE)
        CLICK1_LOC = ((WIDTH / 2) - CLICK1_TEXT.get_width() / 2,
                        (HEIGHT / 2 - 30))
        CLICK2_LOC = ((WIDTH / 2) - CLICK2_TEXT.get_width() / 2,
                        (HEIGHT / 2 + 10))
        JUMP_LOC = ((WIDTH / 2) - JUMP_TEXT.get_width() / 2,
                        (HEIGHT / 2 + 50))
        RESIGN_LOC = ((WIDTH / 2) - RESIGN_TEXT.get_width() / 2,
                        (HEIGHT / 2 + 90))
        CONTINUE_LOC = ((WIDTH / 2) - CONTINUE_TEXT.get_width() / 2,
                        (HEIGHT / 2 + 130))
        WINDOW.blit(CLICK1_TEXT, CLICK1_LOC)
        WINDOW.blit(CLICK2_TEXT, CLICK2_LOC)
        WINDOW.blit(JUMP_TEXT, JUMP_LOC)
        WINDOW.blit(RESIGN_TEXT, RESIGN_LOC)
        WINDOW.blit(CONTINUE_TEXT, CONTINUE_LOC)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            #Return to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    main_menu()
                if event.key == pygame.K_SPACE:
                    main()

        #Update window
        rolling_background(time, CAT)
        pygame.display.update()

    pygame.quit()

def clicked_row_col(pos):
    """
    A helper function used to find the location, x/y coordinates, based on
    mouse click position.

    Inputs:
        pos : tuple : the x and y coordinates of the cursor when click was made.

    Outputs:
        row, col : int, int: the coordinates of the square on the grid that
        corresponds to the area clicked.
    """
    x, y = pos
    row = y // GRID.row_height
    col = x // GRID.column_width
    return row, col

def main():
    """
    A function used to play the Game of Checkers.

    Allows the user to make moves and beat their opponent.
    """
    pygame.display.set_caption('Game of Checkers')
    run = True

    while run:
        time = clock.tick(FPS)/1000

        for event in pygame.event.get():

            #If window is quit
            if event.type == pygame.QUIT:
                run = False

            #Return to main menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    main_menu()
                if event.key == pygame.K_r:
                    end_menu("THE PERSON WHO DID NOT PRESS THE R KEY")

            #To make a move
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = clicked_row_col(pos)
                #Check if piece
                if GRID.GRID_U.board[row][col] != 0:
                    GRID.GRID_U.r = row
                    GRID.GRID_U.c = col
                    GRID.possible_moves = []
                    GRID.possible_moves += GRID.GRID_U.board[row][col].find_possible_moves(GRID.GRID_U)
                    
                #Check if no piece
                if GRID.GRID_U.board[row][col] == 0:
                    if GRID.GRID_U.r is None:
                        pass
                    else:
                        trying = GRID.GRID_U.board[GRID.GRID_U.r][GRID.GRID_U.c].find_possible_moves(GRID.GRID_U)
                        if (col  + 1, row + 1) in trying:
                            GRID.possible_moves = []
                            GRID.GRID_U.move(
                                GRID.GRID_U.board[GRID.GRID_U.r][GRID.GRID_U.c],
                                row, col)
                            winner = GRID.GRID_U.check_winner()
                if GRID.GRID_U.winner:
                    end_menu(winner)

        #Update window
        # GRID.draw_possible_moves(GRID.possible_moves)
        rolling_background(time, BACKGROUND)
        GRID.draw_board(GRID.GRID_U)
        pygame.display.update()

    pygame.quit()

#Show the Main Menu on start up
main_menu()
