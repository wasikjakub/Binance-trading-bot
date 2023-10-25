import websocket
import json
import pandas as pd

def trading_bot(usd):

    endpoint = 'wss://stream.binance.com:9443/ws'

    msg = json.dumps({
        "method": "SUBSCRIBE",
        "params": ['ethusdt@kline_1m', 'ethusdt@kline_15m'],
        "id": 1
    })

    returns = {'1m': 0, '15m': 0}
    open_position = False
    printing = True
    printing2 = True
    buy_price = 0

    def on_open(ws):
        ws.send(msg)

    def on_message(ws, message):
        nonlocal usd, open_position, printing, printing2, buy_price
        out = json.loads(message)
        df = pd.DataFrame(out['k'], index=[pd.to_datetime(out['E'], unit='ms')])[['s', 'i', 'o', 'c']]
        df['ret ' + df.i.values[0]] = float(df.c) / float(df.o) - 1
        returns[df.i.values[0]] = float(df.c) / float(df.o) - 1
        if printing:
            print('Waiting for buying condition to be fulfilled ...')
            printing = False
        if not open_position and returns['15m'] < 0 and returns['1m'] > 0:
            buy_price = float(df.c)
            open_position = True
            print('bought for ' + str(buy_price))
        if open_position:
            if printing2:
                print('target profit: ' + str(round(buy_price * 1.002, 2)))
                print('stop loss: ' + str(round(buy_price * 0.998, 2))) 
                print('USD: ' + str(usd))
                print('current price: ' + str(float(df.c)))
                printing2 = False
            if float(df.c) > buy_price * 1.002:
                print('SOLD! profit made: ' + str(round((float(df.c) - buy_price), 2)))
                open_position = False
                printing = True
                printing2 = True
                usd = usd * (((float(df.c) - buy_price) / 100) + 1)
                print('USD: ' + str(usd))
                print('--------------------')
            elif float(df.c) < buy_price * 0.998:
                print('LOSS STOPPED! loss: ' + str(round((float(df.c) - buy_price), 2)))
                open_position = False
                printing = True
                printing2 = True
                usd = usd * (((float(df.c) - buy_price) / 100) + 1)
                print('USD: ' + str(usd))
                print('--------------------')

    ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_open=on_open)
    try:
        ws.run_forever()
    except Exception as error:
        print('error')