
class Sherlock_Cost:
    def __init__(self):
        self.b = []
    
    def findMaxSum(self):
        n = len(self.b)
        opt = [[0 for i in range(n)] for j in range(2)]
        for i in range(1,n):
            opt[0][i] = max(opt[0][i-1] + abs(self.b[i] - self.b[i-1]) , 
                            opt[1][i-1] + abs(self.b[i]-1))         # high to low sub
            opt[1][i] = max(opt[0][i-1] + abs(self.b[i-1] - 1) , opt[1][i-1])   #low to high
            
        return max(opt[0][n-1],opt[1][n-1])
        
    
if __name__ == "__main__":
    t = int(input())
    for i in range(t):
        n = int(input())
        l = list(map(int,input().split(' ')))
        obj = Sherlock_Cost()
        obj.b = l
        print(obj.findMaxSum())