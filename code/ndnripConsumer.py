from sys import argv # used to read in your router prefix name
from math import inf # used as element(s) within routing tables for Bellman-Ford calculation
import time # used for wait for certain amount of seconds before asking for neighbor's routing table
import pickle # used to serialize and de-serialize a neighbor's routing table in a Data packet
from operator import itemgetter # used for sorting the routing table entries by router name prefix

from router import *
from graph import *
from fib import *
import config

from ndn.app import NDNApp
from ndn.encoding import Name
from ndn.types import *
import asyncio

app = NDNApp()

def findNeighborRouterPrefix(neighborTable):
    for i in range(len(neighborTable)):
        if 0 == neighborTable[i][1]:
            return neighborTable[i][0]
    return None

def findCost(neighborRouterPrefix, routerNeighbors):
    for [s, d, w] in routerNeighbors:
        if d == neighborRouterPrefix:
            return w
    return None

def doBellmanFord(router, routerTable, neighborRoutingTable):
    routerNeighbors = router.neighbors
    print("router neighbors: ")
    print(routerNeighbors)

     # find which router name this neighbor is
    neighborRouterPrefix = findNeighborRouterPrefix(neighborRoutingTable)
    print("neighbor router prefix: ")
    print(neighborRouterPrefix)

    # find the cost of the edge from your router prefix to the neighbor router prefix
    cost = findCost(neighborRouterPrefix, routerNeighbors)
    print("neighbor router cost: ")
    print(cost)
    
    for routerRow, neighborRow in zip(routerTable, neighborRoutingTable):
        # we know your router can reach <destination> in <distance> via <nextHop>
        # we know that the neighbor router can reach <destination2> in <distance2> via <nextHop2>
        # we know the cost of the edges between your router and the neighbor router via routerNeighbors        

        # skip invalid neighbor router prefix and invalid cost if either of them don't exist
        if neighborRouterPrefix != None:
            if cost != None:
                # skip past where your distance is 0 - that is the best distance already
                if routerRow[1] != 0:
                    # compare cost(your router, neighbor) + current distance in routing table to current distance in neighbor table
                    # if the cost + current distance is less than the neighbor's current distance, 
                    # alter your current routing talbe distance and next hop as necessary
                    if (cost + neighborRow[1] < routerRow[1]):
                        routerRow[1] = cost + neighborRow[1]
                        routerRow[2] = neighborRouterPrefix 

def findNextHops(routingTable, routersWithPrefixList):
    nextHops = []
    for row in routingTable:
        if row[0] in routersWithPrefixList:
            nextHops.append((row[1], row[2]))
    
    # then, sort the next hops by distance to show priority of next hops
    nextHops = sorted(nextHops, key=itemgetter(0))

    return nextHops

# This is the main function for the ndnRIP application.
# Each router will run this main function.
# We assume the network topology is known beforehand
# We assume each router knows:
    # its own neighbors and corresponding cost to their neighbors (its edges) via the network topology
    # its own name/identifier
# The main function initializes the given network topology. Then
# the router name prefix is initialized.

async def main():
    forwardInformationBase = Fib()

    # get router name from main function arguments
    routerArg = argv[1]
    print(routerArg)

    # initialize router object given network topology
    router = Router(routerArg)

    # get your router table
    routerTable = config.routerDict.get(routerArg)

    # give neighbors of your router to the Router instance
    neighbors = config.g.getNeighbors(routerArg)
    for neighbor in neighbors:
        router.addNeighbor(neighbor)

    while(True): # todo - not sure what the condition inside this while statement should be
        # wait 30 seconds
        time.sleep(10)

        # Send update to neighbor routers.
        # In NDN, your router would send an Interest asking for routerPrefix's routing table.
        for [s, d, w] in neighbors:
            print(d)
            try:
                data_name, meta_info, content = await app.express_interest(
                    # Interest Name
                    d,
                    must_be_fresh=True,
                    can_be_prefix=False,
                    # Interest lifetime in ms
                    lifetime=6000)

                # do Bellman-Ford algorithm (which compares your routing table with your neighbor's routing table)
                # pickle.dumps(object) serializes object, pickle.loads(object) de-serializes the object
                neighborRoutingTable = pickle.loads(content)
                print("initial routing table: ")
                print(neighborRoutingTable)
                # update the routing table to the new one returned by calling the Bellman-Ford algorithm
                doBellmanFord(router, routerTable, neighborRoutingTable)
                print("after Bellman-Ford")
                print(routerTable)

            except InterestNack as e:
                # A NACK is received
                print(f'Nacked with reason={e.reason}')
            except InterestTimeout:
                # Interest times out
                print(f'Timeout')
            except InterestCanceled:
                # Connection to NFD is broken
                print(f'Canceled')
            except ValidationFailure:
                # Validation failure
                print(f'Data failed to validate')

        # have updated routing table from all neighbor routing tables, now figure out which routers have the prefix you're looking for
        # then, construct multiple next hops (consisting of their distance and corresponding next hop)

        prefixToFind1 = "/a"
        routerList1 = config.prefixDict.get(prefixToFind1)
        if None != routerList1:
            nextHopsList1 = findNextHops(routerTable, routerList1)
        print("nextHops for /a: ")
        print(nextHopsList1)

        prefixToFind2 = "/b"
        routerList2 = config.prefixDict.get(prefixToFind2)
        if None != routerList2:
            nextHopsList2 = findNextHops(routerTable, routerList2)
        print("nextHops for /b: ")
        print(nextHopsList2)

        # have next hops, now add FIB entries
        forwardInformationBase.add(prefixToFind1, nextHopsList1)
        forwardInformationBase.add(prefixToFind2, nextHopsList2)
        print("FIB: ")
        forwardInformationBase.print()


app.run_forever(after_start=main())