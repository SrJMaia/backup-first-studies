import MetaTrader5 as mt5
import pandas as pd
from time import sleep
import financial as fn
from data import get_data
from mt5 import login_mt5
from time import sleep

# Constantes

HONEMAGICNUMBER = 1010
BESTTIMEHONE = 7
VERSION = 'V1.9'

# EUR
order_request_buy_eurusd, order_request_sell_eurusd = 0, 0
flag_buy_eurusd, flag_sell_eurusd = True, True
order_request_buy_eurgbp, order_request_sell_eurgbp = 0, 0
flag_buy_eurgbp, flag_sell_eurgbp = True, True
order_request_buy_eurjpy, order_request_sell_eurjpy = 0, 0
flag_buy_eurjpy, flag_sell_eurjpy = True, True
order_request_buy_eurchf, order_request_sell_eurchf = 0, 0
flag_buy_eurchf, flag_sell_eurchf = True, True
order_request_buy_eurnzd, order_request_sell_eurnzd = 0, 0
flag_buy_eurnzd, flag_sell_eurnzd = True, True
order_request_buy_euraud, order_request_sell_euraud = 0, 0
flag_buy_euraud, flag_sell_euraud = True, True
order_request_buy_eurcad, order_request_sell_eurcad = 0, 0
flag_buy_eurcad, flag_sell_eurcad = True, True
# USD
order_request_buy_gbpusd, order_request_sell_gbpusd = 0, 0
flag_buy_gbpusd, flag_sell_gbpusd = True, True
order_request_buy_usdchf, order_request_sell_usdchf = 0, 0
flag_buy_usdchf, flag_sell_usdchf = True, True
order_request_buy_usdjpy, order_request_sell_usdjpy = 0, 0
flag_buy_usdjpy, flag_sell_usdjpy = True, True
order_request_buy_audusd, order_request_sell_audusd = 0, 0
flag_buy_audusd, flag_sell_audusd = True, True
order_request_buy_nzdusd, order_request_sell_nzdusd = 0, 0
flag_buy_nzdusd, flag_sell_nzdusd = True, True
order_request_buy_usdcad, order_request_sell_usdcad = 0, 0
flag_buy_usdcad, flag_sell_usdcad = True, True
# GBP
order_request_buy_gbpaud, order_request_sell_gbpaud = 0, 0
flag_buy_gbpaud, flag_sell_gbpaud = True, True
order_request_buy_gbpchf, order_request_sell_gbpchf = 0, 0
flag_buy_gbpchf, flag_sell_gbpchf = True, True
order_request_buy_gbpjpy, order_request_sell_gbpjpy = 0, 0
flag_buy_gbpjpy, flag_sell_gbpjpy = True, True
order_request_buy_gbpcad, order_request_sell_gbpcad = 0, 0
flag_buy_gbpcad, flag_sell_gbpcad = True, True
order_request_buy_gbpnzd, order_request_sell_gbpnzd = 0, 0
flag_buy_gbpnzd, flag_sell_gbpnzd = True, True
# JPY
order_request_buy_audjpy, order_request_sell_audjpy = 0, 0
flag_buy_audjpy, flag_sell_audjpy = True, True
order_request_buy_cadjpy, order_request_sell_cadjpy = 0, 0
flag_buy_cadjpy, flag_sell_cadjpy = True, True
order_request_buy_chfjpy, order_request_sell_chfjpy = 0, 0
flag_buy_chfjpy, flag_sell_chfjpy = True, True
order_request_buy_nzdjpy, order_request_sell_nzdjpy = 0, 0
flag_buy_nzdjpy, flag_sell_nzdjpy = True, True
# CHF
order_request_buy_audchf, order_request_sell_audchf = 0, 0
flag_buy_audchf, flag_sell_audchf = True, True
order_request_buy_cadchf, order_request_sell_cadchf = 0, 0
flag_buy_cadchf, flag_sell_cadchf = True, True
order_request_buy_nzdchf, order_request_sell_nzdchf = 0, 0
flag_buy_nzdchf, flag_sell_nzdchf = True, True
# NZD
order_request_buy_audnzd, order_request_sell_audnzd = 0, 0
flag_buy_audnzd, flag_sell_audnzd = True, True
order_request_buy_nzdcad, order_request_sell_nzdcad = 0, 0
flag_buy_nzdcad, flag_sell_nzdcad = True, True
# AUD
order_request_buy_audcad, order_request_sell_audcad = 0, 0
flag_buy_audcad, flag_sell_audcad = True, True

login_mt5(login=40305620,password='x8dcteyv',server='MetaQuotes-Demo')

while True:

    data = get_data(start=0,end=10)

            #EUR
    # EURUSD
    if data['eur'].iloc[-1] < -BESTTIMEHONE and data['usd'].iloc[-1] > BESTTIMEHONE and flag_buy_eurusd:
        if not flag_sell_eurusd:
            fn.close_trade('buy',order_request_sell_eurusd)
            order_request_buy_eurusd = fn.open_trade(action='buy', symbol='EURUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurusd = True
            flag_buy_eurusd = False
        else:
            order_request_buy_eurusd = fn.open_trade(action='buy', symbol='EURUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurusd = False
    elif data['eur'].iloc[-1] > BESTTIMEHONE and data['usd'].iloc[-1] < -BESTTIMEHONE and flag_sell_eurusd:
        if not flag_buy_eurusd:
            fn.close_trade('sell',order_request_buy_eurusd)
            order_request_sell_eurusd = fn.open_trade(action='sell', symbol='EURUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurusd = True
            flag_sell_eurusd = False
        else:
            order_request_sell_eurusd = fn.open_trade(action='sell', symbol='EURUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurusd = False
    # EURGBP
    if data['eur'].iloc[-1] < -BESTTIMEHONE and data['gbp'].iloc[-1] > BESTTIMEHONE and flag_buy_eurgbp:
        if not flag_sell_eurgbp:
            fn.close_trade('buy',order_request_sell_eurgbp)
            order_request_buy_eurgbp = fn.open_trade(action='buy', symbol='EURGBP', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurgbp = True
            flag_buy_eurgbp = False
        else:
            order_request_buy_eurgbp = fn.open_trade(action='buy', symbol='EURGBP', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurgbp = False
    elif data['eur'].iloc[-1] > BESTTIMEHONE and data['gbp'].iloc[-1] < -BESTTIMEHONE and flag_sell_eurgbp:
        if not flag_buy_eurgbp:
            fn.close_trade('sell',order_request_buy_eurgbp)
            order_request_sell_eurgbp = fn.open_trade(action='sell', symbol='EURGBP', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurgbp = True
            flag_sell_eurgbp = False
        else:
            order_request_sell_eurgbp = fn.open_trade(action='sell', symbol='EURGBP', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurgbp = False
    # EURJPY
    if data['eur'].iloc[-1] < -BESTTIMEHONE and data['jpy'].iloc[-1] > BESTTIMEHONE and flag_buy_eurjpy:
        if not flag_sell_eurjpy:
            fn.close_trade('buy',order_request_sell_eurjpy)
            order_request_buy_eurjpy = fn.open_trade(action='buy', symbol='EURJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurjpy = True
            flag_buy_eurjpy = False
        else:
            order_request_buy_eurjpy = fn.open_trade(action='buy', symbol='EURJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurjpy = False
    elif data['eur'].iloc[-1] > BESTTIMEHONE and data['jpy'].iloc[-1] < -BESTTIMEHONE and flag_sell_eurjpy:
        if not flag_buy_eurjpy:
            fn.close_trade('sell',order_request_buy_eurjpy)
            order_request_sell_eurjpy = fn.open_trade(action='sell', symbol='EURJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurjpy = True
            flag_sell_eurjpy = False
        else:
            order_request_sell_eurjpy = fn.open_trade(action='sell', symbol='EURJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurjpy = False
    # EURCHF
    if data['eur'].iloc[-1] < -BESTTIMEHONE and data['chf'].iloc[-1] > BESTTIMEHONE and flag_buy_eurchf:
        if not flag_sell_eurchf:
            fn.close_trade('buy',order_request_sell_eurchf)
            order_request_buy_eurchf = fn.open_trade(action='buy', symbol='EURCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurchf = True
            flag_buy_eurchf = False
        else:
            order_request_buy_eurchf = fn.open_trade(action='buy', symbol='EURCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurchf = False
    elif data['eur'].iloc[-1] > BESTTIMEHONE and data['chf'].iloc[-1] < -BESTTIMEHONE and flag_sell_eurchf:
        if not flag_buy_eurchf:
            fn.close_trade('sell',order_request_buy_eurchf)
            order_request_sell_eurchf = fn.open_trade(action='sell', symbol='EURCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurchf = True
            flag_sell_eurchf = False
        else:
            order_request_sell_eurchf = fn.open_trade(action='sell', symbol='EURCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurchf = False
    # EURNZD
    if data['eur'].iloc[-1] < -BESTTIMEHONE and data['nzd'].iloc[-1] > BESTTIMEHONE and flag_buy_eurnzd:
        if not flag_sell_eurnzd:
            fn.close_trade('buy',order_request_sell_eurnzd)
            order_request_buy_eurnzd = fn.open_trade(action='buy', symbol='EURNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurnzd = True
            flag_buy_eurnzd = False
        else:
            order_request_buy_eurnzd = fn.open_trade(action='buy', symbol='EURNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurnzd = False
    elif data['eur'].iloc[-1] > BESTTIMEHONE and data['nzd'].iloc[-1] < -BESTTIMEHONE and flag_sell_eurnzd:
        if not flag_buy_eurnzd:
            fn.close_trade('sell',order_request_buy_eurnzd)
            order_request_sell_eurnzd = fn.open_trade(action='sell', symbol='EURNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurnzd = True
            flag_sell_eurnzd = False
        else:
            order_request_sell_eurnzd = fn.open_trade(action='sell', symbol='EURNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurnzd = False
    # EURUAD
    if data['eur'].iloc[-1] < -BESTTIMEHONE and data['aud'].iloc[-1] > BESTTIMEHONE and flag_buy_euraud:
        if not flag_sell_euraud:
            fn.close_trade('buy',order_request_sell_euraud)
            order_request_buy_euraud = fn.open_trade(action='buy', symbol='EURAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_euraud = True
            flag_buy_euraud = False
        else:
            order_request_buy_euraud = fn.open_trade(action='buy', symbol='EURAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_euraud = False
    elif data['eur'].iloc[-1] > BESTTIMEHONE and data['aud'].iloc[-1] < -BESTTIMEHONE and flag_sell_euraud:
        if not flag_buy_:
            fn.close_trade('sell',order_request_buy_euraud)
            order_request_sell_euraud = fn.open_trade(action='sell', symbol='EURAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_euraud = True
            flag_sell_euraud = False
        else:
            order_request_sell_euraud = fn.open_trade(action='sell', symbol='EURAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_euraud = False
    # EURCAD
    if data['eur'].iloc[-1] < -BESTTIMEHONE and data['cad'].iloc[-1] > BESTTIMEHONE and flag_buy_eurcad:
        if not flag_sell_eurcad:
            fn.close_trade('buy',order_request_sell_eurcad)
            order_request_buy_eurcad = fn.open_trade(action='buy', symbol='EURCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurcad = True
            flag_buy_eurcad = False
        else:
            order_request_buy_eurcad = fn.open_trade(action='buy', symbol='EURCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurcad = False
    elif data['eur'].iloc[-1] > BESTTIMEHONE and data['cad'].iloc[-1] < -BESTTIMEHONE and flag_sell_eurcad:
        if not flag_buy_eurcad:
            fn.close_trade('sell',order_request_buy_eurcad)
            order_request_sell_eurcad = fn.open_trade(action='sell', symbol='EURCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_eurcad = True
            flag_sell_eurcad = False
        else:
            order_request_sell_eurcad = fn.open_trade(action='sell', symbol='EURCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_eurcad = False
            # USD
   # GBPUSD
    if data['gbp'].iloc[-1] < -BESTTIMEHONE and data['usd'].iloc[-1] > BESTTIMEHONE and flag_buy_gbpusd:
        if not flag_sell_gbpusd:
            fn.close_trade('buy',order_request_sell_gbpusd)
            order_request_buy_gbpusd = fn.open_trade(action='buy', symbol='GBPUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpusd = True
            flag_buy_gbpusd = False
        else:
            order_request_buy_gbpusd = fn.open_trade(action='buy', symbol='GBPUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpusd = False
    elif data['gbp'].iloc[-1] > BESTTIMEHONE and data['usd'].iloc[-1] < -BESTTIMEHONE and flag_sell_gbpusd:
        if not flag_buy_gbpusd:
            fn.close_trade('sell',order_request_buy_gbpusd)
            order_request_sell_gbpusd = fn.open_trade(action='sell', symbol='GBPUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpusd = True
            flag_sell_gbpusd = False
        else:
            order_request_sell_gbpusd = fn.open_trade(action='sell', symbol='GBPUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpusd = False
    # USDCHF
    if data['usd'].iloc[-1] < -BESTTIMEHONE and data['chf'].iloc[-1] > BESTTIMEHONE and flag_buy_usdchf:
        if not flag_sell_usdchf:
            fn.close_trade('buy',order_request_sell_usdchf)
            order_request_buy_usdchf = fn.open_trade(action='buy', symbol='USDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_usdchf = True
            flag_buy_usdchf = False
        else:
            order_request_buy_usdchf = fn.open_trade(action='buy', symbol='USDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_usdchf = False
    elif data['usd'].iloc[-1] > BESTTIMEHONE and data['chf'].iloc[-1] < -BESTTIMEHONE and flag_sell_usdchf:
        if not flag_buy_usdchf:
            fn.close_trade('sell',order_request_buy_usdchf)
            order_request_sell_usdchf = fn.open_trade(action='sell', symbol='USDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_usdchf = True
            flag_sell_usdchf = False
        else:
            order_request_sell_usdchf = fn.open_trade(action='sell', symbol='USDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_usdchf = False
    # USDJPY
    if data['usd'].iloc[-1] < -BESTTIMEHONE and data['jpy'].iloc[-1] > BESTTIMEHONE and flag_buy_usdjpy:
        if not flag_sell_usdjpy:
            fn.close_trade('buy',order_request_sell_usdjpy)
            order_request_buy_usdjpy = fn.open_trade(action='buy', symbol='USDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_usdjpy = True
            flag_buy_usdjpy = False
        else:
            order_request_buy_usdjpy = fn.open_trade(action='buy', symbol='USDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_usdjpy = False
    elif data['usd'].iloc[-1] > BESTTIMEHONE and data['jpy'].iloc[-1] < -BESTTIMEHONE and flag_sell_usdjpy:
        if not flag_buy_usdjpy:
            fn.close_trade('sell',order_request_buy_usdjpy)
            order_request_sell_usdjpy = fn.open_trade(action='sell', symbol='USDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_usdjpy = True
            flag_sell_usdjpy = False
        else:
            order_request_sell_usdjpy = fn.open_trade(action='sell', symbol='USDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_usdjpy = False
    # AUDUSD
    if data['aud'].iloc[-1] < -BESTTIMEHONE and data['usd'].iloc[-1] > BESTTIMEHONE and flag_buy_audusd:
        if not flag_sell_audusd:
            fn.close_trade('buy',order_request_sell_audusd)
            order_request_buy_audusd = fn.open_trade(action='buy', symbol='AUDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audusd = True
            flag_buy_audusd = False
        else:
            order_request_buy_audusd = fn.open_trade(action='buy', symbol='AUDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audusd = False
    elif data['aud'].iloc[-1] > BESTTIMEHONE and data['usd'].iloc[-1] < -BESTTIMEHONE and flag_sell_audusd:
        if not flag_buy_audusd:
            fn.close_trade('sell',order_request_buy_audusd)
            order_request_sell_audusd = fn.open_trade(action='sell', symbol='AUDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audusd = True
            flag_sell_audusd = False
        else:
            order_request_sell_audusd = fn.open_trade(action='sell', symbol='AUDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audusd = False
    # NZDUSD
    if data['nzd'].iloc[-1] < -BESTTIMEHONE and data['usd'].iloc[-1] > BESTTIMEHONE and flag_buy_nzdusd:
        if not flag_sell_nzdusd:
            fn.close_trade('buy',order_request_sell_nzdusd)
            order_request_buy_nzdusd = fn.open_trade(action='buy', symbol='NZDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdusd = True
            flag_buy_nzdusd = False
        else:
            order_request_buy_nzdusd = fn.open_trade(action='buy', symbol='NZDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdusd = False
    elif data['nzd'].iloc[-1] > BESTTIMEHONE and data['usd'].iloc[-1] < -BESTTIMEHONE and flag_sell_:
        if not flag_buy_nzdusd:
            fn.close_trade('sell',order_request_buy_nzdusd)
            order_request_sell_nzdusd = fn.open_trade(action='sell', symbol='NZDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdusd = True
            flag_sell_nzdusd = False
        else:
            order_request_sell_nzdusd = fn.open_trade(action='sell', symbol='NZDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdusd = False
    # USDCAD
    if data['usd'].iloc[-1] < -BESTTIMEHONE and data['cad'].iloc[-1] > BESTTIMEHONE and flag_buy_usdcad:
        if not flag_sell_usdcad:
            fn.close_trade('buy',order_request_sell_usdcad)
            order_request_buy_usdcad = fn.open_trade(action='buy', symbol='USDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_usdcad = True
            flag_buy_usdcad = False
        else:
            order_request_buy_usdcad = fn.open_trade(action='buy', symbol='USDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_usdcad = False
    elif data['usd'].iloc[-1] > BESTTIMEHONE and data['cad'].iloc[-1] < -BESTTIMEHONE and flag_sell_:
        if not flag_buy_nzdusd:
            fn.close_trade('sell',order_request_buy_nzdusd)
            order_request_sell_nzdusd = fn.open_trade(action='sell', symbol='NZDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdusd = True
            flag_sell_nzdusd = False
        else:
            order_request_sell_nzdusd = fn.open_trade(action='sell', symbol='NZDUSD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdusd = False
            # GBP
    # GBPAUD
    if data['gbp'].iloc[-1] < -BESTTIMEHONE and data['aud'].iloc[-1] > BESTTIMEHONE and flag_buy_gbpaud:
        if not flag_sell_gbpaud:
            fn.close_trade('buy',order_request_sell_gbpaud)
            order_request_buy_gbpaud = fn.open_trade(action='buy', symbol='GBPAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpaud = True
            flag_buy_gbpaud = False
        else:
            order_request_buy_gbpaud = fn.open_trade(action='buy', symbol='GBPAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpaud = False
    elif data['gbp'].iloc[-1] > BESTTIMEHONE and data['aud'].iloc[-1] < -BESTTIMEHONE and flag_sell_gbpaud:
        if not flag_buy_gbpaud:
            fn.close_trade('sell',order_request_buy_gbpaud)
            order_request_sell_gbpaud = fn.open_trade(action='sell', symbol='GBPAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpaud = True
            flag_sell_gbpaud = False
        else:
            order_request_sell_gbpaud = fn.open_trade(action='sell', symbol='GBPAUD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpaud = False
    # GBPCHF
    if data['gbp'].iloc[-1] < -BESTTIMEHONE and data['chf'].iloc[-1] > BESTTIMEHONE and flag_buy_gbpchf:
        if not flag_sell_gbpchf:
            fn.close_trade('buy',order_request_sell_gbpchf)
            order_request_buy_gbpchf = fn.open_trade(action='buy', symbol='GBPCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpchf = True
            flag_buy_gbpchf = False
        else:
            order_request_buy_gbpchf = fn.open_trade(action='buy', symbol='GBPCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpchf = False
    elif data['gbp'].iloc[-1] > BESTTIMEHONE and data['chf'].iloc[-1] < -BESTTIMEHONE and flag_sell_:
        if not flag_buy_gbpchf:
            fn.close_trade('sell',order_request_buy_gbpchf)
            order_request_sell_gbpchf = fn.open_trade(action='sell', symbol='GBPCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpchf = True
            flag_sell_gbpchf = False
        else:
            order_request_sell_gbpchf = fn.open_trade(action='sell', symbol='GBPCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpchf = False
    # GBPJPY
    if data['gbp'].iloc[-1] < -BESTTIMEHONE and data['jpy'].iloc[-1] > BESTTIMEHONE and flag_buy_gbpjpy:
        if not flag_sell_gbpjpy:
            fn.close_trade('buy',order_request_sell_gbpjpy)
            order_request_buy_gbpjpy = fn.open_trade(action='buy', symbol='GBPJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpjpy = True
            flag_buy_gbpjpy = False
        else:
            order_request_buy_gbpjpy = fn.open_trade(action='buy', symbol='GBPJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpjpy = False
    elif data['gbp'].iloc[-1] > BESTTIMEHONE and data['jpy'].iloc[-1] < -BESTTIMEHONE and flag_sell_gbpjpy:
        if not flag_buy_gbpjpy:
            fn.close_trade('sell',order_request_buy_gbpjpy)
            order_request_sell_gbpjpy = fn.open_trade(action='sell', symbol='GBPJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpjpy = True
            flag_sell_gbpjpy = False
        else:
            order_request_sell_gbpjpy = fn.open_trade(action='sell', symbol='GBPJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpjpy = False
    # GBPCAD
    if data['gbp'].iloc[-1] < -BESTTIMEHONE and data['cad'].iloc[-1] > BESTTIMEHONE and flag_buy_gbpcad:
        if not flag_sell_gbpcad:
            fn.close_trade('buy',order_request_sell_gbpcad)
            order_request_buy_gbpcad = fn.open_trade(action='buy', symbol='GBPCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpcad = True
            flag_buy_gbpcad = False
        else:
            order_request_buy_gbpcad = fn.open_trade(action='buy', symbol='GBPCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpcad = False
    elif data['gbp'].iloc[-1] > BESTTIMEHONE and data['cad'].iloc[-1] < -BESTTIMEHONE and flag_sell_gbpcad:
        if not flag_buy_gbpcad:
            fn.close_trade('sell',order_request_buy_gbpcad)
            order_request_sell_gbpcad = fn.open_trade(action='sell', symbol='GBPCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpcad = True
            flag_sell_gbpcad = False
        else:
            order_request_sell_gbpcad = fn.open_trade(action='sell', symbol='GBPCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpcad = False
    # GBPNZD
    if data['gbp'].iloc[-1] < -BESTTIMEHONE and data['nzd'].iloc[-1] > BESTTIMEHONE and flag_buy_gbpnzd:
        if not flag_sell_gbpnzd:
            fn.close_trade('buy',order_request_sell_gbpnzd)
            order_request_buy_gbpnzd = fn.open_trade(action='buy', symbol='GBPNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpnzd = True
            flag_buy_gbpnzd = False
        else:
            order_request_buy_gbpnzd = fn.open_trade(action='buy', symbol='GBPNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpnzd = False
    elif data['gbp'].iloc[-1] > BESTTIMEHONE and data['nzd'].iloc[-1] < -BESTTIMEHONE and flag_sell_gbpnzd:
        if not flag_buy_gbpnzd:
            fn.close_trade('sell',order_request_buy_gbpnzd)
            order_request_sell_gbpnzd = fn.open_trade(action='sell', symbol='GBPNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_gbpnzd = True
            flag_sell_gbpnzd = False
        else:
            order_request_sell_gbpnzd = fn.open_trade(action='sell', symbol='GBPNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_gbpnzd = False
            # JPY
    # AUDJPY
    if data['aud'].iloc[-1] < -BESTTIMEHONE and data['jpy'].iloc[-1] > BESTTIMEHONE and flag_buy_audjpy:
        if not flag_sell_audjpy:
            fn.close_trade('buy',order_request_sell_audjpy)
            order_request_buy_audjpy = fn.open_trade(action='buy', symbol='AUDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audjpy = True
            flag_buy_audjpy = False
        else:
            order_request_buy_audjpy = fn.open_trade(action='buy', symbol='AUDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audjpy = False
    elif data['aud'].iloc[-1] > BESTTIMEHONE and data['jpy'].iloc[-1] < -BESTTIMEHONE and flag_sell_audjpy:
        if not flag_buy_audjpy:
            fn.close_trade('sell', order_request_buy_audjpy)
            order_request_sell_audjpy = fn.open_trade(action='sell', symbol='AUDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audjpy = True
            flag_sell_audjpy = False
        else:
            order_request_sell_audjpy = fn.open_trade(action='sell', symbol='AUDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audjpy = False
    # CADJPY
    if data['cad'].iloc[-1] < -BESTTIMEHONE and data['jpy'].iloc[-1] > BESTTIMEHONE and flag_buy_cadjpy:
        if not flag_sell_cadjpy:
            fn.close_trade('buy',order_request_sell_cadjpy)
            order_request_buy_cadjpy = fn.open_trade(action='buy', symbol='CADJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_cadjpy = True
            flag_buy_cadjpy = False
        else:
            order_request_buy_cadjpy = fn.open_trade(action='buy', symbol='CADJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_cadjpy = False
    elif data['cad'].iloc[-1] > BESTTIMEHONE and data['jpy'].iloc[-1] < -BESTTIMEHONE and flag_sell_cadjpy:
        if not flag_buy_cadjpy:
            fn.close_trade('sell',order_request_buy_cadjpy)
            order_request_sell_cadjpy = fn.open_trade(action='sell', symbol='CADJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_cadjpy = True
            flag_sell_cadjpy = False
        else:
            order_request_sell_cadjpy = fn.open_trade(action='sell', symbol='CADJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_cadjpy = False
    # CHFJPY
    if data['chf'].iloc[-1] < -BESTTIMEHONE and data['jpy'].iloc[-1] > BESTTIMEHONE and flag_buy_chfjpy:
        if not flag_sell_chfjpy:
            fn.close_trade('buy',order_request_sell_chfjpy)
            order_request_buy_chfjpy = fn.open_trade(action='buy', symbol='CHFJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_chfjpy = True
            flag_buy_chfjpy = False
        else:
            order_request_buy_chfjpy = fn.open_trade(action='buy', symbol='CHFJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_chfjpy = False
    elif data['chf'].iloc[-1] > BESTTIMEHONE and data['jpy'].iloc[-1] < -BESTTIMEHONE and flag_sell_chfjpy:
        if not flag_buy_chfjpy:
            fn.close_trade('sell',order_request_buy_chfjpy)
            order_request_sell_chfjpy = fn.open_trade(action='sell', symbol='CHFJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_chfjpy = True
            flag_sell_chfjpy = False
        else:
            order_request_sell_chfjpy = fn.open_trade(action='sell', symbol='CHFJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_chfjpy = False
    # NZDJPY
    if data['nzd'].iloc[-1] < -BESTTIMEHONE and data['jpy'].iloc[-1] > BESTTIMEHONE and flag_buy_nzdjpy:
        if not flag_sell_nzdjpy:
            fn.close_trade('buy',order_request_sell_nzdjpy)
            order_request_buy_nzdjpy = fn.open_trade(action='buy', symbol='NZDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdjpy = True
            flag_buy_nzdjpy = False
        else:
            order_request_buy_nzdjpy = fn.open_trade(action='buy', symbol='NZDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdjpy = False
    elif data['nzd'].iloc[-1] > BESTTIMEHONE and data['jpy'].iloc[-1] < -BESTTIMEHONE and flag_sell_nzdjpy:
        if not flag_buy_nzdjpy:
            fn.close_trade('sell',order_request_buy_nzdjpy)
            order_request_sell_nzdjpy = fn.open_trade(action='sell', symbol='NZDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdjpy = True
            flag_sell_nzdjpy = False
        else:
            order_request_sell_nzdjpy = fn.open_trade(action='sell', symbol='NZDJPY', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdjpy = False
            # CHF
    # AUDCHF
    if data['aud'].iloc[-1] < -BESTTIMEHONE and data['chf'].iloc[-1] > BESTTIMEHONE and flag_buy_audchf:
        if not flag_sell_audchf:
            fn.close_trade('buy',order_request_sell_audchf)
            order_request_buy_audchf = fn.open_trade(action='buy', symbol='AUDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audchf = True
            flag_buy_audchf = False
        else:
            order_request_buy_audchf = fn.open_trade(action='buy', symbol='AUDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audchf = False
    elif data['aud'].iloc[-1] > BESTTIMEHONE and data['chf'].iloc[-1] < -BESTTIMEHONE and flag_sell_audchf:
        if not flag_buy_audchf:
            fn.close_trade('sell',order_request_buy_audchf)
            order_request_sell_audchf = fn.open_trade(action='sell', symbol='AUDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audchf = True
            flag_sell_audchf = False
        else:
            order_request_sell_audchf = fn.open_trade(action='sell', symbol='AUDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audchf = False
    # CADCHF
    if data['cad'].iloc[-1] < -BESTTIMEHONE and data['chf'].iloc[-1] > BESTTIMEHONE and flag_buy_cadchf:
        if not flag_sell_cadchf:
            fn.close_trade('buy',order_request_sell_cadchf)
            order_request_buy_cadchf = fn.open_trade(action='buy', symbol='CADCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_cadchf = True
            flag_buy_cadchf = False
        else:
            order_request_buy_cadchf = fn.open_trade(action='buy', symbol='CADCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_cadchf = False
    elif data['cad'].iloc[-1] > BESTTIMEHONE and data['chf'].iloc[-1] < -BESTTIMEHONE and flag_sell_cadchf:
        if not flag_buy_cadchf:
            fn.close_trade('sell',order_request_buy_cadchf)
            order_request_sell_cadchf = fn.open_trade(action='sell', symbol='CADCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_cadchf = True
            flag_sell_cadchf = False
        else:
            order_request_sell_cadchf = fn.open_trade(action='sell', symbol='CADCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_cadchf = False
    # NZDCHF
    if data['nzd'].iloc[-1] < -BESTTIMEHONE and data['chf'].iloc[-1] > BESTTIMEHONE and flag_buy_nzdchf:
        if not flag_sell_nzdchf:
            fn.close_trade('buy',order_request_sell_nzdchf)
            order_request_buy_nzdchf = fn.open_trade(action='buy', symbol='NZDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdchf = True
            flag_buy_nzdchf = False
        else:
            order_request_buy_nzdchf = fn.open_trade(action='buy', symbol='NZDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdchf = False
    elif data['nzd'].iloc[-1] > BESTTIMEHONE and data['chf'].iloc[-1] < -BESTTIMEHONE and flag_sell_nzdchf:
        if not flag_buy_nzdchf:
            fn.close_trade('sell',order_request_buy_nzdchf)
            order_request_sell_nzdchf = fn.open_trade(action='sell', symbol='NZDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdchf = True
            flag_sell_nzdchf = False
        else:
            order_request_sell_nzdchf = fn.open_trade(action='sell', symbol='NZDCHF', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdchf = False
            # NZD
    # AUDNZD
    if data['aud'].iloc[-1] < -BESTTIMEHONE and data['nzd'].iloc[-1] > BESTTIMEHONE and flag_buy_audnzd:
        if not flag_sell_audnzd:
            fn.close_trade('buy',order_request_sell_audnzd)
            order_request_buy_audnzd = fn.open_trade(action='buy', symbol='AUDNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audnzd = True
            flag_buy_audnzd = False
        else:
            order_request_buy_audnzd = fn.open_trade(action='buy', symbol='AUDNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audnzd = False
    elif data['aud'].iloc[-1] > BESTTIMEHONE and data['nzd'].iloc[-1] < -BESTTIMEHONE and flag_sell_audnzd:
        if not flag_buy_audnzd:
            fn.close_trade('sell',order_request_buy_audnzd)
            order_request_sell_audnzd = fn.open_trade(action='sell', symbol='AUDNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audnzd = True
            flag_sell_audnzd = False
        else:
            order_request_sell_audnzd = fn.open_trade(action='sell', symbol='AUDNZD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audnzd = False
    # NZDCAD
    if data['nzd'].iloc[-1] < -BESTTIMEHONE and data['cad'].iloc[-1] > BESTTIMEHONE and flag_buy_nzdcad:
        if not flag_sell_nzdcad:
            fn.close_trade('buy',order_request_sell_nzdcad)
            order_request_buy_nzdcad = fn.open_trade(action='buy', symbol='NZDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdcad = True
            flag_buy_nzdcad = False
        else:
            order_request_buy_nzdcad = fn.open_trade(action='buy', symbol='NZDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdcad = False
    elif data['nzd'].iloc[-1] > BESTTIMEHONE and data['cad'].iloc[-1] < -BESTTIMEHONE and flag_sell_nzdcad:
        if not flag_buy_nzdcad:
            fn.close_trade('sell',order_request_buy_nzdcad)
            order_request_sell_nzdcad = fn.open_trade(action='sell', symbol='NZDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_nzdcad = True
            flag_sell_nzdcad = False
        else:
            order_request_sell_nzdcad = fn.open_trade(action='sell', symbol='NZDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_nzdcad = False
            # AUD
    # AUDCAD
    if data['aud'].iloc[-1] < -BESTTIMEHONE and data['cad'].iloc[-1] > BESTTIMEHONE and flag_buy_audcad:
        if not flag_sell_audcad:
            fn.close_trade('buy',order_request_sell_audcad)
            order_request_buy_audcad = fn.open_trade(action='buy', symbol='AUDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audcad = True
            flag_buy_audcad = False
        else:
            order_request_buy_audcad = fn.open_trade(action='buy', symbol='AUDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audcad = False
    elif data['aud'].iloc[-1] > BESTTIMEHONE and data['cad'].iloc[-1] < -BESTTIMEHONE and flag_sell_audcad:
        if not flag_buy_audcad:
            fn.close_trade('sell',order_request_buy_audcad)
            order_request_sell_audcad = fn.open_trade(action='sell', symbol='AUDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_buy_audcad = True
            flag_sell_audcad = False
        else:
            order_request_sell_audcad = fn.open_trade(action='sell', symbol='AUDCAD', ea_magic_number=HONEMAGICNUMBER)
            flag_sell_audcad = False

mt5.shutdown()
