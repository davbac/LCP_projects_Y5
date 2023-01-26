from basic_strategies import Player, random
from numpy import std, mean

def select(pl, scores, printing=False): ## assumes a player array and a scores array with the same length
    newpl = []
    sc_by_type = {}
    
    for i in range(len(pl)):
        if pl[i].k in sc_by_type: #get all scores for each class
            sc_by_type[pl[i].k].append(scores[i])
        else:
            sc_by_type[pl[i].k] = [scores[i]]
    
    for k in sc_by_type:
        v=sc_by_type[k]
        sc_by_type[k] = sum(v) / len(v) #average score for the class
    
    tot=sum(sc_by_type.values())
    
    if printing:
        print(sc_by_type)
    
    for k in sc_by_type:
        v = sc_by_type[k]
        for i in range(int((v * len(pl)) / tot)): # determine new players' classes depending on class score
            newpl.append(Player(k))
    
    while len(newpl) < len(pl):
        newpl.append(Player(0.5))
        #print("ADDED BALANCED PLAYER")
    
    return newpl

def evolve(pl, scores, sigma_cutoff=-1):
    N = len(pl)
    tot = sum(scores)
    
    newpl, newscores = [], []
    
    for i in range(N):
        if scores[i] > mean(scores) + sigma_cutoff * std(scores):
            newpl.append(pl[i])
            newscores.append(scores[i])
    
    frac = N // len(newscores)
    for i in range(frac-1):
        for j in range(len(newscores)):
            p=newpl[j]
            newpl.append(Player(p.k, p.t))
    
    best_pl=newpl[sorted([(newscores[i], i) for i in range(len(newscores))], key=lambda j:j[0])[0][1]]
    while len(newpl)<N:
        newpl.append(Player(best_pl.k, best_pl.t))
    
    k, t = [], []
    for p in newpl:
        p.k+=(2*random()-1)*0.05
        p.t+=(2*random()-1)*0.05
        p.check()
        k.append(p.k)
        t.append(p.t)
    
    return newpl, k, t    
