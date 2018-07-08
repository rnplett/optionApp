import pandas as pd
import numpy as np

from buyList6030 import buyList6030

from datetime import datetime, time
from time import sleep

# runTime = "7:35"
# startTime = time(*(map(int, runTime.split(':'))))
# while startTime > datetime.today().time():  # you can add here any additional variable to break loop if necessary
#         sleep(1)  # you can change 1 sec interval to any other
#
# print("and so it begins at {}".format(datetime.now()))

# Mac file system
# bullWatchList = pd.read_csv('/Users/rolandplett/GoogleDrive/Very Bullish Stocks.csv', header=None)
# bearWatchList = pd.read_csv('/Users/rolandplett/GoogleDrive/Very Bearish Stocks.csv', header=None)
# f = open('/Users/rolandplett/GoogleDrive/weekliesMAWatchList.csv','w')
# tv = open('/Users/rolandplett/GoogleDrive/weekliesMAWatchList.csv','w')
#
# Windows file system
weeklies = pd.ExcelFile('http://www.cboe.com/publish/weelkysmf/weeklysmf.xls')
w1 = weeklies.parse(weeklies.sheet_names[0])

# Update from https://datahub.io/core/s-and-p-500-companies/r/constituents.csv
symbolList = pd.read_csv('C:\\Users\\Roland\\Google Drive\\symbolListSP500.csv')
#symbolList = pd.read_csv('D:\\Users\\roland.plett\\Google Drive\\symbolListSP500.csv')
if len(symbolList) < 2:
    symbolList = symbolList.transpose()
symbolList = pd.DataFrame(symbolList.loc[:,'Symbol'].astype('str'))
#print(symbolList)
symbolList = symbolList.sort_values(["Symbol"])
#print(symbolList)

f = open('C:\\Users\\Roland\\Google Drive\\TodaysPicks.csv','w')
#f = open('D:\\Users\\roland.plett\\Google Drive\\TodaysPicks.csv','w')

stocksPerDay = 20

def filterMA(a):
    close0 = a.loc[0, 'Close']
    ma8 = a.loc[0:8, 'Close'].mean()
    ma21 = a.loc[0:21, 'Close'].mean()
    ma55 = a.loc[0:55, 'Close'].mean()
    ma8w = a.loc[0:40, 'Close'].mean()
    ma21w = a.loc[0:105, 'Close'].mean()

    low8 = a.loc[0:8, 'Close'].min()
    max8 = a.loc[0:8, 'Close'].max()
    stoch8 = (close0 - low8) / (max8 - low8)

    wStatus = "Unknown"
    AllStatus = "Unknown"

    # check bull status
    wBull = close0 > ma8w > ma21w
    dBull = ma8 > ma21 > ma55
    pBull = (ma8 > close0 > ma21) & (close0 > 20)
    if wBull:
        wStatus = "Bull"
    if wBull & dBull & pBull:
        AllStatus = "Bull"

    # check bear status
    wBear = close0 < ma8w < ma21w
    dBear = ma8 < ma21 < ma55
    pBear = ma8 < close0 < ma21
    if wBear:
        wStatus = "Bear"
    if wBear & dBear & pBear:
        AllStatus = "Bear"

    return([AllStatus, stoch8, close0, wStatus])


if __name__=='__main__':

    print()
    print('Stock Trigger Status \n==================== \n')
    print('Symbol  Price     Weekly_MA All_MA    Squeeze   10x       Stochastic  Profit')

    t = "Symbol,Price,Weekly_MA,All_MA,Squeeze,TenX,Stochastic\n"
    f.write(t)

    for s in symbolList["Symbol"]:
        if len(w1[w1[w1.columns[0]] == s]) > 0:
            # Get Historical Data for current symbol
            try:
                p = pd.read_csv('https://finance.google.com/finance/historical?q=' + s + '&output=csv')
            except:
                try:
                    p = pd.read_csv('https://finance.google.com/finance/historical?q=NYSE:' + s + '&output=csv')
                except:
                    print(s + " - Google lookup error")

            # Determine the MOVING AVERAGE TREND criteria of "Bull", "Bear" or "No_Trend"
            # Determine the current STOCHASTIC to identify a recent pullback from the trend.

            #### Show MA Analysis Data

            try:
                r = filterMA(p)
                wMA = r[3]
                allMA = r[0]
                stochastic = r[1]
                price = r[2]
                print("{0:<8s}{1:8.2f} {2:<10s}{3:<10s}{4:<10s}{5:<10s}{6:5.2f}".
                      format(s, price, wMA, allMA, "NA", "NA", stochastic))
                t = "{0:<8s},{1:8.2f},{2:<10s},{3:<10s},{4:<10s},{5:<10s},{6:5.2f}\n". \
                    format(s, price, wMA, allMA, "NA", "NA", stochastic)
                f.write(t)
            except:
                print(s + " - data error")

    f.close()

    data = pd.read_csv('C:\\Users\\Roland\\Google Drive\\TodaysPicks.csv')
    #data = pd.read_csv('D:\\Users\\roland.plett\\Google Drive\\TodaysPicks.csv')
    data.All_MA = data.All_MA.str.strip()

    if len(data[data.All_MA == "Bull"])*2 > stocksPerDay:
        bull = data[data.All_MA == "Bull"].sample(int(stocksPerDay/2))
    else:
        bull = data[data.All_MA == "Bull"]
    bullList = [str.strip(str(s)) for s in bull.Symbol]
    print()
    print("List of Bull Stocks \n ===================")
    print(bullList)

    if len(data[data.All_MA == "Bear"]) * 2 > stocksPerDay:
        bear = data[data.All_MA == "Bear"].sample(int(stocksPerDay/2))
    else:
        bear = data[data.All_MA == "Bear"]
    print()
    bearList = [str.strip(str(s)) for s in bear.Symbol]
    print("List of Bear Stocks \n ===================")
    print(bearList)
    print()

    buyList6030(bullList, bearList, 500)

