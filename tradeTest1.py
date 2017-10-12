from IBapiMod import *
import logging
from pandas import DataFrame

logging.basicConfig(level=logging.ERROR)

app = TestApp("127.0.0.1", 7401, 1)

sym = "GOOG"
exp = "20171020"
right = "P"

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

#app.reqMarketDataType(2)
app.reqMktData(1032,contract1,"221",False,False,[])
d = app.reqContractDetails(1202,contract2)
time.sleep(5)

print("Price Details:")
try:
    for k in list(app._my_price_details[1032].queue):
        t = dict(k)
        if t['tickType']==9:
            lastPrice = t['price']
        print(t)
except:
    lastPrice = 0
print()
print("{0} Last Price: ${1:4.2f}".format(sym, lastPrice))
print()

rID = 1100
df = DataFrame()
# print("Contract Details:")
for k in list(app._my_contract_details[1202].queue):
    t = list(str(k).split(','))
    try:
        if lastPrice*1.05 > float(t[4]) > lastPrice*0.95:
            df[rID] = t
            contract3 = IBcontract()
            contract3.secType = "OPT"
            contract3.symbol = sym
            contract3.exchange = "SMART"
            contract3.lastTradeDateOrContractMonth = exp
            contract3.strike = float(t[4])
            contract3.right = right
            contract3.multiplier = 100
            #app.reqMarketDataType(2)
            app.reqMktData(rID, contract3, "", False, False, [])
            rID = rID + 1
    except:
        pass
df = df.transpose()
print("Getting option details for {0:2d} strikes:".format(len(df)))
print()

time.sleep(5)

df['undPrice'] = [""]*len(df)
df['delta'] = [""]*len(df)
for s in df.index:
    # for k in list(app._my_price_details[s].queue):
    #     t = dict(k)
    #     print(t)
    #     if t['tickType'] == 4:
    #         lastPrice = t['price']
    #         df[s].price = t['price']
    for k in list(app._my_option_data[s].queue):
        t = dict(k)
        print(s,t)
        print(type(df.loc[s,4]))
        print(type(t['delta']))
        df.loc[s,'undPrice'] = t['undPrice']
        #if t['delta'] != None:
        df.loc[s,'delta'] = t['delta']
#print("Request ID: {0:4d} Close: ${1:4.2f} ".format(t['reqId'],t['price']))

print(df.loc[:,[3,4,'undPrice','delta']].sort_values([4]))

# print("Price Details:")
# for k in list(app._my_price_details[1032].queue):
#     print(k)
# print()
#
# print("Option Chain:")
# for k in list(app._my_option_chain[1136].queue):
#     print(k)
# print(max(list(app._my_option_chain[1136].queue)[0]['strikes']))
# print()
#
# print("Option Data:")
# for k in list(app._my_option_data[1032].queue):
#     print(k)
# print()

app.disconnect()