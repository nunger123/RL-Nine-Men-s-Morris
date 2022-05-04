
class Agent:
    def __init__(self, id):
        self.id = id
        self.place_mode = True
        self.move_mode = False
        self.fly_mode = False
        self.held = 9
        self.on_board = 0
        
    def clone_agent(self):
        clone = Agent(self.id)
        clone.place_mode = self.place_mode
        clone.move_mode = self.move_mode
        clone.fly_mode = self.fly_mode
        clone.held = self.held
        clone.on_board = self.on_board
        return clone
  
class NineMensMorris:
    def __init__(self):
        self.board = [
                        [   0 , None, None,  0, None, None,   0  ],
                        [ None,   0 , None,  0, None,  0  , None ],
                        [ None, None,   0,   0,   0, None , None ],
                        [   0 ,   0 ,   0, None,  0,   0  ,   0  ],
                        [ None, None,   0,   0,   0, None , None ],
                        [ None,   0 , None,  0, None,  0  , None ],
                        [   0 , None, None,  0, None, None,   0  ]
        ]
        
        self.evaluation_coefficients = [14, 37, 4, 14, 20, 2, 16, 43, 11, 8, 7, 42, 1086, 10, 1, 16, 1190]
        #                               r1  r2  r3 r4  r5 r6  r1  r2  r3  r4 r5  r6  r7   r1  r2 r3   r4
        #                               phase 1               phase 2                     phase 3
        self.turns_without_mill = 0
        self.spatial_moves = self._spatial_moves()
        self.to_check_3_pieces = [
                        [(0, 0), (0, 3), (0, 6), (3, 0), (6, 0)], 
                        [(0, 3), (0, 0), (0, 6), (1, 3), (2, 3)], 
                        [(0, 6), (0, 0), (0, 3), (3, 6), (6, 6)], 
                        [(1, 1), (1, 3), (1, 5), (3, 1), (5, 1)], 
                        [(1, 3), (1, 1), (1, 5), (0, 3), (2, 3)], 
                        [(1, 5), (1, 1), (1, 3), (3, 5), (5, 5)], 
                        [(2, 2), (2, 3), (2, 4), (3, 2), (4, 2)], 
                        [(2, 3), (2, 2), (2, 4), (0, 3), (1, 3)], 
                        [(2, 4), (2, 2), (2, 3), (3, 4), (4, 4)], 
                        [(3, 0), (3, 1), (3, 2), (0, 0), (6, 0)], 
                        [(3, 1), (3, 0), (3, 2), (1, 1), (5, 1)], 
                        [(3, 2), (3, 0), (3, 1), (2, 2), (4, 2)], 
                        [(3, 4), (3, 5), (3, 6), (2, 4), (4, 4)], 
                        [(3, 5), (3, 4), (3, 6), (1, 5), (5, 5)], 
                        [(3, 6), (3, 4), (3, 5), (0, 6), (6, 6)], 
                        [(4, 2), (4, 3), (4, 4), (2, 2), (3, 2)], 
                        [(4, 3), (4, 2), (4, 4), (5, 3), (6, 3)], 
                        [(4, 4), (4, 2), (4, 3), (2, 4), (3, 4)], 
                        [(5, 1), (5, 3), (5, 5), (1, 1), (3, 1)], 
                        [(5, 3), (5, 1), (5, 5), (4, 3), (6, 3)], 
                        [(5, 5), (5, 1), (5, 3), (1, 5), (3, 5)], 
                        [(6, 0), (6, 3), (6, 6), (0, 0), (3, 0)], 
                        [(6, 3), (6, 0), (6, 6), (4, 3), (5, 3)], 
                        [(6, 6), (6, 0), (6, 3), (0, 6), (3, 6)]
                    ]
        
        self.horizontal_morrises = [
                        [(0,0), (0,3), (0,6)],
                        [(1,1), (1,3), (1,5)],
                        [(2,2), (2,3), (2,4)],
             [(3,0), (3,1), (3,2)], [(3,4), (3,5), (3,6)],
                        [(4,2), (4,3), (4,4)],
                        [(5,1), (5,3), (5,5)],
                        [(6,0), (6,3), (6,6)],
        ]
        
        self.vertical_morrises = [
                        [(0,0), (3,0), (6,0)],
                        [(1,1), (3,1), (5,1)],
                        [(2,2), (3,2), (4,2)],
             [(0,3), (1,3), (2,3)], [(4,3), (5,3), (6,3)],
                        [(2,4), (3,4), (4,4)],
                        [(1,5), (3,5), (5,5)],
                        [(0,6), (3,6), (6,6)],
        ]
        
        self.horizontal_moves = [[None for _ in range(7)] for _ in range(7)]
        self.horizontal_moves[0][0] = [(0, 3)]
        self.horizontal_moves[0][3] = [(0, 0), (0, 6)]
        self.horizontal_moves[0][6] = [(0, 3)]
        self.horizontal_moves[1][1] = [(1, 3)]
        self.horizontal_moves[1][3] = [(1, 1), (1, 5)]
        self.horizontal_moves[1][5] = [(1, 3)]
        self.horizontal_moves[2][2] = [(2, 3)]
        self.horizontal_moves[2][3] = [(2, 2), (2, 4)]
        self.horizontal_moves[2][4] = [(2, 3)]
        self.horizontal_moves[3][0] = [(3, 1)]
        self.horizontal_moves[3][1] = [(3, 0), (3, 2)]
        self.horizontal_moves[3][2] = [(3, 1)]
        self.horizontal_moves[3][4] = [(3, 5)]
        self.horizontal_moves[3][5] = [(3, 4), (3, 6)]
        self.horizontal_moves[3][6] = [(3, 5)]
        self.horizontal_moves[4][2] = [(4, 3)]
        self.horizontal_moves[4][3] = [(4, 2), (4, 4)]
        self.horizontal_moves[4][4] = [(4, 3)]
        self.horizontal_moves[5][1] = [(5, 3)]
        self.horizontal_moves[5][3] = [(5, 1), (5, 5)]
        self.horizontal_moves[5][5] = [(5, 3)]
        self.horizontal_moves[6][0] = [(6, 3)]
        self.horizontal_moves[6][3] = [(6, 0), (6, 6)]
        self.horizontal_moves[6][6] = [(6, 3)]
    
        self.vertical_moves = [[None for _ in range(7)] for _ in range(7)]
        self.vertical_moves[0][0] = [(3, 0)]
        self.vertical_moves[0][3] = [(1, 3)]
        self.vertical_moves[0][6] = [(3, 6)]
        self.vertical_moves[1][1] = [(3, 1)]
        self.vertical_moves[1][3] = [(0, 3), (2, 3)]
        self.vertical_moves[1][5] = [(3, 5)]
        self.vertical_moves[2][2] = [(3, 2)]
        self.vertical_moves[2][3] = [(1, 3)]
        self.vertical_moves[2][4] = [(3, 4)]
        self.vertical_moves[3][0] = [(0, 0), (6, 0)]
        self.vertical_moves[3][1] = [(1, 1), (5, 1)]
        self.vertical_moves[3][2] = [(2, 2), (4, 2)]
        self.vertical_moves[3][4] = [(2, 4), (4, 4)]
        self.vertical_moves[3][5] = [(1, 5), (5, 5)]
        self.vertical_moves[3][6] = [(0, 6), (6, 6)]
        self.vertical_moves[4][2] = [(3, 2)]
        self.vertical_moves[4][3] = [(5, 3)]
        self.vertical_moves[4][4] = [(3, 4)]
        self.vertical_moves[5][1] = [(3, 1)]
        self.vertical_moves[5][3] = [(4, 3), (6, 3)]
        self.vertical_moves[5][5] = [(3, 5)]
        self.vertical_moves[6][0] = [(3, 0)]
        self.vertical_moves[6][3] = [(5, 3)]
        self.vertical_moves[6][6] = [(3, 6)]
        
        self.horizontal_morris_lookup = [[[(0, 0), (0, 3), (0, 6)], None, None, [(0, 0), (0, 3), (0, 6)], None, None, [(0, 0), (0, 3), (0, 6)]], [None, [(1, 1), (1, 3), (1, 5)], None, [(1, 1), (1, 3), (1, 5)], None, [(1, 1), (1, 3), (1, 5)], None], [None, None, [(2, 2), (2, 3), (2, 4)], [(2, 2), (2, 3), (2, 4)], [(2, 2), (2, 3), (2, 4)], None, None], [[(3, 0), (3, 1), (3, 2)], [(3, 0), (3, 1), (3, 2)], [(3, 0), (3, 1), (3, 2)], None, [(3, 4), (3, 5), (3, 6)], [(3, 4), (3, 5), (3, 6)], [(3, 4), (3, 5), (3, 6)]], [None, None, [(4, 2), (4, 3), (4, 4)], [(4, 2), (4, 3), (4, 4)], [(4, 2), (4, 3), (4, 4)], None, None], [None, [(5, 1), (5, 3), (5, 5)], None, [(5, 1), (5, 3), (5, 5)], None, [(5, 1), (5, 3), (5, 5)], None], [[(6, 0), (6, 3), (6, 6)], None, None, [(6, 0), (6, 3), (6, 6)], None, None, [(6, 0), (6, 3), (6, 6)]]]
        
        self.vertical_morris_lookup = [[[(0, 0), (3, 0), (6, 0)], None, None, [(0, 3), (1, 3), (2, 3)], None, None, [(0, 6), (3, 6), (6, 6)]], [None, [(1, 1), (3, 1), (5, 1)], None, [(0, 3), (1, 3), (2, 3)], None, [(1, 5), (3, 5), (5, 5)], None], [None, None, [(2, 2), (3, 2), (4, 2)], [(0, 3), (1, 3), (2, 3)], [(2, 4), (3, 4), (4, 4)], None, None], [[(0, 0), (3, 0), (6, 0)], [(1, 1), (3, 1), (5, 1)], [(2, 2), (3, 2), (4, 2)], None, [(2, 4), (3, 4), (4, 4)], [(1, 5), (3, 5), (5, 5)], [(0, 6), (3, 6), (6, 6)]], [None, None, [(2, 2), (3, 2), (4, 2)], [(4, 3), (5, 3), (6, 3)], [(2, 4), (3, 4), (4, 4)], None, None], [None, [(1, 1), (3, 1), (5, 1)], None, [(4, 3), (5, 3), (6, 3)], None, [(1, 5), (3, 5), (5, 5)], None], [[(0, 0), (3, 0), (6, 0)], None, None, [(4, 3), (5, 3), (6, 3)], None, None, [(0, 6), (3, 6), (6, 6)]]]

    def removable_pieces(self, agent):
        removable = []
        all_ = []
        
        #mills = sum(self.formed_mills(agent), start=[])
        mills = []
        for (e1,e2,e3) in self.formed_mills(agent):
            mills.append(e1)
            mills.append(e2)
            mills.append(e3)
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == agent.id:
                    all_.append((i,j))
                    if (i,j) not in mills:
                        removable.append((i,j))
        
        if removable:
            return removable
        
        return all_
    
    def get_possible_moves(self, agent):
        positions = self.get_own_positions(agent)
        result = []
        
        if agent.on_board == 3:
            #fly
            free_spaces = self.free_spaces()
            
            result = [(from_i, from_j, to_i, to_j) for from_i, from_j in positions for to_i, to_j in free_spaces]
        else:
            #normal move
            spatial_moves = self._spatial_moves()

            for pos in positions:
                i, j = pos
                for possible_move_to_location in spatial_moves[i][j]:
                    possible_move_to_location_i, possible_move_to_location_j = possible_move_to_location
                    if self.board[possible_move_to_location_i][possible_move_to_location_j] == 0:
                        result.append((i,j,possible_move_to_location_i,possible_move_to_location_j))
        return result
    
    def get_own_positions(self, agent):
        result = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == agent.id:
                    result.append((i,j))
        return result
        
    def free_spaces(self):
        result = []
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == 0:
                    result.append((i,j))
        return result

    def _spatial_moves(self):
        moves = [[None for _ in range(7)] for _ in range(7)]
        
        moves[0][0] = [(0, 3), (3, 0)]
        moves[0][3] = [(0, 0), (1, 3), (0, 6)]
        moves[0][6] = [(0, 3), (3, 6)]
        moves[1][1] = [(3, 1), (1, 3)]
        moves[1][3] = [(1, 1), (0, 3), (2, 3), (1, 5)]
        moves[1][5] = [(1, 3), (3, 5)]
        moves[2][2] = [(3, 2), (2, 3)]
        moves[2][3] = [(2, 2), (1, 3), (2, 4)]
        moves[2][4] = [(2, 3), (3, 4)]
        moves[3][0] = [(0, 0), (6, 0), (3, 1)]
        moves[3][1] = [(3, 0), (1, 1), (3, 2), (5, 1)]
        moves[3][2] = [(3, 1), (2, 2), (4, 2)]
        moves[3][4] = [(2, 4), (3, 5), (4, 4)]
        moves[3][5] = [(3, 4), (1, 5), (5, 5), (3, 6)]
        moves[3][6] = [(3, 5), (0, 6), (6, 6)]
        moves[4][2] = [(3, 2), (4, 3)]
        moves[4][3] = [(4, 2), (5, 3), (4, 4)]
        moves[4][4] = [(4, 3), (3, 4)]
        moves[5][1] = [(3, 1), (5, 3)]
        moves[5][3] = [(5, 1), (4, 3), (5, 5), (6, 3)]
        moves[5][5] = [(5, 3), (3, 5)]
        moves[6][0] = [(3, 0), (6, 3)]
        moves[6][3] = [(6, 0), (5, 3), (6, 6)]
        moves[6][6] = [(6, 3), (3, 6)]

        return moves
    
    def formed_mills(self, agent):
        mills = []

        to_check = [
                        [(0,0), (0,3), (0,6)],
                        [(1,1), (1,3), (1,5)],
                        [(2,2), (2,3), (2,4)],
             [(3,0), (3,1), (3,2)], [(3,4), (3,5), (3,6)],
                        [(4,2), (4,3), (4,4)],
                        [(5,1), (5,3), (5,5)],
                        [(6,0), (6,3), (6,6)],
        ]

        for candidate in to_check:
            (i1, j1), (i2, j2), (i3, j3) = candidate[0], candidate[1], candidate[2]
            if self.board[i1][j1] == self.board[i2][j2] == self.board[i3][j3] == agent.id:
                mills.append(candidate)
            if self.board[j1][i1] == self.board[j2][i2] == self.board[j3][i3] == agent.id:
                mills.append([(j, i) for (i,j) in candidate])
        
        return mills  
    
    def is_position_valid(self, position):
        pi, pj = position
        return pi <= 6 and pj <= 6 and pi >= 0 and pj >= 0 and not (self.board[pi][pj] is None)
    
    def place_piece(self, position, agent):
        
        pi, pj = position

        if not self.is_position_valid(position):
            return False

        if self.board[pi][pj] != 0:
            return False

        self.board[pi][pj] = agent.id
        agent.on_board += 1
        agent.held -= 1

        return True
    
    def move_piece(self, position, destination, agent):

        pi, pj = position
        di, dj = destination

        if not self.is_position_valid(position) or not self.is_position_valid(destination):
            return False

        if self.board[pi][pj] != agent.id or self.board[di][dj] != 0:
            return False

        if destination not in self.spatial_moves[pi][pj] and not agent.fly_mode:
            return False
        
        self.board[pi][pj] = 0
        self.board[di][dj] = agent.id
        self.turns_without_mill += 1
        return True

    def remove_piece(self, position, agent):
        pi, pj = position

        if not self.is_position_valid(position):
            return False

        if position not in self.removable_pieces(agent):
            return False
        

        self.board[pi][pj] = 0
        agent.on_board -= 1
        self.turns_without_mill = 0
        return True
    
    def check_mode(self, agent1, agent2):
        if agent1.held == 0:
            agent1.place_mode = False
            agent1.move_mode = True
        
        if agent2.held == 0:
            agent2.place_mode = False
            agent2.move_mode = True
        
        if not agent1.place_mode and agent1.on_board == 3:
            agent1.fly_mode = True
            agent1.move_mode = False
        
        if not agent2.place_mode and agent2.on_board == 3:
            agent2.fly_mode = True
            agent2.move_mode = False
    
    def check_end_game(self, agent):

        if agent.place_mode:
            return False
        
        if agent.on_board < 3:
            return True
        
        if agent.fly_mode:
            return False
        
        for i in range(7):
            for j in range(7):
                if self.board[i][j] == agent.id:
                    for mi, mj in self.spatial_moves[i][j]:
                        if self.board[mi][mj] == 0:
                            return False if self.turns_without_mill < 30 else "draw"
        

        return True
    
    def clone_game(self):
        clone = NineMensMorris()
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                clone.board[row][column] = self.board[row][column]
        clone.turns_without_mill = self.turns_without_mill
        #assuming spatial_moves do not change, they will not be cloned
        return clone

    def amount_morrises_number(self, agent):
        #is calculated for the defined player
        mills = 0

        to_check = [
                        [(0,0), (0,3), (0,6)],
                        [(1,1), (1,3), (1,5)],
                        [(2,2), (2,3), (2,4)],
             [(3,0), (3,1), (3,2)], [(3,4), (3,5), (3,6)],
                        [(4,2), (4,3), (4,4)],
                        [(5,1), (5,3), (5,5)],
                        [(6,0), (6,3), (6,6)],
        ]

        for candidate in to_check:
            (i1, j1), (i2, j2), (i3, j3) = candidate[0], candidate[1], candidate[2]
            if self.board[i1][j1] == self.board[i2][j2] == self.board[i3][j3] == agent.id:
                mills = mills + 1
            if self.board[j1][i1] == self.board[j2][i2] == self.board[j3][i3] == agent.id:
                mills = mills+1
        
        return mills
    
    def amount_number_of_blocked_opp_pieces(self, agent_enemy):
        #out of the sight of agent
        enemies_positions = self.get_own_positions(agent_enemy)
        blocked = len(enemies_positions)
        for position in enemies_positions:
            i,j = position
            for connection in self.spatial_moves[i][j]:
                x,y = connection
                if self.board[x][y] == 0:
                    blocked = blocked - 1
                    break
        
        return blocked
    
    def amount_pieces_number(self,agent):
        return agent.on_board
        
    def amount_number_of_2_pieces(self, agent):
        to_check = [
                        [(0,0), (0,3), (0,6)],
                        [(1,1), (1,3), (1,5)],
                        [(2,2), (2,3), (2,4)],
             [(3,0), (3,1), (3,2)], [(3,4), (3,5), (3,6)],
                        [(4,2), (4,3), (4,4)],
                        [(5,1), (5,3), (5,5)],
                        [(6,0), (6,3), (6,6)],
        ]
        
        number = 0
        
        for candidate in to_check:
            agents = 0
            free = 0
            for (i, j) in candidate:
                if self.board[i][j] == agent.id:
                    agents = agents+1
                elif self.board[i][j] == 0:
                    free = free + 1
            if agents == 2 and free == 1:
                number = number+1
                
            agents = 0
            free = 0
            for (j, i) in candidate:
                if self.board[i][j] == agent.id:
                    agents = agents+1
                elif self.board[i][j] == 0:
                    free = free + 1
            if agents == 2 and free == 1:
                number = number+1
        
        return number
        
    def amount_number_of_3_pieces(self, agent):
        number = 0

        for [(a1,a2),(a3,a4),(a5,a6),(a7,a8),(a9,a10)] in self.to_check_3_pieces:
            if self.board[a1][a2] == agent.id and ((self.board[a3][a4] == agent.id and self.board[a5][a6] == 0) or (self.board[a3][a4] == 0 and self.board[a5][a6] == agent.id)) and ((self.board[a7][a8] == agent.id and self.board[a9][a10] == 0) or (self.board[a7][a8] == 0 and self.board[a9][a10] == agent.id)):
                number = number+1
                
        return number
        
    def amount_opened_morris(self, agent):
        number = 0

        for candidate in self.horizontal_morrises:
            agents = 0
            free = 0
            agent_next_to_free_spot = False
            for (i, j) in candidate:
                if self.board[i][j] == agent.id:
                    agents = agents+1
                elif self.board[i][j] == 0:
                    free = free + 1
                    for (x,y) in self.vertical_moves[i][j]:
                        if self.board[x][y] == agent.id:
                            agent_next_to_free_spot = True
                            break
            if agents == 2 and free == 1 and agent_next_to_free_spot:
                number = number+1
        
        for candidate in self.vertical_morrises:
            agents = 0
            free = 0
            agent_next_to_free_spot = False
            for (i, j) in candidate:
                if self.board[i][j] == agent.id:
                    agents = agents+1
                elif self.board[i][j] == 0:
                    free = free + 1
                    for (x,y) in self.horizontal_moves[i][j]:
                        if self.board[x][y] == agent.id:
                            agent_next_to_free_spot = True
                            break
            if agents == 2 and free == 1 and agent_next_to_free_spot:
                number = number+1
        
        return number
      
    def amount_double_morris(self, agent):
        number = 0

        for candidate in self.horizontal_morrises:
            agents = 0
            free = 0
            horizontal_morris_next_to_free_spot = False
            for (i, j) in candidate:
                if self.board[i][j] == agent.id:
                    agents = agents+1
                elif self.board[i][j] == 0:
                    free = free + 1
                    for (x,y) in self.vertical_moves[i][j]:
                        if self.board[x][y] == agent.id:
                            isMorris = True
                            for (l1,l2) in self.horizontal_morris_lookup[x][y]:
                                if self.board[l1][l2] != agent.id:
                                    isMorris = False
                            if isMorris:
                                horizontal_morris_next_to_free_spot = True
                                break
            if agents == 2 and free == 1 and horizontal_morris_next_to_free_spot:
                number = number+1
        
        for candidate in self.vertical_morrises:
            agents = 0
            free = 0
            vertical_morris_next_to_free_spot = False
            for (i, j) in candidate:
                if self.board[i][j] == agent.id:
                    agents = agents+1
                elif self.board[i][j] == 0:
                    free = free + 1
                    for (x,y) in self.horizontal_moves[i][j]:
                        if self.board[x][y] == agent.id:
                            isMorris = True
                            for (l1,l2) in self.vertical_morris_lookup[x][y]:
                                if self.board[l1][l2] != agent.id:
                                    isMorris = False
                            if isMorris:
                                vertical_morris_next_to_free_spot = True
                                break
            if agents == 2 and free == 1 and vertical_morris_next_to_free_spot:
                number = number+1
        
        return number
        
    def amount_winning_configuration(self, enemy_agent):
        return 1 if self.check_end_game(enemy_agent) else 0
        
    def get_game_phase(self, agent):
        if not agent.place_mode and agent.on_board == 3:
            return 3
        elif agent.held == 0:
            return 2
        return 1
        
    def calculate_reward(self, agent_self, phase_self, agent_enemy, phase_enemy):
        score_self = 0
        score_enemy = 0
        
        if phase_self == 1:
            score_self = self.evaluation_coefficients[1]*self.amount_morrises_number(agent_self)+self.evaluation_coefficients[2]*self.amount_number_of_blocked_opp_pieces(agent_enemy)+self.evaluation_coefficients[3]*self.amount_pieces_number(agent_self)+self.evaluation_coefficients[4]*self.amount_number_of_2_pieces(agent_self)+self.evaluation_coefficients[5]*self.amount_number_of_3_pieces(agent_self)
        elif phase_self == 2:
            score_self = self.evaluation_coefficients[7]*self.amount_morrises_number(agent_self)+self.evaluation_coefficients[8]*self.amount_number_of_blocked_opp_pieces(agent_enemy)+self.evaluation_coefficients[9]*self.amount_pieces_number(agent_self)+self.evaluation_coefficients[10]*self.amount_opened_morris(agent_self)+self.evaluation_coefficients[11]*self.amount_double_morris(agent_self)+self.evaluation_coefficients[12]*self.amount_winning_configuration(agent_self)
        else:
            score_self = self.evaluation_coefficients[13]*self.amount_number_of_2_pieces(agent_self)+self.evaluation_coefficients[14]*self.amount_number_of_3_pieces(agent_self)+self.evaluation_coefficients[16]*self.amount_winning_configuration(agent_self)
        
        if phase_enemy == 1:
            score_enemy = self.evaluation_coefficients[1]*self.amount_morrises_number(agent_enemy)+self.evaluation_coefficients[2]*self.amount_number_of_blocked_opp_pieces(agent_self)+self.evaluation_coefficients[3]*self.amount_pieces_number(agent_enemy)+self.evaluation_coefficients[4]*self.amount_number_of_2_pieces(agent_enemy)+self.evaluation_coefficients[5]*self.amount_number_of_3_pieces(agent_enemy)
        elif phase_enemy == 2:
            score_enemy = self.evaluation_coefficients[7]*self.amount_morrises_number(agent_enemy)+self.evaluation_coefficients[8]*self.amount_number_of_blocked_opp_pieces(agent_self)+self.evaluation_coefficients[9]*self.amount_pieces_number(agent_enemy)+self.evaluation_coefficients[10]*self.amount_opened_morris(agent_enemy)+self.evaluation_coefficients[11]*self.amount_double_morris(agent_enemy)+self.evaluation_coefficients[12]*self.amount_winning_configuration(agent_enemy)
        else:
            score_enemy = self.evaluation_coefficients[13]*self.amount_number_of_2_pieces(agent_enemy)+self.evaluation_coefficients[14]*self.amount_number_of_3_pieces(agent_enemy)+self.evaluation_coefficients[16]*self.amount_winning_configuration(agent_enemy)
        
        return score_self-score_enemy
        

"""
states:
board config + mode

actions:
place/move/fly
    only
    with capture if mills created

"""