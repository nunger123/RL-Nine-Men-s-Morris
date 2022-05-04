"""
A minimal implementation of Monte Carlo tree search (MCTS) in Python 3
Luke Harold Miles, July 2019, Public Domain Dedication
See also https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
"""
from abc import ABC, abstractmethod
from collections import defaultdict
import math

from nine_mens import NineMensMorris, Agent
import gui
import time
import sys


class MCTS:
    "Monte Carlo tree searcher. First rollout the tree then choose a move."

    def __init__(self, exploration_weight=1):
        self.Q = defaultdict(int)  # total reward of each node
        self.N = defaultdict(int)  # total visit count for each node
        self.children = dict()  # children of each node
        self.exploration_weight = exploration_weight
        print("TEST")

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
        file1 = open('myfile.txt', 'w')
        L = ["This is Delhi \n", "This is Paris \n", "This is London \n"]
        s = "Hello\n"
          
        # Writing a string to file
        file1.write(s)
          
        # Writing multiple strings
        # at a time
        file1.writelines(L)
          
        # Closing file
        file1.close()
          
        # Checking if the data is
        # written to file or not
        file1 = open('myfile.txt', 'r')
        print(file1.read())
        file1.close()
        "Make the tree one layer better. (Train for one iteration.)"
        start = time.time()
        path = self._select(node)
        print(time.time()-start, end="\t", file = sys.stderr)

        start = time.time()
        leaf = path[-1]
        print(time.time()-start, end="\t", file = sys.stdout)
        
        start = time.time()
        self._expand(leaf)
        print(time.time()-start, end="\t", file = sys.stdout)

        start = time.time()
        reward = self._simulate(leaf)
        print(time.time()-start, end="\t", file = sys.stdout)
        
        start = time.time()
        self._backpropagate(path, reward)
        print(time.time()-start, file = sys.stdout)

        
    def _select(self, node):
        "Find an unexplored descendent of `node`"
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                # node is either unexplored or terminal
                return path
            unexplored = self.children[node] - self.children.keys()
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # descend a layer deeper

    def _expand(self, node):
        "Update the `children` dict with the children of `node`"
        if node in self.children:
            return  # already expanded
        self.children[node] = node.find_children()

    def _simulate(self, node):
        "Returns the reward for a random simulation (to completion) of `node`"
        invert_reward = True
        while True:
            if node.is_terminal():
                reward = node.reward()
                return 1 - reward if invert_reward else reward
            node = node.find_random_child()
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
        assert all(n in self.children for n in self.children[node])

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
                
                clone = gui.clone_gamestate(self.game, self.agents, self.playing_agent)
                
                clone[0].place_piece(place_pos, clone[1][clone[2]])
                created_mills = clone[0].formed_mills(clone[1][clone[2]])
                created_mills = [f for f in created_mills if place_pos in f]
                
                if len(created_mills) == 0:
                    node = Node(clone[0],clone[1],1-clone[2])
                    node.game.check_mode(*(node.agents))
                    result.add(node)
                elif len(created_mills) == 1:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = gui.clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece)
                        node = Node(cloneclone[0],cloneclone[1],1-cloneclone[2])
                        node.game.check_mode(*(node.agents))
                        result.add(node)
                elif len(created_mills) == 2:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = gui.clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece)
                        for removable_piece2 in cloneclone[0].removable_pieces(cloneclone[1][1-cloneclone[2]]):
                            clonecloneclone = gui.clone_gamestate(cloneclone[0], cloneclone[1], cloneclone[2])
                            clonecloneclone[0].remove_piece(removable_piece2)
                            node = Node(clonecloneclone[0],clonecloneclone[1],1-clonecloneclone[2])
                            node.game.check_mode(*(node.agents))
                            result.add(node)
  
        else:
            for move_to_make in self.game.get_possible_moves(self.agents[self.playing_agent]):
                from_i, from_j, to_i, to_j = move_to_make
                
                clone = gui.clone_gamestate(self.game, self.agents, self.playing_agent)
                
                clone[0].move_piece((from_i, from_j),(to_i, to_j),clone[1][clone[2]])
                
                
                created_mills = clone[0].formed_mills(clone[1][clone[2]])
                created_mills = [f for f in created_mills if place_pos in f]
                
                if len(created_mills) == 0:
                    node = Node(clone[0],clone[1],1-clone[2])
                    node.game.check_mode(*(node.agents))
                    result.add(node)
                elif len(created_mills) == 1:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = gui.clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece)
                        node = Node(cloneclone[0],cloneclone[1],1-cloneclone[2])
                        node.game.check_mode(*(node.agents))
                        result.add(node)
                elif len(created_mills) == 2:
                    for removable_piece in clone[0].removable_pieces(clone[1][1-clone[2]]):
                        cloneclone = gui.clone_gamestate(clone[0], clone[1], clone[2])
                        cloneclone[0].remove_piece(removable_piece)
                        for removable_piece2 in cloneclone[0].removable_pieces(cloneclone[1][1-cloneclone[2]]):
                            clonecloneclone = gui.clone_gamestate(cloneclone[0], cloneclone[1], cloneclone[2])
                            clonecloneclone[0].remove_piece(removable_piece2)
                            node = Node(clonecloneclone[0],clonecloneclone[1],1-clonecloneclone[2])
                            node.game.check_mode(*(node.agents))
                            result.add(node)
        return result

    def find_random_child(self):
        gamestate = gui.clone_gamestate(self.game, self.agents, self.playing_agent)
        random_child = Node(gamestate[0], gamestate[1], gamestate[2])
        gui.make_random_move(random_child.game, random_child.agents, random_child.playing_agent)
        random_child.playing_agent = 1 - random_child.playing_agent
        random_child.game.check_mode(*(random_child.agents))
        return random_child

    def is_terminal(self):
        if self.game.check_end_game(self.agents[self.playing_agent]):
            return True
        return False

    def reward(self):
        return_elem = self.game.check_end_game(self.agents[self.playing_agent])
        if return_elem == "draw":
            return 0.5
        if return_elem == True:
            return 0
        else:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board {board}")
            return 1

    def __hash__(self):
        return hash(self.game.board[0][0], self.game.board[0][3], self.game.board[0][6], self.game.board[1][1], self.game.board[1][3], self.game.board[1][5], self.game.board[2][2], self.game.board[2][3], self.game.board[2][4], self.game.board[3][0], self.game.board[3][1], self.game.board[3][2], self.game.board[3][4], self.game.board[3][5], self.game.board[3][6], self.game.board[4][2], self.game.board[4][3], self.game.board[4][4], self.game.board[5][1], self.game.board[5][3], self.game.board[5][5], self.game.board[6][0], self.game.board[6][3], self.game.board[6][6],self.game.turns_without_mill,self.agents[0].place_mode,self.agents[0].move_mode,self.agents[0].held,self.agents[0].on_board,self.agents[1].place_mode,self.agents[1].move_mode,self.agents[1].held,self.agents[1].on_board,self.playing_agent)

    def __eq__(self, other):
        if isinstance(other, A):
            return self.__key() == other.__key()
        return NotImplemented