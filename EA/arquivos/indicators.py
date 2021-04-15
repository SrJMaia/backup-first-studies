import numpy as np
from numba import njit
from arquivos.constants import Pairs
from arquivos.data import Data

"""
Usar as funções njit em vez de pandas quando:
find_min_max: Quando for calcular mais de 500x
"""

class IndicatorsCalc:
    """
    Futuramente usar pandas?
    """

    @staticmethod
    @njit
    def find_min_max(array, periodo):
        all_min = np.empty((array.size), dtype='float64')
        all_max = np.empty((array.size), dtype='float64')
        calc = np.empty((periodo), dtype='float64')
        for i in np.arange(array.size):
            if i < periodo:
                all_min[i] = np.nan
                all_max[i] = np.nan
                continue
            for j in np.arange(periodo):
                calc[j] = array[i-j]
            all_min[i] = calc.min()
            all_max[i] = calc.max()

        return all_min, all_max


    @staticmethod
    def count_all(series):
        #high = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        #low = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        geral = []
        count = 0

        for i, v in enumerate(series):

            if v < 0:
                if count < 0: count = 0
                #high[count] += 1
                count += 1
            elif v > 0:
                if count > 0: count = 0
                #low[abs(count)] += 1
                count -= 1
            else:
                count == 0

            geral.append(count)

        #return geral, high, low
        return geral


    @staticmethod
    def EMA_PANDAS(array, period, mode='com', min_periods = 1, act_adjust = False):
        """
        Modes: com, span, halflife, alpha
        if alpha, period must be between 0 > period > 1
        """
        array = pd.Series(array)
        if mode == 'com':
            array = array.ewm(com=period, min_periods=min_periods, adjust=act_adjust).mean()
        elif mode == 'span':
            array = array.ewm(span=period, min_periods=min_periods, adjust=act_adjust).mean()
        elif mode == 'halflife':
            array = array.ewm(halflife=period, min_periods=min_periods, adjust=act_adjust).mean()
        elif mode == 'alpha':
            array = array.ewm(span=period, min_periods=min_periods, adjust=act_adjust).mean()

        return array


    @staticmethod
    def find_min_max_pandas(array, period, round_n=5):
        max_ = pd.Series(array).rolling(period).max().to_numpy()
        min_ = pd.Series(array).rolling(period).min().to_numpy()
        return min_, max_


    @classmethod
    def STOCHASTIC(cls, array, periodo, k_period=3):
        mini, maxi = cls.find_min_max_pandas(array, periodo)

        k1 = array-mini
        k2 = maxi-mini
        k = np.where(k2 != 0.0, (k1 / k2) * 100, 0.0)
        d = cls.SMA(k, k_period)

        return k, d


    @staticmethod
    @njit
    def EMA_NORMAL(series, periodo, coef=True, min_periods_1=False, pmo=False):
        ema = np.empty((series.size), dtype='float64')
        alpha = 0
        if coef:
            alpha = 2 / (periodo+1)
        else:
            alpha = 1 / periodo

        if pmo:
            alpha = 2 / periodo

        if min_periods_1:
            for i in range(series.size):
                if i < 1:
                    ema[i] = series[i]
                    continue
                ema[i] = alpha * (series[i] - ema[i-1]) + ema[i-1]
        else:
            for i in range(series.size):
                if i < periodo:
                    ema[i] = np.nan
                    continue
                elif i == periodo:
                    ema[i] = series[i]
                    continue

                ema[i] = alpha * (series[i] - ema[i-1]) + ema[i-1]

        return ema


    @staticmethod
    @njit
    def EMA_MT(series, periodo):
        alpha = 2 / (periodo + 1)
        ema = np.empty((series.size), dtype='float64')
        for i in np.arange(series.size):
            if i < 1:
                ema[i] = series[i]
            ema[i] = (series[i] * alpha) + (ema[i-1] * (1-alpha))

        return ema


    @classmethod
    def MACD(cls, series, first_period, second_period, signal_line, act_min_period=False, only_hist = True):
        first_line = cls.EMA_NORMAL(series=series, periodo=first_period, coef=True, min_periods_1=act_min_period)
        second_line = cls.EMA_NORMAL(series=series, periodo=second_period, coef=True, min_periods_1=act_min_period)

        macd_line = first_line - second_line

        signal_line = cls.EMA_NORMAL(series=macd_line, periodo=signal_line, coef=True, min_periods_1=act_min_period)

        macd_hist = macd_line - signal_line

        macd_hist = np.around(macd_hist, round_n)
        signal_line = np.around(signal_line, round_n)

        if only_hist:
            return macd_hist
        else:
            return macd_line, signal_line


    @staticmethod
    @njit
    def WMA(array, periodo):
        wma = np.empty((array.size), dtype='float64')
        weights = np.arange(period, 0, -1)
        weights_sum = weights.sum()
        for i in np.arange(len(array)):
            if i < period:
                wma[i] = np.nan
                continue
            calc = 0
            for j in np.arange(period):
                calc = calc + (array[i-j] * weights[j])
            wma[i] = calc/weights_sum

        return wma


    @staticmethod
    @njit
    def SMA(array, periodo):
        # Fazer uso qunado usar mais de 300x
        sma = np.empty((array.size), dtype='float64')
        for i in np.arange(array.size):
            if i < periodo:
                sma[i] = array[i]
                continue
            calc = 0
            for j in np.arange(periodo):
                calc += array[i-j]
            sma[i] = calc / periodo

        return sma


    @staticmethod
    def SMA_PANDAS(array, periodo, round_n=5):
        array = np.around(pd.Series(array).rolling(periodo).mean().to_numpy(), round_n)


    @staticmethod
    @njit
    def KAMA(array, fast_coef_period, slow_coef_period, change, volatility_sum):
        er = np.where(volatility_sum != 0.0, change / volatility_sum, 0.0)
        fast_coef = 2 / (fast_coef_period + 1)
        slow_coef = 2 / (slow_coef_period + 1)
        alpha = (er * (fast_coef - slow_coef) + fast_coef) ** 2
        kama = np.empty((array.size), dtype='float64')
        for i in np.arange(array.size):
            if i < np.isnan(alpha).sum():
                kama[i] = array[i]
                continue
            kama[i] = alpha[i] * (array[i] - kama[i-1]) + kama[i-1]

        return kama


    @staticmethod
    @njit
    def diff_change(array, periodo, absolute=False, inverse=False):
        diff = np.empty((array.size), dtype='float64')
        for i in np.arange(array.size):
            if i < periodo:
                diff[i] = np.nan
                continue
            diff[i] = array[i] - array[i-periodo]
        if absolute:
            diff = np.absolute(diff)
        elif inverse:
            diff = -1 * diff

        return diff


    @staticmethod
    @njit
    def sum_periodo(array, periodo):
        """
        Passar array ja tendo feito o diff com o diff_change,
        caso contrário dará erro do numba
        """
        sum_array = np.empty((array.size), dtype='float64')
        for i in np.arange(array.size):
            if i < periodo:
                sum_array[i] = np.nan
                continue
            calc_sum = 0
            for j in np.arange(periodo):
                calc_sum += array[i-j]
            sum_array[i] = calc_sum

        return sum_array


    @classmethod
    def PMO(cls, array, periodo1, periodo2, periodo3):

        smothing1 = 2/periodo1
        smothing2 = 2/periodo2
        smothing3 = 2/(periodo3+1)

        roc_ma = cls.EMA_NORMAL(array, periodo1, pmo=True)
        roc_ma_shift = np.append(np.nan, np.roll(roc_ma, 1)[1:])
        roc_ma = roc_ma_shift + (array - roc_ma_shift) * smothing1

        pmo = cls.EMA_NORMAL(roc_ma, periodo2, pmo=True)
        pmo_shift = np.append(np.nan, np.roll(pmo, 1)[1:])
        pmo = pmo_shift + (roc_ma - pmo_shift) * smothing2

        signal = cls.EMA_NORMAL(pmo, periodo3)
        signal_shift = np.append(np.nan, np.roll(signal, 1)[1:])
        signal = smothing3 * (pmo - signal_shift) + signal_shift

        return pmo, signal


    @staticmethod
    @njit
    def RSI(array, periodo):
        avg_loss = np.empty((array.size), dtype='float64')
        avg_profit = np.empty((array.size), dtype='float64')
        for i in np.arange(array.size):
            loss = 0
            profit = 0
            if i < periodo:
                avg_profit[i] = np.nan
                avg_loss[i] = np.nan
                continue
            for j in range(periodo):
                if array[i-j] < 0:
                    loss += array[i-j]
                elif array[i-j] > 0:
                    profit += array[i-j]
            avg_loss[i] = np.absolute(loss)/periodo
            avg_profit[i] = profit/periodo

        rsi = np.empty((array.size), dtype='float64')
        for i in range(array.size):
            if avg_loss[i] == 0:
                rsi[i] = 0
            else:
                rsi[i] = 100 - (100 / (1 + (avg_profit[i] / avg_loss[i])))

        return rsi


class Indicators(IndicatorsCalc, Data):

    def calc_rsi(self, string, periodo, round_n=5):
        """
        string = string com o nome da coluna a ser calculada
        periodo = int > 0
        """
        diff = super().diff_change(super().get_normal_data()[string].to_numpy(), 1)
        return np.around(super().RSI(diff, periodo), round_n)


    def calc_kama(self, string, periodo_kama, fast_coef_period, slow_coef_period, round_n=5):
        """
        string = string com o nome da coluna a ser calculada
        period_kama = int > 0
                      Valor que será feito o diff
        fast_coef_period = int > 0
        slow_coef_period = int > 0
        """
        change = super().diff_change(super().get_normal_data()[string].to_numpy(), periodo_kama, absolute=True)
        change_one = super().diff_change(super().get_normal_data()[string].to_numpy(), 1, absolute=True)
        sum_period = super().sum_periodo(change_one, periodo_kama)
        return np.around(super().KAMA(super().get_normal_data()[string].to_numpy(),
                                        fast_coef_period,
                                        slow_coef_period,
                                        change,
                                        sum_period, round_n))


    def calc_stochastic(self, string, periodo, k_periodo = 3, round_n=5):
        """
        string = string com o nome da coluna a ser calculada
        period = int > 0
        k_periodo = int > 0
        k_periodo > Média de d, slow stochastic
        return
        k% e d%
        """
        return np.around(super().STOCHASTIC(super().get_normal_data()[string].to_numpy(), periodo, k_period=k_periodo),round_n)


    def calc_pmo(self, string, periodo1, periodo2, periodo3, round_n=5):
        """
        Ao informar a string certificar que ira pegar um ROC
        """
        return np.around(super().PMO(super().get_normal_data()[string].to_numpy(), periodo1, periodo2, periodo3),round_n)


    def calc_sma(self, string, periodo, round_n=5):
        """
        string = string com o nome da coluna a ser calculada
        period = int > 0
        """
        return np.around(super().SMA(super().get_normal_data()[string].to_numpy(), periodo=periodo),round_n)


    def calc_wma(self, string, periodo, round_n=5):
        """
        string = string com o nome da coluna a ser calculada
        period = int > 0
        """
        return np.around(super().WMA(super().get_normal_data()[string].to_numpy(), periodo=periodo),round_n)


    def calc_ema(self, string, periodo, coef=True, min_periods_1=False, mt=False, round_n=5):
        """
        Parametros
        string = string com o nome da coluna a ser calculada
        periodo = int > 0
        coef = Se True calcula alpha = 2 / (periodo+1) equivalente ao span de ewm do pandas
               Se False calcula alpha = 1 / periodo, equivalente a passar apenas alpha em ewm
        min_periods_1 = Se True, sera calculado com um minimo de periodos de 1, caso contrario
                        minimo será periodo
        mt = Se True, calculo ema conforme calculo do mt5
        ---
        Retornos
        EWM em np.array()
        """
        if mt:
            return np.around(super().EMA_MT(super().get_normal_data()[string].to_numpy(),
                                            periodo=periodo), round_n)
        else:
            return np.around(super().EMA_NORMAL(super().get_normal_data()[string].to_numpy(),
                                                periodo=periodo,
                                                coef=coef,
                                                min_periods_1=min_periods_1), round_n)


    def calc_macd(self, string, first_period, second_period, signal_line, act_min_period=False, only_hist=True, round_n=5):
        """
        string = string com o nome da coluna a ser calculada
        first_period = int > 0
        second_period = int > 0
        signal_line = int > 0
        act_min_period = Ativar minimo de periodo para 1 no calculo em vez de n periodos
        only_hist = Se True retorna o macd_hist que é a diferença entre macd_line e signal_line
        ---
        Pode ser no cruzamento macd_line e signal_line
        Poder ser quando os dois passarem 0

        Em vez de analsiar o cruzamento dos dois pode ver se o macd_hist esta pos ou neg
        cuidar para caso a primeira media seja maior que a segunda ira inverter
        """
        return np.around(super().MACD(super().get_normal_data()[string].to_numpy(),
                        first_period=first_period,
                        second_period=second_period,
                        signal_line=signal_line,
                        act_min_period=act_min_period,
                        only_hist=only_hist), round_n)
