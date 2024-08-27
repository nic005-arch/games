import copy
import sys
import pygame
import random
import numpy as np
import time

from var import *

# --- PYGAME SETUP ---

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

pygame.font.init()
font = pygame.font.SysFont('Arial', 35)
FONT = font

# --- CLASSES ---

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_sqrs = self.squares 
        self.marked_sqrs = 0

    def final_state(self, show=False):

        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[0][0] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[0][0]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[2][0] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[2][0]

        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(len(empty_sqrs))
        return empty_sqrs[idx] 

    def minimax(self, board, maximizing):
        case = board.final_state()
        if case == 1:
            return 1, None  
        if case == 2:
            return -1, None
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.rnd(main_board)
        else:
            eval, move = self.minimax(main_board, False)
        return move 

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1  
        self.player1_name = ''
        self.player2_name = ''
        self.gamemode = None  
        self.running = True
        self.home_screen = True  
        self.reset_button = False
        self.replay_button = False
        self.game_var = 0

    def show_lines(self):
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
        elif self.player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

    def create_button(self, text, x, y, width, height, color, hover_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        pressed = False

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(screen, hover_color, (x, y, width, height), border_radius=10)
            if click[0] == 1:
                pressed = True
        else:
            pygame.draw.rect(screen, color, (x, y, width, height), border_radius=10)

        text_surf = font.render(text, True, BIANCO)
        text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surf, text_rect)
        pygame.display.update((x, y, width, height))
        
        return pressed
    
    def show_home(self):
        screen.fill(BG_COLOR)
        pvp_pressed = self.create_button('PvP', WIDTH // 2 - 105, HEIGHT // 2 - 75, 200, 70, LINE_COLOR, CIRC_COLOR)
        ai_pressed = self.create_button('Contro il bot',  WIDTH // 2 - 105, HEIGHT // 2 + 25, 200, 70, LINE_COLOR, CIRC_COLOR)
        pygame.display.update()
        return pvp_pressed, ai_pressed
    
    def ask_names(self):
        input_box1 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 150, 200, 50)
        input_box2 = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        color_active = YELLOW 
        color_inactive = CIRC_COLOR
        fill_color = ALICEBLUE  
        border_color = STEELBLUE  
        color1 = color_inactive
        color2 = color_inactive
        active1 = False
        active2 = False
        text1 = ''
        text2 = ''
        font = FONT
    
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box1.collidepoint(event.pos):
                        active1 = True
                        active2 = False
                    elif input_box2.collidepoint(event.pos):
                        active2 = True
                        active1 = False
                    else:
                        active1 = active2 = False

                if event.type == pygame.KEYDOWN:
                    if active1:
                        if event.key == pygame.K_RETURN:
                            active1 = False
                        elif event.key == pygame.K_BACKSPACE:
                            text1 = text1[:-1]
                        else:
                            text1 += event.unicode
                    elif active2:
                        if event.key == pygame.K_RETURN:
                            active2 = False
                        elif event.key == pygame.K_BACKSPACE:
                            text2 = text2[:-1]
                        else:
                            text2 += event.unicode

                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.game_var == 1:
                    if text1 and text2:
                        self.player1_name = text1
                        self.player2_name = text2
                        self.start_pvp()
                        return  

            color1 = color_active if active1 else color_inactive
            color2 = color_active if active2 else color_inactive

            screen.fill(BG_COLOR)

            pygame.draw.rect(screen, fill_color, input_box1, border_radius=10)
            pygame.draw.rect(screen, color1, input_box1, 2, border_radius=10)
            pygame.draw.rect(screen, fill_color, input_box2, border_radius=10)
            pygame.draw.rect(screen, color2, input_box2, 2, border_radius=10)

            label1 = font.render("Player 1:", True, BIANCO)
            screen.blit(label1, (input_box1.x - label1.get_width() - 10, input_box1.y + 10))

            label2 = font.render("Player 2:", True, BIANCO)
            screen.blit(label2, (input_box2.x - label2.get_width() - 10, input_box2.y + 10))


            txt_surface1 = font.render(text1, True, border_color)
            screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))

            txt_surface2 = font.render(text2, True, border_color)
            screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))


            val = self.create_button('Start', WIDTH // 2 - 50, HEIGHT // 2 + 100, 100, 50, LINE_COLOR, CIRC_COLOR)
            if val and text1 and text2:
                self.game_var = self.set_game_var()
                if self.game_var == 1:
                    self.player1_name = text1
                    self.player2_name = text2
                    self.start_pvp()
                    return  

            pygame.display.flip()

    def set_game_var(self):
        self.game_var = 1
        return self.game_var
    
    def start_pvp(self):
        self.gamemode = 'pvp'
        self.home_screen = False
        self.show_lines()
   


    def start_ai(self):
        self.gamemode = 'ai'
        self.home_screen = False
        self.player2_name = 'Bot'
        self.show_lines()

    def show_winner(self):
        if self.board.final_state() == 1:
            winner = self.player1_name
        elif self.board.final_state() == 2:
            winner = self.player2_name
        else:
            winner = 'Nobody'
    
        screen.fill(BG_COLOR)

        font = pygame.font.Font(None, 72)
        shadow_text = font.render(f'{winner} wins!', True, (0, 0, 0)) 
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 2 + 3))
        text = font.render(f'{winner} wins!', True, BIANCO)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        screen.blit(shadow_text, shadow_rect)
        screen.blit(text, text_rect)

        pygame.draw.rect(screen, (255, 215, 0), text_rect.inflate(20, 20), 3, border_radius=15) 
        pygame.display.update()

        clock = pygame.time.Clock()  
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            restart_pressed = self.create_button('Home', WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50, LINE_COLOR, CIRC_COLOR)
            replay_pressed = self.create_button('Play again', WIDTH // 2 - 100, HEIGHT // 2 + 200, 200, 50, LINE_COLOR, CIRC_COLOR)

            if restart_pressed:
                return True, False
            if replay_pressed:
                return False, True
            clock.tick(120)
                
        

        

def main():
    game = Game()
    clock = pygame.time.Clock()

    while True:
        if game.home_screen:
            pvp_pressed, ai_pressed = game.show_home()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if pvp_pressed:
                game.ask_names()
            elif ai_pressed:
                game.start_ai()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        game.change_gamemode()
                    if event.key == pygame.K_r:
                        game.reset()
                    if event.key == pygame.K_0:
                        game.ai.level = 0
                    if event.key == pygame.K_1:
                        game.ai.level = 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE
                    if game.board.empty_sqr(row, col) and game.running:
                        game.make_move(row, col)
                        if game.isover():
                            game.running = False

            if game.gamemode == 'ai' and game.player == game.ai.player and game.running:
                pygame.display.update()
                row, col = game.ai.eval(game.board)
                game.make_move(row, col)
                if game.isover():
                    game.running = False

            if not game.running:
                pygame.display.update()
                time.sleep(1)
                restart , replay = game.show_winner()
            
                if restart ==  True and not game.running :
                    game.reset()
                    game.reset_button = False

                if replay  == True and not game.running and game.gamemode == 'pvp':
                    game.reset()
                    game.home_screen = False
                    game.ask_names()
                    game.running = True
                    game.reset_button = False
                    game.replay_button = False  
                
                if replay  == True and not game.running and game.gamemode == 'ai':
                    game.reset()
                    game.start_ai()
                    game.running = True
                    game.reset_button = False
                    game.replay_button = False

            pygame.display.update()
            pygame.display.flip()
            clock.tick(120)

main()
