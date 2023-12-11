import pandas as pd
import matplotlib.pyplot as plt

def create_dframe(msg):                                 # Data cleaning
    df = pd.DataFrame([msg])
    df = df.loc[:,['s','E','c']]
    df.columns = ['currency', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df

def plot_prices(df):
    df.Price.plot()
    plt.xlabel('Time')
    plt.ylabel('Price($)')
    plt.title('ETH/USDT')
    plt.ticklabel_format(useOffset=False)
    plt.grid()
    plt.show()