from basic_strategies import game

def round_robin(pl,it):
    results = []
    N = len(pl)
    
    scores=[0 for i in range(N)]
    
    for i in range(N):
        for j in range(i+1, N):
            res=game(pl[i],pl[j],it)
            scores[i] += res[0]
            scores[j] += res[1]
            
    return scores 
