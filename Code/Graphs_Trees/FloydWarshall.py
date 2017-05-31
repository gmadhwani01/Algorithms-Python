from Graph import Graph
class FloydWarshall:
    def __init__(self):
        self.g=Graph()
        # Initialize the graph and add edges to it
        bidirVal = False
        self.g.addEdge(0,1,5,bidirectional=bidirVal)
        self.g.addEdge(1,2,3,bidirectional=bidirVal)
        self.g.addEdge(2,3,1,bidirectional=bidirVal)
        self.g.addEdge(0,3,10,bidirectional=bidirVal)
#         self.g.addEdge(2,5,bidirectional=bidirVal)
#         self.g.addEdge(3,5,bidirectional=bidirVal)
#         self.g.addEdge(4,6,bidirectional=bidirVal)
#         self.g.addEdge(5,7,bidirectional=bidirVal)
#         self.g.addEdge(6,8,bidirectional=bidirVal)
#         self.g.addEdge(7,8,bidirectional=bidirVal)

        
    def get_initial_matrix(self):
        result = []
        for i in set(self.g.vertices):
            tempList = []
            for j in set(self.g.vertices):
                if i==j:
                    tempList.append(0)
                elif(self.g.pathExists(i,j)):
                    tempList.append(self.g.distance[(i,j)])
                else:
                    tempList.append(float("inf"))
            result.append(tempList)
            
        return result
    def floyd_warshall(self):
        result = self.get_initial_matrix()
        for i in range(len(self.g.vertices)):
            for j in range(len(self.g.vertices)):
                for k in range(len(self.g.vertices)):
                    result[i][j] = min(result[i][j],result[i][k]+result[k][j])
        print(result)
    
if __name__=="__main__":
    obj = FloydWarshall()
    obj.floyd_warshall()