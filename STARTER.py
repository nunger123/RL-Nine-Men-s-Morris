from gui import *

#player2 = HumanPlayer()

headlessMode = True
winnerfile = "results.txt" #if None then not being outputted
amount_matches = 3
exploration_weight_list = [(1,1)]
prob_educatedFirst_list = [(0,0.3)]
prob_educatedSecond_list = [(0,0.1)]
rollouts_list = [(10,10)]


for e in exploration_weight_list:
    for p1 in prob_educatedFirst_list:
        for p2 in prob_educatedSecond_list:
            for r in rollouts_list:
                for _ in range(amount_matches):
                    a = MainGame(headlessMode)
                    player1 = ComputerPlayer(exploration_weight=e[0], prob_educatedFirst=p1[0], prob_educatedSecond=p2[0], rollouts=r[0], showThinking=True)
                    player2 = ComputerPlayer(exploration_weight=e[1], prob_educatedFirst=p1[1], prob_educatedSecond=p2[1], rollouts=r[1], showThinking=True)
                    winner = a.play(player1, player2)



                    if not winnerfile == None:
                        with open(winnerfile, 'a') as f:
                            f.write(player1.get_details()+';')
                            f.write(player2.get_details()+';')
                            f.write(str(winner)+'\n')


                    a = MainGame(headlessMode)
                    player2 = ComputerPlayer(exploration_weight=e[0], prob_educatedFirst=p1[0], prob_educatedSecond=p2[0], rollouts=r[0], showThinking=True)
                    player1 = ComputerPlayer(exploration_weight=e[1], prob_educatedFirst=p1[1], prob_educatedSecond=p2[1], rollouts=r[1], showThinking=True)
                    winner = a.play(player1, player2)



                    if not winnerfile == None:
                        with open(winnerfile, 'a') as f:
                            f.write(player2.get_details()+';')
                            f.write(player1.get_details()+';')
                            if winner == 1:
                                winner = 2
                            elif winner == 2:
                                winner = 1
                            f.write(str(winner)+'\n')




