import pandas as pd
import numpy as np
import indicators as indi
from constants import Pairs

def pct_data_signals_std(data, std_lvl=1):

    for i in range(len(Pairs.ALL_PAIRS_BUY)):

        pair1 = data[Pairs.SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[Pairs.SPLIT_PAIRS[i][1]].to_numpy()

        std1 = pair1.std() * std_lvl
        std2 = pair2.std() * std_lvl

        data[Pairs.ALL_PAIRS_SELL[i]] = pd.Series((pair1 > std1) & (pair2 < -std2))
        data[Pairs.ALL_PAIRS_BUY[i]] = pd.Series((pair1 < -std1) & (pair2 > std2))

    return data


def pct_data_signals_quantile(data, low, high):

    for i in range(len(Pairs.ALL_PAIRS_BUY)):

        pair1 = data[Pairs.SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[Pairs.SPLIT_PAIRS[i][1]].to_numpy()

        pair1_1 = data[Pairs.SPLIT_PAIRS[i][0]].shift().to_numpy()
        pair2_1 = data[Pairs.SPLIT_PAIRS[i][1]].shift().to_numpy()

        std1_pos = np.quantile(pair1, high)
        std1_neg = np.quantile(pair1, low)
        std2_pos = np.quantile(pair2, high)
        std2_neg = np.quantile(pair2, low)

        data[Pairs.ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos))
        data[Pairs.ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg))

    return data


def sma_ema(data, sma_period = 21, ema_period=8):

    for i in range(len(Pairs.ALL_PAIRS_BUY)):

        sma = np.array(indi.MA(data[Pairs.ALL_PAIRS_OPEN[i]], sma_period, mode='sma'))
        ema = np.array(indi.MA(data[Pairs.ALL_PAIRS_OPEN[i]], ema_period, mode='ema'))
        sma_1 = np.array(pd.Series(sma).shift())
        ema_1 = np.array(pd.Series(ema).shift())

        data[Pairs.ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1))
        data[Pairs.ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1))

    return data


def sma_ema_pct(data, low, high, sma_period = 21, ema_period=8):

    for i in range(len(Pairs.ALL_PAIRS_BUY)):

        pair1 = data[Pairs.SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[Pairs.SPLIT_PAIRS[i][1]].to_numpy()

        std1_pos = np.quantile(pair1, high)
        std1_neg = np.quantile(pair1, low)
        std2_pos = np.quantile(pair2, high)
        std2_neg = np.quantile(pair2, low)

        sma = np.array(indi.MA(data[Pairs.ALL_PAIRS_OPEN[i]], sma_period, mode='sma'))
        ema = np.array(indi.MA(data[Pairs.ALL_PAIRS_OPEN[i]], ema_period, mode='ema'))
        sma_1 = np.array(pd.Series(sma).shift())
        ema_1 = np.array(pd.Series(ema).shift())

        data[Pairs.ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1) & (pair1 < std1_neg) & (pair2 > std2_pos))
        data[Pairs.ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1) & (pair1 > std1_pos) & (pair2 < std2_neg))

    return data


def sma_pct(data, high, low, sma_period=50):

    for i in range(len(Pairs.ALL_PAIRS_BUY)):

        pair1 = data[Pairs.SPLIT_PAIRS[i][0]].to_numpy()
        pair2 = data[Pairs.SPLIT_PAIRS[i][1]].to_numpy()

        std1_pos = np.quantile(pair1, high)
        std1_neg = np.quantile(pair1, low)
        std2_pos = np.quantile(pair2, high)
        std2_neg = np.quantile(pair2, low)

        sma = np.array(indi.MA(data[Pairs.ALL_PAIRS_OPEN[i]], sma_period, mode='sma'))
        prices = np.array(data[Pairs.ALL_PAIRS_OPEN[i]])

        data[Pairs.ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos) & (sma < prices))
        data[Pairs.ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg) & (sma > prices))

    return data


def teste(data, pair_window, corr_window, corr_cut, higher, shift=1, inverse=False):

    for i in range(len(Pairs.ALL_PAIRS_BUY)):

        pair1 = data[Pairs.SPLIT_PAIRS[i][0]].rolling(window=pair_window).mean().to_numpy()
        pair2 = data[Pairs.SPLIT_PAIRS[i][1]].rolling(window=pair_window).mean().to_numpy()
        pair1_1 = data[Pairs.SPLIT_PAIRS[i][0]].rolling(window=pair_window).mean().shift(shift).to_numpy()
        pair2_1 = data[Pairs.SPLIT_PAIRS[i][1]].rolling(window=pair_window).mean().shift(shift).to_numpy()

        corr = data[Pairs.SPLIT_PAIRS[i][0]].rolling(window=corr_window).corr(data[Pairs.SPLIT_PAIRS[i][1]]).to_numpy()

        kama = indi.MA(data[Pairs.ALL_PAIRS_OPEN[i]], 10, mode='kama', fast_coef_kama = 8, slow_coef_kama = 21)
        sma = indi.MA(data[Pairs.ALL_PAIRS_OPEN[i]], 21, mode='sma')
        kama_s = kama.shift()
        sma_s = sma.shift()

        price = data[Pairs.ALL_PAIRS_OPEN[i]].to_numpy()

        corr_flag = 0
        if higher:
            corr_flag = corr > corr_cut
        else:
            corr_flag = corr < corr_cut

        if inverse:
            data[Pairs.ALL_PAIRS_BUY[i]] = pd.Series((pair1 < pair2) & (pair1_1 > pair2_1) & (corr_flag))
            data[Pairs.ALL_PAIRS_SELL[i]] = pd.Series((pair1 > pair2) & (pair1_1 < pair2_1) & (corr_flag))
        else:
            data[Pairs.ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2) & (kama < sma) & (kama_s > sma_s))
            data[Pairs.ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2) & (kama > sma) & (kama_s < sma_s))

    return data
