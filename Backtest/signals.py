import pandas as pd
import numpy as np
import indicators as indi
from indicators import Indicators
from constants import Pairs

class Signals(Pairs, Indicators):

    def pct_data_signals_std(self, std_lvl=1):

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = self.data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = self.data[super().SPLIT_PAIRS[i][1]].to_numpy()

            std1 = pair1.std() * std_lvl
            std2 = pair2.std() * std_lvl

            self.data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 > std1) & (pair2 < -std2))
            self.data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 < -std1) & (pair2 > std2))


    def pct_data_signals_quantile(self, low, high):

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = self.data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = self.data[super().SPLIT_PAIRS[i][1]].to_numpy()

            pair1_1 = self.data[super().SPLIT_PAIRS[i][0]].shift().to_numpy()
            pair2_1 = self.data[super().SPLIT_PAIRS[i][1]].shift().to_numpy()

            std1_pos = np.quantile(pair1, high)
            std1_neg = np.quantile(pair1, low)
            std2_pos = np.quantile(pair2, high)
            std2_neg = np.quantile(pair2, low)

            self.data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos))
            self.data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg))


    def sma_ema(self, sma_period = 21, ema_period=8):

        for i in range(len(super().ALL_PAIRS_BUY)):

            sma = super().calc_sma(super().ALL_PAIRS_OPEN[i], sma_period)
            ema = super().calc_ema(super().ALL_PAIRS_OPEN[i], ema_period)
            sma_1 = np.array(pd.Series(sma).shift())
            ema_1 = np.array(pd.Series(ema).shift())

            self.data[super().ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1))
            self.data[super().ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1))


    def sma_ema_pct(self, low, high, sma_period = 21, ema_period=8):

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = self.data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = self.data[super().SPLIT_PAIRS[i][1]].to_numpy()

            std1_pos = np.quantile(pair1, high)
            std1_neg = np.quantile(pair1, low)
            std2_pos = np.quantile(pair2, high)
            std2_neg = np.quantile(pair2, low)

            sma = super().calc_ema(super().ALL_PAIRS_OPEN[i], sma_period)
            ema = super().calc_ema(super().ALL_PAIRS_OPEN[i], ema_period)
            sma_1 = np.array(pd.Series(sma).shift())
            ema_1 = np.array(pd.Series(ema).shift())

            self.data[super().ALL_PAIRS_SELL[i]] = pd.Series((ema < sma) & (ema_1 > sma_1) & (pair1 < std1_neg) & (pair2 > std2_pos))
            self.data[super().ALL_PAIRS_BUY[i]] = pd.Series((ema > sma) & (ema_1 < sma_1) & (pair1 > std1_pos) & (pair2 < std2_neg))


    def sma_pct(self, high, low, sma_period=50):

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = self.data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = self.data[super().SPLIT_PAIRS[i][1]].to_numpy()

            std1_pos = np.quantile(pair1, high)
            std1_neg = np.quantile(pair1, low)
            std2_pos = np.quantile(pair2, high)
            std2_neg = np.quantile(pair2, low)

            sma = super().calc_sma(super().ALL_PAIRS_OPEN[i], sma_period)
            prices = np.array(self.data[super().ALL_PAIRS_OPEN[i]])

            self.data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < std1_neg) & (pair2 > std2_pos) & (sma < prices))
            self.data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > std1_pos) & (pair2 < std2_neg) & (sma > prices))


    def teste(self, periodo_sma, periodo_kama, fast_kama, slow_kama):

        for i in range(len(super().ALL_PAIRS_BUY)):

            pair1 = self.data[super().SPLIT_PAIRS[i][0]].to_numpy()
            pair2 = self.data[super().SPLIT_PAIRS[i][1]].to_numpy()
            pair1_1 = self.data[super().SPLIT_PAIRS[i][0]].shift().to_numpy()
            pair2_1 = self.data[super().SPLIT_PAIRS[i][1]].shift().to_numpy()

            teste = super().calc_stochastic(super().ALL_PAIRS_OPEN[i], 20)
            kama = super().calc_kama(super().ALL_PAIRS_OPEN[i], periodo_kama, fast_kama, slow_kama)
            sma = super().calc_sma(super().ALL_PAIRS_OPEN[i], periodo_sma)
            kama_s = pd.Series(kama).shift().to_numpy()
            sma_s = pd.Series(sma).shift().to_numpy()

            price = self.data[super().ALL_PAIRS_OPEN[i]].to_numpy()

            self.data[super().ALL_PAIRS_SELL[i]] = pd.Series((pair1 < pair2) & (kama < sma) & (kama_s > sma_s))
            self.data[super().ALL_PAIRS_BUY[i]] = pd.Series((pair1 > pair2) & (kama > sma) & (kama_s < sma_s))
