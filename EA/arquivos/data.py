import pandas as pd
import numpy as np
from arquivos.constants import Pairs
from arquivos.meta_trader import MetaTrader

class Data(MetaTrader, Pairs):

    def __init__(self, login, senha, servidor):
        super().__init__(login, senha, servidor)


    # Normal Data
    def get_normal_data(self):
        return self.__normal_data


    def set_normal_data(self, new_data):
        self.__normal_data = new_data


    def get_tf_data(self):
        return self.__tf_data


    def normal_data_to_array(self):
        array = self.get_normal_data()[[f'{__single_pair_name}_Open',
                                        f'{__single_pair_name}_High',
                                        f'{__single_pair_name}_Low',
                                        f'{__single_pair_name}_Close',
                                        f'{__data_timeframe}',
                                        'Sell_Flag',
                                        'Buy_Flag']].to_numpy().T

        array = array = array.astype(np.float64)

        self.__numpy_normal_data = array


    def del_numpy_normal_data(self):
        del self.__numpy_normal_data


    def get_numpy_normal_data(self):
        return self.__numpy_normal_data


    # EA Online
    def get_new_normal_data(self):
        return self.__new_normal_data


    def set_new_normal_data(self, data):
        self.__new_normal_data = data


    def get_normal_data_csv(self,
                            path,
                            timeframe,
                            pair,
                            single_currency=False,
                            separator=',',
                            drop=False,
                            drop_list=[]):
        """
        path = str do caminho do arquivo
        timeframe = 'H1', 'H4', 'D1'
        sepator = separador do csv
        drop = Se True, passar lista de colunas a serem dropadas
        """
        if single_currency:
            self.__single_pair_name = pair
        self.__data_timeframe = timeframe
        if drop:
            self.__normal_data = pd.read_csv(path, sep=separator).drop(columns=drop_list)
        else:
            self.__normal_data = pd.read_csv(path, sep=separator)

        if timeframe == 'H1':
            self.__tf_data = self.get_normal_data().loc[self.get_normal_data()['time'].dt.minute == 0, f'{pair}_Open']
        elif timeframe == 'H4':
            self.__tf_data = self.get_normal_data().loc[(self.get_normal_data()['time'].dt.hour.isin([0, 4, 8, 12, 16, 20])) & (self.get_normal_data()['time'].dt.minute == 0), f'{pair}_Open']
        elif tiemframe == 'D1':
            self.__tf_data = self.get_normal_data().loc[(self.get_normal_data()['time'].dt.hour == 0) & (self.get_normal_data()['time'].dt.minute == 0), f'{pair}_Open']

        print('Dados Carregados com Sucesso.')


    def walk_forward_split(self):
        """
        Futuramente em big_data, dividir antes e depois passar para array
        dará menos trabalho
        """

        c = 0
        comp = len(self.get_normal_data())
        lista = []
        initial = 0.
        final = 0.7
        step = 0.05
        c_final = int(final/step)
        index_count = []
        for i in np.arange(initial, final, step):
            ind_c = []
            if c == 0:
                array = self.pandas_to_array(self.get_normal_data()[:int(comp*0.15)])
                lista.append(array)
                ind_c.append([0, int(comp*0.15)])
                array = self.pandas_to_array(self.get_normal_data()[int(comp*0.15):int(comp*0.2)])
                ind_c.append([int(comp*0.15), int(comp*0.2)])
                lista.append(array)
                index_count.append(ind_c)
            elif c == c_final:
                array = self.pandas_to_array(self.get_normal_data()[int(comp*(i+0.15)):])
                ind_c.append([int(comp*(i+0.15)), len(self.get_normal_data())])
                lista.append(array)
                index_count.append(ind_c)
                break
            else:
                array = self.pandas_to_array(self.get_normal_data()[int(comp*i):int(comp*(i+0.15))])
                ind_c.append([int(comp*i), int(comp*(i+0.15))])
                lista.append(array)
                array = self.pandas_to_array(self.get_normal_data()[int(comp*(i+0.15)):int(comp*(i+0.2))])
                ind_c.append([int(comp*(i+0.15)), int(comp*(i+0.2))])
                lista.append(array)
                index_count.append(ind_c)
            c += 1

        self.normal_walk_forward = lista
        self.index_list_wfa = index_count
