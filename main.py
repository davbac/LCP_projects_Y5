from basic_strategies import *
from evolution import *
from multi_player import *
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import matplotlib as mpl
import numpy as np

def init(N):
    pl = []
    Nsq=int(N**0.5)
    for i in range(Nsq):
        for j in range(Nsq):
            pl.append(Player(i/Nsq, j*2/Nsq - 1))
    while len(pl) < N:
        pl.append(Player(0.5,0))
    return pl

def init_classed(N):
    pl=[]
    """for i in range(N//6):
        pl.append(Player(0,0))
        pl.append(Player(0.25,0))
        pl.append(Player(0.5,0))
        pl.append(Player(0.75,0))
        pl.append(Player(1,0))
        
        pl.append(Player(0.5,1))
        pl.append(Player(0.5,-1))
    
    while len(pl) < N:
        pl.append(Player(0.5,1))
    """
    for i in range(95):
        pl.append(Player(0.5,0))
    for i in range(5):
        pl.append(Player(0,1))
    return pl

def repeated(N, it, cyc, classed=False):
    if classed:
        pl=init_classed(N)
    else:
        pl = init(N)
    
    hist=[]
    scores = round_robin(pl, it)
    hist.append((pl, scores)) 
    
    for i in range(cyc-1):
        if classed:
            pl = select(pl, scores)
            #print("selecting")
        else:
            pl = evolve(pl, scores)
            #print("evolving")
        
        scores = round_robin(pl, it)
        
        hist.append((pl, scores))
        
        if np.allclose(scores, hist[i][1], atol=0.00001*max(scores)) :  #aggiunta da electro
            stop_counter += 1
        else:
            stop_counter = 0
        if stop_counter == 20:
            break
    
    #if classed:
        #pl=select(pl, scores)
    #else:
        #pl=evolve(pl, scores)
        
    #scores = round_robin(pl, it)
    
    return hist

def stats(hist):
    
    scores=[]
    counts=[]
    cl, sc, nums = select(hist[0][0], hist[0][1], True)
    names = [str(c) for c in cl]
    
    scores.append(sc)
    counts.append(nums)
    
    for i in range(1,len(hist)):
        cl, sc, nums = select(hist[i][0], hist[i][1], True)
        new_names = [str(c) for c in cl]
        
        sc_ord = []
        num_ord = []
    
        for j in range(len(names)):
            
            for k in range(len(new_names)):
                if new_names[k] == names[j]:
                        sc_ord.append(sc[k])
                        num_ord.append(nums[k])
                        break
            else:
                sc_ord.append(0)
                num_ord.append(0)
                
        scores.append(sc_ord)
        counts.append(num_ord)
    
    scores = np.array(scores).T
    counts = np.array(counts).T
   
    means = []
    dev = []
    
    
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(12,8))
    for j in range(len(names)):
        means.append( np.mean(scores[j][-20:]) )
        dev.append( np.std(scores[j][-20:]) )
        ax[0].plot(np.arange(0,len(hist)),scores[j], label=names[j])
        ax[1].plot(np.arange(0,len(hist)),counts[j], label=names[j])
        ax[0].legend()
        
        #print(cl[j][1],means[j],dev[j])
    
    plt.show()
    return cl, means, dev

def main(N=100, it=100, cyc=100, classed=False):
    hist = repeated(N, it, cyc, classed)
    if not classed:
        fig, ax = plt.subplots()
        ax.set_xlim(0,1)
        ax.set_ylim(-1, 1)
        ax.set_xlabel("k")
        ax.set_ylabel("t")
        
        col = 255 * (np.array(hist[0][1]) - min(hist[0][1])) / (max(hist[0][1]) - min(hist[0][1]))
        rgb = mpl.colormaps["coolwarm"](col)[np.newaxis, :, :3][0]
        
        lines=[]
        
        for j in range(len(hist[0][0])):
            k,t=hist[0][0][j].init_values()
            line, = ax.plot(k,t, c=rgb[j], marker=".", linewidth=0)
            lines.append(line)
        
        #print(lines)
        def animate(i):
            col = 255 * (np.array(hist[i][1]) - min(hist[i][1])) / (max(hist[i][1]) - min(hist[i][1]))
            rgb = mpl.colormaps["coolwarm"](col)[np.newaxis, :, :3][0]
            #print(hist[i][2], col, rgb)
            for j in range(len(lines)):
                lines[j].set_data(hist[i][0][j].init_values())
                lines[j].set_color(rgb[j])
            return lines
        ani = animation.FuncAnimation(fig, animate, interval=500, blit=True, frames=len(hist))
        plt.show()
    else:
        fig, ax = plt.subplots(1,2)
        cl, sc, nums = select(hist[0][0], hist[0][1], True)
        #col = 255 * (np.array(sc) - min(sc)) / (max(sc) - min(sc))
        col=[i for i in range(len(sc))]
        #rgb = mpl.colormaps["coolwarm"](col)[np.newaxis, :, :3][0]
        rgb = mpl.colormaps["tab20"](col)[np.newaxis, :, :3][0]
        names = [str(c) for c in cl]
        b = ax[0].bar(names, sc, color=rgb)
        b2 = ax[1].bar(names, nums, color=rgb)
        ax[0].set_xticks('')
        ax[1].set_xticks('')
        fig.legend(handles=b.get_children(), labels=names)
        #print(names)
        def animate(i):
            cl, sc, nums = select(hist[i][0], hist[i][1], True)
            new_names = [str(c) for c in cl]
            sc_ord = []
            num_ord = []
            for j in range(len(names)):
                for k in range(len(new_names)):
                    if new_names[k] == names[j]:
                        sc_ord.append(sc[k])
                        num_ord.append(nums[k])
                        break
                else:
                    sc_ord.append(0)
                    num_ord.append(0)
            
            for j in range(len(sc_ord)):
                b.get_children()[j].set_height(sc_ord[j])
                b2.get_children()[j].set_height(num_ord[j])
            #info=np.array(np.array(sc_ord)*N/sum(sc_ord)).astype(int)
            #print(num_ord, info)
            return *b.get_children(), *b2.get_children()
        
        ani = animation.FuncAnimation(fig, animate, interval=500, frames=len(hist))
        plt.show()
        stats(hist)

if __name__ == "__main__":
    main(classed=True)
    #main()
