from IBapiMod import *
import logging
from pandas import DataFrame
import datetime
import sys

logging.basicConfig(level=logging.ERROR)

app = TestApp("127.0.0.1", 7401, 1)

sym = "ACN"
direction = "Bull"
exp = ""

if direction == "Bull":
    right = "Put"
else:
    right = "Call"

if exp == "":
    d = datetime.date.today()
    d += datetime.timedelta(10)
    while d.weekday() != 4:
        d += datetime.timedelta(1)
    exp = d.strftime("%Y%m%d")


contract1 = IBcontract()
contract1.secType = "STK"
contract1.symbol = sym
contract1.exchange = "SMART"

contract2 = IBcontract()
contract2.secType = "OPT"
contract2.symbol = sym
contract2.exchange = "SMART"
contract2.lastTradeDateOrContractMonth = exp
contract2.right = right
contract2.multiplier = 100

app.reqMarketDataType(2)
app.reqMktData(1032,contract1,"221",False,False,[])
d = app.reqContractDetails(1202,contract2)
time.sleep(1)
print(d)

print("Price Details:")
try:
    for k in list(app._my_price_details[1032].queue):
        t = dict(k)
        if t['tickType']==9:
            lastPrice = t['price']
        print(t)
except:
    print("No pricing available for {} at this time.".format(sym))
    sys.exit()
#print()
#print("{0} Last Price: ${1:4.2f}".format(sym, lastPrice))
#print()

rID = 1100
df = DataFrame()
print("Contract Details:")
for k in list(app._my_contract_details[1202].queue):
    t = list(str(k).split(','))
    #print(t)
    try:
        if lastPrice*1.10 > float(t[4]) > lastPrice*0.90:
            df[rID] = t
            contract3 = IBcontract()
            contract3.secType = "OPT"
            contract3.symbol = sym
            contract3.exchange = "SMART"
            contract3.lastTradeDateOrContractMonth = exp
            contract3.strike = float(t[4])
            contract3.right = right
            contract3.multiplier = 100
            app.reqMarketDataType(2)
            app.reqMktData(rID, contract3, "", False, False, [])
            rID = rID + 1
    except:
        pass
df = df.transpose()
#print(df)
#print("Getting option details for {0:2d} strikes:".format(len(df)))
#print()

time.sleep(1)

df['undPrice'] = [""]*len(df)
df['delta'] = [""]*len(df)
df['strike'] = [""]*len(df)
df['delta60'] = [""]*len(df)
for s in df.index:
    app.cancelMktData(s)
    for k in list(app._my_option_data[s].queue):
        t = dict(k)
        #print(s,t)
        if t['delta']:
            try:
                df.loc[s,'conId'] = int(df.loc[s,0])
                df.loc[s,'strike'] = float(df.loc[s,4])
                df.loc[s,'undPrice'] = t['undPrice']
                df.loc[s,'delta'] = abs(t['delta'])
                df.loc[s,'delta60'] = abs(abs(t['delta']) - 0.60)
            except:
                pass

#print(df.loc[:,['conId',3,'strike','undPrice','delta','delta60']].sort_values(['strike']))
#print()
d60 = df.loc[df['delta60']==df['delta60'].min()].index.min()
#print("Sell a {} with the {:7.2f} strike".format(right,df.strike[d60]))

t30 = (df.delta[d60]-0.3)
p = df.loc[df.delta > t30].delta.min()
d30plus = df.loc[df.delta == p].index.min()
m = df.loc[df.delta < t30].delta.max()
d30min = df.loc[df.delta == m].index.min()
if abs(df.delta[d30plus]-t30) > abs(df.delta[d30min]-t30):
    d30 = d30min
else:
    d30 = d30plus

# Order variables
#####
cdelta = df.delta[d60]- df.delta[d30]
lim = abs(df.strike[d60]-df.strike[d30])*0.40
takeProfitLimitPrice = lim*0.3
stopLossPrice = lim*1.75
quantity = 1
action = "SELL"
parentOrderId = 101

# print("Buy a {} with the  {:7.2f} strike ".format(right,df.strike[d30]))
# print("Combo delta is {:5.3f}".format(cdelta))
# print("Combo limit price is ${:7.2f}".format(lim))
# print("Combo Expiry is {}".format(exp))
# print()
print("{} - Price: ${:7.2f} - Sell a {} {:7.2f}/{:7.2f} {} Spread - Limit price: ${:5.2f} - Combo delta: {:5.3f}".
      format(sym, lastPrice, exp, df.strike[d60], df.strike[d30], right, lim, cdelta))

#
#  Send order for the Spread above
####

contract3 = IBcontract()
contract3.secType = "BAG"
contract3.symbol = sym
contract3.exchange = "SMART"
contract3.currency = "USD"

leg1 = IBcomboLeg()
leg1.conId = int(df.conId[d60])  # Sell the delta 60 option
leg1.ratio = 1
leg1.action = "SELL" if action == "BUY" else "BUY"
leg1.exchange = "SMART"

leg2 = IBcomboLeg()
leg2.conId = int(df.conId[d30])  # Buy the delta 30 option as protection
leg2.ratio = 1
leg2.action = "BUY" if action == "BUY" else "SELL"
leg2.exchange = "SMART"

contract3.comboLegs = []
contract3.comboLegs.append(leg1)
contract3.comboLegs.append(leg2)

order3 = Order()
order3.action = action
order3.orderType = "LMT"
order3.totalQuantity = quantity
order3.lmtPrice = lim
order3.tif = 'DAY'
order3.transmit = False

parentOrderId = app.place_new_IB_order(contract3, order3, orderid=None)

takeProfit = Order()
takeProfit.action = "SELL" if action == "BUY" else "BUY"
takeProfit.orderType = "LMT"
takeProfit.totalQuantity = quantity
takeProfit.lmtPrice = takeProfitLimitPrice
takeProfit.parentId = parentOrderId
takeProfit.tif = 'GTC'
takeProfit.transmit = False
app.place_new_IB_order(contract3, takeProfit, orderid=None)

stopLoss = Order()
stopLoss.action = "SELL" if action == "BUY" else "BUY"
stopLoss.orderType = "STP"
# Stop trigger price
stopLoss.auxPrice = stopLossPrice
stopLoss.totalQuantity = quantity
stopLoss.parentId = parentOrderId
stopLoss.tif = 'GTC'
# In this case, the low side order will be the last child being sent. Therefore, it needs to set this attribute to True
# to activate all its predecessors
stopLoss.transmit = True
app.place_new_IB_order(contract3, stopLoss, orderid=None)

time.sleep(1)

print()
app.disconnect()
sys.exit("Now we're done")
