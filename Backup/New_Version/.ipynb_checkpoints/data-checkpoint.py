import pandas as pd
import MetaTrader5 as mt5
import numpy as np
from constants import Pairs

def preprocess_mt5(symbol, start=0,end=70_000, time_frame=mt5.TIMEFRAME_H1,data_type='close'):
    df_rates = pd.DataFrame(mt5.copy_rates_from_pos(symbol, time_frame , start, end))
    return df_rates[data_type]


def get_data(start_pos, end_pos, time_frame, all_four = False, one_pair = False, symbol = 'EURUSD', only_one = 'open', monte_carlo=False):
    """
    Se all_four for False, passar parametro only_one para qual dos 4 OHLC irá querer
    """

    df = pd.DataFrame()

    if one_pair:
        if not all_four:
            df[symbol]=preprocess_mt5(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type=only_one)
        elif all_four:
            df[f'{symbol}_Open']=preprocess_mt5(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')
            df[f'{symbol}_Close']=preprocess_mt5(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='close')
            df[f'{symbol}_High']=preprocess_mt5(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='high')
            df[f'{symbol}_Low']=preprocess_mt5(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='low')
    elif not one_pair:
        x = []
        if not all_four:
            if only_one == 'open':
                x = Pairs.ALL_PAIRS_OPEN
            elif only_one == 'close':
                x = Pairs.ALL_PAIRS_CLOSE
            elif only_one == 'high':
                x = Pairs.ALL_PAIRS_HIGH
            elif only_one == 'low':
                x = Pairs.ALL_PAIRS_LOW

            for i in range(len(x)):
                df[x[i]]=preprocess_mt5(symbol=Pairs.ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type=only_one)
        elif all_four:
            for i in range(len(Pairs.ALL_PAIRS)):
                df[Pairs.ALL_PAIRS_OPEN[i]]=preprocess_mt5(symbol=Pairs.ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')
                df[Pairs.ALL_PAIRS_CLOSE[i]]=preprocess_mt5(symbol=Pairs.ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='close')
                df[Pairs.ALL_PAIRS_HIGH[i]]=preprocess_mt5(symbol=Pairs.ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='high')
                df[Pairs.ALL_PAIRS_LOW[i]]=preprocess_mt5(symbol=Pairs.ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='low')

    if monte_carlo:
        return df.sample(frac=1).reset_index(drop=True)
    else:
        return df


def pct_data(data, period=1, complement='_Open'):
    """
    No futuro colcoar a soma, subtração de todos os 4
    """

    for i in Pairs.DIFF_SYMBOLS:
        df = pd.DataFrame()
        for j in i[1]:
            df[j]=data[j+complement].pct_change(periods=period)
            if i[0] == 'gbp':
                if j == 'EURGBP':
                    df[j] = df[j] * -1
            if i[0] == 'usd':
                if j in ['GBPUSD','AUDUSD','NZDUSD','EURUSD']:
                    df[j] = df[j] * -1
            if i[0] == 'jpy':
                df[j] = df[j] * -1
            if i[0] == 'chf':
                if j in ['AUDCHF','CADCHF','USDCHF','EURCHF','GBPCHF','NZDCHF']:
                    df[j] = df[j] * -1
            if i[0] == 'nzd':
                if j in ['AUDNZD','EURNZD','GBPNZD']:
                    df[j] = df[j] * -1
            if i[0] == 'aud':
                if j in ['EURAUD','GBPAUD']:
                    df[j] = df[j] * -1
            if i[0] == 'cad':
                if j in ['AUDCAD','USDCAD','EURCAD','GBPCAD','NZDCAD']:
                    df[j] = df[j] * -1
        data[f'{i[0]}'] = df.sum(axis=1)*100

    return data


def walk_forward_split(data):

    tot_len = len(data)

    split1 = int(round(tot_len * 0.105, 0))
    split2 = int(round(tot_len * 0.14, 0))
    split3 = int(round(tot_len * 0.245, 0))
    split4 = int(round(tot_len * 0.28, 0))
    split5 = int(round(tot_len * 0.385, 0))
    split6 = int(round(tot_len * 0.42, 0))
    split7 = int(round(tot_len * 0.525, 0))
    split8 = int(round(tot_len * 0.56, 0))
    split9 = int(round(tot_len * 0.665, 0))
    split10 = int(round(tot_len * 0.7, 0))

    walk1 = data.iloc[:split1]
    test1 = data.iloc[split1:split2]
    walk2 = data.iloc[split2:split3]
    test2 = data.iloc[split3:split4]
    walk3 = data.iloc[split4:split5]
    test3 = data.iloc[split5:split6]
    walk4 = data.iloc[split6:split7]
    test4 = data.iloc[split7:split8]
    walk5 = data.iloc[split8:split9]
    test5 = data.iloc[split9:split10]
    final = data.iloc[split10:]

    x = len(walk1) + len(test1) + len(walk2) + len(test2) + len(walk3) + len(test3) + len(walk4) + len(test4) + len(walk5) + len(test5) + len(final)
    y = len(data)

    print(f'Dados tem len de {y} e o split tem len de {x}.')

    walk1 = pandas_to_array(walk1)
    test1 = pandas_to_array(test1)
    walk2 = pandas_to_array(walk2)
    test2 = pandas_to_array(test2)
    walk3 = pandas_to_array(walk3)
    test3 = pandas_to_array(test3)
    walk4 = pandas_to_array(walk4)
    test4 = pandas_to_array(test4)
    walk5 = pandas_to_array(walk5)
    test5 = pandas_to_array(test5)
    final = pandas_to_array(final)
    data_numpy = pandas_to_array(data)

    return walk1, test1, walk2, test2, walk3, test3, walk4, test4, walk5, test5, final, data_numpy


def pandas_to_array(data):

    array = np.array(
            [
                np.transpose(np.array(data[['EURUSD_Open','EURUSD_buy','EURUSD_sell','EURUSD_Open','EURUSD_High','EURUSD_Low']])),
                np.transpose(np.array(data[['EURCHF_Open','EURCHF_buy','EURCHF_sell','EURCHF_Open','EURCHF_High','EURCHF_Low']])),
                np.transpose(np.array(data[['EURGBP_Open','EURGBP_buy','EURGBP_sell','EURGBP_Open','EURGBP_High','EURGBP_Low']])),
                np.transpose(np.array(data[['EURJPY_Open','EURJPY_buy','EURJPY_sell','EURJPY_Open','EURJPY_High','EURJPY_Low']])),
                np.transpose(np.array(data[['EURNZD_Open','EURNZD_buy','EURNZD_sell','EURNZD_Open','EURNZD_High','EURNZD_Low']])),
                np.transpose(np.array(data[['EURAUD_Open','EURAUD_buy','EURAUD_sell','EURAUD_Open','EURAUD_High','EURAUD_Low']])),
                np.transpose(np.array(data[['EURCAD_Open','EURCAD_buy','EURCAD_sell','EURCAD_Open','EURCAD_High','EURCAD_Low']])),
                np.transpose(np.array(data[['GBPAUD_Open','GBPAUD_buy','GBPAUD_sell','EURGBP_Open','GBPAUD_High','GBPAUD_Low']])),
                np.transpose(np.array(data[['GBPCHF_Open','GBPCHF_buy','GBPCHF_sell','EURGBP_Open','GBPCHF_High','GBPCHF_Low']])),
                np.transpose(np.array(data[['GBPJPY_Open','GBPJPY_buy','GBPJPY_sell','EURGBP_Open','GBPJPY_High','GBPJPY_Low']])),
                np.transpose(np.array(data[['GBPCAD_Open','GBPCAD_buy','GBPCAD_sell','EURGBP_Open','GBPCAD_High','GBPCAD_Low']])),
                np.transpose(np.array(data[['GBPUSD_Open','GBPUSD_buy','GBPUSD_sell','EURGBP_Open','GBPUSD_High','GBPUSD_Low']])),
                np.transpose(np.array(data[['GBPNZD_Open','GBPNZD_buy','GBPNZD_sell','EURGBP_Open','GBPNZD_High','GBPNZD_Low']])),
                np.transpose(np.array(data[['USDCHF_Open','USDCHF_buy','USDCHF_sell','EURUSD_Open','USDCHF_High','USDCHF_Low']])),
                np.transpose(np.array(data[['USDJPY_Open','USDJPY_buy','USDJPY_sell','EURUSD_Open','USDJPY_High','USDJPY_Low']])),
                np.transpose(np.array(data[['AUDUSD_Open','AUDUSD_buy','AUDUSD_sell','EURAUD_Open','AUDUSD_High','AUDUSD_Low']])),
                np.transpose(np.array(data[['NZDUSD_Open','NZDUSD_buy','NZDUSD_sell','EURNZD_Open','NZDUSD_High','NZDUSD_Low']])),
                np.transpose(np.array(data[['USDCAD_Open','USDCAD_buy','USDCAD_sell','EURUSD_Open','USDCAD_High','USDCAD_Low']])),
                np.transpose(np.array(data[['AUDJPY_Open','AUDJPY_buy','AUDJPY_sell','EURAUD_Open','AUDJPY_High','AUDJPY_Low']])),
                np.transpose(np.array(data[['CADJPY_Open','CADJPY_buy','CADJPY_sell','EURCAD_Open','CADJPY_High','CADJPY_Low']])),
                np.transpose(np.array(data[['CHFJPY_Open','CHFJPY_buy','CHFJPY_sell','EURCHF_Open','CHFJPY_High','CHFJPY_Low']])),
                np.transpose(np.array(data[['NZDJPY_Open','NZDJPY_buy','NZDJPY_sell','EURNZD_Open','NZDJPY_High','NZDJPY_Low']])),
                np.transpose(np.array(data[['AUDCHF_Open','AUDCHF_buy','AUDCHF_sell','EURAUD_Open','AUDCHF_High','AUDCHF_Low']])),
                np.transpose(np.array(data[['CADCHF_Open','CADCHF_buy','CADCHF_sell','EURCAD_Open','CADCHF_High','CADCHF_Low']])),
                np.transpose(np.array(data[['NZDCHF_Open','NZDCHF_buy','NZDCHF_sell','EURNZD_Open','NZDCHF_High','NZDCHF_Low']])),
                np.transpose(np.array(data[['AUDNZD_Open','AUDNZD_buy','AUDNZD_sell','EURAUD_Open','AUDNZD_High','AUDNZD_Low']])),
                np.transpose(np.array(data[['NZDCAD_Open','NZDCAD_buy','NZDCAD_sell','EURNZD_Open','NZDCAD_High','NZDCAD_Low']])),
                np.transpose(np.array(data[['AUDCAD_Open','AUDCAD_buy','AUDCAD_sell','EURAUD_Open','AUDCAD_High','AUDCAD_Low']])),
            ], dtype=np.float64)
    return array
