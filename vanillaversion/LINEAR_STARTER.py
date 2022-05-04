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
    exploration_weight_list = [0.9,1,1.1]
    prob_educatedFirst_list = [0,0.2, 0.5]
    prob_educatedSecond_list = [0,0.1]
    rollouts_list = [500,1000,2000]
    #rollouts_list = [2,3,4]

    listofconfs = []

    for e in exploration_weight_list:
        for p1 in prob_educatedFirst_list:
            for p2 in prob_educatedSecond_list:
                for r in rollouts_list:
                    listofconfs.append((e,p1,p2,r))
                
    end = int(len(listofconfs)/threads*(partindex+1))
    i = int(len(listofconfs)/threads*partindex)
                    
    currentchefindex = i
    chef = ComputerPlayer(exploration_weight=listofconfs[i][0], prob_educatedFirst=listofconfs[i][1], prob_educatedSecond=listofconfs[i][2], rollouts=listofconfs[i][3], showThinking=True)
    with open(winnerfile, 'a', encoding="utf-8") as f:
        f.write('START CONF   : '+chef.get_details()+'\n')

    i = i+1
    
                
    for index in range(i,end+1):
        print('start '+str(i-1)+' current '+str(index)+' end '+str(end))
        chefwins =0
        oppwins =0
        for _ in range(amount_matches):
            a = MainGame(headlessMode)
            chef = ComputerPlayer(exploration_weight=listofconfs[currentchefindex][0], prob_educatedFirst=listofconfs[currentchefindex][1], prob_educatedSecond=listofconfs[currentchefindex][2], rollouts=listofconfs[currentchefindex][3], showThinking=False)
            opp = ComputerPlayer(exploration_weight=listofconfs[index][0], prob_educatedFirst=listofconfs[index][1], prob_educatedSecond=listofconfs[index][2], rollouts=listofconfs[index][3], showThinking=False)
            winner = a.play(chef, opp)
            
            if winner==1:
                chefwins=chefwins+1
            elif winner==2:
                oppwins=oppwins+1
            
            
            a = MainGame(headlessMode)
            chef = ComputerPlayer(exploration_weight=listofconfs[currentchefindex][0], prob_educatedFirst=listofconfs[currentchefindex][1], prob_educatedSecond=listofconfs[currentchefindex][2], rollouts=listofconfs[currentchefindex][3], showThinking=False)
            opp = ComputerPlayer(exploration_weight=listofconfs[index][0], prob_educatedFirst=listofconfs[index][1], prob_educatedSecond=listofconfs[index][2], rollouts=listofconfs[index][3], showThinking=False)
            winner = a.play(opp,chef)
            
            if winner==2:
                chefwins=chefwins+1
            elif winner==1:
                oppwins=oppwins+1
            
        if oppwins >= chefwins:
            currentchefindex=index
            if not winnerfile == None:
                with open(winnerfile, 'a', encoding="utf-8") as f:
                    f.write('NEW BEST     : '+opp.get_details()+' won '+str(oppwins)+' to '+str(chefwins)+'\n')
        else:
            if not winnerfile == None:
                with open(winnerfile, 'a', encoding="utf-8") as f:
                    f.write('--WON AGAINST: '+opp.get_details()+' won '+str(chefwins)+' to '+str(oppwins)+'\n')
        
