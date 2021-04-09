import MetaTrader5 as mt5
import pandas as pd
from time import sleep
import financial as fn
from data import get_data
from mt5 import login_mt5
from time import sleep

HONEMAGICNUMBER = 1010
EVENTS = fn.MY_EVENTS

login_mt5(login=41442678,password='0cxebqvs',server='MetaQuotes-Demo')

while True:

    data = get_data(start=0,end=60_000)

    for i in EVENTS.values():

        orders = mt5.positions_get(symbol=i['symbol'])

        trade_buy, trade_sell = False, False
        if orders == ():
            trade_buy = True
            trade_sell = True
        else:
            if orders[0][5] == 1:
                trade_buy = True
            elif orders[0][5] == 0:
                trade_sell = True

        if data[i['first_currency']].iloc[-1] < -data[i['first_currency']].std() and data[i['second_currency']].iloc[-1] > data[i['second_currency']].std() and trade_buy:
            fn.open_trade(action='buy',tksl = 8, symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)

        elif data[i['first_currency']].iloc[-1] > data[i['first_currency']].std() and data[i['second_currency']].iloc[-1] < -data[i['second_currency']].std() and trade_sell:
            fn.open_trade(action='sell', tksl = 8, symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)

    sleep(1800)

mt5.shutdown()
