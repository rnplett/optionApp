## Financial market libraries

NOTE: I just reorganized my folders and broke a number of paths that need fixing. Please consider these scripts as educational and not a library to use out of the box.

The libraries in this repo are a combination of code I've found in other repos and my own. Once they start generating a lot of income for me I may keep them a little more privately but I hope they can be helpful for people who are dabbling in python automation of trading activities.

#### API libraries
I use IB's Trader Workstation (TWS) as my trading platform and as a result the IBapiMod library contains an API object definition that interacts with TWS locally on my PC.

The googleApi library is used with limited success to interact with my financial dashboard in Google sheets to record current account balances and trade logs.

The emailApi is simply used for sending alerts to my SMS address and email reports to my regular email.

#### Primary Scripts
There are three main scripts that I use regularly.

1) TodaysPicks - is a stock screening script that looks at the last 200 days of EOD data for the S&P 500 to identify trending stocks that have pulled back past the 8ma and haven't crossed the 21ma. I've also started including the Squeeze indictor into the screening list.

2) buyList6030 - is a script for purchasing a list of spreads based on a prescreened list of underlying stocks. I used this in combination with the screening script inside my demo account but haven't achieved consistent results yet.

3) spreadLogUpdate - is the update script that keeps my Google sheets dashboard up to date with account balances and a log of trades. This script is a work in progress.
