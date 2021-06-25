import pandas as pd
import MetaTrader5 as mt5
import numpy as np
from collections import deque

ALL_PAIRS = ('EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD',
             'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD','USDCHF',
             'USDJPY','AUDUSD','NZDUSD','USDCAD','AUDJPY','CADJPY','CHFJPY',
             'NZDJPY','AUDCHF','CADCHF','NZDCHF','AUDNZD','NZDCAD','AUDCAD')

ALL_PAIRS_BUY = (
    'EURCHF_buy','EURGBP_buy','EURJPY_buy','EURNZD_buy','EURUSD_buy','EURAUD_buy','EURCAD_buy',
    'GBPAUD_buy','GBPCHF_buy','GBPJPY_buy','GBPCAD_buy','GBPUSD_buy','GBPNZD_buy','USDCHF_buy',
    'USDJPY_buy','AUDUSD_buy','NZDUSD_buy','USDCAD_buy','AUDJPY_buy','CADJPY_buy','CHFJPY_buy',
    'NZDJPY_buy','AUDCHF_buy','CADCHF_buy','NZDCHF_buy','AUDNZD_buy','NZDCAD_buy','AUDCAD_buy'
)

ALL_PAIRS_SELL = (
    'EURCHF_sell','EURGBP_sell','EURJPY_sell','EURNZD_sell','EURUSD_sell','EURAUD_sell','EURCAD_sell',
    'GBPAUD_sell','GBPCHF_sell','GBPJPY_sell','GBPCAD_sell','GBPUSD_sell','GBPNZD_sell','USDCHF_sell',
    'USDJPY_sell','AUDUSD_sell','NZDUSD_sell','USDCAD_sell','AUDJPY_sell','CADJPY_sell','CHFJPY_sell',
    'NZDJPY_sell','AUDCHF_sell','CADCHF_sell','NZDCHF_sell','AUDNZD_sell','NZDCAD_sell','AUDCAD_sell'
)

SPLIT_PAIRS = (
    ('eur','chf'),('eur','gbp'),('eur','jpy'),('eur','nzd'),('eur','usd'),
    ('eur','aud'),('eur','cad'),('gbp','aud'),('gbp','chf'),('gbp','jpy'),
    ('gbp','cad'),('gbp','usd'),('gbp','nzd'),('usd','chf'),('usd','jpy'),
    ('aud','usd'),('nzd','usd'),('usd','cad'),('aud','jpy'),('cad','jpy'),
    ('chf','jpy'),('nzd','jpy'),('aud','chf'),('cad','chf'),('nzd','chf'),
    ('aud','nzd'),('nzd','cad'),('aud','cad')
)

def preprocess_mt5(symbol, start=0,end=70_000, time_frame=mt5.TIMEFRAME_H1,data_type='open'):
    df_rates = pd.DataFrame(mt5.copy_rates_from_pos(symbol, time_frame , start, end))
    return df_rates[data_type]


def get_data(start_pos, end_pos, time_frame):

    df = pd.DataFrame()

    for i in range(len(ALL_PAIRS)):
        df[ALL_PAIRS[i]]=preprocess_mt5(symbol=ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')

    return df


def pct_data(data, period=1):

    diff_symbols = (
        ('eur',('EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD')),
        ('gbp',('EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD')),
        ('usd',('GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD')),
        ('jpy',('AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY')),
        ('chf',('AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF')),
        ('nzd',('AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY')),
        ('aud',('AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD')),
        ('cad',('AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD'))
        )

    for i in diff_symbols:
        df = pd.DataFrame()
        for j in i[1]:
            df[j]=data[j].pct_change(period)
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


def signals(data):

    for index, value in enumerate(SPLIT_PAIRS):

        pair1 = data[value[0]].to_numpy()
        pair2 = data[value[1]].to_numpy()

        std1 = np.std(pair1)
        std2 = np.std(pair2)

        data[ALL_PAIRS_BUY[index]] = pd.Series(((pair1 > pair2)))
        data[ALL_PAIRS_SELL[index]] = pd.Series(((pair1 < pair2)))

    return data
