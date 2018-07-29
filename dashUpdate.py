from IBapiMod import *
import logging
import datetime
import pandas as pd
from pandas import DataFrame
import googleApi as g
from inputs.settings import *

logging.basicConfig(level=logging.INFO)

appR = TestApp("127.0.0.1", 7401, 1)
appN = TestApp("127.0.0.1", 7402, 1)
RANGE = "Spreads!A7"

credentials = g.service_account.Credentials.from_service_account_file(
    g.CLIENT_SECRET_FILE)
scoped_credentials = credentials.with_scopes(
    [g.SCOPES])
authed_session = g.AuthorizedSession(scoped_credentials)

d = datetime.datetime.today().strftime('%Y-%m-%d-%H-%M-%S')

print("\nDate: {}\n=================\n".format(d))

appR.reqAccountSummary(1,"All", "AccountType,NetLiquidation,TotalCashValue")
appN.reqAccountSummary(2,"All", "AccountType,NetLiquidation,TotalCashValue")

appR.reqCurrentTime()
appN.reqPositions()

time.sleep(10)


appR.disconnect()
appN.disconnect()
