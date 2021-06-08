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
        self.otimization_flag = True


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


    def prepare_otimization(self, period, fix_tpsl=False):
        if fix_tpsl:
            df = self.get_normal_data()
            df['TPSL'] = 0
            self.set_normal_data(df)
        else:
            self.tpsl_calculation_otimization_single(period)
        self.normal_data_to_array()
        np.nan_to_num(self.get_numpy_normal_data()[6], copy=False, nan=0.0)
        np.nan_to_num(self.get_numpy_normal_data()[7], copy=False, nan=0.0)
        self.size_buy = int(self.get_numpy_normal_data()[7].sum() + 1)
        self.size_sell = int(self.get_numpy_normal_data()[6].sum() + 1)


    def otimization_exit(self):
        self.otimization_flag = True


    def back_tpsl(self,
                multiply_tp,
                multiply_sl,
                tpsl_mean=14,
                fix_tpsl=False,
                uni_flag=False,
                jpy=False,
                analyse=True,
                plot=False,
                single_test=False,
                otimization=False):
        """
        single_test = True
            Deverá ser chamado antes robot.tpsl_calculation_otimization_single(periodo)
                                    robot.normal_data_to_array()
        otimization = True
            Apenas passar tpsl_mean
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        if single_test:

            if otimization and self.otimization_flag:
                self.prepare_otimization(tpsl_mean, fix_tpsl=fix_tpsl)
                self.otimization_flag = False

            tot, sell, buy = bt.single_backtest(self.get_numpy_normal_data(),
                                                multiply_tp=multiply_tp,
                                                multiply_sl=multiply_sl,
                                                size_buy=self.size_buy,
                                                size_sell=self.size_sell,
                                                fix_tpsl=fix_tpsl,
                                                universal_flag=uni_flag,
                                                jpy=jpy)

            if analyse:
                return self.analysis_backtest(self.clean_results(tot, sell, buy))
            else:
                return self.clean_results(tot, sell, buy)
        elif not single_test:
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
