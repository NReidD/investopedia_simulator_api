from yfinance import Screener
from yfinance import EquityQuery
from yfinance import Ticker
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import json
from investopedia_api import InvestopediaApi, StockTrade, OptionTrade, Expiration, OrderLimit, TransactionType, OptionScope, OptionChain


# Parse the JSON string
credentials = {}
with open('credentials.json') as ifh:
    credentials = json.load(ifh)
client = InvestopediaApi(credentials)

p = client.portfolio
screen = Screener()
query = EquityQuery('EQ',['region',"us"])

screen.set_default_body(query)
response = screen._fetch()
resFrame = pd.DataFrame.from_dict(response)


# Iterate over values
for value in response.values():
    fullres = pd.DataFrame.from_dict(response['finance']['result'][0])
    print(fullres.loc[0,'quotes'])

    fullres = pd.DataFrame.from_dict(response['finance']['result'][0]['quotes'])
    x=0
    while (x < fullres.columns.size):
        
        
        print(fullres.loc[x,'symbol'])
        stock = Ticker(fullres.loc[x,'symbol'])
        stock.get_news()
        analyzer = SentimentIntensityAnalyzer()
        compound_scores = []

        for o in stock.news:
            #print(o['title'])
            vs = analyzer.polarity_scores(o["title"])
            print("{:-<65} {}".format(o["title"], str(vs)))
            scores = vs
            compound_scores.append(scores['compound'])
        if (len(compound_scores)>0):
            average_compound_score = sum(compound_scores) / len(compound_scores)
            if (average_compound_score > .25):
                print("Should Buy")
                try:
                    trade3 = StockTrade(portfolio_id=p.portfolio_id, symbol=fullres.loc[x,'symbol'], quantity=1, transaction_type=TransactionType.BUY)

                    trade3.validate()
                    if (trade3._validated):
                        trade3.execute()
                    
                except:
                    continue
                    
            elif (average_compound_score < -.5):
                print("Should Short")
            else:
                print("Meh.")
        x = x+1
        