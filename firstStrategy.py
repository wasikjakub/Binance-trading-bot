import websocket
import json
import pandas as pd

def ConnectToStream():
    return json.dumps({
                        "method": "SUBSCRIBE",
                        "params": ['ethusdt@kline_1m',
                                'ethusdt@kline_15m'],
                                "id":1})

def SimulationTrade(msg, endpoint, usd, open_position):
    returns = {'1m': 0, '15m':0}

    def on_open(ws): 
        ws.send(msg)

    def on_message(ws, message):
        global df, open_position, buy_price, usd, loss_counter, profit_counter
        out = json.loads(message)
        df = pd.DataFrame(out['k'],index=[pd.to_datetime(out['E'], unit='ms')])[['s','i','o','c']]
        df['ret ' + df.i.values[0]] = float(df.c)/float(df.o) - 1
        returns[df.i.values[0]] = float(df.c)/float(df.o) - 1
        print(df)
        if not open_position and returns['15m'] < 0 and returns['1m'] > 0:
            buy_price = float(df.c)
            open_position = True 
            print('bought for ' + str(buy_price))
        if open_position:
            print('target profit: ' + str(buy_price * 1.002))
            print('stop loss: ' + str(buy_price * 0.998))
            print('USD: ' + str(usd))
            if float(df.c) > buy_price * 1.002:
                print('SOLD! profit made: ' + str(float(df.c) - buy_price))
                open_position = False
                usd = usd * (((float(df.c) - buy_price) / 100) + 1)
                profit_counter += 1
                print('profits: ' + profit_counter)
            elif float(df.c) < buy_price * 0.998:
                print('LOSS STOPPED! loss: ' + str(float(df.c) - buy_price))
                open_position = False
                usd = usd * (((float(df.c) - buy_price) / 100) + 1)
                loss_counter += 1
                print('losses: ' +loss_counter)

    ws = websocket.WebSocketApp(endpoint, on_message=on_message, on_open=on_open)

    ws.run_forever()


# msg = ConnectToStream()
# endpoint = 'wss://stream.binance.com:9443/ws' 
# open_position=False
# SimulationTrade(msg, endpoint, usd=1000,open_position=False)