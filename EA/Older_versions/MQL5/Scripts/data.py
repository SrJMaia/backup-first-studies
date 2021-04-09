import MetaTrader5 as mt5
import pandas as pd

def diff_data(list_symbol,start,end):
    df2 = pd.DataFrame()
    for i in range(len(list_symbol)):
        df=pd.DataFrame(mt5.copy_rates_from_pos(list_symbol[i], mt5.TIMEFRAME_H1 , start, end))
        df2[list_symbol[i]] = df['close'].pct_change()
        del df
    df2['sum'] = df2.sum(axis=1)
    df2['sma'] = round(df2['sum'].rolling(5).sum()*10000,0)
    return df2['sma']


def get_data(start, end):

    data_frame = pd.DataFrame()

    pairs = [
            ['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD'],
            ['EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD'],
            ['GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD'],
            ['AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY'],
            ['AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF'],
            ['AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY'],
            ['AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD'],
            ['AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD']
            ]

    all_pairs = ['eur','gbp','usd','jpy','chf','nzd','aud','cad']

    for i in range(len(pairs)):
        data_frame[all_pairs[i]] = diff_data(list_symbol = pairs[i], start = start, end = end)
    data_frame.dropna(inplace=True)

    return data_frame
