import pybithumb
import numpy as np
from datetime import datetime, timedelta


coinName = "BTC"
find_days = 7

def get_ror(k=0.5):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=find_days)
    
    all_data = pybithumb.get_ohlcv(coinName, interval="day")
    df = all_data.loc[start_date:end_date].copy()
    
    
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod().iloc[-2]
    return ror

for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))
