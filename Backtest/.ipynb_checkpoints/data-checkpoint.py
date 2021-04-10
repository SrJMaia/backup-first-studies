import pandas as pd
import numpy as np
from constants import Pairs
from meta_trader import MetaTrader

class Data(MetaTrader, Pairs):

    def __init__(self, login, senha, servidor):
        super().__init__(login, senha, servidor)
        self.__normal_data = 0


    # Normal Data
    def get_normal_data(self):
        return self.__normal_data


    def set_normal_data(self, new_data):
        self.__normal_data = new_data


    def normal_data_to_array(self):
        self.__numpy_normal_data = self.pandas_to_array(self.get_normal_data())


    def get_numpy_normal_data(self):
        return self.__numpy_normal_data


    # Big Data
    def get_big_data(self):
        return self.__big_data


    def big_data_to_array(self):
        self.__numpy_big_data = self.pandas_to_array_big(self.get_big_data(), len(self.get_normal_data()))


    def get_numpy_big_data(self):
        return self.__numpy_big_data


    def get_normal_data_csv(self, path, separator=',', drop=False, drop_list=[]):
        """
        path = str do caminho do arquivo
        sepator = separador do csv
        drop = Se True, passar lista de colunas a serem dropadas
        """
        if drop:
            self.__normal_data = pd.read_csv(path, sep=separator).drop(columns=drop_list)
            print('Dados Carregados com Sucesso.')
        else:
            self.__normal_data = pd.read_csv(path, sep=separator)
            print('Dados Carregados com Sucesso.')


    def get_big_data_csv(self, path, separator=',', drop=False, drop_list=[]):
        """
        path = str do caminho do arquivo
        sepator = separador do csv
        drop = Se True, passar lista de colunas a serem dropadas
        """
        if drop:
            self.__big_data = pd.read_csv(path, sep=separator).drop(columns=drop_list)
            print('Dados Carregados com Sucesso.')
        else:
            self.__big_data = pd.read_csv(path, sep=separator)
            print('Dados Carregados com Sucesso.')


    def get_data_mt5_count(self,
                           start_pos,
                           end_pos,
                           time_frame,
                           all_four = False,
                           one_pair = False,
                           symbol = 'EURUSD',
                           only_one = 'open',
                           monte_carlo=False):

        df = pd.DataFrame()
        self.mt_login()
        if one_pair:
            if not all_four:
                df[symbol]=self.mt_get_data_count(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type=only_one)
            elif all_four:
                df[f'{symbol}_Open']=self.mt_get_data_count(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')
                df[f'{symbol}_Close']=self.mt_get_data_count(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='close')
                df[f'{symbol}_High']=self.mt_get_data_count(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='high')
                df[f'{symbol}_Low']=self.mt_get_data_count(symbol=symbol,start=start_pos,end=end_pos,time_frame=time_frame,data_type='low')
        elif not one_pair:
            x = []
            if not all_four:
                if only_one == 'open':
                    x = super().ALL_PAIRS_OPEN
                elif only_one == 'close':
                    x = super().ALL_PAIRS_CLOSE
                elif only_one == 'high':
                    x = super().ALL_PAIRS_HIGH
                elif only_one == 'low':
                    x = super().ALL_PAIRS_LOW

                for i in range(len(x)):
                    df[x[i]]=self.mt_get_data_count(symbol=super().ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type=only_one)
            elif all_four:
                for i in range(len(super().ALL_PAIRS)):
                    df[super().ALL_PAIRS_OPEN[i]]=self.mt_get_data_count(symbol=super().ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')
                    df[super().ALL_PAIRS_CLOSE[i]]=self.mt_get_data_count(symbol=super().ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='close')
                    df[super().ALL_PAIRS_HIGH[i]]=self.mt_get_data_count(symbol=super().ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='high')
                    df[super().ALL_PAIRS_LOW[i]]=self.mt_get_data_count(symbol=super().ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='low')

        self.mt_logoff()
        if monte_carlo:
            self.set_normal_data(df.sample(frac=1).reset_index(drop=True))
            print('Dados Baixados com Sucesso.')
        else:
            self.set_normal_data(df)
            print('Dados Baixados com Sucesso.')


    def pct_data(self, period=1, complement='_Open'):
        """
        No futuro colcoar a soma, subtração de todos os 4
        """
        new_data = self.get_normal_data()
        for i in super().DIFF_SYMBOLS:
            df = pd.DataFrame()
            for j in i[1]:
                df[j]=new_data[j+complement].pct_change(periods=period)
                if i[0] == 'gbp':
                    if j == 'EURGBP':
                        df[j] = df[j] * -1
                if i[0] == 'usd':
                    if j in ['GBPUSD','AUDUSD','NZDUSD','EURUSD']:
                        df[j] = df[j] * -1
                if i[0] == 'jpy':
                    df[j] = df[j] * -1
                if i[0] == 'chf':
                    if j in ['AUDCHF','CADCHF','USDCHF','EURCHF','GBPCHF','NZDCHF']:
                        df[j] = df[j] * -1
                if i[0] == 'nzd':
                    if j in ['AUDNZD','EURNZD','GBPNZD']:
                        df[j] = df[j] * -1
                if i[0] == 'aud':
                    if j in ['EURAUD','GBPAUD']:
                        df[j] = df[j] * -1
                if i[0] == 'cad':
                    if j in ['AUDCAD','USDCAD','EURCAD','GBPCAD','NZDCAD']:
                        df[j] = df[j] * -1
            new_data[f'{i[0]}'] = df.sum(axis=1)*100

        self.set_normal_data(new_data)


    @staticmethod
    def pandas_to_array_big(data, comp):

        array = np.array(
                [
                    np.transpose(np.array(data[['EURCHF_Open','EURCHF_High','EURCHF_Low','EURCHF_Close']])),
                    np.transpose(np.array(data[['EURGBP_Open','EURGBP_High','EURGBP_Low','EURGBP_Close']])),
                    np.transpose(np.array(data[['EURJPY_Open','EURJPY_High','EURJPY_Low','EURJPY_Close']])),
                    np.transpose(np.array(data[['EURNZD_Open','EURNZD_High','EURNZD_Low','EURNZD_Close']])),
                    np.transpose(np.array(data[['EURUSD_Open','EURUSD_High','EURUSD_Low','EURUSD_Close']])),
                    np.transpose(np.array(data[['EURAUD_Open','EURAUD_High','EURAUD_Low','EURAUD_Close']])),
                    np.transpose(np.array(data[['EURCAD_Open','EURCAD_High','EURCAD_Low','EURCAD_Close']])),
                    np.transpose(np.array(data[['GBPAUD_Open','GBPAUD_High','GBPAUD_Low','EURGBP_Close']])),
                    np.transpose(np.array(data[['GBPCHF_Open','GBPCHF_High','GBPCHF_Low','EURGBP_Close']])),
                    np.transpose(np.array(data[['GBPJPY_Open','GBPJPY_High','GBPJPY_Low','EURGBP_Close']])),
                    np.transpose(np.array(data[['GBPCAD_Open','GBPCAD_High','GBPCAD_Low','EURGBP_Close']])),
                    np.transpose(np.array(data[['GBPUSD_Open','GBPUSD_High','GBPUSD_Low','EURGBP_Close']])),
                    np.transpose(np.array(data[['GBPNZD_Open','GBPNZD_High','GBPNZD_Low','EURGBP_Close']])),
                    np.transpose(np.array(data[['USDCHF_Open','USDCHF_High','USDCHF_Low','EURUSD_Close']])),
                    np.transpose(np.array(data[['USDJPY_Open','USDJPY_High','USDJPY_Low','EURUSD_Close']])),
                    np.transpose(np.array(data[['AUDUSD_Open','AUDUSD_High','AUDUSD_Low','EURAUD_Close']])),
                    np.transpose(np.array(data[['NZDUSD_Open','NZDUSD_High','NZDUSD_Low','EURNZD_Close']])),
                    np.transpose(np.array(data[['USDCAD_Open','USDCAD_High','USDCAD_Low','EURUSD_Close']])),
                    np.transpose(np.array(data[['AUDJPY_Open','AUDJPY_High','AUDJPY_Low','EURAUD_Close']])),
                    np.transpose(np.array(data[['CADJPY_Open','CADJPY_High','CADJPY_Low','EURCAD_Close']])),
                    np.transpose(np.array(data[['CHFJPY_Open','CHFJPY_High','CHFJPY_Low','EURCHF_Close']])),
                    np.transpose(np.array(data[['NZDJPY_Open','NZDJPY_High','NZDJPY_Low','EURNZD_Close']])),
                    np.transpose(np.array(data[['AUDCHF_Open','AUDCHF_High','AUDCHF_Low','EURAUD_Close']])),
                    np.transpose(np.array(data[['CADCHF_Open','CADCHF_High','CADCHF_Low','EURCAD_Close']])),
                    np.transpose(np.array(data[['NZDCHF_Open','NZDCHF_High','NZDCHF_Low','EURNZD_Close']])),
                    np.transpose(np.array(data[['AUDNZD_Open','AUDNZD_High','AUDNZD_Low','EURAUD_Close']])),
                    np.transpose(np.array(data[['NZDCAD_Open','NZDCAD_High','NZDCAD_Low','EURNZD_Close']])),
                    np.transpose(np.array(data[['AUDCAD_Open','EURAUD_High','AUDCAD_Low','AUDCAD_Close']])),
                ], dtype=np.float64)

        massive = np.array([
                  [
                   np.array_split(array[0][0], comp),
                   np.array_split(array[0][1], comp),
                   np.array_split(array[0][2], comp),
                   np.array_split(array[0][3], comp)
                  ],
                  [
                   np.array_split(array[1][0], comp),
                   np.array_split(array[1][1], comp),
                   np.array_split(array[1][2], comp),
                   np.array_split(array[1][3], comp)
                  ],
                  [
                   np.array_split(array[2][0], comp),
                   np.array_split(array[2][1], comp),
                   np.array_split(array[2][2], comp),
                   np.array_split(array[2][3], comp)
                  ],
                  [
                   np.array_split(array[3][0], comp),
                   np.array_split(array[3][1], comp),
                   np.array_split(array[3][2], comp),
                   np.array_split(array[3][3], comp)
                  ],
                  [
                   np.array_split(array[4][0], comp),
                   np.array_split(array[4][1], comp),
                   np.array_split(array[4][2], comp),
                   np.array_split(array[4][3], comp)
                  ],
                  [
                   np.array_split(array[5][0], comp),
                   np.array_split(array[5][1], comp),
                   np.array_split(array[5][2], comp),
                   np.array_split(array[5][3], comp)
                  ],
                  [
                   np.array_split(array[6][0], comp),
                   np.array_split(array[6][1], comp),
                   np.array_split(array[6][2], comp),
                   np.array_split(array[6][3], comp)
                  ],
                  [
                   np.array_split(array[7][0], comp),
                   np.array_split(array[7][1], comp),
                   np.array_split(array[7][2], comp),
                   np.array_split(array[7][3], comp)
                  ],
                  [
                   np.array_split(array[8][0], comp),
                   np.array_split(array[8][1], comp),
                   np.array_split(array[8][2], comp),
                   np.array_split(array[8][3], comp)
                  ],
                  [
                   np.array_split(array[9][0], comp),
                   np.array_split(array[9][1], comp),
                   np.array_split(array[9][2], comp),
                   np.array_split(array[9][3], comp)
                  ],
                  [
                   np.array_split(array[10][0], comp),
                   np.array_split(array[10][1], comp),
                   np.array_split(array[10][2], comp),
                   np.array_split(array[10][3], comp)
                  ],
                  [
                   np.array_split(array[11][0], comp),
                   np.array_split(array[11][1], comp),
                   np.array_split(array[11][2], comp),
                   np.array_split(array[11][3], comp)
                  ],
                  [
                   np.array_split(array[12][0], comp),
                   np.array_split(array[12][1], comp),
                   np.array_split(array[12][2], comp),
                   np.array_split(array[12][3], comp)
                  ],
                  [
                   np.array_split(array[13][0], comp),
                   np.array_split(array[13][1], comp),
                   np.array_split(array[13][2], comp),
                   np.array_split(array[13][3], comp)
                  ],
                  [
                   np.array_split(array[14][0], comp),
                   np.array_split(array[14][1], comp),
                   np.array_split(array[14][2], comp),
                   np.array_split(array[14][3], comp)
                  ],
                  [
                   np.array_split(array[15][0], comp),
                   np.array_split(array[15][1], comp),
                   np.array_split(array[15][2], comp),
                   np.array_split(array[15][3], comp)
                  ],
                  [
                   np.array_split(array[16][0], comp),
                   np.array_split(array[16][1], comp),
                   np.array_split(array[16][2], comp),
                   np.array_split(array[16][3], comp)
                  ],
                  [
                   np.array_split(array[17][0], comp),
                   np.array_split(array[17][1], comp),
                   np.array_split(array[17][2], comp),
                   np.array_split(array[17][3], comp)
                  ],
                  [
                   np.array_split(array[18][0], comp),
                   np.array_split(array[18][1], comp),
                   np.array_split(array[18][2], comp),
                   np.array_split(array[18][3], comp)
                  ],
                  [
                   np.array_split(array[19][0], comp),
                   np.array_split(array[19][1], comp),
                   np.array_split(array[19][2], comp),
                   np.array_split(array[19][3], comp)
                  ],
                  [
                   np.array_split(array[20][0], comp),
                   np.array_split(array[20][1], comp),
                   np.array_split(array[20][2], comp),
                   np.array_split(array[20][3], comp)
                  ],
                  [
                   np.array_split(array[21][0], comp),
                   np.array_split(array[21][1], comp),
                   np.array_split(array[21][2], comp),
                   np.array_split(array[21][3], comp)
                  ],
                  [
                   np.array_split(array[22][0], comp),
                   np.array_split(array[22][1], comp),
                   np.array_split(array[22][2], comp),
                   np.array_split(array[22][3], comp)
                  ],
                  [
                   np.array_split(array[23][0], comp),
                   np.array_split(array[23][1], comp),
                   np.array_split(array[23][2], comp),
                   np.array_split(array[23][3], comp)
                  ],
                  [
                   np.array_split(array[24][0], comp),
                   np.array_split(array[24][1], comp),
                   np.array_split(array[24][2], comp),
                   np.array_split(array[24][3], comp)
                  ],
                  [
                   np.array_split(array[25][0], comp),
                   np.array_split(array[25][1], comp),
                   np.array_split(array[25][2], comp),
                   np.array_split(array[25][3], comp)
                  ],
                  [
                   np.array_split(array[26][0], comp),
                   np.array_split(array[26][1], comp),
                   np.array_split(array[26][2], comp),
                   np.array_split(array[26][3], comp)
                  ],
                  [
                   np.array_split(array[27][0], comp),
                   np.array_split(array[27][1], comp),
                   np.array_split(array[27][2], comp),
                   np.array_split(array[27][3], comp)
                  ]
        ])

        return massive


    @staticmethod
    def pandas_to_array(data):

        array = np.array(
                [
                    np.transpose(np.array(data[['EURCHF_Open','EURCHF_buy','EURCHF_sell','EURCHF_Open','EURCHF_High','EURCHF_Low']])),
                    np.transpose(np.array(data[['EURGBP_Open','EURGBP_buy','EURGBP_sell','EURGBP_Open','EURGBP_High','EURGBP_Low']])),
                    np.transpose(np.array(data[['EURJPY_Open','EURJPY_buy','EURJPY_sell','EURJPY_Open','EURJPY_High','EURJPY_Low']])),
                    np.transpose(np.array(data[['EURNZD_Open','EURNZD_buy','EURNZD_sell','EURNZD_Open','EURNZD_High','EURNZD_Low']])),
                    np.transpose(np.array(data[['EURUSD_Open','EURUSD_buy','EURUSD_sell','EURUSD_Open','EURUSD_High','EURUSD_Low']])),
                    np.transpose(np.array(data[['EURAUD_Open','EURAUD_buy','EURAUD_sell','EURAUD_Open','EURAUD_High','EURAUD_Low']])),
                    np.transpose(np.array(data[['EURCAD_Open','EURCAD_buy','EURCAD_sell','EURCAD_Open','EURCAD_High','EURCAD_Low']])),
                    np.transpose(np.array(data[['GBPAUD_Open','GBPAUD_buy','GBPAUD_sell','EURGBP_Open','GBPAUD_High','GBPAUD_Low']])),
                    np.transpose(np.array(data[['GBPCHF_Open','GBPCHF_buy','GBPCHF_sell','EURGBP_Open','GBPCHF_High','GBPCHF_Low']])),
                    np.transpose(np.array(data[['GBPJPY_Open','GBPJPY_buy','GBPJPY_sell','EURGBP_Open','GBPJPY_High','GBPJPY_Low']])),
                    np.transpose(np.array(data[['GBPCAD_Open','GBPCAD_buy','GBPCAD_sell','EURGBP_Open','GBPCAD_High','GBPCAD_Low']])),
                    np.transpose(np.array(data[['GBPUSD_Open','GBPUSD_buy','GBPUSD_sell','EURGBP_Open','GBPUSD_High','GBPUSD_Low']])),
                    np.transpose(np.array(data[['GBPNZD_Open','GBPNZD_buy','GBPNZD_sell','EURGBP_Open','GBPNZD_High','GBPNZD_Low']])),
                    np.transpose(np.array(data[['USDCHF_Open','USDCHF_buy','USDCHF_sell','EURUSD_Open','USDCHF_High','USDCHF_Low']])),
                    np.transpose(np.array(data[['USDJPY_Open','USDJPY_buy','USDJPY_sell','EURUSD_Open','USDJPY_High','USDJPY_Low']])),
                    np.transpose(np.array(data[['AUDUSD_Open','AUDUSD_buy','AUDUSD_sell','EURAUD_Open','AUDUSD_High','AUDUSD_Low']])),
                    np.transpose(np.array(data[['NZDUSD_Open','NZDUSD_buy','NZDUSD_sell','EURNZD_Open','NZDUSD_High','NZDUSD_Low']])),
                    np.transpose(np.array(data[['USDCAD_Open','USDCAD_buy','USDCAD_sell','EURUSD_Open','USDCAD_High','USDCAD_Low']])),
                    np.transpose(np.array(data[['AUDJPY_Open','AUDJPY_buy','AUDJPY_sell','EURAUD_Open','AUDJPY_High','AUDJPY_Low']])),
                    np.transpose(np.array(data[['CADJPY_Open','CADJPY_buy','CADJPY_sell','EURCAD_Open','CADJPY_High','CADJPY_Low']])),
                    np.transpose(np.array(data[['CHFJPY_Open','CHFJPY_buy','CHFJPY_sell','EURCHF_Open','CHFJPY_High','CHFJPY_Low']])),
                    np.transpose(np.array(data[['NZDJPY_Open','NZDJPY_buy','NZDJPY_sell','EURNZD_Open','NZDJPY_High','NZDJPY_Low']])),
                    np.transpose(np.array(data[['AUDCHF_Open','AUDCHF_buy','AUDCHF_sell','EURAUD_Open','AUDCHF_High','AUDCHF_Low']])),
                    np.transpose(np.array(data[['CADCHF_Open','CADCHF_buy','CADCHF_sell','EURCAD_Open','CADCHF_High','CADCHF_Low']])),
                    np.transpose(np.array(data[['NZDCHF_Open','NZDCHF_buy','NZDCHF_sell','EURNZD_Open','NZDCHF_High','NZDCHF_Low']])),
                    np.transpose(np.array(data[['AUDNZD_Open','AUDNZD_buy','AUDNZD_sell','EURAUD_Open','AUDNZD_High','AUDNZD_Low']])),
                    np.transpose(np.array(data[['NZDCAD_Open','NZDCAD_buy','NZDCAD_sell','EURNZD_Open','NZDCAD_High','NZDCAD_Low']])),
                    np.transpose(np.array(data[['AUDCAD_Open','AUDCAD_buy','AUDCAD_sell','EURAUD_Open','AUDCAD_High','AUDCAD_Low']])),
                ], dtype=np.float64)
        return array


    def walk_forward_split(self):
        """
        Futuramente em big_data, dividir antes e depois passar para array
        dará menos trabalho
        """

        tot_len = len(self.get_normal_data())

        split1 = int(round(tot_len * 0.105, 0))
        split2 = int(round(tot_len * 0.14, 0))
        split3 = int(round(tot_len * 0.245, 0))
        split4 = int(round(tot_len * 0.28, 0))
        split5 = int(round(tot_len * 0.385, 0))
        split6 = int(round(tot_len * 0.42, 0))
        split7 = int(round(tot_len * 0.525, 0))
        split8 = int(round(tot_len * 0.56, 0))
        split9 = int(round(tot_len * 0.665, 0))
        split10 = int(round(tot_len * 0.7, 0))

        self.walk1 = self.pandas_to_array(self.get_normal_data()[:split1])
        self.test1 = self.pandas_to_array(self.get_normal_data()[split1:split2])
        self.walk2 = self.pandas_to_array(self.get_normal_data()[split2:split3])
        self.test2 = self.pandas_to_array(self.get_normal_data()[split3:split4])
        self.walk3 = self.pandas_to_array(self.get_normal_data()[split4:split5])
        self.test3 = self.pandas_to_array(self.get_normal_data()[split5:split6])
        self.walk4 = self.pandas_to_array(self.get_normal_data()[split6:split7])
        self.test4 = self.pandas_to_array(self.get_normal_data()[split7:split8])
        self.walk5 = self.pandas_to_array(self.get_normal_data()[split8:split9])
        self.test5 = self.pandas_to_array(self.get_normal_data()[split9:split10])
        self.final = self.pandas_to_array(self.get_normal_data()[split10:])
        self.data_numpy = self.pandas_to_array(self.get_normal_data())

        x = (len(self.walk1) + len(self.test1) + len(self.walk2) +
            len(self.test2) + len(self.walk3) + len(self.test3) +
            len(self.walk4) + len(self.test4) + len(self.walk5) +
            len(self.test5) + len(self.final))
        y = len(self.data)

        print(f'Dados tem len de {y} e o split tem len de {x}.')
