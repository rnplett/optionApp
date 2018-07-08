import pandas as pd

from .input.settings import *
import quandl
import pymongo

from datetime import datetime, time, timedelta
from time import sleep

runTime = "5:35"
startTime = time(*(map(int, runTime.split(':'))))
while startTime > datetime.today().time():  # you can add here any additional variable to break loop if necessary
        sleep(1)  # you can change 1 sec interval to any other

print("and so it begins at {}".format(datetime.now()))

quandl.ApiConfig.api_key = QUANDL_API_KEY

#
#  Establish Weekly option list inside the SP500
#===========================================================================

w = pd.ExcelFile('http://www.cboe.com/publish/weelkysmf/weeklysmf.xls')
weeklies = w.parse().iloc[:,[0]]
weeklies.columns = ['Symbol']
sp500 = pd.read_csv('https://datahub.io/core/s-and-p-500-companies/r/constituents.csv')
symbolList = pd.merge(weeklies,sp500).iloc[:,[0]].transpose().values.tolist()[0]

f = open('D:\\Users\\Roland\\Google Drive\\TodaysPicks.csv','w') # Workspaces workstation - Windows 10

stocksPerDay = 20

def bollinger_bands(df, m, n):
    """

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    MA = pd.Series(df['Close'].rolling(n, min_periods=n).mean())
    MSD = pd.Series(df['Close'].rolling(n, min_periods=n).std())
    b1 = MA + m*MSD
    B3 = pd.Series(b1, name='BBU_' + str(n))
    df = df.join(B3)
    b1 = MA - m*MSD
    B4 = pd.Series(b1, name='BBD_' + str(n))
    df = df.join(B4)
    return df

def keltner_channel(df, m, n):
    """Calculate Keltner Channel for given data.
    true range=max[(high - low), abs(high - previous close), abs (low - previous close)]

    :param df: pandas.DataFrame
    :param n:
    :return: pandas.DataFrame
    """
    KelChM = pd.Series(df['Close'].rolling(n, min_periods=n).mean(),name='KelChM')
    r1 = df['High']-df['Low']
    r2 = (df['High']-df['Close'].shift(1)).abs()
    r3 = (df['Low']-df['Close'].shift(1)).abs()
    TR = pd.DataFrame({'r1':r1,'r2':r2, 'r3':r3}).max(axis=1)
    ATR = pd.Series(TR.rolling(n, min_periods=n).mean())
    KelChU = pd.Series(KelChM + ATR*m, name='KelChU')
    KelChD = pd.Series(KelChM - ATR*m, name='KelChD')
    df = df.join(KelChM)
    df = df.join(KelChU)
    df = df.join(KelChD)
    return df

def squeeze(df):
    df = bollinger_bands(df,2,20)
    df = keltner_channel(df,1.5,20)
    df = df.join(pd.Series((df["BBU_20"] < df["KelChU"]) & (df["BBD_20"] > df["KelChD"]), name='Squeeze'))
    return(df)

def squeezeLen(df):
    l = 0
    for x in range(1,26):
        if df["Squeeze"].iloc[-x]:
            l = l + 1
        else:
            break
    return l

def filterMA(a):
    a = a.sort_values('Date', ascending=False).reset_index(drop=True)
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

    #  Calculate the date range for the quandl query
    # *** today =
    #
    base = datetime.today()
    dateList = [(base - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, 200)]

    for s in symbolList:
        try:
            p = quandl.get_table('SHARADAR/SEP', ticker=s, date=dateList,
                                       qopts={"columns": ["ticker", "date", "open", "high", "low", "close"]})
            p.columns = ["Symbol","Date","Open","High","Low","Close"]
        except:
            print("Quandl read error")
        try:
            r = filterMA(p)
            p = squeeze(p)
            sq = squeezeLen(p)

            wMA = r[3]
            allMA = r[0]
            stochastic = r[1]
            price = r[2]
            print("{0:<8s}{1:8.2f} {2:<10s}{3:<10s}    {4:}      {5:10s}{6:5.2f}".
                  format(s, price, wMA, allMA, sq, "NA", stochastic))
            t = "{0:<8s},{1:8.2f},{2:<10s},{3:<10s},{4:},{5:<10s},{6:5.2f}\n". \
                format(s, price, wMA, allMA, sq, "   NA", stochastic)
            f.write(t)
        except Exception as e:
            print(s + " - data error: " + str(e))

    f.close()

    data = pd.read_csv('D:\\Users\\Roland\\Google Drive\\TodaysPicks.csv')
    data.Weekly_MA = data.Weekly_MA.str.strip()

    bull = data[data.Weekly_MA == "Bull"]
    print()
    print("List of Bull Stocks \n===================")
    print(bull.loc[:,["Symbol","Squeeze"]].sort_values(by='Squeeze', ascending=False))
    print()

    bear = data[data.Weekly_MA == "Bear"]
    print()
    print("List of Bear Stocks \n===================")
    print(bear.loc[:,["Symbol","Squeeze"]].sort_values(by='Squeeze', ascending=False))
    print()
