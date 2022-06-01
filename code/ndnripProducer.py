""" from ndn.app import NDNApp
app = NDNApp()

async def main():
    @app.route('/example/testApp')
    def on_interest(name, interest_param, application_param):
        app.put_data(name, content=b'content', freshness_period=10000)

app.run_forever(after_start=main()) """

# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

from ndn.app import NDNApp

from sys import argv # used to read in your router prefix name

app = NDNApp()

async def main():
    routerPrefix = argv[1]
    print("announcing " + routerPrefix)

    @app.route(routerPrefix)
    def on_interest(name, interest_param, application_param):
        app.put_data(name, content=b'routing table', freshness_period=10000)

app.run_forever(after_start=main())
