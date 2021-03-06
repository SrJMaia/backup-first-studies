#import numpy as mt5
import MetaTrader5 as mt5
# Mudar se for usar
import pandas as pd
from time import sleep
from datetime import datetime

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


    @staticmethod
    def get_hour():
        return f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year} {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}'


    def mt_login(self):
        mt5.initialize()

        info = mt5.terminal_info()

        if not info[4]:
            print(f'AlgoTrading não ativado! Erro: {mt5.last_error()}')
            mt5.shutdown()

        if not mt5.initialize(login=self.login, password=self.senha, server=self.servidor):
            print('MT5 não iniciado.')
            mt5.shutdown()


    @staticmethod
    def mt_logoff():
        mt5.shutdown()


    def mt_get_data_count(self, symbol, start, end, time_frame, data_type='open'):
        """
        symbol = ativo
        start = 0 = hoje
        end = x -> int de quantos dados no passado deseja
        time_frame = str exemplos em tf
        data_type = retorn apenas open
        """
        tf = {'M1':mt5.TIMEFRAME_M1, 'M5':mt5.TIMEFRAME_M5, 'M15':mt5.TIMEFRAME_M15,
              'M30':mt5.TIMEFRAME_M30, 'H1':mt5.TIMEFRAME_H1, 'H4':mt5.TIMEFRAME_H4,
              'D1':mt5.TIMEFRAME_D1, 'W1':mt5.TIMEFRAME_W1}
        dt = pd.DataFrame(mt5.copy_rates_from_pos(symbol, tf[time_frame] , start, end))[data_type]
        return dt


    @staticmethod
    def account_information():
        account = mt5.account_info()._asdict()
        if account == None:
            print(f'Erro ao pegar dados da conta. Erro: {mt5.last_error()}')
            mt5.shutdown()
        else:
            return account['margin_free']


    @staticmethod
    def get_info(symbol):
        '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
        '''
        # get symbol properties
        info=mt5.symbol_info(symbol)
        return info


    def refresh_flags(self):
        for i in self.control_dict.values():

            result = mt5.positions_get(symbol=i['symbol'])

            r = []

            for k in range(len(result)):
                r.append(result[k]._asdict()['type'])

            if not i['buy'] or not i['sell']:
                if not 0 in r:
                    self.control_dict[i['symbol']]['buy'] = True
                if not 1 in r:
                    self.control_dict[i['symbol']]['sell'] = True


    def open_trade(self, action, tksl, symbol, ea_magic_number, multiply=2):
        '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
        '''
        # prepare the buy request structure
        symbol_info = self.get_info(symbol)

        tk, sl = 0, 0

        balance = self.account_information()

        jpy_check = False

        if symbol in self.JPY:
            tk = tksl * self.tp_multi
            sl = tksl * self.sl_multi
            jpy_check = True
        else:
            tk = tksl * self.tp_multi
            sl = tksl * self.sl_multi

        if action == 'buy':
            trade_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
            tk = round(price + tk,3) if jpy_check else round(price+tk, 5)
            sl = round(price - sl, 3) if jpy_check else round(price - sl, 5)
        elif action =='sell':
            trade_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
            tk = round(price - tk, 3) if jpy_check else round(price - tk, 5)
            sl = round(price + sl, 3) if jpy_check else round(price + sl, 5)

        point = mt5.symbol_info(symbol).point

        order_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": self.lot_calculation(balance, symbol),
            "type": trade_type,
            "price": price,
            "sl": sl,
            "tp": tk,
            "deviation": 10,
            "magic": ea_magic_number,
            "comment": "MAYBE LATER A COMMENT",
            "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # send a trading request
        result = mt5.order_send(order_request)
        """
        Depois arrumar isso
        """

        if result[0] == 10009:
            print(f"Hour: {self.get_hour()} | Type: {action.title()} | Symbol: {symbol} | Price: {order_request['price']} | Volume: {order_request['volume']}")
            if action == 'buy':
                self.control_dict[symbol]['buy_request'] = order_request
            elif action == 'sell':
                self.control_dict[symbol]['sell_request'] = order_request
        elif result[0] == 10004 or result[0] == 10018 or result[0] == 10021:
            while result[0] == 10004 or result[0] == 10018:
                if result[0] == 10018:
                    if datetime.today().weekday() == 5 or datetime.today().weekday() == 6:
                        print(f'Hour: {self.get_hour()} Weekend.')
                        break
                result = mt5.order_send(order_request)
                print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]} | New Price. Hour: {self.get_hour()}")
                sleep(1)
            if result[0] == 10009:
                print(f"Hour: {self.get_hour()} | Type: {action.title()} | Symbol: {symbol} | Price: {order_request['price']} | Volume: {order_request['volume']}")
                if action == 'buy':
                    self.control_dict[symbol]['buy_request'] = order_request
                elif action == 'sell':
                    self.control_dict[symbol]['sell_request'] = order_request
            else:
                print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]}. Hour: {self.get_hour()}")
        else:
            print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]}. Hour: {self.get_hour()}")


    def close_trade(self, action, symbol):
        '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
        '''
        # create a close request
        order_request = 0
        if action == 'buy':
            order_request = self.control_dict[symbol]['sell_request']
        elif action == 'sell':
            order_send = self.control_dict[symbol]['buy_request']

        symbol = order_request['symbol']
        if action == 'buy':
            trade_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
        elif action =='sell':
            trade_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).bid
        position_id=mt5.positions_get(symbol=symbol)
        lot = order_request['volume']

        close_request={
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": trade_type,
            "position": position_id[0][0],
            "price": price,
            "deviation": 10,
            "magic": order_request['magic'],
            "comment": f"Closing position: {order_request['symbol']}",
            "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
            "type_filling": mt5.ORDER_FILLING_RETURN,
        }
        # send a close request
        result=mt5.order_send(close_request)
        # Erro 10004
        while result[0] != 10009 or result[0] == 10021:
            result=mt5.order_send(close_request)
            print(f'Error Closing {symbol}: {mt5.last_error()} | Code: {result[0]}. Hour: {self.get_hour()}')
        print(f"Hour: {self.get_hour()} | Closing as: {action.title()} | Symbol: {symbol} | Volume: {result[3]} | Price: {result[4]}")
        if action == 'buy':
            self.control_dict[symbol]['sell_request'] = 0
        elif action == 'sell':
            self.control_dict[symbol]['buy_request'] = 0


        # Backup
        # if result[0] == 10009:
        #     print(f"Closing as: {action.title()} | Symbol: {symbol} | Volume: {result[3]} | Price: {result[4]}")
        # else:
        #     print(f'Error Closing {symbol}: {mt5.last_error()} | Code: {result[0]}')



# def open_trade(action, symbol, ea_magic_number):
#     '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
#     '''
#     # prepare the buy request structure
#     symbol_info = get_info(symbol)

#     leverage, balance = account_information()

#     if action == 'buy':
#         trade_type = mt5.ORDER_TYPE_BUY
#         price = mt5.symbol_info_tick(symbol).ask
#     elif action =='sell':
#         trade_type = mt5.ORDER_TYPE_SELL
#         price = mt5.symbol_info_tick(symbol).bid
#     point = mt5.symbol_info(symbol).point

#     order_request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot_calculation(balance,leverage,symbol),
#         "type": trade_type,
#         "price": price,
#         "deviation": 10,
#         "magic": ea_magic_number,
#         "comment": "MAYBE LATER A COMMENT",
#         "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
#         "type_filling": mt5.ORDER_FILLING_RETURN,
#     }
#     # send a trading request
#     result = mt5.order_send(order_request)

#     if result[0] == 10009:
#         print(f"{action.title()} | Symbol: {symbol} | Price: {order_request['price']} | Volume: {order_request['volume']}")
#         return False, True, order_request
#     elif result[0] == 10004 or result[0] == 10021:
#         while result[0] == 10004:
#             result = mt5.order_send(order_request)
#             print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]} | New Price.")
#         if result[0] == 10009:
#             print(f"{action.title()} | Symbol: {symbol} | Price: {order_request['price']} | Volume: {order_request['volume']}")
#             return False, True, order_request
#         else:
#             print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]}")
#             return True, False, order_request
#         #print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]} | New Price.")
#         #return True, False, order_request
#     else:
#         print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]}")
#         return True, False, order_request
