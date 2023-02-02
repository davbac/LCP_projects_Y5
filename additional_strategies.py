from numpy import sum as np_sum
from numpy import random

class SusTFT:
    def __init__(self, *args):
        pass
    
    def init_values(self):
        return (None,)
    
    def play(self, hist):
        if len(hist) > 0:
            return hist[-1]
        else:
            return False

class Spiteful:
    def __init__(self, *args):
        pass
    
    def init_values(self):
        return (None,)
    
    def play(self, hist):
        if False in hist:
            return False
        else:
            return True

class Periodic:
    def __init__(self, *args): ## give any sequence of booleans
        self.seq = args
        self.cnt = -1
    
    def init_values(self):
        return self.seq
    
    def play(self, hist):
        self.cnt += 1
        if self.cnt >= len(self.seq):
            self.cnt = 0
        return self.seq[self.cnt]

class TF2T:
    def __init__(self, *args):
        pass
    
    def init_values(self):
        return (None,)
    
    def play(self, hist):
        if len(hist) > 1:
            return hist[-1] or hist[-2]
        else:
            return True

class Majority:
    def __init__(self, typ): ## True -> soft  ##  False -> hard
        self.typ=typ
    
    def init_values(self):
        return (self.typ,)
    
    def play(self, hist):
        if len(hist) > 0:
            if self.typ:
                return np_sum(hist) >= (len(hist) // 2)
            else:
                return not np_sum(hist) <= (len(hist) // 2)
        else:
            if self.typ:
                return True
            else:
                return False

class HTFT:
    def __init__(self, *args):
        pass
    
    def init_values(self):
        return (None,)
    
    def play(self, hist):
        res = True
        if len(hist) > 0:
            res = res and hist[-1]
        if len(hist) > 1:
            res = res and hist[-2]
        if len(hist) > 2:
            res = res and hist[-3]
        return res

class Responsive:
    def __init__(self,k, a):
        self.k = k
        self.a = a
    
    def init_values(self):
        return self.k, self.a
    
    def play(self, hist):
        return random.random() < self.k + self.a * ((np_sum(hist) / len(hist)) - 0.5)
