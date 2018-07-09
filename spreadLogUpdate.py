from IBapiMod import *
from emailApi import *
import logging
import datetime
import pandas as pd
import numpy as np
from pandas import DataFrame
import googleApi as g
import math
from inputs.settings import *

logging.basicConfig(level=logging.WARNING)

app = TestApp("127.0.0.1", 7410, 1)

RANGE = "Spreads!A7"

credentials = g.service_account.Credentials.from_service_account_file(
    g.CLIENT_SECRET_FILE)
scoped_credentials = credentials.with_scopes(
    [g.SCOPES])
authed_session = g.AuthorizedSession(scoped_credentials)

d = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
f = open('logs/log{}.txt'.format(d),'w')
tradeLog = pd.read_csv('tradeLog.txt', header=0)
#tradeLog = pd.read_csv('logDataGS.csv', header=0)

print("\nDate: {}\n=================\n".format(d))
f.write("\nDate: {}\n=================\n".format(d))

app.reqPositions()
time.sleep(2)
#print("Positions:\n=================")
#f.write("Positions:\n=================\n")
positions = list(app._my_positions.queue)
dfPositions = DataFrame()
for p in positions:
    c = p["contract"]
    c.exchange = "SMART"
    #print(c)
    app.reqMktData(c.conId, c, "", False, False, [])
    #print("{}  {:5}  {:6}  {}  {:2.0f}  {:7.2f}".format(c.lastTradeDateOrContractMonth,c.symbol,
    #                                                c.strike,c.right,p["position"],p["avgCost"]))
    #f.write("{}  {:5}  {:6}  {}  {:2.0f}  {:7.2f}\n".format(c.lastTradeDateOrContractMonth,c.symbol,
    #                                                c.strike,c.right,p["position"],p["avgCost"]))
    dfPositions = dfPositions.append(DataFrame(data={"symbol":[c.symbol],
                                                     "conId":[c.conId],
                                                     "expiry":[c.lastTradeDateOrContractMonth],
                                                     "strike":[c.strike],
                                                     "right":[c.right],
                                                     "position":[p["position"]],
                                                     "avgCost":[p["avgCost"]]}),ignore_index = True)

print()

executions = app.get_executions_and_commissions()
print("\nToday's Executions:\n=========================")
f.write("\nToday's Executions:\n=========================\n")
for d in executions:
    e = executions[d]
    c = executions[d].contract
    print("{}  {:5}  {:6}  {}  {}  {:3.0f}  {:5.2f} {} {}".format(c.lastTradeDateOrContractMonth,c.symbol,c.strike,c.right,
                                                        e.time, e.Shares, e.AvgPrice,e.Price,e.OrderId))
    f.write("{}  {:5}  {:6}  {}  {}  {:3.0f}  {:5.2f} {} {}\n".format(c.lastTradeDateOrContractMonth, c.symbol, c.strike, c.right,
                                                        e.time, e.Shares, e.AvgPrice,e.Price,e.OrderId))

app.disconnect()

#
#  Group combos in single line
######

print("\nPosition Table for Dashboard\n==============================\n")
f.write("\nPosition Table for Dashboard\n==============================\n")


dfPositions = dfPositions.sort_values(["expiry","symbol","strike","right","position"])
sheetData = [["LogTime","Expiry","Symbol","Strike1","Strike2","Right","Position","CostBase","UnitCost","UnitPrice","Gain","Target","Stop"]]
f.write("Expiry   Symbol  Str1  Str2  R Pos Costbase  UCost UPrice   Gain    Targ   Stop\n")
print("Expiry   Symbol  Str1    Str2  R Pos Costbase   UCost UPrice   Gain  Targ  Stop")
for index, row in dfPositions.iterrows():
    price = None
    if row["expiry"] == "":
        continue
    if row["position"] < 0:

        lastPrice = None
        try:
            for k in list(app._my_price_details[row["conId"]].queue):
                t = dict(k)
                if t['tickType'] == 4:
                    lastPrice = t['price']
                if t['tickType'] == 9 and lastPrice == None:
                    lastPrice = t['price']
                #print(t)
            #print("p1: {}".format(lastPrice))
            p1 = lastPrice
        except:
            pass

        d2 = dfPositions[dfPositions["symbol"] == row["symbol"]]
        d2 = d2[d2["expiry"] == row["expiry"]]
        d1 = d2[d2["position"] < 0].reset_index(drop=True)
        d2 = d2[d2["position"] > 0].reset_index(drop=True)
        s = DataFrame({"s1":d1["strike"],"s2":d2["strike"]})
        s2 = float(s[s.s1 == row["strike"]].s2)
        d2 = d2[d2["strike"] == s2]

        lastPrice = None
        try:
            for k in list(app._my_price_details[d2["conId"].min()].queue):
                t = dict(k)
                if t['tickType'] == 4:
                    lastPrice = t['price']
                if t['tickType'] == 9 and lastPrice == None:
                    lastPrice = t['price']
                #print(t)
            #print("p2: {}".format(lastPrice))
            p2 = lastPrice
            price = p1 - p2
        except:
            pass

        Note = ""
        cost = (row["avgCost"]-d2["avgCost"].min())*row["position"]
        unitCost = cost/100/row["position"]
        gain = (unitCost-price)/unitCost
        if gain < -0.5:
            Note = "Close - Stop Loss"
        if gain > 0.7:
            Note = "Close - Target"

        r = [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),row["expiry"],row["symbol"],row["strike"],d2["strike"].min(),row["right"],row["position"],cost,unitCost,price,gain*100,unitCost*0.3,unitCost*0.7]
        sheetData.append(r)
        print("{} {:5} {:6.1f} /{:6.1f}  {} {:3.0f} {:7.2f} {:7.2f} {:5.2f}  {:7.2f} {:5.2f} {:5.2f} {}".format(row["expiry"],row["symbol"],row["strike"],
                                                          d2["strike"].min(),row["right"],row["position"],
                                                            cost, unitCost, price, gain*100, unitCost*0.3, unitCost*1.5, Note))
        f.write("{} {:5} {:6.1f} {:6.1f} {} {:3.0f} {:7.2f} {:7.2f} {:6.2f} {:7.2f} {:6.2f} {:6.2f} {}\n".format(row["expiry"], row["symbol"], row["strike"],
                                                          d2["strike"].min(), row["right"],row["position"],
                                                              cost, unitCost, price, gain*100, unitCost*0.3, unitCost*1.5, Note))

posTable = DataFrame(sheetData[1:],columns=sheetData[0])
tradeLog["Expiry"] = tradeLog["Expiry"].astype(int)
posTable["Expiry"] = posTable["Expiry"].astype(int)

# update UnitPrice for positions already in the trade log
t = pd.merge(tradeLog.loc[:,["LogTime","Opened","Expiry","Symbol","Strike1","Strike2","Right","Position","CostBase","UnitCost","Closed"]],
             posTable.loc[:,["Symbol","Expiry","UnitPrice"]],
             how='outer', on=['Symbol','Expiry'])

# add back in UnitPrice for all the positions that have closed and are not in the position list
u = t["UnitPrice"].isna()
t.loc[u,"UnitPrice"] = tradeLog.loc[u,"UnitPrice"]

# Update closed date for newly closed positions
o = t["Closed"].isna()
c = u & o
t.loc[c,"Closed"] = datetime.datetime.now().strftime("%Y-%m-%d")

# add new positions into the Log
n = t["LogTime"].isna()
t.loc[n,"LogTime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
t.loc[n,"Opened"] = datetime.datetime.now().strftime("%Y-%m-%d")

ndf = pd.merge(t.loc[n,["Expiry","Symbol"]],
               posTable.loc[:,["Symbol","Expiry","Strike1","Strike2","Right","Position","CostBase","UnitCost"]],
               how="left", on=['Symbol','Expiry'])

t.loc[n,["Strike1","Strike2","Right","Position","CostBase","UnitCost"]] = \
    ndf.loc[:,["Strike1","Strike2","Right","Position","CostBase","UnitCost"]].values

t["Gain"]=100*(t["UnitCost"]-t["UnitPrice"])/t["UnitCost"]

#write the updated log to the tradeLog file
t = t.sort_values(["Expiry","Closed"],ascending=[False,True])
tradeLog = t
tradeLog.to_csv('tradeLog.txt', index=False)

tList = t.fillna(" ").values.tolist()
r = g.updateValues(authed_session,SHEETID,"Spreads!A7",tList)
r = g.header1(authed_session,SHEETID,GID,6)
c = t.loc[:,['Expiry','Symbol']].groupby('Expiry').count()

g.clearLines(authed_session, SHEETID, GID, 7)

line = 6 + len(t)
for i in c['Symbol']:
    r = g.divider1(authed_session, SHEETID, GID, line)
    line = line - i

# print and write tables for gain and sample size by expiry date
f.write("\n\nGain by Expiry Date\n================\n")
table = t.pivot_table(columns='Expiry', values='Gain')
print("\n",table)
f.write(table.to_string())
r = g.updateValues(authed_session,SHEETID,"Spreads!C2",[table.columns.values.tolist()])
print(r)
r = g.updateValues(authed_session,SHEETID,"Spreads!C3",table.values.tolist())
print(r)

f.write("\n\nSample Size by Expiry Date\n=====================\n")
table = t.pivot_table(columns='Expiry', values='Symbol', aggfunc=DataFrame.count)
print("\n",table)
f.write(table.to_string())
r = g.updateValues(authed_session,SHEETID,"Spreads!C4",table.values.tolist())
print(r)

f.close()
