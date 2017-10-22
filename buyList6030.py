from IBapiMod import *
import logging

def buyList6030(bullList, bearList):

    for s in bullList:
        app = TestApp("127.0.0.1", 7401, 1)
        app.buy6030(s)
        app.disconnect()

    for s in bearList:
        app = TestApp("127.0.0.1", 7401, 1)
        app.buy6030(s,"Bear")
        app.disconnect()
