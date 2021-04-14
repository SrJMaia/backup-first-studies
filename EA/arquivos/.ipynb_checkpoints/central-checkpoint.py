from arquivos.signals import Signals
import pandas as pd
import numpy as np
import arquivos.backtest as bt
import arquivos.analysis_functions as af
import matplotlib.pyplot as plt
plt.style.use('dark_background')
plt.rcParams["figure.figsize"] = (30,10)


class Central(Signals):

    def __init__(self, login=5528104, senha='YUWNehok', servidor='ActivTradesCorp-Server', balance=1000):
        super().__init__(login, senha, servidor)
        self.balance = balance


    def back_tpsl(self, tpsl, multiply_tpsl, multi_test=False, plot=False):
        """
        se for um multi_test tpsl devera ser uma lista dos take profit e stop loss
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        if multi_test:
            self.walk_forward_split()
            bests_out_sample = []
            for i in range(1,len(self.get_normal_walk_forward()),2):
                results_walk = pd.DataFrame()
                for j in tpsl:
                    tot, _, _, _ =  bt.otimizado_tpsl(self.get_normal_walk_forward()[i-1], j, multiply_tpsl)
                    tot = np.delete(tot, np.where(tot == 0.))
                    results_walk[j] = pd.Series(tot)
                if plot:
                    try:
                        results_walk.plot()
                        plt.title(f'In Sample {i-1}', fontsize=30)
                        plt.grid()
                        plt.show()
                    except TypeError:
                        print('Apenas prejuízos')

                results_out = pd.DataFrame()
                for j in results_walk.columns:
                    tot, _, _, _ =  bt.otimizado_tpsl(self.get_normal_walk_forward()[i], j, multiply_tpsl)
                    tot = np.delete(tot, np.where(tot == 0.))
                    results_out[j] = pd.Series(tot)
                if plot:
                    try:
                        results_out.plot()
                        plt.title(f'Out Sample {i}', fontsize=30)
                        plt.grid()
                        plt.show()
                        bests_out_sample.append(results_out.columns)
                    except TypeError:
                        print('Apenas prejuízos')

                if i == len(self.get_normal_walk_forward())-2:
                    x = af.compare(bests_out_sample)
                    live = pd.DataFrame()
                    for j in x:
                        tot, _, _, _ =  bt.otimizado_tpsl(self.get_normal_walk_forward()[i+1], j, multiply_tpsl)
                        tot = np.delete(tot, np.where(tot == 0.))
                        live[j] = pd.Series(tot)
                    if plot:
                        try:
                            live.plot()
                            plt.title('Live', fontsize=30)
                            plt.grid()
                            plt.show()
                        except TypeError:
                            print('Apenas prejuízos')

        else:
            tot, sell, buy, each_pair =  bt.otimizado_tpsl(self.get_numpy_normal_data(), tpsl=tpsl, multiply_tpsl=multiply_tpsl)
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


    def back_tpsl_ohl(self, tpsl, multiply_tpsl, multi_test=False, plot=False):
        """
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        if multi_test:
            self.walk_forward_split()
            bests_out_sample = []
            for i in range(1,len(self.get_normal_walk_forward()),2):
                results_walk = pd.DataFrame()
                for j in tpsl:
                    tot, _, _, _ =  bt.otimizado_tpsl_ohl(self.get_normal_walk_forward()[i-1], j, multiply_tpsl)
                    tot = np.delete(tot, np.where(tot == 0.))
                    results_walk[j] = pd.Series(tot)
                if plot:
                    try:
                        results_walk.plot()
                        plt.title(f'In Sample {i-1}', fontsize=30)
                        plt.grid()
                        plt.show()
                    except TypeError:
                        print('Apenas prejuízos')

                results_out = pd.DataFrame()
                for j in results_walk.columns:
                    tot, _, _, _ =  bt.otimizado_tpsl_ohl(self.get_normal_walk_forward()[i], j, multiply_tpsl)
                    tot = np.delete(tot, np.where(tot == 0.))
                    results_out[j] = pd.Series(tot)
                if plot:
                    try:
                        results_out.plot()
                        plt.title(f'Out Sample {i}', fontsize=30)
                        plt.grid()
                        plt.show()
                        bests_out_sample.append(results_out.columns)
                    except TypeError:
                        print('Apenas prejuízos')

                if i == len(self.get_normal_walk_forward())-2:
                    x = af.compare(bests_out_sample)
                    live = pd.DataFrame()
                    for j in x:
                        tot, _, _, _ =  bt.otimizado_tpsl_ohl(self.get_normal_walk_forward()[i+1], j, multiply_tpsl)
                        tot = np.delete(tot, np.where(tot == 0.))
                        live[j] = pd.Series(tot)
                    if plot:
                        try:
                            live.plot()
                            plt.title('Live', fontsize=30)
                            plt.grid()
                            plt.show()
                        except TypeError:
                            print('Apenas prejuízos')
        else:
            tot, sell, buy, each_pair =  bt.otimizado_tpsl_ohl(self.get_numpy_normal_data(), tpsl=tpsl, multiply_tpsl=multiply_tpsl)
            tot = np.delete(tot, np.where(tot == 0.))
            sell = np.delete(sell, np.where(sell == 0.))
            buy = np.delete(buy, np.where(buy == 0.))
            results_df = pd.DataFrame()
            for index, value in enumerate(each_pair):
                results_df[super().ALL_PAIRS[index]] = pd.Series(np.delete(value, np.where(value == 0.)))
            return tot, sell, buy, results_df


    def back_big_tpsl_ohl(self, tpsl, multiply_tpsl):
        """
        Cuidar no split, de big data pois usa len(data normal)
        tem que haver uma divisão inteira, caso contrario sera criado
        um array dtype=object
        Returns
        list_backtest = Todos os trades
        sell_orders
        buy_orders
        each_pair = resultado de cada par
        """
        if multi_test:
            self.walk_forward_split()
            bests_out_sample = []
            for i in range(1,len(self.get_normal_walk_forward()),2):
                results_walk = pd.DataFrame()
                for j in tpsl:
                    tot, _, _, _ =  bt.big_backtest_otimizado_tpsl(self.get_normal_walk_forward()[i-1], j, multiply_tpsl)
                    tot = np.delete(tot, np.where(tot == 0.))
                    results_walk[j] = pd.Series(tot)
                if plot:
                    try:
                        results_walk.plot()
                        plt.title(f'In Sample {i-1}', fontsize=30)
                        plt.grid()
                        plt.show()
                    except TypeError:
                        print('Apenas prejuízos')

                results_out = pd.DataFrame()
                for j in results_walk.columns:
                    tot, _, _, _ =  bt.big_backtest_otimizado_tpsl(self.get_normal_walk_forward()[i], j, multiply_tpsl)
                    tot = np.delete(tot, np.where(tot == 0.))
                    results_out[j] = pd.Series(tot)
                if plot:
                    try:
                        results_out.plot()
                        plt.title(f'Out Sample {i}', fontsize=30)
                        plt.grid()
                        plt.show()
                        bests_out_sample.append(results_out.columns)
                    except TypeError:
                        print('Apenas prejuízos')

                if i == len(self.get_normal_walk_forward())-2:
                    x = af.compare(bests_out_sample)
                    live = pd.DataFrame()
                    for j in x:
                        tot, _, _, _ =  bt.big_backtest_otimizado_tpsl(self.get_normal_walk_forward()[i+1], j, multiply_tpsl)
                        tot = np.delete(tot, np.where(tot == 0.))
                        live[j] = pd.Series(tot)
                    if plot:
                        try:
                            live.plot()
                            plt.title('Live', fontsize=30)
                            plt.grid()
                            plt.show()
                        except TypeError:
                            print('Apenas prejuízos')
        else:
            tot, sell, buy, each_pair =  bt.big_backtest_otimizado_tpsl(self.get_numpy_normal_data(), self.get_numpy_big_data(), tpsl=tpsl, multiply_tpsl=multiply_tpsl)
            tot = np.delete(tot, np.where(tot == 0.))
            sell = np.delete(sell, np.where(sell == 0.))
            buy = np.delete(buy, np.where(buy == 0.))
            results_df = pd.DataFrame()
            for index, value in enumerate(each_pair):
                results_df[super().ALL_PAIRS[index]] = pd.Series(np.delete(value, np.where(value == 0.)))
            return tot, sell, buy, results_df
