from Graph import Graph
import math

class Dijkstras:
    def __init__(self):
        self.g = Graph()
        self.g.addEdge(0,1,4)
        self.g.addEdge(0,7,8)
        self.g.addEdge(1,2,8)
        self.g.addEdge(2,3,7)
        self.g.addEdge(3,4,9)
        self.g.addEdge(7,6,1)
        self.g.addEdge(6,5,2)
        self.g.addEdge(5,4,10)
        self.g.addEdge(7,8,7)
        self.g.addEdge(2,5,4)
        self.g.addEdge(3,5,14)
        self.g.addEdge(1,7,11)
        self.g.addEdge(2,8,2)
        self.g.addEdge(8,6,6)
    
    def minDistance(self,S, dist):
        minDist = math.inf
        minIndex=-1
        for i in range(len(self.g.graph)):
            if(not S.__contains__(i) and dist[i]<=minDist):
                minDist = dist[i]
                minIndex = i
        return minIndex
    
    
    def dijkstras(self, s):
        S = []
        parent = [-1] * len(self.g.graph)
        dist = [math.inf] * len(self.g.graph)
        dist[s] = 0
        for i in range(len(self.g.graph)-1):
            u = self.minDistance(S, dist)
            S.append(u)
            for v in self.g.graph[u]:
                if(not S.__contains__(v) and dist[u]!=math.inf and dist[u]+self.g.distance[(u,v)] < dist[v]):
                    dist[v] = dist[u] + self.g.distance[(u,v)]
                    parent[i] = u
                    
        for i in range(len(self.g.graph)):
            print(i , "   " , dist[i])
            
        print(parent)
        
    
    
if __name__=="__main__":
    obj = Dijkstras()
    obj.dijkstras(0)
    