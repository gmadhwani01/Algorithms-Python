from Graphs_Trees.Graph import Graph

class UnionFind:
    def __init__(self):
        self.g = Graph()
        bidir = False
        self.g.addEdge(0,1,bidirectional=bidir)
        self.g.addEdge(1,2,bidirectional=bidir)
        self.g.addEdge(2,0,bidirectional=bidir)
        self.parent = [-1] * len(self.g.vertices)
        
    def find(self, i):
        if self.parent[i]==-1:
            return i
        else:
            self.parent[i] = self.find(self.parent[i])  # update the parent on way along to reduce the time complexity of next iterations
            return self.find(self.parent[i])
        
    def find_len(self,x):
        if self.parent[x] == -1:
            return 1
        else:
            return 1+self.find_len(x)
    def union(self,x,y):
        x_parent = self.find(x)
        y_parent = self.find(y)
        #find the length of the tree so that final height is as min as possible to reduce recursions in next iterations
        x_len = self.find_len(x)
        y_len = self.find_len(y)
        if x_len>y_len:
            self.parent[x] = y_parent
        else:
            self.parent[y] = x_parent
            
    def isCyclic(self):
        for i in self.g.graph:
            for j in self.g.graph[i]:
                x = self.find(i)
                y = self.find(j)
                if(x==y):
                    return True
                self.union(x, y)
        return False
                
if __name__=="__main__":
    obj = UnionFind()
    print("Does not contain cycle" if obj.isCyclic() is False else "Contains cycle")