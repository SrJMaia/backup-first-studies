import pandas as pd
import numpy as np
from collections import deque
import indicators as indi

SPLIT_PAIRS = np.array([
    ['eur','chf'],['eur','gbp'],['eur','jpy'],['eur','nzd'],['eur','usd'],
    ['eur','aud'],['eur','cad'],['gbp','aud'],['gbp','chf'],['gbp','jpy'],
    ['gbp','cad'],['gbp','usd'],['gbp','nzd'],['usd','chf'],['usd','jpy'],
    ['aud','usd'],['nzd','usd'],['usd','cad'],['aud','jpy'],['cad','jpy'],
    ['chf','jpy'],['nzd','jpy'],['aud','chf'],['cad','chf'],['nzd','chf'],
    ['aud','nzd'],['nzd','cad'],['aud','cad']
])

ALL_PAIRS_OPEN = ['EURCHF_Open','EURGBP_Open','EURJPY_Open','EURNZD_Open','EURUSD_Open','EURAUD_Open','EURCAD_Open',
                  'GBPAUD_Open','GBPCHF_Open','GBPJPY_Open','GBPCAD_Open','GBPUSD_Open','GBPNZD_Open','USDCHF_Open',
                  'USDJPY_Open','AUDUSD_Open','NZDUSD_Open','USDCAD_Open','AUDJPY_Open','CADJPY_Open','CHFJPY_Open',
                  'NZDJPY_Open','AUDCHF_Open','CADCHF_Open','NZDCHF_Open','AUDNZD_Open','NZDCAD_Open','AUDCAD_Open']

ALL_PAIRS_BUY = np.array([
    'EURCHF_buy','EURGBP_buy','EURJPY_buy','EURNZD_buy','EURUSD_buy','EURAUD_buy','EURCAD_buy',
    'GBPAUD_buy','GBPCHF_buy','GBPJPY_buy','GBPCAD_buy','GBPUSD_buy','GBPNZD_buy','USDCHF_buy',
    'USDJPY_buy','AUDUSD_buy','NZDUSD_buy','USDCAD_buy','AUDJPY_buy','CADJPY_buy','CHFJPY_buy',
    'NZDJPY_buy','AUDCHF_buy','CADCHF_buy','NZDCHF_buy','AUDNZD_buy','NZDCAD_buy','AUDCAD_buy'
])

ALL_PAIRS_SELL = np.array([
    'EURCHF_sell','EURGBP_sell','EURJPY_sell','EURNZD_sell','EURUSD_sell','EURAUD_sell','EURCAD_sell',
    'GBPAUD_sell','GBPCHF_sell','GBPJPY_sell','GBPCAD_sell','GBPUSD_sell','GBPNZD_sell','USDCHF_sell',
    'USDJPY_sell','AUDUSD_sell','NZDUSD_sell','USDCAD_sell','AUDJPY_sell','CADJPY_sell','CHFJPY_sell',
    'NZDJPY_sell','AUDCHF_sell','CADCHF_sell','NZDCHF_sell','AUDNZD_sell','NZDCAD_sell','AUDCAD_sell'
])

SIGNAL_LIST = np.array([
    ['eur_signal','chf_signal'],['eur_signal','gbp_signal'],['eur_signal','jpy_signal'],['eur_signal','nzd_signal'],['eur_signal','usd_signal'],
    ['eur_signal','aud_signal'],['eur_signal','cad_signal'],['gbp_signal','aud_signal'],['gbp_signal','chf_signal'],['gbp_signal','jpy_signal'],
    ['gbp_signal','cad_signal'],['gbp_signal','usd_signal'],['gbp_signal','nzd_signal'],['usd_signal','chf_signal'],['usd_signal','jpy_signal'],
    ['aud_signal','usd_signal'],['nzd_signal','usd_signal'],['usd_signal','cad_signal'],['aud_signal','jpy_signal'],['cad_signal','jpy_signal'],
    ['chf_signal','jpy_signal'],['nzd_signal','jpy_signal'],['aud_signal','chf_signal'],['cad_signal','chf_signal'],['nzd_signal','chf_signal'],
    ['aud_signal','nzd_signal'],['nzd_signal','cad_signal'],['aud_signal','cad_signal']
])

PMO_LIST = np.array([
    ['eur_pmo','chf_pmo'],['eur_pmo','gbp_pmo'],['eur_pmo','jpy_pmo'],['eur_pmo','nzd_pmo'],['eur_pmo','usd_pmo'],
    ['eur_pmo','aud_pmo'],['eur_pmo','cad_pmo'],['gbp_pmo','aud_pmo'],['gbp_pmo','chf_pmo'],['gbp_pmo','jpy_pmo'],
    ['gbp_pmo','cad_pmo'],['gbp_pmo','usd_pmo'],['gbp_pmo','nzd_pmo'],['usd_pmo','chf_pmo'],['usd_pmo','jpy_pmo'],
    ['aud_pmo','usd_pmo'],['nzd_pmo','usd_pmo'],['usd_pmo','cad_pmo'],['aud_pmo','jpy_pmo'],['cad_pmo','jpy_pmo'],
    ['chf_pmo','jpy_pmo'],['nzd_pmo','jpy_pmo'],['aud_pmo','chf_pmo'],['cad_pmo','chf_pmo'],['nzd_pmo','chf_pmo'],
    ['aud_pmo','nzd_pmo'],['nzd_pmo','cad_pmo'],['aud_pmo','cad_pmo']
])


def pct_data_signals_std(data, std_lvl=1):

    for i in range(len(ALL_PAIRS_BUY)):

        results_sell = deque()
        results_buy = deque()

        pair1 = data[SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[SPLIT_PAIRS[i][1]].to_numpy()

        std1 = pair1.std() * std_lvl
        std2 = pair2.std() * std_lvl

        data[ALL_PAIRS_SELL[i]] = pd.Series((pair1 > std1) & (pair2 < -std2))
        data[ALL_PAIRS_BUY[i]] = pd.Series((pair1 < -std1) & (pair2 > std2))

    return data


def pct_data_signals_quantile(data, low, high):

    for i in range(len(ALL_PAIRS_BUY)):

        results_sell = deque()
        results_buy = deque()

        pair1 = data[SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[SPLIT_PAIRS[i][1]].to_numpy()

        std1_pos = np.quantile(pair1, high)
        std1_neg = np.quantile(pair1, low)
        std2_pos = np.quantile(pair2, high)
        std2_neg = np.quantile(pair2, low)

        data[ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos))
        data[ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg))

    return data


def sma_ema(data, sma_period = 21, ema_period=8):

    for i in range(len(ALL_PAIRS_BUY)):

        results_sell = deque()
        results_buy = deque()

        sma = np.array(indi.MA(data[ALL_PAIRS_OPEN[i]], sma_period, mode='sma'))
        ema = np.array(indi.MA(data[ALL_PAIRS_OPEN[i]], ema_period, mode='ema'))
        sma_1 = np.array(pd.Series(sma).shift())
        ema_1 = np.array(pd.Series(ema).shift())

        data[ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1))
        data[ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1))

    return data


def sma_ema_pct(data, low, high, sma_period = 21, ema_period=8):

    for i in range(len(ALL_PAIRS_BUY)):

        results_sell = deque()
        results_buy = deque()

        pair1 = data[SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[SPLIT_PAIRS[i][1]].to_numpy()

        std1_pos = np.quantile(pair1, high)
        std1_neg = np.quantile(pair1, low)
        std2_pos = np.quantile(pair2, high)
        std2_neg = np.quantile(pair2, low)
        
        sma = np.array(indi.MA(data[ALL_PAIRS_OPEN[i]], sma_period, mode='sma'))
        ema = np.array(indi.MA(data[ALL_PAIRS_OPEN[i]], ema_period, mode='ema'))
        sma_1 = np.array(pd.Series(sma).shift())
        ema_1 = np.array(pd.Series(ema).shift())

        data[ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1) & (pair1 < std1_neg) & (pair2 > std2_pos))
        data[ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1) & (pair1 > std1_pos) & (pair2 < std2_neg))

    return data


def sma_pct(data, high, low, sma_period=50):

    for i in range(len(ALL_PAIRS_BUY)):

        results_sell = deque()
        results_buy = deque()

        pair1 = data[SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[SPLIT_PAIRS[i][1]].to_numpy()

        std1_pos = np.quantile(pair1, high)
        std1_neg = np.quantile(pair1, low)
        std2_pos = np.quantile(pair2, high)
        std2_neg = np.quantile(pair2, low)

        sma = np.array(indi.MA(data[ALL_PAIRS_OPEN[i]], sma_period, mode='sma'))
        prices = np.array(data[ALL_PAIRS_OPEN[i]])

        data[ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos) & (sma < prices))
        data[ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg) & (sma > prices))

    return data


def sma_ema(data):

    for i in range(len(ALL_PAIRS_BUY)):

        results_sell = deque()
        results_buy = deque()

        #pair1 = data[SPLIT_PAIRS[i][0]].to_numpy()
        #pair2 = data[SPLIT_PAIRS[i][1]].to_numpy()

        #std1_pos = np.quantile(pair1, high)
        #std1_neg = np.quantile(pair1, low)
        #std2_pos = np.quantile(pair2, high)
        #std2_neg = np.quantile(pair2, low)

        #k1, d1 = indi.STOCHASTIC(data[SPLIT_PAIRS[i][0]], 14)
        #k2, d2 = indi.STOCHASTIC(data[SPLIT_PAIRS[i][1]], 14)

        #rsi1 = indi.RSI(data[SPLIT_PAIRS[i][0]], dias)
        #rsi2 = indi.RSI(data[SPLIT_PAIRS[i][1]], dias)

        sma = np.array(indi.MA(data[ALL_PAIRS_OPEN[i]], 21, mode='sma'))
        ema = np.array(indi.MA(data[ALL_PAIRS_OPEN[i]], 8, mode='ema'))
        sma_1 = np.array(pd.Series(sma).shift())
        ema_1 = np.array(pd.Series(ema).shift())

        data[ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1))
        data[ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1))

    return data
