import json
import eikon as ek
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

from investopedia_api import InvestopediaApi, StockTrade, OptionTrade, Expiration, OrderLimit, TransactionType, OptionScope, OptionChain

ek.set_app_key('0a320f36e7e0448cb8842ec884bb278d1c54af3c')

df, err = ek.get_data(instruments = 'SCREEN(U(IN(Equity(active,public,primary))), IN(TR.HQCountryCode,"US"), TR.TRESGCScore>=50, Contains(TR.TRESGCScoreGrade,"A"), CURN=USD)', fields = list("TR.CommonName"))
credentials = {}
with open('credentials.json') as ifh:
    credentials = json.load(ifh)
client = InvestopediaApi(credentials)

p = client.portfolio
# print(df)
x=0
analyzer = SentimentIntensityAnalyzer()


while (x < df.count(axis='columns').size):
    compound_scores = []

    print(df.loc[x].loc['Instrument'])
    headlines = None
    try:
        headlines = ek.get_news_headlines("( R:"+df.loc[x].loc['Instrument']+" ) and Language:LEN AND ( Source:RTRS OR Source:FT )", count = 100)
    finally:
            print("go")
    for o in headlines['text']:
        #print(o['title'])
        vs = analyzer.polarity_scores(o)
        print("{:-<65} {}".format(o["title"], str(vs)))
        scores = vs
        compound_scores.append(scores['compound'])
    if (len(compound_scores)>0):
        average_compound_score = sum(compound_scores) / len(compound_scores)
        if (average_compound_score > .25):
            print("Should Buy")
            trade3 = StockTrade(portfolio_id=p.portfolio_id, symbol=str(df.loc[x].loc['Instrument']).split('.')[0], quantity=1, transaction_type=TransactionType.BUY)
            trade3.validate()
            if (trade3._validated):
                trade3.execute()   
        elif (average_compound_score < -.5):
            print("Should Short")
        else:
            print("Meh.")
    x = x+1

   
