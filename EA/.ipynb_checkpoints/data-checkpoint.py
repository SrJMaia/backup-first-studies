import pandas as pd
import MetaTrader5 as mt5
import numpy as np
from collections import deque

ALL_PAIRS = ['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD',
             'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD','USDCHF',
             'USDJPY','AUDUSD','NZDUSD','USDCAD','AUDJPY','CADJPY','CHFJPY',
             'NZDJPY','AUDCHF','CADCHF','NZDCHF','AUDNZD','NZDCAD','AUDCAD']

def preprocess_mt5(symbol, start=0,end=70_000, time_frame=mt5.TIMEFRAME_H1,data_type='open'):
    df_rates = pd.DataFrame(mt5.copy_rates_from_pos(symbol, time_frame , start, end))
    return df_rates[data_type]


def get_data(start_pos, end_pos, time_frame):

    df = pd.DataFrame()

    for i in range(len(ALL_PAIRS)):
        df[ALL_PAIRS[i]]=preprocess_mt5(symbol=ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')

    return df


def pct_data(data, period=1):

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

    df2 = pd.DataFrame()

    for i in diff_symbols.items():
        df = pd.DataFrame()
        for j in i[1]:
            df[j]=data[j]
            if i[0] == 'gbp':
                if j == 'EURGBP':
                    df[j] = 1 / df[j]
            if i[0] == 'usd':
                if j in ['GBPUSD','AUDUSD','NZDUSD','EURUSD']:
                    df[j] = 1 / df[j]
            if i[0] == 'jpy':
                df[j] = 1 / df[j]
            if i[0] == 'chf':
                if j in ['AUDCHF','CADCHF','USDCHF','EURCHF','GBPCHF','NZDCHF']:
                    df[j] = 1 / df[j]
            if i[0] == 'nzd':
                if j in ['AUDNZD','EURNZD','GBPNZD']:
                    df[j] = 1 / df[j]
            if i[0] == 'aud':
                if j in ['EURAUD','GBPAUD']:
                    df[j] = 1 / df[j]
            if i[0] == 'cad':
                if j in ['AUDCAD','USDCAD','EURCAD','GBPCAD','NZDCAD']:
                    df[j] = 1 / df[j]
        df2[f'{i[0]}'] = df.pct_change(periods=period).sum(axis=1)*100

    return df2
