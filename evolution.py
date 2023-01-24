 
def select(pl, scores): ## assumes a player array and a scores array with the same length
    newpl=[]
    sc_by_type={}
    
    for i in range(len(pl)):
        if pl[i].k in sc_by_type:
            sc_by_type[pl[i].k].append(scores[i])
        else:
            sc_by_type[pl[i].k]=[scores[i]]
    
    for k,v in sc_by_type:
        sc_by_type[k]=sum(v)/len(v)
    
    tot=sum(sc_by_type.values())
    
    for k, v in sc_by_type:
        for i in range((v*len(pl))//tot):
            newpl.append(Player(k))
    
    while len(newpl)<len(pl):
        newpl.append(Player(0.5))
        print("ADDED BALANCED PLAYER")
    
