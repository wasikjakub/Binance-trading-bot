from binance.client import Client
import pandas as pd

# Trend following strategy
# if the price is incresing by x % we are Buying
# exiting when profit is above set % or loss is crossing set %

def trend_following(entry, lookback, qty, df, bought=False):
    while True:
        lookback_period = df.iloc[-lookback:]
        cumret = (lookback_period.Price.pct_change() + 1).cumprod() - 1
        if not bought:
            if cumret[cumret.last_valid_index()] > entry:
                order = Client.create_order(symbol='ETHUSDT',
                                            side='BUY',
                                            type='MARKET',
                                            quantity=qty)
                print(order)
                bought = True
                break
    if bought:
        while True:
            sincebuy = df.loc[df.Time > pd.to_datetime(order['transactTime'], unit='ms')]
            if len(sincebuy) > 1:
                sincebuyret = (sincebuy.Price.pct_change() + 1).cumprod() - 1
                last_entry = sincebuyret[sincebuyret[sincebuyret.last_valid_index()]]
                if last_entry > 0.0015 or last_entry < -0.0015:
                    order = Client.create_order(symbol='ETHUSDT',
                                                side='SELL',
                                                type='MARKET',
                                                quantitiy=qty)
                    print(order)
                    break
