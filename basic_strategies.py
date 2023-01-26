from numpy.random import random

class Player:
    def __init__(self, k, t):
        self.k = k
        self.t = t
    
    def play(self, hist):
        t=random()
        if t < self.t: #
            return hist[-1]
        elif t < -self.t:
            return not hist[-1]
        
        return random() < self.k
    
    def __str__(self):
        return str(self.k) + str(self.t)
    
    def __repr__(self):
        return "Player(" + str(self.k) + ", " + str(self.t) + ")"

# so for example we can have

nice_guy = Player(1,0)  # always cooperates
bad_guy = Player(0,0)   # never cooperates
avg_guy = Player(0.5,0) # cooperates half the time
mn_guy = Player(0.75,0) # mostly cooperates
mb_guy = Player(0.25,0) # rarely cooperates
tt_guy = Player(0,1)   # reacts with last opponent move


# basic mechanics for 1-on-1 game
def game(pl1, pl2, it, payoff=(3, 2, 1, 0)):
    hist1 = [True] # only for the correct initialization of tt_guy
    hist2 = [True] # same
    points = [0, 0]
    
    for i in range(it):
        res1=pl1.play(hist2)
        res2=pl2.play(hist1)
        hist1.append(res1)
        hist2.append(res2)
        if hist1[-1] and hist2[-1]:
            points[0] += payoff[1]
            points[1] += payoff[1]
        elif hist1[-1] and not hist2[-1]:
            points[1] += payoff[0]
            points[0] += payoff[3]
        elif not hist1[-1] and hist2[-1]:
            points[1] += payoff[3]
            points[0] += payoff[0]
        elif not hist1[-1] and not hist2[-1]:
            points[0] += payoff[2]
            points[1] += payoff[2]
 
    return points
