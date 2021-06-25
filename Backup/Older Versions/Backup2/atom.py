def KAMA(array, periodo_kama, fast_coef_period, slow_coef_period, change, volatility_sum):
    change = abs(series.diff(period)).to_numpy()
    volatility_sum = (abs(series.diff())).rolling(period).sum().to_numpy()
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
