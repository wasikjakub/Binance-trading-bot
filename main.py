from binance.client import Client
import sqlalchemy
import BinanceKeys
import pandas as pd
import asyncio
import websockets
import json

api_key = BinanceKeys.api_key           # Hidden API data
api_secret = BinanceKeys.api_secret  

stream = websockets.connect("wss://stream.binance.com:9443/stream?streams=ethusdt@miniTicker")

async def main():                                    # Collecting live data throught websocket(server connection) 

    client = Client(api_key, api_secret)
    df = pd.DataFrame()
    open_position = False
    
    async with stream as reciver:
        while True:
            data = await reciver.recv()
            data = json.loads(data)['data']
            df = pd.concat([df, createframe(data)])  # Saving out data to one df
            print(df)        

    
def createframe(msg):                                 # Data cleaning
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','c']]
    df.columns = ['currency', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())