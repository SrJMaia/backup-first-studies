from signals import Signals
import pandas as pd
import numpy as np
import backtest as bt


class Central(Signals):

    def __init__(self, login=5528104, senha='YUWNehok', servidor='ActivTradesCorp-Server', balance=1000):
        super().__init__(login, senha, servidor)
        self.balance = balance


    def back_tpsl(self, tpsl, multiply_tpsl):
        """
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        tot, sell, buy, each_pair =  bt.otimizado_tpsl(self.get_numpy_normal_data(), tpsl, multiply_tpsl)
        tot = np.delete(tot, np.where(tot == 0.))
        sell = np.delete(sell, np.where(sell == 0.))
        buy = np.delete(buy, np.where(buy == 0.))
        results_df = pd.DataFrame()
        for index, value in enumerate(each_pair):
            results_df[super().ALL_PAIRS[index]] = pd.Series(np.delete(value, np.where(value == 0.)))
        return tot, sell, buy, results_df


    def back_no_tpsl(self):
        """
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        tot, sell, buy, each_pair =  bt.otimizado_no_tpsl(self.get_numpy_normal_data())
        tot = np.delete(tot, np.where(tot == 0.))
        sell = np.delete(sell, np.where(sell == 0.))
        buy = np.delete(buy, np.where(buy == 0.))
        results_df = pd.DataFrame()
        for index, value in enumerate(each_pair):
            results_df[super().ALL_PAIRS[index]] = pd.Series(np.delete(value, np.where(value == 0.)))
        return tot, sell, buy, results_df


    def back_tpsl_ohl(self, tpsl, multiply_tpsl):
        """
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        tot, sell, buy, each_pair =  bt.otimizado_tpsl_ohl(self.get_numpy_normal_data(), tpsl, multiply_tpsl)
        tot = np.delete(tot, np.where(tot == 0.))
        sell = np.delete(sell, np.where(sell == 0.))
        buy = np.delete(buy, np.where(buy == 0.))
        results_df = pd.DataFrame()
        for index, value in enumerate(each_pair):
            results_df[super().ALL_PAIRS[index]] = pd.Series(np.delete(value, np.where(value == 0.)))
        return tot, sell, buy, results_df


    def back_big_tpsl_ohl(self, tpsl, multiply_tpsl):
        """
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        tot, sell, buy, each_pair =  bt.big_backtest_otimizado_tpsl(self.get_numpy_normal_data(), self.get_numpy_big_data(), tpsl, multiply_tpsl)
        tot = np.delete(tot, np.where(tot == 0.))
        sell = np.delete(sell, np.where(sell == 0.))
        buy = np.delete(buy, np.where(buy == 0.))
        results_df = pd.DataFrame()
        for index, value in enumerate(each_pair):
            results_df[super().ALL_PAIRS[index]] = pd.Series(np.delete(value, np.where(value == 0.)))
        return tot, sell, buy, results_df
