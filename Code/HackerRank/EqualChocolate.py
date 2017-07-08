import sys

class EqualChocolate:
    def __init__(self):
        self.initial = [1,5,5]
    
    def returnCount(self,m):
        count = 0
        m = max(0,m)
        for i in range(len(self.initial)):
            count += (self.initial[i]-m)/5 + (self.initial[i]-m)%5/2 + (self.initial[i]-m)%5%2
            
        return count

if __name__=="__main__":
    t = int(input())
    for i in range(t):
        n = int(input())
        l = list(map(int,input().split(' ')))
        obj = EqualChocolate()
        obj.initial = l
        m = min(obj.initial)
        print(int(min(obj.returnCount(m),obj.returnCount(m-1),obj.returnCount(m-2))))