import MetaTrader5 as mt5
import pandas as pd
from time import sleep
import financial as fn
from data import get_data
from mt5 import login_mt5
from time import sleep

# Constantes

HONEMAGICNUMBER = 1010
EVENTS = fn.MY_EVENTS

login_mt5(login=41442678,password='0cxebqvs',server='MetaQuotes-Demo')

while True:
    
    data = get_data(start=0,end=60_000)

    for i in EVENTS.values():
        if 0 > data[i['first_currency']].iloc[-2] > -(data[i['first_currency']].std()*2) and 0 < data[i['second_currency']].iloc[-2] < (data[i['second_currency']].std()*2) and  i['buy']:
            if not i['sell']:
                fn.close_trade('buy',i['sell_request'])
                i['buy'], i['sell'], i['buy_request'] = fn.open_trade(action='buy', symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)
            else:
                i['buy'], _,i['buy_request'] = fn.open_trade(action='buy', symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)
        elif 0 < data[i['first_currency']].iloc[-2] < (data[i['first_currency']].std()*2) and 0 > data[i['second_currency']].iloc[-2] > -(data[i['second_currency']].std()*2) and i['sell']:
            if not i['buy']:
                fn.close_trade('sell',i['buy_request'])
                i['sell'], i['buy'], i['sell_request'] = fn.open_trade(action='sell', symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)
            else:
                i['sell'], _, i['sell_request'] = fn.open_trade(action='sell', symbol=i['symbol'], ea_magic_number=HONEMAGICNUMBER)

    sleep(1800)
                
mt5.shutdown()