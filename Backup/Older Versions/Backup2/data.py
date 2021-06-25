import pandas as pd
import MetaTrader5 as mt5
import numpy as np

ALL_PAIRS_OPEN = ['EURCHF_Open','EURGBP_Open','EURJPY_Open','EURNZD_Open','EURUSD_Open','EURAUD_Open','EURCAD_Open',
                  'GBPAUD_Open','GBPCHF_Open','GBPJPY_Open','GBPCAD_Open','GBPUSD_Open','GBPNZD_Open','USDCHF_Open',
                  'USDJPY_Open','AUDUSD_Open','NZDUSD_Open','USDCAD_Open','AUDJPY_Open','CADJPY_Open','CHFJPY_Open',
                  'NZDJPY_Open','AUDCHF_Open','CADCHF_Open','NZDCHF_Open','AUDNZD_Open','NZDCAD_Open','AUDCAD_Open']

ALL_PAIRS_CLOSE = ['EURCHF_Close','EURGBP_Close','EURJPY_Close','EURNZD_Close','EURUSD_Close','EURAUD_Close','EURCAD_Close',
                  'GBPAUD_Close','GBPCHF_Close','GBPJPY_Close','GBPCAD_Close','GBPUSD_Close','GBPNZD_Close','USDCHF_Close',
                  'USDJPY_Close','AUDUSD_Close','NZDUSD_Close','USDCAD_Close','AUDJPY_Close','CADJPY_Close','CHFJPY_Close',
                  'NZDJPY_Close','AUDCHF_Close','CADCHF_Close','NZDCHF_Close','AUDNZD_Close','NZDCAD_Close','AUDCAD_Close']

ALL_PAIRS_HIGH = ['EURCHF_High','EURGBP_High','EURJPY_High','EURNZD_High','EURUSD_High','EURAUD_High','EURCAD_High',
                  'GBPAUD_High','GBPCHF_High','GBPJPY_High','GBPCAD_High','GBPUSD_High','GBPNZD_High','USDCHF_High',
                  'USDJPY_High','AUDUSD_High','NZDUSD_High','USDCAD_High','AUDJPY_High','CADJPY_High','CHFJPY_High',
                  'NZDJPY_High','AUDCHF_High','CADCHF_High','NZDCHF_High','AUDNZD_High','NZDCAD_High','AUDCAD_High']

ALL_PAIRS_LOW = ['EURCHF_Low','EURGBP_Low','EURJPY_Low','EURNZD_Low','EURUSD_Low','EURAUD_Low','EURCAD_Low',
                  'GBPAUD_Low','GBPCHF_Low','GBPJPY_Low','GBPCAD_Low','GBPUSD_Low','GBPNZD_Low','USDCHF_Low',
                  'USDJPY_Low','AUDUSD_Low','NZDUSD_Low','USDCAD_Low','AUDJPY_Low','CADJPY_Low','CHFJPY_Low',
                  'NZDJPY_Low','AUDCHF_Low','CADCHF_Low','NZDCHF_Low','AUDNZD_Low','NZDCAD_Low','AUDCAD_Low']


ALL_PAIRS = ['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD',
             'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD','USDCHF',
             'USDJPY','AUDUSD','NZDUSD','USDCAD','AUDJPY','CADJPY','CHFJPY',
             'NZDJPY','AUDCHF','CADCHF','NZDCHF','AUDNZD','NZDCAD','AUDCAD']

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
                x = ALL_PAIRS_OPEN
            elif only_one == 'close':
                x = ALL_PAIRS_CLOSE
            elif only_one == 'high':
                x = ALL_PAIRS_HIGH
            elif only_one == 'low':
                x = ALL_PAIRS_LOW

            for i in range(len(x)):
                df[x[i]]=preprocess_mt5(symbol=ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type=only_one)
        elif all_four:
            for i in range(len(ALL_PAIRS)):
                df[ALL_PAIRS_OPEN[i]]=preprocess_mt5(symbol=ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')
                df[ALL_PAIRS_CLOSE[i]]=preprocess_mt5(symbol=ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='close')
                df[ALL_PAIRS_HIGH[i]]=preprocess_mt5(symbol=ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='high')
                df[ALL_PAIRS_LOW[i]]=preprocess_mt5(symbol=ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='low')

    if monte_carlo:
        return df.sample(frac=1).reset_index(drop=True)
    else:
        return df


def pct_data(data, period=1, complement='_Open'):
    """
    No futuro colcoar a soma, subtração de todos os 4
    """

    diff_symbols = {
        'eur':['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD'],
        'gbp':['EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD'],
        'usd':['GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD'],
        'jpy':['AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY'],
        'chf':['AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF'],
        'nzd':['AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY'],
        'aud':['AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD'],
        'cad':['AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD']
    }

    for i in diff_symbols.items():
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
