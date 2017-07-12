class Knapsack:
    def __init__(self):
        self.val = []
        self.w = []
        self.maxW = 0
        
    def returnKnapsackMax(self):
        opt = [[0 for i in range(self.maxW+1)]for j in range(len(self.val)+1)]
        for i in range(1,len(self.val)):
            for w in range(1,self.maxW):
                if(self.w[i]<=self.maxW):
                    opt[i][w] = max(opt[i-1][w] + self.val[i],opt[i-1][w])
                else:
                    opt[i][w] = opt[i-1][w]
                    
        return opt[i][self.maxW-1]
    
    
if __name__ == '__main__':
    obj = Knapsack()
    obj.val = [60,100,120]
    obj.w = [10,20,30]
    obj.maxW = 50 
    print(obj.returnKnapsackMax())
    
