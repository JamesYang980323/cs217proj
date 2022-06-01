# Reference: https://pythonwife.com/bellman-fords-algorithm-in-python/
#Initializing the Graph Class

# The Graph class will be used as a pre-configured topology that is already known.
# The Router class instances will be able to know its neighbors by querying for its own edges from the Graph.
class Graph:
    def __init__(self, numVertices):
        self.V = numVertices
        self.graph = []   
        self.nodes = []

    def add_edge(self, s, d, w):
        self.graph.append([s, d, w])
    
    def addNode(self, value):
        self.nodes.append(value)
    
    # given a router name prefix, if that prefix matches with the source or destination prefix,
    # that means that there is an edge from that router prefix to some other node.
    # Return that edge
    def getNeighbors(self, routerPrefix):
        neighbors = []
        for [s, d, w] in self.graph:
            if routerPrefix == s:
                neighbors.append([s, d, w])
            elif routerPrefix == d:
                neighbors.append([d, s, w])

        return neighbors