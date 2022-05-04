from gui import *
import sys

if (len(sys.argv)!=3):
	print("You can call this program with optional height and width: 'python run.py <partindex> <threads>'")
else:
    partindex = int(sys.argv[1])
    threads = int(sys.argv[2])


    #player2 = HumanPlayer()

    headlessMode = True
    winnerfile = "results"+str(partindex)+"outof"+str(threads)+".txt" #if None then not being outputted
    amount_matches = 4

    listofconfs = [(0.9,0,0,1000),
                    (0.9,0.5,0,500),
                    (0.9,0.5,0.1,2000),
                    (1,0,0.1,2000),
                    (1,0.2,0,2000),
                    (1,0.5,0,2000),
                    (1.1,0,0.1,2000),
                    (1.1,0.2,0,2000),
                    (1.1,0.5,0.1,2000)]
    
    
    i = partindex
    
    chef = ComputerPlayer(exploration_weight=listofconfs[i][0], prob_educatedFirst=listofconfs[i][1], prob_educatedSecond=listofconfs[i][2], rollouts=listofconfs[i][3], showThinking=True)
    with open(winnerfile, 'a', encoding="utf-8") as f:
        f.write('CONF OF      : '+chef.get_details()+'\n')
    
                
    for index in range(threads):
        if index == i:
            continue
            
        print('start '+str(index))
        chefwins =0
        oppwins =0
        for _ in range(amount_matches):
            a = MainGame(headlessMode)
            chef = ComputerPlayer(exploration_weight=listofconfs[i][0], prob_educatedFirst=listofconfs[i][1], prob_educatedSecond=listofconfs[i][2], rollouts=listofconfs[i][3], showThinking=False)
            opp = ComputerPlayer(exploration_weight=listofconfs[index][0], prob_educatedFirst=listofconfs[index][1], prob_educatedSecond=listofconfs[index][2], rollouts=listofconfs[index][3], showThinking=False)
            winner = a.play(chef, opp)
            
            if winner==1:
                chefwins=chefwins+1
            elif winner==2:
                oppwins=oppwins+1

        if not winnerfile == None:
            with open(winnerfile, 'a', encoding="utf-8") as f:
                f.write('AGAINST      : '+opp.get_details()+' won '+str(chefwins)+' lost '+str(oppwins)+' of '+str(amount_matches)+' matches\n')
        
