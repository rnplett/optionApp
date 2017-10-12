
from IBapiMod import *
import logging

logging.basicConfig(level=logging.INFO)

app = TestApp("127.0.0.1", 7401, 1)

app.reqSecDefOptParams(1001,"KSU","","STK",8949)

time.sleep(1)

## lets get prices for this
ibcontract = IBcontract()
ibcontract.secType = "STK"
#ibcontract.lastTradeDateOrContractMonth="20171013"
ibcontract.symbol="GOOG"
ibcontract.exchange=""

mdo = TagValue()
app.reqMktData(1002,ibcontract,"221",True,False,mdo)

time.sleep(1)

# ibcontract.secType = "BAG"
#
# leg1 = IBcomboLeg()
# leg1.conId = 287769049 # GOOG 952.5 P
# leg1.ratio = 1
# leg1.action = "SELL"
#
# leg2 = IBcomboLeg()
# leg2.conId = 287769023 # GOOG 952.5 P
# leg2.ratio = 1
# leg2.action = "BUY"
#
# ibcontract.comboLegs = []
# ibcontract.comboLegs.append(leg1)
# ibcontract.comboLegs.append(leg2)
#
# ## And here is a limit order, unlikely ever to be filled
# ## Note limit price of 100
#
# order2=Order()
# order2.action="BUY"
# order2.orderType="LMT"
# order2.totalQuantity=1
# order2.lmtPrice = 9
# order2.tif = 'DAY'
# order2.transmit = True
#
# orderid2 = app.place_new_IB_order(ibcontract, order2, orderid=None)
# print("Placed limit order, orderid is %d" % orderid2)
#
# ## Short wait ...
# time.sleep(5)
#
# #p = app.securityDefinitionOptionParameter(1001,8949)
#
# print("Open orders (should be one)")
# open_orders = app.get_open_orders()
# print(open_orders)

# ## put in another limit order
# order3=Order()
# order3.action="BUY"
# order3.orderType="LMT"
# order3.totalQuantity=5
# order3.lmtPrice = 10.0
# order3.tif = 'DAY'
# order3.transmit = True
#
#
# orderid3 = app.place_new_IB_order(ibcontract, order3, orderid=None)
# print("Placed limit order, orderid is %d" % orderid2)
#
# print("Open orders (should be two)")
# open_orders = app.get_open_orders()
# print(open_orders.keys())
#
time.sleep(20)
#
# ## modify the order
#
# print("Modifying order %d" % orderid3)
#
# order3.lmtPrice = 15.0
#
# print("Limit price was %f will become %f" % (open_orders[orderid3].order.lmtPrice, order3.lmtPrice ))
#
# app.place_new_IB_order(ibcontract, order3, orderid=orderid3)
# time.sleep(5)
# open_orders = app.get_open_orders()
# print("New limit price %f " % open_orders[orderid3].order.lmtPrice)
#
# ## Cancel a single limit order, leaving one active limit order (order3)
# print("Cancel order %d " % orderid2)
# app.cancel_order(orderid2)
# open_orders = app.get_open_orders()
#
print("Open orders (should just be %d)" % orderid2)
print(open_orders.keys())

print("Cancelling all orders")
app.cancel_all_orders()

print("Any open orders? - should be False")
print(app.any_open_orders())

app.disconnect()


