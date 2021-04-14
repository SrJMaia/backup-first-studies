from arquivos.signals import Signals
import pandas as pd
import numpy as np

class ea_online(Signals):

    def __init__(self,
                 login=5528104,
                 senha='YUWNehok',
                 servidor='ActivTradesCorp-Server',
                 risk,
                 multiply,
                 magic_number,
                 timeframe):
        super().__init__(login, senha, servidor)
        self.risk = risk
        self.multiply = multiply
        self.magic_number = magic_number
        self.tf = timeframe
        self.control_dict = super().MY_EVENTS


    def lot_calculation(self, balance, symbol):
        lot = round(balance*self.risk/100_000,2)
        if lot < 0.01:
            lot = 0.01
        elif symbol in ['NZDCAD','NZDCHF','NZDJPY'] and lot < 0.1:
            lot = 0.1
        return lot



    self.mt_login()

        self.get_data_mt5_count(0, 3000, self.tf)
        self.pct_data()
        self.pct_data_signals_std()

        new_df = pd.DataFrame()
        """
        Testar primeiro se funciona
        Posso retirar o while true e colocar o schedule
        em vez de alterar em i, altero em self
        """

        while True:

            for i in self.control_dict:

                if data[i['buy_strategy']].iloc[-1] and i['buy']:
                    super().open_trade(action='buy',tksl = TPSL, symbol=i['symbol'], ea_magic_number=self.magic_number, multiply=self.multiply)
                    i['buy'] = False
                elif data[i['sell_strategy']].iloc[-1] and i['sell']:
                    super().open_trade(action='sell', tksl = TPSL, symbol=i['symbol'], ea_magic_number=self.magic_number, multiply=self.multiply)
                    i['sell'] = False

            sleep(3600)

            while True:
                try:
                    self.get_new_data_mt5(0, 1, self.tf)
                except:
                    print('Erro ao obter dados.')
                else:
                    print('Dados obtidos com sucesso.')
                    break

            if (self.get_new_normal_data().iloc[-1] == self.get_normal_data()[self.ALL_PAIRS_FOR_DF].iloc[-1]).sum() == 0:
                self.set_normal_data(pd.concat([df,new_df]).reset_index(drop=True))
                self.pct_data()
                self.pct_data_signals_std()
            else:
                print('Não há dados novos.')

    self.mt_logoff()
