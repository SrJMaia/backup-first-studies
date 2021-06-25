import pandas as pd
import numpy as np
from numba import njit


def MACD(series, first_period, second_period, signal_line, min_period=1, act_min_period=False, only_hist = True):

    """
    Pode ser no cruzamento macd_line e signal_line
    Poder ser quando os dois passarem 0

    Em vez de analsiar o cruzamento dos dois pode ver se o macd_hist esta pos ou neg
    cuidar para caso a primeira media seja maior que a segunda ira inverter
    """

    macd_line = series.ewm(first_period, min_periods=min_period if act_min_period else first_period).mean() - series.ewm(second_period, min_periods=min_period if act_min_period else second_period).mean()
    signal_line = macd_line.ewm(signal_line, min_periods=min_period if act_min_period else first_period).mean()
    macd_hist = macd_line - signal_line

    if only_hist:
        return macd_hist
    else:
        return macd_line, signal_line


@njit
def WMA(array, period):
    wma = []
    weights = np.arange(period, 0, -1)
    weights_sum = weights.sum()
    for i in np.arange(len(array)):
        if i < period:
            wma.append(np.nan)
            continue
        calc = 0
        for j in np.arange(period):
            calc = calc + (array[i-j] * weights[j])
        wma.append(calc/weights_sum)

    return wma


def MA(series, period, mode='sma', times_to_do=1, min_period=1, act_min_period=False, fast_coef_kama = 8, slow_coef_kama = 21):
    """
    modes:
    sma = simple moving average
    ema = exponential moving average
    wma = weight moving average
    kama = kaufman adaptative moving average
    """
    if mode == 'sma':
        for i in range(times_to_do):
            series = series.rolling(window = period, min_periods = min_period if act_min_period else period).mean()
        return series
    elif mode == 'ema':
        for i in range(times_to_do):
            series = series.ewm(period, min_periods = min_period if act_min_period else period).mean()
        return series
    elif mode == 'wma':
        for i in range(times_to_do):
                series = WMA(series.to_numpy(), period)
        return pd.Series(series)
    elif mode == 'kama':
        change = abs(series.diff(period)).to_numpy()
        volatility_sum = (abs(series.diff())).rolling(period).sum().to_numpy()
        for i in range(times_to_do):
            series = KAMA(np.array(series), period, fast_coef_kama, slow_coef_kama, change, volatility_sum)
        return pd.Series(series)


def PMO(serie, p1, p2, p3, adjust_ewm = True):

    smothing1 = 2/p1
    smothing2 = 2/p2
    smothing3 = 2/(p3+1)

    roc = serie
    roc_ma = roc.ewm(alpha=smothing1, adjust=adjust_ewm).mean()
    roc_ma = roc_ma.shift() + (roc - roc_ma.shift()) * smothing1
    pmo = roc_ma.ewm(alpha=smothing2, adjust=adjust_ewm).mean()
    pmo = pmo.shift() + (roc_ma - pmo.shift()) * smothing2
    signal = pmo.ewm(alpha=smothing3, adjust=adjust_ewm).mean()
    signal = smothing3 * (pmo - signal.shift()) + signal.shift()

    return pmo, signal


def STOCHASTIC(series, period):

    k = ((series - series.rolling(period).min()) / (series.rolling(period).max() - series.rolling(period).min())) * 100
    d = k.rolling(3).mean()

    return k, d


@njit
def KAMA(array, periodo_kama, fast_coef_period, slow_coef_period, change, volatility_sum):
    er = np.where(volatility_sum != 0.0, change / volatility_sum, 0.0)
    fast_coef = 2 / (fast_coef_period + 1)
    slow_coef = 2 / (slow_coef_period + 1)
    alpha = (er * (fast_coef - slow_coef) + fast_coef) ** 2
    kama = np.empty((change.size))
    first_value = True
    for i in np.arange(change.size):
        if alpha[i] != alpha[i]:
            kama[i] = np.nan
        else:
            if first_value:
                kama[i] = array[i]
                first_value = False
            else:
                kama[i] = alpha[i] * (array[i] - kama[i-1]) + kama[i-1]
    return kama


@njit
def RSI(array, periodo):
    """
    Se passar os preços no array, usar .diff().to_numpy() ou .pct_change().to_numpy()
    """
    avg_loss = []
    avg_profit = []
    for i in np.arange(len(array)):

        loss = 0
        profit = 0

        if i < periodo:
            avg_profit.append(np.nan)
            avg_loss.append(np.nan)
            continue

        for j in range(periodo):
            if array[i-j] < 0:
                loss += array[i-j]
            elif array[i-j] > 0:
                profit += array[i-j]

        # É possível usar SMA, EMA e Wilders Smoothing Method
        avg_loss.append(abs(loss)/periodo)
        avg_profit.append(profit/periodo)


    rsi = []
    for i in range(len(avg_loss)):
        if avg_loss[i] == 0:
            rsi.append(0)
        else:
            rsi.append(100 - (100 / (1 + (avg_profit[i] / avg_loss[i]))))

    return rsi
