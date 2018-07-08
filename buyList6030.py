from IBapiMod import *


def buyList6030(bullList, bearList, budget=500):

    for s in bullList:
        for i in range(1,5):
            app = TestApp("127.0.0.1", 7401, 1)
            success = app.buy6030(s,budget=budget)
            app.disconnect()
            if success:
                break

    for s in bearList:
        for i in range(1,5):
            app = TestApp("127.0.0.1", 7401, 1)
            success = app.buy6030(s,"Bear",budget=budget)
            app.disconnect()
            if success:
                break

