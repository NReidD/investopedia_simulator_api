from investopedia_api import InvestopediaApi, StockTrade, OptionTrade, Expiration, OrderLimit, TransactionType, OptionScope, OptionChain
import json
from datetime import datetime, timedelta

credentials = {}
with open('credentials.json') as ifh:
    credentials = json.load(ifh)
# look at credentials_example.json
# credentials = {"username": "you@example.org", "password": "yourpassword" }
client = InvestopediaApi(credentials)

p = client.portfolio
print("\nMACD Strategy On!")
print("-------------------------------------------------")
print("\nPortfolio Details")
print("-------------------------------------------------")
print("Portfolio Value: %s" % p.account_value)
print("Cash: %s" % p.cash)
print("Buying Power: %s" % p.buying_power)
print("Annual Return Percent: %s" % p.annual_return_pct)
print("-------------------------------------------------")
stock = client.get_stock_quote("AAPL")
print(stock.__getattribute__("previous_close"))
trade3 = StockTrade(portfolio_id=p.portfolio_id, symbol='MSFT', quantity=1, transaction_type=TransactionType.BUY)
trade3.validate()
trade3.execute()