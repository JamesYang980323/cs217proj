""" from ndn.encoding import Name
from ndn.types import *
from ndn.app import NDNApp

app = NDNApp()

async def main():
    for i in range(10):
        try:
            data_name, meta_info, content = await app.express_interest(
                # Interest Name
                '/example/testApp/random',
                must_be_fresh=True,
                can_be_prefix=False,
                # Interest lifetime in ms
                lifetime=6000)
            # Print out Data Name, MetaInfo and its conetnt.
            print(f'Received Data Name: {Name.to_str(data_name)}')
            print(meta_info)
            print(bytes(content) if content else None)
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
        finally:
            print("hello")
app.run_forever(after_start=main()) """

# --------------------------------------------------------------
# --------------------------------------------------------------
# --------------------------------------------------------------

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
#def doBellmanFord(router, routerTable):
    routerNeighbors = router.getNeighbors()

     # find which router name this neighbor is
    neighborRouterPrefix = findNeighborRouterPrefix(neighborRoutingTable)

    # find the cost of the edge from your router prefix to the neighbor router prefix
    cost = findCost(neighborRouterPrefix, routerNeighbors)
    
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
                    if (cost + routerRow[1]) < neighborRow[1]:
                        routerRow[1] = neighborRow[1]
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
                # Print out Data Name, MetaInfo and its conetnt.
                #print(f'Received Data Name: {Name.to_str(data_name)}')
                #print(meta_info)
                #print(bytes(content) if content else None)
                

                # do Bellman-Ford algorithm (which compares your routing table with your neighbor's routing table)
                # pickle.dumps(object) serializes object, pickle.loads(object) de-serializes the object
                #neighborRoutingTable = bytes(content)
                neighborRoutingTable = pickle.loads(content)
                print(neighborRoutingTable)
                # update the routing table to the new one returned by calling the Bellman-Ford algorithm
                #doBellmanFord(router, routerTable, neighborRoutingTable)

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
            finally:
                # see if Interest is valid
                print("here")

        # have updated routing table from all neighbor routing tables, now figure out which routers have the prefix you're looking for
        # then, construct multiple next hops (consisting of their distance and corresponding next hop)
        #prefixToFind = "/a"
        #routerList = config.prefixDict.get(prefixToFind)
        #if None != routerList:
        #    nextHopsList = findNextHops(routerTable, routerList)
        
        # have next hops, now add a FIB entry
        #prefixKey = prefixToFind
        #forwardInformationBase.addKeyValue(prefixKey, nextHopsList)

app.run_forever(after_start=main())