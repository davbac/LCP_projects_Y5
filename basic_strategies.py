from random import random

class Player:
    def __init__(self, k):
        self.k = k
    
    def play(self, hist):
        return random() < self.k
 
class TftPlayer(Player):
    def play(self, hist):
        return hist[-1]
    
# so for example we can have
nice_guy = Player(1)  # always cooperates
bad_guy = Player(0)   # never cooperates
avg_guy = Player(0.5) # cooperates half the time
mn_guy = Player(0.75) # mostly cooperates
mb_guy = Player(0.25) # rarely cooperates
tt_guy = TftPlayer(-1) # reacts with last opponent move

# basic mechanics for 1-on-1 game
def game(pl1, pl2, it, payoff=(3, 2, 1, 0)):
    # initialize hists to true to correctly handle the first
    # iteration for a tit-for-tat player (needs to cooperate on
    # first move)
    hist1 = [True] * it
    hist2 = [True] * it
    points = [0, 0]
    
    for i in range(it):
        res1 = pl1.play(hist2)
        res2 = pl2.play(hist1)
        hist1[i] = res1
        hist2[i] = res2
        if res1 and res2:
            points[0] += payoff[1]
            points[1] += payoff[1]
        elif res1 and not res2:
            points[1] += payoff[0]
            points[0] += payoff[3]
        elif not res1 and res2:
            points[1] += payoff[3]
            points[0] += payoff[0]
        else:
            points[0] += payoff[2]
            points[1] += payoff[2]
 
    return points