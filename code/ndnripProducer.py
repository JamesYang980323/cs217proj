from ndn.app import NDNApp

import config
import pickle # used to serialize and de-serialize a neighbor's routing table in a Data packet

from sys import argv # used to read in your router prefix name

app = NDNApp()

async def main():
    routerPrefix = argv[1]
    print("announcing " + routerPrefix)

    specificRouter = routerPrefix.split("/router", 1)[1]
    print(specificRouter)

    resultTable = []
    if specificRouter == "X":
        resultTable = config.routingTableX
    elif specificRouter == "Y":
        resultTable = config.routingTableY
    elif specificRouter == "Z":
        resultTable = config.routingTableZ
    print(resultTable)

    @app.route(routerPrefix)
    def on_interest(name, interest_param, application_param):
        app.put_data(name, content=pickle.dumps(resultTable), freshness_period=10000)

app.run_forever(after_start=main())