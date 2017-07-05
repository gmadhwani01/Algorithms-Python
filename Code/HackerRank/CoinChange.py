#!/bin/python3

import sys

class CoinChange:
    def __init__(self,n,m,c):
        self.n = n
        self.m = m
        self.c = c
        self.opt = [[0 for i in range(n+1)] for j in range(m+1)]
        for i in range(m+1):
            self.opt[i][0] = 1
        
    def calculateWays(self):
        if(self.n<0):
            return 0
        if(self.m==0):
            return 0
        for i in range(1,self.m+1):
            for j in range(1,self.n+1):
                if self.c[i-1]>j:
                    self.opt[i][j] = self.opt[i-1][j]
                else:
                    self.opt[i][j] = self.opt[i-1][j] + self.opt[i][j-self.c[i-1]]
                
        return(self.opt[self.m][self.n])

c = CoinChange(85,25,list(map(int,("50 10 17 21 8 3 12 41 9 13 43 37 49 19 23 28 45 46 29 16 34 25 2 22 1").split(' '))))
print(c.calculateWays())