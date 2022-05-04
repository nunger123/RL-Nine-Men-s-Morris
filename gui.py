import pygame
import sys

import time
import random

from tqdm import tqdm
from nine_mens import NineMensMorris, Agent
from collections import namedtuple
import pandas as pd
import numpy as np

FRAME_WIDTH = 600
FRAME_HEIGHT = 600

# size of a cell
INC_X = 70
INC_Y = 70

# starting corner of the board
SHIFT_X = 100
SHIFT_Y = 100

# line width of board lines and buttons borders
LINE_WIDTH = 1

# some colors predifined
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GREY = (200, 200, 200)
    
GameState = namedtuple("GameState", ["game","agents","playing_agent"])


others = 0
draws = 0

class MainGame:
    """
    this class contains the GUI, handles user inputs, and runs the main game
    """
    
    def __init__(self):
        self.game = NineMensMorris()
        self.agents = [Agent(1), Agent(2)]
        self.playing_agent = 0
        
        '''
        self.game.board[0][0] = 1
        self.game.board[3][0] = 1
        self.game.board[6][0] = 1
        self.game.board[1][1] = 1
        self.game.board[3][1] = 1
        self.game.board[5][1] = 1
        self.game.board[2][2] = 1
        self.game.board[3][2] = 1
        self.game.board[4][2] = 1
        
        self.agents[0].place_mode = False
        self.agents[0].move_mode = True
        self.agents[0].held = 0
        self.agents[0].on_board = 9
        
   
        self.game.board[0][3] = 2
        self.game.board[1][3] = 2
        self.game.board[2][3] = 2
 
        self.agents[1].place_mode = False
        self.agents[1].fly_mode = True
        self.agents[1].held = 0
        self.agents[1].on_board = 3
        
        self.playing_agent = 1
        '''
   
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
        global others
        global draws
        # initialize pygame and record start time
        pygame.init()
        pygame.display.set_caption('Nine Men\'s Morris')

        # initialize screen surface to draw on
        self.surface = pygame.display.set_mode((FRAME_WIDTH,FRAME_HEIGHT))
        # initialize board class

        # # load the images and scale them
        self.black_im = pygame.image.load("black.png")
        self.black_im = pygame.transform.scale(self.black_im, (50, 50))

        self.white_im = pygame.image.load("white.png")
        self.white_im = pygame.transform.scale(self.white_im, (50, 50))
        
        tree = MCTS()
        '''print("black:")
        print(self.game.amount_morrises_number(self.agents[0]))
        print(self.game.amount_number_of_blocked_opp_pieces(self.agents[1]))
        print(self.game.amount_pieces_number(self.agents[0]))
        print(self.game.amount_number_of_2_pieces(self.agents[0]))
        print(self.game.amount_number_of_3_pieces(self.agents[0]))
        print("white:")
        print(self.game.amount_morrises_number(self.agents[1]))
        print(self.game.amount_number_of_blocked_opp_pieces(self.agents[0]))
        print(self.game.amount_pieces_number(self.agents[1]))
        print(self.game.amount_number_of_2_pieces(self.agents[1]))
        print(self.game.amount_number_of_3_pieces(self.agents[1]))'''
        source = None
        target = None
        done = False
        change = False
        round_cnt = 0
        while not done:
#            if False:
#            if True:

            if round_cnt % 2 == 0:
                board = Node(self.game, self.agents, self.playing_agent)
                for _ in tqdm(range(2500), desc="thinking...", ascii=False, ncols=75):
                #for i in range(2500):
                    tree.do_rollout(board)
                #df = pd.DataFrame(tree.records_table)
                #df.to_csv("test.csv")
                print("draws: "+str(draws)+" out of "+str(draws+others)+". That is "+str(draws/(draws+others)*100)+"%")
                draws = 0
                others = 0
                print("black:")
                '''
                print(self.game.amount_morrises_number(self.agents[0]))
                print(self.game.amount_number_of_blocked_opp_pieces(self.agents[1]))
                print(self.game.amount_pieces_number(self.agents[0]))
                print(self.game.amount_number_of_2_pieces(self.agents[0]))
                print(self.game.amount_number_of_3_pieces(self.agents[0]))'''
                print(self.game.amount_double_morris(self.agents[0]))
                print("white:")
                '''
                print(self.game.amount_morrises_number(self.agents[1]))
                print(self.game.amount_number_of_blocked_opp_pieces(self.agents[0]))
                print(self.game.amount_pieces_number(self.agents[1]))
                print(self.game.amount_number_of_2_pieces(self.agents[1]))
                print(self.game.amount_number_of_3_pieces(self.agents[1]))'''
                print(self.game.amount_double_morris(self.agents[1]))
                
                board = tree.choose(board)
                self.game = board.game
                self.agents = board.agents
                self.playing_agent = board.playing_agent
                
                print("black:")
                '''
                print(self.game.amount_morrises_number(self.agents[0]))
                print(self.game.amount_number_of_blocked_opp_pieces(self.agents[1]))
                print(self.game.amount_pieces_number(self.agents[0]))
                print(self.game.amount_number_of_2_pieces(self.agents[0]))
                print(self.game.amount_number_of_3_pieces(self.agents[0]))'''
                print(self.game.amount_double_morris(self.agents[0]))
                print("white:")
                '''
                print(self.game.amount_morrises_number(self.agents[1]))
                print(self.game.amount_number_of_blocked_opp_pieces(self.agents[0]))
                print(self.game.amount_pieces_number(self.agents[1]))
                print(self.game.amount_number_of_2_pieces(self.agents[1]))
                print(self.game.amount_number_of_3_pieces(self.agents[1]))'''
                print(self.game.amount_double_morris(self.agents[1]))

                
                #random move
                #make_random_move(self.game, self.agents, self.playing_agent)
                
                #self.playing_agent = 1 - self.playing_agent
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

def clone_gamestate(game, agents, playing_agent):
    cloned_game = game.clone_game()
    cloned_agents = [agents[0].clone_agent(), agents[1].clone_agent()]
    return GameState(cloned_game, cloned_agents, playing_agent)
    
def make_random_move(game, agents, playing_agent):
    if agents[playing_agent].place_mode:
        place_pos = random.choice(game.free_spaces())
        game.place_piece(place_pos, agents[playing_agent])
        created_mills = game.formed_mills(agents[playing_agent])
        for mill in created_mills:
            if place_pos in mill:
                to_remove = random.choice(game.removable_pieces(agents[1-playing_agent]))
                game.remove_piece(to_remove,agents[1-playing_agent])
                
    else:
        move_to_make = random.choice(game.get_possible_moves(agents[playing_agent]))
        from_i, from_j, to_i, to_j = move_to_make
        game.move_piece((from_i, from_j),(to_i, to_j),agents[playing_agent])
        created_mills = game.formed_mills(agents[playing_agent])
        for mill in created_mills:
            if (to_i, to_j) in mill:
                to_remove = random.choice(game.removable_pieces(agents[1-playing_agent]))
                game.remove_piece(to_remove,agents[1-playing_agent])


"""
Source for large part of MCTS implementation:
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication, https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""

from collections import defaultdict
import math

class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=3):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # only explored children of each node
        self.unexplored_children = dict() #only unexplored children of each node
        self.exploration_weight = exploration_weight
        #self.records_table = np.empty((2500,4))
        self.index = 0

    def choose(self, node):
        "Choose the best successor of node. (Choose a move in the game)"
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal node {node}")

        if node not in self.children:
            print("should never be taken i think")
            return node.find_random_child()

        def score(n):
            if self.N[n] == 0:
                return float("-inf")  # avoid unseen moves
            return self.Q[n] / self.N[n]  # average reward

        return max(self.children[node], key=score)

    def do_rollout(self, node):
        "Make the tree one layer better. (Train for one iteration.)"
        #self.records_table[self.index,3] = 0
        #start = time.time()
        path = self._select(node)
        #self.records_table[self.index,0] = time.time()-start
        #self.records_table[self.index,1] = self.loops

        #start = time.time()
        leaf = path[-1]
        #self.records_table[self.index,2] = len(self.children)
        
        self._expand(leaf)
        
        reward = self._simulate(leaf)
        
        self._backpropagate(path, reward)
        
        self.index = self.index + 1

    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        self.loops = 0
        while True:
            self.loops = self.loops+1
            path.append(node)
            '''if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path'''
            if (self.N[node] == 0 and node not in self.unexplored_children) or node.is_terminal():
                return path
            #start = time.time()
            condition = node in self.unexplored_children
            #self.records_table[self.index,3] = self.records_table[self.index,3]+time.time()-start
            if condition :
                #print(unexplored)
                n = self.unexplored_children[node].pop()
                if len(self.unexplored_children[node]) == 0:
                    del self.unexplored_children[node]
                #print(n)
                #print(self.unexplored_children[n])
                #print(self.unexplored_children[node])
                if node in self.children:
                    self.children[node].add(n)
                    #print(self.children[node])
                else:
                    self.children[node] = {n}
                    #print(self.children[node])
                #print(self.children[node])
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children or node in self.unexplored_children:
            return  # already expanded
        self.unexplored_children[node] = node.find_children()

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        computer_player = node.playing_agent
        computer_player_phase = node.game.get_game_phase(node.agents[computer_player])
        invert_reward = True
        if node.is_terminal():
            reward = node.reward()
            return 1 - reward if invert_reward else reward
        node = node.find_random_child()
        if computer_player_phase != node.game.get_game_phase(node.agents[computer_player]):
            #state changed
            pass
        invert_reward = not invert_reward
        while True:
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            make_random_move(node.game, node.agents, node.playing_agent)
            node.game.check_mode(*(node.agents))
            node.playing_agent = 1-node.playing_agent
            invert_reward = not invert_reward

    def _backpropagate(self, path, reward):
        "Send the reward back up to the ancestors of the leaf"
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += reward
            reward = 1 - reward  # 1 for me is 0 for my enemy, and vice versa

    def _uct_select(self, node):
        "Select a child of node, balancing exploration & exploitation"

        # All children of node should already be expanded:
        assert all(n in self.children or n in self.unexplored_children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            "Upper confidence bound for trees"
            return self.Q[n] / self.N[n] + self.exploration_weight * math.sqrt(
                log_N_vertex / self.N[n]
            )

        return max(self.children[node], key=uct)


class Node:
    def __init__(self, game, agents, playing_agent):
        self.game = game
        self.agents = agents
        self.playing_agent = playing_agent

    def find_children(self):
        result = set()
        if self.agents[self.playing_agent].place_mode:
            for place_pos in self.game.free_spaces():
                
                clone = clone_gamestate(self.game, self.agents, self.playing_agent)
                
                clone[0].place_piece(place_pos, clone[1][clone[2]])
                created_mills = clone[0].formed_mills(clone[1][clone[2]])
                created_mills = [f for f in created_mills if place_pos in f]
                
                if len(created_mills) == 0:
                    node = Node(clone[0],clone[1],1-clone[2])
                    node.game.check_mode(*(node.agents))
                    result.add(node)
                elif len(created_mills) == 1:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece, cloneclone[1][1-cloneclone[2]])
                        node = Node(cloneclone[0],cloneclone[1],1-cloneclone[2])
                        node.game.check_mode(*(node.agents))
                        result.add(node)
                elif len(created_mills) == 2:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece, cloneclone[1][1-cloneclone[2]])
                        for removable_piece2 in cloneclone[0].removable_pieces(cloneclone[1][1-cloneclone[2]]):
                            clonecloneclone = clone_gamestate(cloneclone[0], cloneclone[1], cloneclone[2])
                            clonecloneclone[0].remove_piece(removable_piece2, clonecloneclone[1][1-clonecloneclone[2]])
                            node = Node(clonecloneclone[0],clonecloneclone[1],1-clonecloneclone[2])
                            node.game.check_mode(*(node.agents))
                            result.add(node)
  
        else:
            for move_to_make in self.game.get_possible_moves(self.agents[self.playing_agent]):
                from_i, from_j, to_i, to_j = move_to_make
                
                clone = clone_gamestate(self.game, self.agents, self.playing_agent)
                
                clone[0].move_piece((from_i, from_j),(to_i, to_j),clone[1][clone[2]])
                
                
                created_mills = clone[0].formed_mills(clone[1][clone[2]])
                created_mills = [f for f in created_mills if (to_i, to_j) in f]
                
                if len(created_mills) == 0:
                    node = Node(clone[0],clone[1],1-clone[2])
                    node.game.check_mode(*(node.agents))
                    result.add(node)
                elif len(created_mills) == 1:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece, cloneclone[1][1-cloneclone[2]])
                        node = Node(cloneclone[0],cloneclone[1],1-cloneclone[2])
                        node.game.check_mode(*(node.agents))
                        result.add(node)
                elif len(created_mills) == 2:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece, cloneclone[1][1-cloneclone[2]])
                        for removable_piece2 in cloneclone[0].removable_pieces(cloneclone[1][1-cloneclone[2]]):
                            clonecloneclone = clone_gamestate(cloneclone[0], cloneclone[1], cloneclone[2])
                            clonecloneclone[0].remove_piece(removable_piece2, clonecloneclone[1][1-clonecloneclone[2]])
                            node = Node(clonecloneclone[0],clonecloneclone[1],1-clonecloneclone[2])
                            node.game.check_mode(*(node.agents))
                            result.add(node)
        return result

    def find_random_child(self):
        gamestate = clone_gamestate(self.game, self.agents, self.playing_agent)
        random_child = Node(gamestate[0], gamestate[1], gamestate[2])
        make_random_move(random_child.game, random_child.agents, random_child.playing_agent)
        random_child.playing_agent = 1 - random_child.playing_agent
        random_child.game.check_mode(*(random_child.agents))
        return random_child

    def is_terminal(self):
        if self.game.check_end_game(self.agents[self.playing_agent]):
            return True
        return False

    def reward(self):
        global others
        global draws
        return_elem = self.game.check_end_game(self.agents[self.playing_agent])
        if return_elem == "draw":
            draws = draws+1
            return 0.5
        if return_elem == True:
            others = others +1
            return 0
        else:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board {board}")
            return 1

    def __hash__(self):
        return hash((self.game.board[0][0], self.game.board[0][3], self.game.board[0][6], self.game.board[1][1], self.game.board[1][3], self.game.board[1][5], self.game.board[2][2], self.game.board[2][3], self.game.board[2][4], self.game.board[3][0], self.game.board[3][1], self.game.board[3][2], self.game.board[3][4], self.game.board[3][5], self.game.board[3][6], self.game.board[4][2], self.game.board[4][3], self.game.board[4][4], self.game.board[5][1], self.game.board[5][3], self.game.board[5][5], self.game.board[6][0], self.game.board[6][3], self.game.board[6][6],self.game.turns_without_mill,self.agents[0].place_mode,self.agents[0].move_mode,self.agents[0].held,self.agents[0].on_board,self.agents[1].place_mode,self.agents[1].move_mode,self.agents[1].held,self.agents[1].on_board,self.playing_agent))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
        
        

a = MainGame()
a.play()
