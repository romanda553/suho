import pybithumb
import numpy as np
from datetime import datetime, timedelta

coinName = "BTC"
find_days = 7

def find_best_k():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=find_days)

    all_data = pybithumb.get_ohlcv(coinName, interval="day")
    df = all_data.loc[start_date:end_date].copy()

    k_values = np.arange(0.1, 1.0, 0.1)
    best_k = None
    best_ror = 0

    for k in k_values:
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)

        df['ror'] = np.where(df['high'] > df['target'],
                             df['close'] / df['target'],
                             1)

        ror = df['ror'].cumprod().iloc[-2]

        if ror > best_ror:
            best_ror = ror
            best_k = k

    return best_k, best_ror


best_k, best_ror = find_best_k()
print(f"Best k: {best_k}, Best ROI: {best_ror}")