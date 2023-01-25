from basic_strategies import Player

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
        v=sc_by_type[k]
        for i in range(int((v * len(pl)) / tot)): # determine new players' classes depending on class score
            newpl.append(Player(k))
    
    while len(newpl) < len(pl):
        newpl.append(Player(0.5))
        #print("ADDED BALANCED PLAYER")
    
    return newpl
