class Router:
    def __init__(self, name):
        self.routerName = name # router1 is an example router name prefix
        self.neighbors = [] # neighbor table containing [node1Prefix, node2Prefix, cost(node1, node2)] vectors as elements
    
    # neighbor comes in from Graph as [your node, neighbor node, weight]
    def addNeighbor(self, neighbor):
        self.neighbors.append(neighbor)
