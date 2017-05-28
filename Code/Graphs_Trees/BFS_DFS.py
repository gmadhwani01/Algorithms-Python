from Graph import Graph
class BFS_DFS:
    def __init__(self):
        self.g=Graph()
        # Initialize the graph and add edges to it
        self.g.addEdge(0,1)
        self.g.addEdge(1,2)
        self.g.addEdge(1,3)
        self.g.addEdge(2,4)
        self.g.addEdge(2,5)
        self.g.addEdge(3,5)
        self.g.addEdge(4,6)
        self.g.addEdge(5,7)
        self.g.addEdge(6,8)
        self.g.addEdge(7,8)
    
    def performBfs(self,s):
        queue = []
        visited = [False] * (len(self.g.graph)+1)   # visited list will store if the node is visited or not
        queue.append(s)
        visited[s] = True
        print("BFS Traversal: ")
        while queue:
            curr = queue.pop(0)
            print(curr, end="\t")
            for i in self.g.graph[curr]:
                if(visited[i] == False):
                    queue.append(i)
                    visited[i] = True
                    
                    
    def performDfsRec(self,s):
        visited = [False] * (len(self.g.graph)+1)
        print("DFS Traversal: ")
        self.dfs(s, visited)
    
    def dfs(self,curr, visited):
        print(curr, end="\t")
        for i in self.g.graph[curr]:
            if visited[i] == False:
                self.dfs(i, visited)

if __name__=="__main__":
    obj= BFS_DFS()
    obj.performDfsRec(0)