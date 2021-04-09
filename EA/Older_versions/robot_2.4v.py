import MetaTrader5 as mt5
import pandas as pd
from time import sleep
import financial as fn
import data as dt
from mt5 import login_mt5
from time import sleep

HONEMAGICNUMBER = 1010
events = fn.MY_EVENTS

login_mt5(login=41442678,password='0cxebqvs',server='MetaQuotes-Demo')

df = dt.get_data(0, 63000, mt5.TIMEFRAME_H1)
data = dt.pct_data(df, period=16)
new_df = pd.DataFrame()

while True:

    # Talvez dar um while true
    while True:
        try:
            new_df = dt.get_data(0, 1, mt5.TIMEFRAME_H1)
        except:
            print('Erro ao obter dados.')
        else:
            print('Dados obtidos com sucesso.')
            break

    if (new_df.iloc[-1] == df.iloc[-1]).sum() == 0:
        df = pd.concat([df,new_df]).reset_index(drop=True)
        data = dt.pct_data(df, period=16)
    else:
        print('Não há dados novos.')

    for i in events.values():

        # Futuramente passar para uma função
        orders = mt5.positions_get(symbol=i['symbol'])
        trade_buy, trade_sell = False, False
        right_now_orders = []
        for j in orders:
            right_now_orders.append(j[5])
        if 1 not in right_now_orders:
            trade_buy = True
        elif 0 not in right_now_orders:
            trade_sell = True

        if data[i['first_currency']].iloc[-1] < data[i['first_currency']].quantile(0.45) and data[i['second_currency']].iloc[-1] > data[i['second_currency']].quantile(0.55) and trade_buy:
            fn.open_trade(action='buy',tksl = 50, symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)
            i['buy'] = False
        elif data[i['first_currency']].iloc[-1] > data[i['first_currency']].quantile(0.55) and data[i['second_currency']].iloc[-1] < data[i['second_currency']].quantile(0.45) and trade_sell:
            fn.open_trade(action='sell', tksl = 50, symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)
            i['sell'] = False

    sleep(3600)

mt5.shutdown()
