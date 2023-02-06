from basic_strategies import game
from multiprocessing import Pool        

def round_robin(pl,it):
    N = len(pl)
    results = [[None for i in range(N)] for j in range(N)]
    
    scores=[0 for i in range(N)]
    with Pool() as pool:
        for i in range(N):
            for j in range(i+1, N):
                res=pool.apply_async(game, (pl[i], pl[j],it))
                results[i][j]=res
        
        for i in range(N):
            for j in range(i+1, N):
                res=results[i][j].get()
                scores[i] += res[0]
                scores[j] += res[1]
    
    return scores 
