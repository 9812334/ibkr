from ib_async import *

util.startLoop()

ib = IB()
ib.connect("127.0.0.1", 4001, clientId=16)

from IPython.display import display, clear_output
import pandas as pd

df = pd.DataFrame(index=range(5), columns="bidSize bidPrice askPrice askSize".split())

# NQM2024 contract
contract = Contract(conId=620730920)
ib.qualifyContracts(contract)

ticker = ib.reqMktDepth(contract)

def onTickerUpdate(ticker):
    bids = ticker.domBids
    for i in range(5):
        df.iloc[i, 0] = bids[i].size if i < len(bids) else 0
        df.iloc[i, 1] = bids[i].price if i < len(bids) else 0
    asks = ticker.domAsks
    for i in range(5):
        df.iloc[i, 2] = asks[i].price if i < len(asks) else 0
        df.iloc[i, 3] = asks[i].size if i < len(asks) else 0
    clear_output(wait=True)
    display(df)


ticker.updateEvent += onTickerUpdate

IB.sleep(15)

