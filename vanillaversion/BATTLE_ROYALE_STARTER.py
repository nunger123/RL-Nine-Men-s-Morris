from gui import *

#player2 = HumanPlayer()

headlessMode = True
winnerfile = "results.txt" #if None then not being outputted
amount_matches = 4
exploration_weight_list = [0.9,1,1.1]
prob_educatedFirst_list = [0,0.2, 0.5]
prob_educatedSecond_list = [0,0.1]
rollouts_list = [500,1000,2000]


for p1_e in exploration_weight_list:
    for p1_p1 in prob_educatedFirst_list:
        for p1_p2 in prob_educatedSecond_list:
            for p1_r in rollouts_list:
                for p2_e in exploration_weight_list:
                    for p2_p1 in prob_educatedFirst_list:
                        for p2_p2 in prob_educatedSecond_list:
                            for p2_r in rollouts_list:
                                if p1_p1 < p1_p2 or p2_p1 < p2_p2 or (p1_p1 == p2_p1 and p1_p2 == p2_p2 and p1_e == p2_e and p1_r == p2_r):
                                    continue
                                    
                                for _ in range(amount_matches):
                                    a = MainGame(headlessMode)
                                    player1 = ComputerPlayer(exploration_weight=p1_e, prob_educatedFirst=p1_p1, prob_educatedSecond=p1_p2, rollouts=p1_r, showThinking=True)
                                    player2 = ComputerPlayer(exploration_weight=p2_e, prob_educatedFirst=p2_p1, prob_educatedSecond=p2_p2, rollouts=p2_r, showThinking=True)
                                    winner = a.play(player1, player2)

                                    if not winnerfile == None:
                                        with open(winnerfile, 'a') as f:
                                            f.write(player1.get_details()+';')
                                            f.write(player2.get_details()+';')
                                            f.write(str(winner)+'\n')
