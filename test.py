from IBapiMod import *
from emailApi import *
import logging
from buyList6030 import buyList6030
from googleApi import *
import pygsheets

logging.basicConfig(level=logging.DEBUG)

from datetime import datetime, time
from time import sleep

runTime = "7:45"
startTime = time(*(map(int, runTime.split(':'))))
while startTime > datetime.today().time():  # you can add here any additional variable to break loop if necessary
    sleep(1)  # you can change 1 sec interval to any other

print("and so it begins at {}".format(datetime.now()))

#app = TestApp("127.0.0.1", 7401, 1)

# app.buy6030("AAPL","Bull",budget=350)

# c = IBcontract()
# #c.conId = 292255231
# c.conId = 292255235
# # c.secType = "STK"
# # c.symbol = "GOOG"
# c.exchange = "SMART"
# p = app.quote(c)
# print(p)

#app.disconnect()

#buyList6030([],
#            ['MNK', 'PM', 'GE', 'ED', 'COG', 'PG', 'LLY', 'LRCX', 'CELG', 'PCG'])

#textRoland("Message at 10:15", "This is the body")

SHEETID = "1aZwZQ-KtXr-7_9ZYIZxMano85zckb86gj67kcwQczYI"
# RANGE = "Trades!A1"
# sheetData = [["Expiry1","Symbol","Strike1","Strike2","Right","Position","CostBase","UnitCost","UnitPrice","Gain"]]
# updateValues(SHEETID,RANGE,sheetData)

gc = pygsheets.authorize(outh_file='sheets.googleapis.com-python.json')

sht1 = gc.open_by_key('1aZwZQ-KtXr-7_9ZYIZxMano85zckb86gj67kcwQczYI')

wks = sht1.add_worksheet("new sheet",rows=50,cols=60)

# # Open spreadsheet and then workseet
# sh = gc.open('my new ssheet')
# wks = sh.sheet1
#
# # Update a cell with value (just to let him know values is updated ;) )
# wks.update_cell('A1', "Hey yank this numpy array")
#
# # update the sheet with array
# wks.update_cells('A2', ["Hi","There"])
#
# # share the sheet with your friend
# sh.share("myFriend@gmail.com")