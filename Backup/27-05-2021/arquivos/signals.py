import pandas as pd
import numpy as np
from arquivos.indicators import Indicators

class Signals(Indicators):

    def tpsl_calculation(self, periodo):

        data = super().get_normal_data()
        calc = pd.DataFrame()

        for i in range(len(super().ALL_PAIRS_BUY)):

            at = pd.DataFrame()

            high = data[super().ALL_PAIRS_HIGH[i]].shift()
            low = data[super().ALL_PAIRS_LOW[i]].shift()
            close = data[super().ALL_PAIRS_CLOSE[i]].shift(2)

            at['a1'] = high-low
            at['a2'] = abs(high - close)
            at['a3'] = abs(low - close)
            atr = pd.Series(at.values.max(1)).rolling(periodo).mean()

            calc[super().ALL_PAIRS[i]] = atr.fillna(atr.mean())

        self.slcalc = calc.values.T


    def tpsl_calculation_otimization(self, periodo):

        data = super().get_normal_data()
        calc = pd.DataFrame()

        for i in range(len(super().ALL_PAIRS_BUY)):

            at = pd.DataFrame()

            high = data[super().ALL_PAIRS_HIGH[i]].shift()
            low = data[super().ALL_PAIRS_LOW[i]].shift()
            close = data[super().ALL_PAIRS_CLOSE[i]].shift(2)

            at['a1'] = high-low
            at['a2'] = abs(high - close)
            at['a3'] = abs(low - close)
            atr = pd.Series(at.values.max(1)).rolling(periodo).mean()

            data[super().ALL_PAIRS_TPSL[i]] = atr.fillna(atr.mean())

        super().set_normal_data(data)


    def tpsl_online(self, periodo):

        data = super().get_normal_data()
        calc = pd.DataFrame()

        for i in range(len(super().ALL_PAIRS_BUY)):

            at = pd.DataFrame()

            high = data[super().ALL_PAIRS_HIGH[i]].shift()
            low = data[super().ALL_PAIRS_LOW[i]].shift()
            close = data[super().ALL_PAIRS_CLOSE[i]].shift(2)

            at['a1'] = high-low
            at['a2'] = abs(high - close)
            at['a3'] = abs(low - close)
            atr = pd.Series(at.values.max(1)).rolling(periodo).mean()

            data[super().ALL_PAIRS_TPSL[i]] = atr.fillna(atr.mean())

        super().set_normal_data(data)


    def main_online(self):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2))

        super().set_normal_data(data)


    def tpsl_calculation_wfe(self, periodo, array):

        calc = pd.DataFrame()

        for i in range(len(array)):

            at = pd.DataFrame()

            high = pd.Series(array[i][3]).shift()
            low = pd.Series(array[i][4]).shift()
            close = pd.Series(array[i][0]).shift(2)

            at['a1'] = high-low
            at['a2'] = abs(high - close)
            at['a3'] = abs(low - close)
            atr = pd.Series(at.values.max(1)).rolling(periodo).mean()

            calc[super().ALL_PAIRS[i]] = atr.fillna(atr.mean())

        self.slcalc = calc.values.T

    def pct_data_signals_std(self, std_lvl=1):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            std1 = pair1.std() * std_lvl
            std2 = pair2.std() * std_lvl

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 > std1) & (pair2 < -std2))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 < -std1) & (pair2 > std2))

        super().set_normal_data(data)


    def pct_data_signals_quantile(self, low, high):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            pair1_1 = data[super().SPLIT_PAIRS[i][0]].shift().to_numpy()
            pair2_1 = data[super().SPLIT_PAIRS[i][1]].shift().to_numpy()

            std1_pos = np.quantile(pair1, high)
            std1_neg = np.quantile(pair1, low)
            std2_pos = np.quantile(pair2, high)
            std2_neg = np.quantile(pair2, low)

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg))

        super().set_normal_data(data)


    def sma_ema(self, sma_period = 21, ema_period=8):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            sma = super().calc_sma(super().ALL_PAIRS_OPEN[i], sma_period)
            ema = super().calc_ema(super().ALL_PAIRS_OPEN[i], ema_period)
            sma_1 = np.array(pd.Series(sma).shift())
            ema_1 = np.array(pd.Series(ema).shift())

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1))

        super().set_normal_data(data)


    def sma_ema_pct(self, low, high, sma_period = 21, ema_period=8):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            std1_pos = np.quantile(pair1, high)
            std1_neg = np.quantile(pair1, low)
            std2_pos = np.quantile(pair2, high)
            std2_neg = np.quantile(pair2, low)

            sma = super().calc_ema(super().ALL_PAIRS_OPEN[i], sma_period)
            ema = super().calc_ema(super().ALL_PAIRS_OPEN[i], ema_period)
            sma_1 = np.array(pd.Series(sma).shift())
            ema_1 = np.array(pd.Series(ema).shift())

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1) & (pair1 < std1_neg) & (pair2 > std2_pos))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1) & (pair1 > std1_pos) & (pair2 < std2_neg))

        super().set_normal_data(data)


    def sma_pct(self, high, low, sma_period=50):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            std1_pos = np.quantile(pair1, high)
            std1_neg = np.quantile(pair1, low)
            std2_pos = np.quantile(pair2, high)
            std2_neg = np.quantile(pair2, low)

            sma = super().calc_sma(super().ALL_PAIRS_OPEN[i], sma_period)
            prices = np.array(data[super().ALL_PAIRS_OPEN[i]])

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos) & (sma < prices))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg) & (sma > prices))

        super().set_normal_data(data)


    def balance_signal0(self, cut):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            pair1_count = np.array(self.count_all(pair1))
            pair2_count = np.array(self.count_all(pair2))

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2) & (pair1_count > cut) & (pair2_count < -cut))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2) & (pair1_count < -cut) & (pair2_count > cut))

        super().set_normal_data(data)


    def balance_signal1(self, cut):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            pair1_count = np.array(self.count_all(pair1))
            pair2_count = np.array(self.count_all(pair2))

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < -np.std(pair1)) & (pair2 > np.std(pair2)) & (pair1_count > cut) & (pair2_count < -cut))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > np.std(pair1)) & (pair2 < -np.std(pair2)) & (pair1_count < -cut) & (pair2_count > cut))

        super().set_normal_data(data)


    def balance_signal3(self, cut, period):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            pair1_count = np.array(self.count_all(pair1))
            pair2_count = np.array(self.count_all(pair2))

            sma = super().calc_sma(super().ALL_PAIRS_OPEN[i], period)
            prices = np.array(data[super().ALL_PAIRS_OPEN[i]])

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2) & (prices < sma) & (pair1_count > cut) & (pair2_count < -cut))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2) & (prices > sma) & (pair1_count < -cut) & (pair2_count > cut))

        super().set_normal_data(data)


    def balance_signal4(self):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2))

        super().set_normal_data(data)

    def balance_signal5(self, cut):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()

            pair1_count = np.array(self.count_all(pair1))
            pair2_count = np.array(self.count_all(pair2))

            prices = np.array(data[super().ALL_PAIRS_OPEN[i]])

            prices_count = np.array(self.count_all(pd.Series(prices).diff()))

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2) & (prices_count > cut))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2) & (prices_count < -cut))

        super().set_normal_data(data)


    def teste(self, periodo_sma, periodo_kama, fast_kama, slow_kama):

        data = super().get_normal_data()

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = data[super().SPLIT_PAIRS[i][1]].to_numpy()
            pair1_1 = data[super().SPLIT_PAIRS[i][0]].shift().to_numpy()
            pair2_1 = data[super().SPLIT_PAIRS[i][1]].shift().to_numpy()

            teste = super().calc_stochastic(super().ALL_PAIRS_OPEN[i], 20)
            kama = super().calc_kama(super().ALL_PAIRS_OPEN[i], periodo_kama, fast_kama, slow_kama)
            sma = super().calc_sma(super().ALL_PAIRS_OPEN[i], periodo_sma)
            kama_s = pd.Series(kama).shift().to_numpy()
            sma_s = pd.Series(sma).shift().to_numpy()

            price = data[super().ALL_PAIRS_OPEN[i]].to_numpy()

            data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2) & (kama < sma) & (kama_s > sma_s))
            data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2) & (kama > sma) & (kama_s < sma_s))

        super().set_normal_data(data)
