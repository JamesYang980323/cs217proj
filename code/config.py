from graph import *

global numVertices
numVertices = 3

global nodes
nodes = ["/routerX", "/routerY", "/routerZ"]

global edges
edges = [["/routerX", "/routerY", 1], ["/routerY", "/routerZ", 2], ["/routerX", "/routerZ", 5]]

global routingTableX
routingTableX = [["/routerX", 0, None], ["/routerY", 1, "/routerY"], ["/routerZ", 5, "/routerZ"]]

global routingTableY
routingTableY = [["/routerX", 1, "/routerX"], ["/routerY", 0, None], ["/routerZ", 2, "/routerZ"]]

global routingTableZ
routingTableZ = [["/routerX", 5, "/routerX"], ["/routerY", 2, "/routerY"], ["/routerZ", 0, None]]

global g
g = Graph(numVertices)
for node in nodes:
    g.addNode(node)
for [source, destination, weight] in edges:
    g.add_edge(source, destination, weight)

# define the prefixes that each router advertises
global prefixDict
prefixDict = {
    "/a": ["/routerY", "/routerZ"],
    "/b": ["/routerX"]
}

# map router name prefixes to routing tables
global routerDict
routerDict = {    
    "/routerX": routingTableX,
    "/routerY": routingTableY,
    "/routerZ": routingTableZ
}