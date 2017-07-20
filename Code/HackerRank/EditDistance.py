class EditDistance:
    def __init__(self):
        self.str1=""
        self.str2=""
    
    def findEditDistance(self):
        m = len(self.str1)
        n = len(self.str2)
        opt = [[0 for i in range(n+1)] for j in range(m+1)]
        for i in range(m+1):
            for j in range(n+1):
                if i==0:
                    opt[i][j] = j
                if j==0:
                    opt[i][j] = i
                elif self.str1[i-1] == self.str2[j-1]:
                    opt[i][j] = opt[i-1][j-1]
                else:
                    opt[i][j] = 1 + min(opt[i-1][j],opt[i][j-1],opt[i-1][j-1])
                    
        return opt[m][n]
    
if __name__=="__main__":
    obj = EditDistance()
    obj.str1 = "Sunday"
    obj.str2 = "Saturday"
    print(obj.findEditDistance())