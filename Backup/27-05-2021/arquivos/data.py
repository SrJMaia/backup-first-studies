import pandas as pd
import numpy as np
from arquivos.constants import Pairs
from arquivos.meta_trader import MetaTrader

class Data(MetaTrader, Pairs):

    def __init__(self, login, senha, servidor):
        super().__init__(login, senha, servidor)
        self.__normal_data = 0


    # Normal Data
    def get_normal_data(self):
        return self.__normal_data


    def set_normal_data(self, new_data):
        self.__normal_data = new_data


    def get_new_normal_data(self):
        return self.__new_normal_data


    def set_new_normal_data(self, data):
        self.__new_normal_data = data


    def normal_data_to_array(self):
        self.__numpy_normal_data = self.pandas_to_array(self.get_normal_data())


    def del_numpy_normal_data(self):
        del self.__numpy_normal_data


    def get_numpy_normal_data(self):
        return self.__numpy_normal_data


    def get_normal_walk_forward(self):
        return self.normal_walk_forward


    def del_normal_walk_forward(self):
        del self.normal_walk_forward


    # Big Data
    def get_big_data(self):
        return self.__big_data


    def set_big_data(self, df):
        self.__big_data = df


    def big_data_to_array(self):
        self.__numpy_big_data = self.pandas_to_array_big(self.get_big_data(), len(self.get_normal_data()))


    def big_data_to_array_wfa(self, comp, start, stop):
        self.__numpy_big_data = self.pandas_to_array_big_wfa(self.get_big_data(),
                                                            comp,
                                                            start,
                                                            stop,
                                                            self.division_big_data)


    def get_numpy_big_data(self):
        return self.__numpy_big_data


    def del_numpy_big_data(self):
        del self.__numpy_big_data


    def del_big_data(self):
        del self.__big_data


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
                           monte_carlo=False,
                           ea=False):

        df = pd.DataFrame()
        self.mt_login()

        if ea:
            for i in range(len(self.ALL_PAIRS)):
                df[self.ALL_PAIRS[i]]=self.mt_get_data_count(symbol=super().ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type='open')

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


    def new_normal_data_mt5(self, start_pos, end_pos, time_frame):

        df = pd.DataFrame()

        for i in range(len(super().ALL_PAIRS)):
            for j in ['Open','High','Low','Close']:
                df[super().ALL_PAIRS[i]+'_'+j]=self.mt_get_data_count(symbol=super().ALL_PAIRS[i],start=start_pos,end=end_pos,time_frame=time_frame,data_type=j.lower())

        self.set_new_normal_data(df)
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
            new_data[f'{i[0]}'] = round(df.sum(axis=1)*100_000)

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
                   np.array_split(array[0][0], comp),# [par][open]
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
    def pandas_to_array_big_wfa(data, comp, start, stop, div):

        array = np.array(
                [
                    np.transpose(np.array(data[['EURCHF_Open','EURCHF_High','EURCHF_Low','EURCHF_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['EURGBP_Open','EURGBP_High','EURGBP_Low','EURGBP_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['EURJPY_Open','EURJPY_High','EURJPY_Low','EURJPY_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['EURNZD_Open','EURNZD_High','EURNZD_Low','EURNZD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['EURUSD_Open','EURUSD_High','EURUSD_Low','EURUSD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['EURAUD_Open','EURAUD_High','EURAUD_Low','EURAUD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['EURCAD_Open','EURCAD_High','EURCAD_Low','EURCAD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['GBPAUD_Open','GBPAUD_High','GBPAUD_Low','EURGBP_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['GBPCHF_Open','GBPCHF_High','GBPCHF_Low','EURGBP_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['GBPJPY_Open','GBPJPY_High','GBPJPY_Low','EURGBP_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['GBPCAD_Open','GBPCAD_High','GBPCAD_Low','EURGBP_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['GBPUSD_Open','GBPUSD_High','GBPUSD_Low','EURGBP_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['GBPNZD_Open','GBPNZD_High','GBPNZD_Low','EURGBP_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['USDCHF_Open','USDCHF_High','USDCHF_Low','EURUSD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['USDJPY_Open','USDJPY_High','USDJPY_Low','EURUSD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['AUDUSD_Open','AUDUSD_High','AUDUSD_Low','EURAUD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['NZDUSD_Open','NZDUSD_High','NZDUSD_Low','EURNZD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['USDCAD_Open','USDCAD_High','USDCAD_Low','EURUSD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['AUDJPY_Open','AUDJPY_High','AUDJPY_Low','EURAUD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['CADJPY_Open','CADJPY_High','CADJPY_Low','EURCAD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['CHFJPY_Open','CHFJPY_High','CHFJPY_Low','EURCHF_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['NZDJPY_Open','NZDJPY_High','NZDJPY_Low','EURNZD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['AUDCHF_Open','AUDCHF_High','AUDCHF_Low','EURAUD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['CADCHF_Open','CADCHF_High','CADCHF_Low','EURCAD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['NZDCHF_Open','NZDCHF_High','NZDCHF_Low','EURNZD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['AUDNZD_Open','AUDNZD_High','AUDNZD_Low','EURAUD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['NZDCAD_Open','NZDCAD_High','NZDCAD_Low','EURNZD_Close']].iloc[start*div:stop*div])),
                    np.transpose(np.array(data[['AUDCAD_Open','EURAUD_High','AUDCAD_Low','AUDCAD_Close']].iloc[start*div:stop*div])),
                ], dtype=np.float64)

        massive = np.array([
                  [
                   np.array_split(array[0][0], comp),# [par][open]
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
                    np.transpose(np.array(data[['EURCHF_Open','EURCHF_buy','EURCHF_sell','EURCHF_High','EURCHF_Low','EURCHF_TPSL']])),
                    np.transpose(np.array(data[['EURGBP_Open','EURGBP_buy','EURGBP_sell','EURGBP_High','EURGBP_Low','EURGBP_TPSL']])),
                    np.transpose(np.array(data[['EURJPY_Open','EURJPY_buy','EURJPY_sell','EURJPY_High','EURJPY_Low','EURJPY_TPSL']])),
                    np.transpose(np.array(data[['EURNZD_Open','EURNZD_buy','EURNZD_sell','EURNZD_High','EURNZD_Low','EURNZD_TPSL']])),
                    np.transpose(np.array(data[['EURUSD_Open','EURUSD_buy','EURUSD_sell','EURUSD_High','EURUSD_Low','EURUSD_TPSL']])),
                    np.transpose(np.array(data[['EURAUD_Open','EURAUD_buy','EURAUD_sell','EURAUD_High','EURAUD_Low','EURAUD_TPSL']])),
                    np.transpose(np.array(data[['EURCAD_Open','EURCAD_buy','EURCAD_sell','EURCAD_High','EURCAD_Low','EURCAD_TPSL']])),
                    np.transpose(np.array(data[['GBPAUD_Open','GBPAUD_buy','GBPAUD_sell','GBPAUD_High','GBPAUD_Low','GBPAUD_TPSL']])),
                    np.transpose(np.array(data[['GBPCHF_Open','GBPCHF_buy','GBPCHF_sell','GBPCHF_High','GBPCHF_Low','GBPCHF_TPSL']])),
                    np.transpose(np.array(data[['GBPJPY_Open','GBPJPY_buy','GBPJPY_sell','GBPJPY_High','GBPJPY_Low','GBPJPY_TPSL']])),
                    np.transpose(np.array(data[['GBPCAD_Open','GBPCAD_buy','GBPCAD_sell','GBPCAD_High','GBPCAD_Low','GBPCAD_TPSL']])),
                    np.transpose(np.array(data[['GBPUSD_Open','GBPUSD_buy','GBPUSD_sell','GBPUSD_High','GBPUSD_Low','GBPUSD_TPSL']])),
                    np.transpose(np.array(data[['GBPNZD_Open','GBPNZD_buy','GBPNZD_sell','GBPNZD_High','GBPNZD_Low','GBPNZD_TPSL']])),
                    np.transpose(np.array(data[['USDCHF_Open','USDCHF_buy','USDCHF_sell','USDCHF_High','USDCHF_Low','USDCHF_TPSL']])),
                    np.transpose(np.array(data[['USDJPY_Open','USDJPY_buy','USDJPY_sell','USDJPY_High','USDJPY_Low','USDJPY_TPSL']])),
                    np.transpose(np.array(data[['AUDUSD_Open','AUDUSD_buy','AUDUSD_sell','AUDUSD_High','AUDUSD_Low','AUDUSD_TPSL']])),
                    np.transpose(np.array(data[['NZDUSD_Open','NZDUSD_buy','NZDUSD_sell','NZDUSD_High','NZDUSD_Low','NZDUSD_TPSL']])),
                    np.transpose(np.array(data[['USDCAD_Open','USDCAD_buy','USDCAD_sell','USDCAD_High','USDCAD_Low','USDCAD_TPSL']])),
                    np.transpose(np.array(data[['AUDJPY_Open','AUDJPY_buy','AUDJPY_sell','AUDJPY_High','AUDJPY_Low','AUDJPY_TPSL']])),
                    np.transpose(np.array(data[['CADJPY_Open','CADJPY_buy','CADJPY_sell','CADJPY_High','CADJPY_Low','CADJPY_TPSL']])),
                    np.transpose(np.array(data[['CHFJPY_Open','CHFJPY_buy','CHFJPY_sell','CHFJPY_High','CHFJPY_Low','CHFJPY_TPSL']])),
                    np.transpose(np.array(data[['NZDJPY_Open','NZDJPY_buy','NZDJPY_sell','NZDJPY_High','NZDJPY_Low','NZDJPY_TPSL']])),
                    np.transpose(np.array(data[['AUDCHF_Open','AUDCHF_buy','AUDCHF_sell','AUDCHF_High','AUDCHF_Low','AUDCHF_TPSL']])),
                    np.transpose(np.array(data[['CADCHF_Open','CADCHF_buy','CADCHF_sell','CADCHF_High','CADCHF_Low','CADCHF_TPSL']])),
                    np.transpose(np.array(data[['NZDCHF_Open','NZDCHF_buy','NZDCHF_sell','NZDCHF_High','NZDCHF_Low','NZDCHF_TPSL']])),
                    np.transpose(np.array(data[['AUDNZD_Open','AUDNZD_buy','AUDNZD_sell','AUDNZD_High','AUDNZD_Low','AUDNZD_TPSL']])),
                    np.transpose(np.array(data[['NZDCAD_Open','NZDCAD_buy','NZDCAD_sell','NZDCAD_High','NZDCAD_Low','NZDCAD_TPSL']])),
                    np.transpose(np.array(data[['AUDCAD_Open','AUDCAD_buy','AUDCAD_sell','AUDCAD_High','AUDCAD_Low','AUDCAD_TPSL']])),
                ], dtype=np.float64)
        return array


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
