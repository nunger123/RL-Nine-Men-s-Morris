import pygame
import sys

import time
import random
from monte_carlo_tree_search import MCTS, Node

from nine_mens import NineMensMorris, Agent

FRAME_WIDTH = 800
FRAME_HEIGHT = 600

# size of a cell
INC_X = 70
INC_Y = 70

# starting corner of the board
SHIFT_X = 200
SHIFT_Y = 100

# line width of board lines and buttons borders
LINE_WIDTH = 1

# some colors predifined
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GREY = (200, 200, 200)


class MainGame:
    """
    this class contains the GUI, handles user inputs, and runs the main game
    """

    def __init__(self):
        
        # initialize pygame and record start time
        pygame.init()
        pygame.display.set_caption('Nine Men\'s Morris')

        # initialize screen surface to draw on
        self.surface = pygame.display.set_mode((FRAME_WIDTH,FRAME_HEIGHT))
        # initialize board class
        self.game = NineMensMorris()

        self.agents = [Agent(1), Agent(2)]
        self.playing_agent = 0


        # # load the images and scale them
        self.black_im = pygame.image.load("black.png")
        self.black_im = pygame.transform.scale(self.black_im, (50, 50))

        self.white_im = pygame.image.load("white.png")
        self.white_im = pygame.transform.scale(self.white_im, (50, 50))


    def draw_line(self, start, end):
        """
        quick function to draw lines based on coordinated of the board, not pixels
        args:
            start: (i,j): coordinates of the first point of the line
            end: (ei,ej): coordinates of the end point of the line
        """

        pygame.draw.line(self.surface,
                         Colors.BLACK,
                         (SHIFT_X + start[0]*INC_X, SHIFT_Y + start[1]*INC_Y),
                         (SHIFT_X +   end[0]*INC_X, SHIFT_Y +   end[1]*INC_Y),
                         width=LINE_WIDTH)
    
    def draw_dot(self, point):
        pygame.draw.circle(
            self.surface, 
            Colors.BLACK, 
            (SHIFT_X+point[0]*INC_X, SHIFT_Y+point[1]*INC_Y),
            3)


    def draw_board(self):
        """
        fills all screen white then draws the board (without pieces)
        """
        self.surface.fill(Colors.WHITE)

        for k in [0, 1, 2]:

            for i in [k, 3, 6-k]:
                for j in [k, 3, 6-k]:
                    if i!=3 or j!=3:
                        self.draw_dot((i,j))
            
            self.draw_line((k,k), (k,6-k))
            self.draw_line((k,6-k), (6-k,6-k))
            self.draw_line((6-k,6-k), (6-k,k))
            self.draw_line((6-k,k), (k,k))
        
        self.draw_line((3,0), (3,2))
        self.draw_line((0,3), (2,3))
        self.draw_line((6,3), (4,3))
        self.draw_line((3,6), (3,4))

    def transform_input(self, pos):
        i, j = pos

        return (round((j - SHIFT_Y) / INC_Y), round((i - SHIFT_X) / INC_X))

    def apply_user_input(self, source, target=None, to_remove=False):
        """
        takes the mouse pos, transforms it into board coordinates, and check move validity
        """

        
        source = self.transform_input(source)

        if target is None:
            if to_remove:
                return self.game.remove_piece(source, self.agents[1 - self.playing_agent])
            return self.game.place_piece(source, self.agents[self.playing_agent])
        
        target = self.transform_input(target)

        return self.game.move_piece(source, target, self.agents[self.playing_agent])
        
    
    def ask_for_removal(self):
        target = None
        done = False
        while not done:
            for event in pygame.event.get():
                # for exit
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                # if the case of waiting a left click (ordinary play)
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    return self.apply_user_input(pos, to_remove=True)

    def play(self):
        source = None
        target = None
        done = False
        change = False
        round_cnt = 0
        while not done:
#            if False:
#            if True:
            if round_cnt % 2 == 0:
                #random move
                time.sleep(0.1)
                self.make_random_move(self.game, self.agents, self.playing_agent)
                
                self.playing_agent = 1 - self.playing_agent
                change = True
                round_cnt = round_cnt + 1
                
            else:
                for event in pygame.event.get():
                    # for exit
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit(0)

                    # if the case of waiting a left click (ordinary play)
                    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        if source is None:
                            source = pos
                        else:
                            target = pos
                        
                condition1 = self.agents[self.playing_agent].place_mode and source is not None

                condition2 = not self.agents[self.playing_agent].place_mode  and target is not None
                

                if condition1 or condition2: 
                    valid = self.apply_user_input(source, target)

                    if valid:
                        new_moved = self.transform_input(source) if condition1 else self.transform_input(target)
                        created_mills = self.game.formed_mills(self.agents[self.playing_agent])
                        for mill in created_mills:
                            self.draw_board()
                            self.draw_pieces()

                            pygame.display.update()
                            if new_moved in mill:
                                valid = self.ask_for_removal()
                                while not valid:
                                    valid = self.ask_for_removal()
                                    print("invalid")
                                    
                        self.playing_agent = 1 - self.playing_agent
                        change = True
                        round_cnt = round_cnt + 1

                    else:
                        print("invalid")
                    
                    source = None
                    target = None
                
            self.draw_board()
            self.draw_pieces()

            pygame.display.update()
            print(self.game.turns_without_mill)
            if change:
                change = False
                self.game.check_mode(*(self.agents))
                if self.game.check_end_game(self.agents[self.playing_agent]):
                    done = True
                    if self.game.turns_without_mill >= 30:
                        print("---DRAW---")
                    elif self.playing_agent == 0:
                        print("---WHITE WON---")
                    else:
                        print("---BLACK WON---")
                    time.sleep(10)
    def draw_pieces(self):
        """
        draws the pieces using the two images, and the board state
        """
        black_rect = self.black_im.get_rect()
        white_rect = self.white_im.get_rect()

        for i in range(len(self.game.board)):
            for j in range(len(self.game.board[0])):
                if self.game.board[i][j] == self.agents[0].id:
                    black_rect.center = (SHIFT_X + j*INC_X, SHIFT_Y + i*INC_Y)
                    self.surface.blit(self.black_im, black_rect)
                
                elif self.game.board[i][j] == self.agents[1].id:
                    white_rect.center = (SHIFT_X + j*INC_X, SHIFT_Y + i*INC_Y)
                    self.surface.blit(self.white_im, white_rect)

    def clone_gamestate(self):
        cloned_game = self.game.clone_game()
        cloned_agents = [self.agents[0].clone_agent(), self.agents[1].clone_agent()]
        return [cloned_game, cloned_agents, self.playing_agent]
        
    def make_random_move(self, game, agents, playing_agent):
        if agents[playing_agent].place_mode:
            place_pos = random.choice(game.free_spaces())
            game.place_piece(place_pos, agents[playing_agent])
            created_mills = game.formed_mills(agents[playing_agent])
            for mill in created_mills:
                if place_pos in mill:
                    print("made mill")
                    to_remove = random.choice(game.removable_pieces(agents[1-playing_agent]))
                    game.remove_piece(to_remove,agents[1-playing_agent])
                    
        else:
            move_to_make = random.choice(game.get_possible_moves(agents[playing_agent]))
            from_i, from_j, to_i, to_j = move_to_make
            game.move_piece((from_i, from_j),(to_i, to_j),agents[playing_agent])
            created_mills = game.formed_mills(agents[playing_agent])
            for mill in created_mills:
                if (to_i, to_j) in mill:
                    print("made mill")
                    to_remove = random.choice(game.removable_pieces(agents[1-playing_agent]))
                    game.remove_piece(to_remove,agents[1-playing_agent])

a = MainGame()
a.play()
