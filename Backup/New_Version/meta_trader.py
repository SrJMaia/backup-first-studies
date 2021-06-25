import MetaTrader5 as mt5
import pandas as pd

class MetaTrader:

    def __init__(self, login, senha, servidor):
        """
        login = int
        senha = str
        servidor = str

        """
        self.login = login
        self.senha = senha
        self.servidor = servidor


    def mt_login(self):
        mt5.initialize()
        if not mt5.initialize(login=self.login, password=self.senha, server=self.servidor):
            print('MT5 não iniciado.')
            mt5.shutdown()


    @staticmethod
    def mt_logoff():
        mt5.shutdown()


    def mt_get_data_count(self, symbol, start, end, time_frame, data_type='close'):
        tf = {'M1':mt5.TIMEFRAME_M1, 'M5':mt5.TIMEFRAME_M5, 'M15':mt5.TIMEFRAME_M15,
              'M30':mt5.TIMEFRAME_M30, 'H1':mt5.TIMEFRAME_H1, 'H4':mt5.TIMEFRAME_H4,
              'D1':mt5.TIMEFRAME_D1, 'W1':mt5.TIMEFRAME_W1}
        dt = pd.DataFrame(mt5.copy_rates_from_pos(symbol, tf[time_frame] , start, end))[data_type]
        return dt
