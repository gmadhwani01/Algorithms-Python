from copy import deepcopy
import time
class Solver:
    def __init__(self, cnf):
#         self.cnf = cnf
        self.cnf = cnf
        self.literal = 0
        self.track_cnfs = []
        self.track_literals = []
    
    def solve(self):
#         print (self.cnf)
        retVal = self.dpll(self.cnf)
        self.track_cnfs = []
#         print ("retVal->",retVal)
        return retVal
        
    def dpll(self, cnf):
#         print ("DPLL-> ",cnf)
        if self.is_cnf_empty(cnf):
#             print ("Return False")
            return False
        elif len(cnf) == 0:
#             print ("Return True")
            return True
        else:            
            p = self.find_unit_literal(cnf)
#             print ("Unit literal p->",p)
#             print ("is cnf empty-> ",self.is_cnf_empty(cnf))
            if p is not None and self.dpll(self.reduce_True(cnf, p,True)):                
                return True        
            p = self.find_pure_literal(cnf)
#             print ("Pure literal p->",p)
#             print ("is cnf empty-> ",self.is_cnf_empty(cnf))
            if p is not None and not self.is_cnf_empty(cnf) and self.dpll(self.reduce_True(cnf, p, True)):                
                return True
            p = self.get_literal(cnf)
#             print ("CNF after pure and unit-> ",cnf)
#             print ("p set to True ->",p)
#             print ("is cnf empty-> ",self.is_cnf_empty(cnf))
            if (not self.is_cnf_empty(cnf)) and self.dpll(self.reduce_True(cnf, p,True)):                
                return True
            else:  
                cnf = self.pop_cnf()
                p = self.pop_literal()
#                 print ("CNF found an empty set ,cnf-> ",cnf)
#                 print ("p set to False -> ",p)
                return self.dpll(self.reduce_True(cnf, -p,False))
    
    def reduce_True(self, cnf, p,is_true):
#         print ("Reducing taking %d true",p)
        if is_true:
            self.track_cnfs.append(deepcopy(cnf))
            self.track_literals.append(deepcopy(p)) # May be no need of deepcopy here
        i=0
        while(i<len(cnf)):
            for j in cnf[i]:                
                if j==p:
                    # since true found, remove the clause                    
                    cnf.remove(cnf[i])
                    i=i-1
                    break
                elif j==-p:
                    # since false found, remove only literal
                    cnf[i].remove(j)
                    # this break is because there will not be more than one 'p' literal in the SET/Clause. So I can safely put a break
                    break
            i=i+1
        return cnf
    
    def reduce_False(self, cnf, p):
#         print ("Reducing taking %d false",p)
        i=0
        while(i<len(cnf)):            
            for j in cnf[i]:
                if j==p:
                    # since false found remove only literal
                    cnf[i].remove(j)                    
                    break
                elif j==-p:
                    # since true found, remove clause
                    cnf.remove(cnf[i])
                    i=i-1                    
                    break
            i=i+1
        return cnf
          
    def get_literal(self, cnf):
        j=[None]        
        for i in range(0, len(cnf)):
            if cnf[i] != set():
                j = list(cnf[i])
                break
        return j[0]
    
    def is_cnf_empty(self, cnf):
        flag = False
        for i in range(0, len(cnf)):
            if cnf[i] == set():
                flag = True
                break
        return flag
    
    def pop_cnf(self):
        return self.track_cnfs.pop()
    
    def pop_literal(self):
        return self.track_literals.pop()
            
    def find_unit_literal(self, cnf):
        j=[None]
        for i in range(0, len(cnf)):
            if len(cnf[i]) == 1:
                j = list(cnf[i])
        return j[0]
    
    def find_pure_literal(self, cnf):
        flag = False
        elt=[None]
        for i in cnf:
            if(i == set()):
                continue           
            for j in i:
                flag = False
                elt[0]=j
                for k in cnf:                    
                    for f in k:                        
                        if f==j:                            
                            break
                        if f==-j:                            
                            flag = True
                            break
                    if flag:                        
                        elt=[None]
                        break
                if not flag:
                    break
            if not flag:
                    break

        return elt[0]
cnf = [{36, -3, 7}, {-48, -3, -42}, {-47, -41, -49}, {8, 17, -40}, {-31, -21, -39}, {49, -22, 36}, {27, 38, 14}, {6, -18, 15}, {-43, 6, 7}, {-7, 34, 23}, {2, -13, 14}, {2, -42, 47}, {3, -35, -33}, {40, 49, 44}, {50, 36, 31}, {-37, -36, -3}, {43, 26, -29}, {-45, 29, 15}, {24, 18, -11}, {-47, -26, 6}, {-10, -50, -33}, {32, 16, 6}, {41, 37, -34}, {-17, -28, 7}, {19, -44, 46}, {-48, 22, 7}, {34, 3, 39}, {-43, 46, 31}, {32, -27, 23}, {-18, 37, -50}, {11, 20, 5}, {-24, -45, 6}, {-23, -14, -34}, {-22, 20, 21}, {24, 50, -17}, {-24, -27, -25}, {35, 3, 21}, {-36, -26, 47}, {49, -45, -28}, {-6, -21, 12}, {-15, -39, -17}, {41, 2, -14}, {25, 36, -23}, {-40, -39, -3}, {50, 35, 20}, {-39, 27, 31}, {-40, -15, 45}, {34, 35, 50}, {-48, 12, -1}, {18, -35, -30}, {-24, 27, -25}, {-12, -4, -33}, {-24, -37, -43}, {-37, -44, 31}, {-38, 14, -9}, {-16, 33, 34}, {-5, 4, -35}, {-19, -21, -3}, {-29, -36, -35}, {36, -43, 7}, {41, 30, 14}, {-24, -7, -35}, {35, -42, 6}, {-15, -1, 39}, {-16, 49, 27}, {49, -37, -10}, {-46, 50, -3}, {34, 20, -41}, {28, -1, 23}, {-20, -30, -12}, {-24, -37, 29}, {-44, 12, 5}, {48, -6, -2}, {-43, -2, -49}, {24, 1, -50}, {-7, -44, -50}, {43, 4, -41}, {-11, 13, 15}, {-11, -3, 23}, {48, 33, 41}, {9, -49, 23}, {1, -43, 47}, {-40, 16, -29}, {3, 19, 30}, {48, 19, -34}, {-16, -44, 14}, {-45, -12, 38}, {-31, -14, -4}, {-48, 35, -1}, {19, -13, 45}, {9, 42, -7}, {8, -15, -1}, {-14, -13, -44}, {-31, -37, -43}, {-29, -27, 47}, {17, 4, 7}, {10, 35, 7}, {17, 20, -25}, {35, -42, -5}, {24, -5, -50}, {2, -21, -26}, {-8, -21, 45}, {-16, 33, 49}, {16, -38, 6}, {21, 37, 5}, {8, 38, 31}, {33, -21, 14}, {40, -5, 20}, {-29, 31, -9}, {-7, 42, -22}, {-48, 8, 26}, {48, 33, -38}, {46, 49, -34}, {-46, -14, 25}, {-46, 18, 4}, {-12, -31, 36}, {12, -18, 14}, {-16, -7, 46}, {-8, 9, 7}, {49, -22, -42}, {38, -15, 22}, {34, 47, -41}, {32, -26, 22}, {-45, -21, -25}, {32, -11, -26}, {26, -25, 15}, {46, 25, -1}, {-31, -14, 30}, {-22, 12, -9}, {26, -35, -18}, {-16, -21, -32}, {-49, -21, 31}, {9, 11, 41}, {19, -30, -13}, {4, -10, 6}, {-22, 3, -4}, {-18, -50, -25}, {-40, 9, 4}, {20, 37, 46}, {-29, -27, 22}, {34, 3, 14}, {-31, 3, 20}, {2, -26, -50}, {17, -29, 38}, {-41, 12, -49}, {-43, -35, 15}, {-23, -22, -49}, {48, 33, -9}, {26, 35, 29}, {27, 37, -50}, {-7, -43, 46}, {-8, -46, -37}, {-40, 36, -24}, {-44, 46, 15}, {-16, 36, -3}, {-48, 9, 43}, {-4, 44, -25}, {-7, -22, 37}, {-31, -22, -17}, {-48, 17, -11}, {34, -28, 23}, {-48, -39, 23}, {-23, -37, -1}, {27, -19, 14}, {33, -22, -6}, {-32, -6, -26}, {-46, 18, -20}, {27, 43, 22}, {49, 34, -13}, {-46, 3, -35}, {32, -43, 39}, {-39, 6, -9}, {-16, 27, 39}, {25, -15, -17}, {34, 27, -43}, {49, -6, 5}, {-38, 11, 14}, {40, -38, 47}, {17, -14, 37}, {36, 29, 39}, {-39, -28, 1}, {-16, -18, 14}, {-40, 50, 15}, {18, 37, -42}, {33, -13, 31}, {33, 2, -42}, {8, -22, -3}, {1, -31, 23}, {26, -45, -20}, {49, 42, 11}, {-43, 11, 29}, {-21, -20, 30}, {-35, 45, 23}, {-30, 38, -14}, {48, -29, -9}, {-23, 11, -18}, {-29, -1, -41}, {41, 26, 5}, {-7, -30, 44}, {-6, 38, -41}, {48, -15, 46}, {-47, -10, -18}, {46, -32, 38}, {-32, 12, 46}, {40, 14, 31}, {49, 2, -18}, {-38, 27, 28}, {-16, -21, 14}, {-29, 12, 15}, {49, 34, 5}, {-12, 14, 22}, {33, 20, 30}, {-24, 25, 22}, {-48, -23, 4}, {9, -30, -36}, {-35, 44, 12}, {3, 38, -21}, {33, -11, 49}]
start_time=time.time()
s = Solver(cnf)

print(s.solve())
print(time.time()-start_time)