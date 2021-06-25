import pandas as pd

def EMA(series, periods):
    """
    Inputs: A pandas series
    Inputs: Period

    Output: EMA Series
    """
    EMA = series.ewm(span=periods, min_periods=periods).mean()
    return EMA


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
