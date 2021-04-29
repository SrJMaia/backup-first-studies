from arquivos.signals import Signals
import pandas as pd
import numpy as np
from time import sleep
import schedule

class eaonline(Signals):

    def __init__(self,
                 risk,
                 multiply,
                 magic_number,
                 timeframe,
                 tpsl,
                 pct_period,
                 login=50549136,
                 senha='TqmGUgqp',
                 servidor='ICMarketsSC-Demo'):
        super().__init__(login, senha, servidor)
        self.risk = risk
        self.multiply = multiply
        self.magic_number = magic_number
        self.get_final = 0
        if timeframe == 'D1':
            self.get_final == 3000
        elif timeframe == 'H4':
            self.get_final == 17000
        elif timeframe == 'H1':
            self.get_final == 66000
        self.tf = timeframe
        self.tpsl = tpsl
        self.pct_period = pct_period
        self.control_dict = super().MY_EVENTS


    def lot_calculation(self, balance, symbol):
        lot = round(balance/100_000,2)
        if lot < 0.01:
            lot = 0.01
        elif symbol in ['NZDCAD','NZDCHF','NZDJPY'] and lot < 0.1:
            lot = 0.1
        return lot


    def start(self):
        self.prepare()
        schedule.every().day.at("00:00").do(self.main_body)
        while True:
            schedule.run_pending()
            sleep(10)


    def prepare(self):
        while True:
            try:
                self.get_data_mt5_count(0, self.get_final, self.tf, ea=True)
                self.pct_data(self.pct_period)
                self.main_online()
                self.tpsl_online(10)
                self.main_online()
            except:
                print('Erro a iniciar.')
            else:
                print('Iniciado.')
                break


    def main_body(self):

        self.mt_login()

        self.refresh_flags()

        while True:
            try:
                self.new_normal_data_mt5(0, 1, self.tf)
            except:
                print('Erro ao obter dados.')
            else:
                print('Dados obtidos com sucesso.')
                break

        if (self.get_new_normal_data().iloc[-1] == self.get_normal_data()[self.ALL_PAIRS_FOR_DF].iloc[-1]).sum() == 0:
            self.set_normal_data(pd.concat([self.get_normal_data()[self.ALL_PAIRS_FOR_DF],self.get_new_normal_data()]).reset_index(drop=True))
            self.pct_data()
            self.main_online()
            self.tpsl_online(10)
        else:
            print('Não há dados novos.')

        for i in self.control_dict:
            if self.get_normal_data()[self.control_dict[i]['buy_strategy']].iloc[-1] and self.control_dict[i]['buy']:
                super().open_trade(action='buy',
                                   tksl = self.get_normal_data()[self.control_dict[i]['TPSL']].iloc[-1],
                                   symbol=self.control_dict[i]['symbol'],
                                   ea_magic_number=self.magic_number,
                                   multiply=self.multiply)
                self.control_dict[i]['buy'] = False
            elif self.get_normal_data()[self.control_dict[i]['sell_strategy']].iloc[-1] and self.control_dict[i]['sell']:
                super().open_trade(action='sell',
                                   tksl = self.get_normal_data()[self.control_dict[i]['TPSL']].iloc[-1],
                                   symbol=self.control_dict[i]['symbol'],
                                   ea_magic_number=self.magic_number,
                                   multiply=self.multiply)
                self.control_dict[i]['sell'] = False

        self.mt_logoff()
