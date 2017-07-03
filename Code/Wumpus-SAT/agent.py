import random
from enum import IntEnum
import dpll
import pickle
from dpll import Solver
from copy import deepcopy

class Map(IntEnum):
    b=0 #Breeze
    p=1 #Pit
    w=2 #wumpus
    s=3 #stench


class Agent:
    def __init__(self):
        self.rows=20
        self.cols=20
        self.b=[]   #array for breeze
        self.p=[]   #array for pit
        self.w=[]   #array for wumpus
        self.s=[]   #array for stench
        self.world=[self.b,self.p,self.w,self.s]
        self.kb=[]     #knowledge base
        self.wumpus_world=[[False]*21 for _ in range(21)]
        self.has_arrow=True
        self.breeze=False
        self.stench=False
        self.action_list={0:'MOVE_RIGHT',1:'MOVE_LEFT',2:'MOVE_UP',3:'MOVE_DOWN',4:'SHOOT_RIGHT',5:'SHOOT_LEFT',6:'SHOOT_UP',7:'SHOOT_DOWN',8:'QUIT'}
        self.last_action=''
        self.location=(-1,-1)
        self.wumpus_dead=False
        self.wall_bump=False
        self.move_history=[]
        self.initial_KB()
        
        
    def initial_KB(self):
        start_value=1
        for i in range(len(self.world)):
            start_value=self.create_world(self.world[i], start_value)
        self.add_wumpus_clauses()
        
                            
    def add_wumpus_clauses(self):
        atleast_set=set()
        for i in range(1,self.rows+1):
            for j in range(1,self.cols+1):
                atleast_set.add(self.world[Map.w][i][j])
        self.kb.append(atleast_set)
    
    def add_breeze_stench(self):
        self.get_clauses(self.world[Map.b], self.world[Map.p], self.location[0], self.location[1])
        self.get_clauses(self.world[Map.s], self.world[Map.w], self.location[0], self.location[1])
        start=self.location[0]-2
        end=self.location[0]+2
        s=self.location[1]-2
        e=self.location[1]+2
        if self.stench:
            # at most one
            for i in range(start, (end)):
                for j in range(s, (e)):            
                    for k in range(start, end):
                        for l in range(s, e):
                            if (k==i and l==j):
                                continue
                            if (k==i and l>j or k>i):
                                clause={-self.world[Map.w][i][j], -self.world[Map.w][k][l]}
                                if clause not in self.kb:
                                    self.kb.append(clause)
    
    def get_clauses(self,f,r,i,j):
        temp_set=set()
        temp_set.add(-f[i][j])
        if (i+1) in range(1,self.rows+1):
            self.kb.append({-r[i+1][j],f[i][j]})
            temp_set.add(r[i+1][j])
        if (i-1) in range(1,self.rows+1):
            self.kb.append({-r[i-1][j],f[i][j]})
            temp_set.add(r[i-1][j])
        if (j+1) in range(1,self.cols+1):
            self.kb.append({-r[i][j+1],f[i][j]})
            temp_set.add(r[i][j+1])
        if (j-1) in range(1,self.cols+1):
            self.kb.append({-r[i][j-1],f[i][j]})
            temp_set.add(r[i][j-1])

        self.kb.append(temp_set)
    
    def create_world(self,world_obj,start_value):
        for i in range(0,self.rows+1):
            temp=[]
            for j in range(0,self.cols+1):
                try:
                    temp.append(start_value)
                    start_value+=1
                except:
                    pass
            world_obj.append(temp)
        return start_value
                
    
    
    def get_action(self):
        if not self.wall_bump:
            if self.breeze:
                self.update_kb([{self.world[Map.b][self.location[0]][self.location[1]]}])
            else:
                self.update_kb([{-self.world[Map.b][self.location[0]][self.location[1]]}])
            if self.stench:
                self.update_kb([{self.world[Map.s][self.location[0]][self.location[1]]}])
            else:
                self.update_kb([{-self.world[Map.s][self.location[0]][self.location[1]]}])
            self.update_kb([{-self.world[Map.p][self.location[0]][self.location[1]]}])
            if not self.wumpus_dead:
                self.update_kb([{-self.world[Map.w][self.location[0]][self.location[1]]}])
            self.add_breeze_stench()
        if not self.breeze and not self.stench and self.wumpus_world[self.location[0]][self.location[1]]==False:
            self.last_action=self.action_list[0]
            self.move_history.append(self.action_list[1])
            return self.action_list[0]
        possible_move=self.get_possible_move(self.location[0],self.location[1])
        if possible_move is not None:
            self.last_action=possible_move
            if possible_move==self.action_list[0]:
                self.move_history.append(self.action_list[1])
            elif possible_move==self.action_list[1]:
                self.move_history.append(self.action_list[0])
            elif possible_move==self.action_list[2]:
                self.move_history.append(self.action_list[3])
            elif possible_move==self.action_list[3]:
                self.move_history.append(self.action_list[2])
            return possible_move
        else:
            if len(self.move_history)>0:
                return self.move_history.pop()
            else:
                return self.action_list[8]
    
    def get_possible_move(self,x,y):
        possible_moves=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        for move in possible_moves:
            if move[0] == (x+1) and (x+1) not in range(1,self.rows+1):
                continue
            if move[0] == (x-1) and (x-1) not in range(1,self.rows+1):
                continue
            if move[1] == (y+1) and (y+1) not in range(1,self.cols+1):
                continue
            if move[1] == (y-1) and (y-1) not in range(1,self.cols+1):
                continue
            if  self.wumpus_world[move[0]][move[1]]=="V" or self.wumpus_world[move[0]][move[1]]=="B":
                continue
            
            pit_clause=[{self.world[Map.p][move[0]][move[1]]}]
            pit=self.check_entailment(pit_clause)
            wumpus=False
            if not self.wumpus_dead:
                wumpus_clause=[{self.world[Map.w][move[0]][move[1]]}]
                wumpus=self.check_entailment(wumpus_clause)
            if not pit and not wumpus:
                return self.action_list[possible_moves.index(move)]
            if not self.wumpus_dead and wumpus:
                no_wumpus_clause=[{-self.world[Map.w][move[0]][move[1]]}]
                no_wumpus=self.check_entailment(no_wumpus_clause)
                if not no_wumpus:
                    return self.action_list[possible_moves.index(move)+4]
                  
    
    def give_senses(self,location,breeze,stench):
        self.breeze=breeze
        self.stench=stench
        self.wall_bump=False
        
        if(self.location==location):
            # agent bumped into the boundary
            if(self.last_action==self.action_list[2]):
                self.wumpus_world[self.location[0]][self.location[1]+1]='B'     #Boundary
            elif(self.last_action==self.action_list[3]):
                self.wumpus_world[self.location[0]][self.location[1]-1]='B'
            elif(self.last_action==self.action_list[1]):
                self.wumpus_world[self.location[0]-1][self.location[1]]='B'
            elif(self.last_action==self.action_list[0]):
                self.wumpus_world[self.location[0]+1][self.location[1]]='B'
            self.wall_bump=True
        else:
            self.location=location
            self.wumpus_world[location[0]][location[1]]='V'     #Visited
            self.wall_bump=False
    
    def update_kb(self,new_clauses):
        for clause in new_clauses:
            if clause not in self.kb:
                self.kb.append(clause)  
    
    
    def check_entailment(self,query_clause):
#         kb_copy=pickle.loads(pickle.dumps(self.kb,-1))
        kb_copy=deepcopy(self.kb)
        for clause in query_clause:
            if clause not in kb_copy:
                kb_copy.append(clause)
        solver = Solver(kb_copy)
        if(solver.solve()):
            return True
        else:
            return False
    def killed_wumpus(self):
        self.wumpus_dead=True
        self.has_arrow=False
    
    