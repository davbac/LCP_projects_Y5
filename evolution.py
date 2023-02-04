from basic_strategies import Player, random
from numpy import std, mean, array, ones

def select(pl, scores, notquite=False): ## assumes a player array and a scores array with the same length
    newpl = []
    
    types = []
    sc_by_type = []
    num_by_type = []
    
    for p in pl:
        for t in types:
            if t[0] == p.__class__ and t[1] == p.init_values():
                break
        else:
            types.append((p.__class__, p.init_values()))
    
    for i in range(len(types)):
        sc_by_type.append([])
        for j in range(len(pl)):
            if types[i][0] == pl[j].__class__ and types[i][1] == pl[j].init_values():
                sc_by_type[i].append(scores[j])
        num_by_type.append(len(sc_by_type[i]))
        sc_by_type[i]=mean(sc_by_type[i])
        
    
    if notquite:
        return types, sc_by_type, num_by_type
    
    glob = sorted([(types[i], sc_by_type[i], num_by_type[i]) for i in range(len(types))], key=lambda i:i[1], reverse=True)
    
    types = [g[0] for g in glob]
    sc_by_type = [g[1] for g in glob]
    num_by_type = [g[2] for g in glob]
    
    totscore=sum(sc_by_type)
    N = len(pl)
    #print(types, '\n',  sc_by_type, '\n', num_by_type) 
    mu = sum(array(num_by_type)*array(sc_by_type))/N
    
    new_nums = array( num_by_type + array(num_by_type)*(sc_by_type-mu*ones(len(sc_by_type)))/mu ).astype(int)
    
    for i in range(len(types)):
        for j in range(new_nums[i]):
            newpl.append(types[i][0](*types[i][1]))
    while len(newpl) < len(pl):
        newpl.append(types[0][0](*types[0][1]))
    
    return newpl

def evolve(pl, scores, sigma_cutoff=-1):
    N = len(pl)
    tot = sum(scores)
    
    newpl, newscores = [], []
    
    m, s = mean(scores), std(scores)
    
    for i in range(N):
        if scores[i] > m + sigma_cutoff * s:
            newpl.append(pl[i])
            newscores.append(scores[i])
    
    frac = N // len(newscores)
    for i in range(frac-1):
        for j in range(len(newscores)):
            p=newpl[j]
            newpl.append(Player(p.k, p.t))
    
    best_pl=newpl[sorted([(newscores[i], i) for i in range(len(newscores))], key=lambda j:j[0], reverse=True)[0][1]]
    while len(newpl)<N:
        newpl.append(Player(best_pl.k, best_pl.t))
    
    for p in newpl:
        p.randomize()
        #p.k+=(2*random()-1)*0.05
        #p.t+=(2*random()-1)*0.05
        #p.check()
    
    return newpl
