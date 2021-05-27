from arquivos.signals import Signals
import arquivos.backtest as bt
import arquivos.analysis_functions as af
from arquivos.analysis_functions import Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('dark_background')
plt.rcParams["figure.figsize"] = (30,10)


class Central(Signals, Analysis):

    def __init__(self, login=5528104, senha='YUWNehok', servidor='ActivTradesCorp-Server', balance=1000):
        super().__init__(login, senha, servidor)
        self.balance_backtest = balance


    def clean_results(self, tot, sell, buy, each_pair=[], multi_pairs=False, multi_tf=False):
        df = pd.DataFrame()
        df['Result'] = pd.Series(np.delete(tot, np.where(tot == 0.)))
        df['Short_Trades'] = pd.Series(np.delete(sell, np.where(sell == 0.)))
        df['Long_Trades'] = pd.Series(np.delete(buy, np.where(buy == 0.)))
        if multi_pairs:
            for index, value in enumerate(each_pair):
                df[self.ALL_PAIRS[index]] = pd.Series(np.delete(value, np.where(value == 0.)))
        elif multi_tf:
            pass
            # Em construção
        return df


    def back_tpsl(self, multiply_tp, multiply_sl, tpsl_mean=14, analyse=True, multi_test=False, plot=False):
        """
        se for um multi_test tpsl devera ser uma lista dos take profit e stop loss
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        if not multi_test:
            self.tpsl_calculation_otimization(tpsl_mean)
            self.normal_data_to_array()
            tot, sell, buy =  bt.single_backtest(self.get_numpy_normal_data(),
                                                multiply_tp=multiply_tp,
                                                multiply_sl=multiply_sl)
            self.del_numpy_normal_data()
            if analyse:
                return self.analysis_backtest(self.clean_results(tot, sell, buy))
            else:
                return self.clean_results(tot, sell, buy)
        else:
            # wfe_tot = pd.DataFrame()
            # c = 0
            # self.walk_forward_split()
            # """
            # Bug, e feito a operação duas vezes
            # """
            # for i in range(1,len(self.get_normal_walk_forward()),2):
            #     """
            #     Mudar o len de i e passar um valro especifico
            #     Criar um unico loop de 2 a 31
            #     """
            #     # In Sample
            #     results_in = pd.DataFrame()
            #     wfe_is = np.zeros((31),dtype=np.float64)
            #     self.set_period(len(self.get_normal_walk_forward()[i-1][0][0]), multi=True)
            #     for j in range(2, 31):
            #         self.tpsl_calculation_otimization(j)
            #         self.walk_forward_split()
            #         tot, sell, buy, each_pair =  bt.otimizado_tpsl(self.get_normal_walk_forward()[i-1],
            #                                                         multiply_tp=multiply_tp,
            #                                                         multiply_sl=multiply_sl)
            #         tot = self.clean_results(tot, sell, buy, each_pair)
            #         results_in[j] = tot['Result']
            #         wfe_is[j] = self.wfe(tot['Result'])
            #     if plot:
            #         try:
            #             results_in.plot()
            #             plt.title(f'In Sample {i-1}', fontsize=30)
            #             plt.grid()
            #             plt.show()
            #         except TypeError:
            #             print('Apenas prejuízos')
            #     wfe_is = np.delete(wfe_is, np.where(wfe_is == 0.))
            #     self.del_period_data()
            #
            #     # Out of Sample
            #     self.set_period(len(self.get_normal_walk_forward()[i][0][0]), multi=True)
            #     results_out = pd.DataFrame()
            #     wfe_oos = np.zeros((31),dtype=np.float64)
            #     for j in range(2, 31):
            #         self.tpsl_calculation_otimization(j)
            #         self.walk_forward_split()
            #         tot, sell, buy, each_pair =  bt.otimizado_tpsl(self.get_normal_walk_forward()[i],
            #                                                         multiply_tp=multiply_tp,
            #                                                         multiply_sl=multiply_sl)
            #         tot = self.clean_results(tot, sell, buy, each_pair)
            #         results_out[j] = tot['Result']
            #         wfe_oos[j] = self.wfe(tot['Result'])
            #     if plot:
            #         try:
            #             results_out.plot()
            #             plt.title(f'Out Sample {i}', fontsize=30)
            #             plt.grid()
            #             plt.show()
            #         except TypeError:
            #             print('Apenas prejuízos')
            #     wfe_oos = np.delete(wfe_oos, np.where(wfe_oos == 0.))
            #     self.del_period_data()
            #
            #     wfe_tot[str(c)] = pd.Series(wfe_oos / wfe_is)
            #
            #     c += 1
            #
            #     # Live
            #     if i == len(self.get_normal_walk_forward())-2:
            #         live = pd.DataFrame()
            #         self.set_period(len(self.get_normal_walk_forward()[i+1][0][0]), multi=True)
            #         self.walk_forward_split()
            #         for j in range(2,31):
            #             self.tpsl_calculation_otimization(j)
            #             tot, sell, buy, each_pair =  bt.otimizado_tpsl(self.get_normal_walk_forward()[i+1],
            #                                                             multiply_tp=multiply_tp,
            #                                                             multiply_sl=multiply_sl)
            #             tot = self.clean_results(tot, sell, buy, each_pair)
            #             live[j] = tot['Result']
            #         self.del_normal_walk_forward()
            #         self.del_period_data()
            #         if plot:
            #             try:
            #                 live.plot()
            #                 plt.title('Live', fontsize=30)
            #                 plt.grid()
            #                 plt.show()
            #             except TypeError:
            #                 print('Apenas prejuízos')
            # return wfe_tot
            print('Em desenvolvimento')
