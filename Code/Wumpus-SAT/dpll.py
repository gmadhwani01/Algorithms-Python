import glob
import random
import math
import operator
import pickle
import time

class Solver:
    def __init__(self, cnf):
        self.clause = cnf
        self.clause_history=[]
        self.literals_history=[]

    def solve(self):
        self.clause_history=[]
        self.literals_history=[]
        return self.dpll(self.clause)
    
    def get_symbol_count(self, list_set):
        abs_symbols = {}
        ori_symbols = {}
        for i in list_set:
            for j in i:
                abs_value = abs(j)
                # get the absolute value list. ie actual symbols
                if(abs_value in abs_symbols):
                    value = abs_symbols[abs_value] + 1
                    abs_symbols[abs_value] = value
                else:
                    abs_symbols[abs_value] = 1
                # get the original list, with actual sign of symbols
                if(j in ori_symbols):
                    val = ori_symbols[j] + 1
                    ori_symbols[j] = val
                else:
                    ori_symbols[j] = 1
        return abs_symbols, ori_symbols
    
    def dpll(self,clauses):
        if self.check_cnf_empty(clauses):
            return False
        elif len(clauses)==0:
            return True
        unit_clause=self.find_unit_clause(clauses)

        if unit_clause is not None and self.dpll(self.reduce(clauses,unit_clause,True)):
            return True
        pure_literal,value=self.find_pure_clause(clauses)
        if pure_literal is not None and not self.check_cnf_empty(clauses) and self.dpll(self.reduce(clauses,pure_literal,True)):
            return True
        abs_sym,ori_sym=self.get_symbol_count(clauses)
        new_literal=self.get_literal(clauses)
        try:
            new_literal = max(abs_sym.items(), key=operator.itemgetter(1))[0]
        except:
            pass
#        
        if (not self.check_cnf_empty(clauses)) and self.dpll(self.reduce(clauses,new_literal,True)):
            return True
        else:
            clauses=self.clause_history.pop()
            literal=self.literals_history.pop()
            return self.dpll(self.reduce(clauses, -literal,False))
    
    def take_backup(self,clauses,literals):
        self.clause_history.append(pickle.loads(pickle.dumps(clauses, -1)))
        self.literals_history.append(literals)
    
    def get_literal(self,clauses):
        for clause in clauses:
            if(len(clause)!=0):
                return list(clause)[0]  
        return None
    
    def check_cnf_empty(self,clauses):
        for clause in clauses:
            if(len(clause)==0):
                return True
        return False
        

    def reduce(self,clauses,literal, is_true):
        if is_true:
            self.take_backup(clauses, literal)
        i=0
        while (i < len(clauses)):
            for literals in clauses[i]:
                if(literals==literal):
                    clauses.remove(clauses[i])
                    i-=1
                    break
                elif literals==-literal:
                    clauses[i].remove(literals)
                    break
            i+=1
        return clauses   
    
    def find_unit_clause(self, l_clauses):
        for clause in l_clauses:
            if(len(clause) == 1):
                return list(clause)[0]
        return None
    
    def find_pure_clause(self, l_clauses):
        abs_symbols, ori_symbols = self.get_symbol_count(l_clauses)
        new_clauses = []
        for sym in abs_symbols:
            neg_sym = -sym
            abs_sym_count = abs_symbols[sym]
            pure_exists = False
            if(sym in ori_symbols):
                ori_sym_count = ori_symbols[sym]
                if(ori_sym_count == abs_sym_count):
                    return sym, True
                else:
                    return None,None
            elif(neg_sym in ori_symbols):
                neg_sym_count = ori_symbols[neg_sym]
                if(neg_sym_count == abs_sym_count):
                    return sym, False
                else:
                    return None,None
        return None,None
    
     
# print(unit_propagate_int_repr([[1, 2], [3, -2], [2]], 2))

def load(fn):
  f = open(fn, 'r')
  data = f.read()
  f.close()
  clauses = []
  lines = data.split("\n")
  for line in lines:
    if len(line) == 0 or line[0] in ['c', 'p', '%', '0']:
      continue
    clause = [int(x) for x in line.split()[0:-1]]
    clauses.append({x for x in clause})
  return clauses
