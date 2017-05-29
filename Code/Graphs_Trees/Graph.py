from _collections import defaultdict
class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        self.distance = defaultdict(list)
        
    def addEdge(self,u,v,cost=None, bidirectional=True):
        self.graph[u].append(v)
        if(bidirectional):
            self.graph[v].append(u)
        if(cost is not None):
            self.distance[(u,v)] = cost
            if(bidirectional):
                self.distance[(v,u)] = cost
        
    def pathExists(self,u,v):
        if self.graph[u].__contains__(v):
            return True
        else:
            return False