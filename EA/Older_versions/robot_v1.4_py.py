import MetaTrader5 as mt5
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import numpy as np
import robot_functions as func
from time import sleep
from IPython.display import clear_output
from PySimpleGUI import PySimpleGUI as sg

plt.style.use('dark_background')
plt.rcParams["figure.figsize"] = (30,10)

# Constantes

pairs = [
        ['EURCHF','EURGBP','EURJPY','EURNZD','EURUSD','EURAUD','EURCAD'],
        ['EURGBP','GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD'],
        ['GBPUSD','USDCHF','USDJPY','AUDUSD','NZDUSD','USDCAD','EURUSD'],
        ['AUDJPY','CADJPY','CHFJPY','EURJPY','USDJPY','GBPJPY','NZDJPY'],
        ['AUDCHF','CADCHF','CHFJPY','USDCHF','EURCHF','GBPCHF','NZDCHF'],
        ['AUDNZD','EURNZD','GBPNZD','NZDUSD','NZDCAD','NZDCHF','NZDJPY'],
        ['AUDCAD','AUDCHF','AUDJPY','AUDUSD','AUDNZD','EURAUD','GBPAUD'],
        ['AUDCAD','CADCHF','CADJPY','USDCAD','EURCAD','GBPCAD','NZDCAD']
        ]

all_pairs = ['eur','gbp','usd','jpy','chf','nzd','aud','cad']

risk = 0.01

data = pd.DataFrame()

ea_magic_number = 1010

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

best_time = 7

eur_best_time = 7
usd_best_time = 7
gbp_best_time = 7
jpy_best_time = 7
chf_best_time = 7
nzd_best_time = 7
aud_best_time = 7

func.login_mt5(login=40305620,password='x8dcteyv',server='MetaQuotes-Demo')


sg.theme('SystemDefault')

layout = [
    [sg.Text("",font=[_,15],size=(25,1),auto_size_text=True,key='-MARGIN_FREE0-',justification='c',background_color='grey80'),
     sg.Text("",font=[_,15],size=(25,1),auto_size_text=True,key='-BALANCE0-',justification='c',background_color='grey80'),
     sg.Text("",font=[_,15],size=(25,1),auto_size_text=True,key='-PROFIT0-',justification='c',background_color='grey80')],
    [sg.Text("")],
    [sg.Text("",size=(25,1),key='-EUR0-',justification='l')],
    [sg.Text("",size=(25,1),key='-USD0-',justification='l')],
    [sg.Text("",size=(25,1),key='-GBP0-',justification='l')],
    [sg.Text("",size=(25,1),key='-JPY0-',justification='l')],
    [sg.Text("",size=(25,1),key='-CHF0-',justification='l')],
    [sg.Text("",size=(25,1),key='-NZD0-',justification='l')],
    [sg.Text("",size=(25,1),key='-AUD0-',justification='l')],
    [sg.Text("",size=(25,1),key='-CAD0-',justification='l')],
]

window = sg.Window('Robot V1.4',layout,auto_size_text=True,size=(960,320),resizable=True)

while True:

    # Get Data
    for i in range(len(pairs)):
        data[all_pairs[i]] = func.diff_data(list_symbol = pairs[i], start = 0, end = 10)
    data.dropna(inplace=True)

    leverage, margin_free, balance, profit = func.account_information()

    event, _ = window.read(timeout=1)
    if event == sg.WIN_CLOSED:
        exit_flag = True
        window.close()
        break

    window['-MARGIN_FREE0-'].update(f"Margin Free: {margin_free}€")
    window['-BALANCE0-'].update(f"Balance: {balance}€")
    window['-PROFIT0-'].update(f"Profit: {profit}€",text_color=['red' if profit<0 else 'green'])
    window['-EUR0-'].update(f"EUR - C0: {data['eur'].iloc[-1]} | C-1: {data['eur'].iloc[-2]}")
    window['-USD0-'].update(f"USD - C0: {data['usd'].iloc[-1]} | C-1: {data['usd'].iloc[-2]}")
    window['-GBP0-'].update(f"GBP - C0: {data['gbp'].iloc[-1]} | C-1: {data['gbp'].iloc[-2]}")
    window['-JPY0-'].update(f"JPY - C0: {data['jpy'].iloc[-1]} | C-1: {data['jpy'].iloc[-2]}")
    window['-CHF0-'].update(f"CHF - C0: {data['chf'].iloc[-1]} | C-1: {data['chf'].iloc[-2]}")
    window['-NZD0-'].update(f"NZD - C0: {data['nzd'].iloc[-1]} | C-1: {data['nzd'].iloc[-2]}")
    window['-AUD0-'].update(f"AUD - C0: {data['aud'].iloc[-1]} | C-1: {data['aud'].iloc[-2]}")
    window['-CAD0-'].update(f"CAD - C0: {data['cad'].iloc[-1]} | C-1: {data['cad'].iloc[-2]}")

            #EUR
    # EURUSD
    if data['eur'].iloc[-1] < -best_time and data['usd'].iloc[-1] > best_time and flag_buy_eurusd:
        if not flag_sell_eurusd:
            func.close_trader('buy',order_request_sell_eurusd, ea_magic_number=ea_magic_number)
            order_request_buy_eurusd = func.open_trade(action='buy', symbol='EURUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurusd = True
            flag_buy_eurusd = False
        else:
            order_request_buy_eurusd = func.open_trade(action='buy', symbol='EURUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurusd = False
    elif data['eur'].iloc[-1] > best_time and data['usd'].iloc[-1] < -best_time and flag_sell_eurusd:
        if not flag_buy_eurusd:
            func.close_trader('sell',order_request_buy_eurusd, ea_magic_number=ea_magic_number)
            order_request_sell_eurusd = func.open_trade(action='sell', symbol='EURUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurusd = True
            flag_sell_eurusd = False
        else:
            order_request_sell_eurusd = func.open_trade(action='sell', symbol='EURUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurusd = False
    # EURGBP
    if data['eur'].iloc[-1] < -best_time and data['gbp'].iloc[-1] > best_time and flag_buy_eurgbp:
        if not flag_sell_eurgbp:
            func.close_trader('buy',order_request_sell_eurgbp, ea_magic_number=ea_magic_number)
            order_request_buy_eurgbp = func.open_trade(action='buy', symbol='EURGBP', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurgbp = True
            flag_buy_eurgbp = False
        else:
            order_request_buy_eurgbp = func.open_trade(action='buy', symbol='EURGBP', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurgbp = False
    elif data['eur'].iloc[-1] > best_time and data['gbp'].iloc[-1] < -best_time and flag_sell_eurgbp:
        if not flag_buy_eurgbp:
            func.close_trader('sell',order_request_buy_eurgbp, ea_magic_number=ea_magic_number)
            order_request_sell_eurgbp = func.open_trade(action='sell', symbol='EURGBP', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurgbp = True
            flag_sell_eurgbp = False
        else:
            order_request_sell_eurgbp = func.open_trade(action='sell', symbol='EURGBP', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurgbp = False
    # EURJPY
    if data['eur'].iloc[-1] < -best_time and data['jpy'].iloc[-1] > best_time and flag_buy_eurjpy:
        if not flag_sell_eurjpy:
            func.close_trader('buy',order_request_sell_eurjpy, ea_magic_number=ea_magic_number)
            order_request_buy_eurjpy = func.open_trade(action='buy', symbol='EURJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurjpy = True
            flag_buy_eurjpy = False
        else:
            order_request_buy_eurjpy = func.open_trade(action='buy', symbol='EURJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurjpy = False
    elif data['eur'].iloc[-1] > best_time and data['jpy'].iloc[-1] < -best_time and flag_sell_eurjpy:
        if not flag_buy_eurjpy:
            func.close_trader('sell',order_request_buy_eurjpy, ea_magic_number=ea_magic_number)
            order_request_sell_eurjpy = func.open_trade(action='sell', symbol='EURJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurjpy = True
            flag_sell_eurjpy = False
        else:
            order_request_sell_eurjpy = func.open_trade(action='sell', symbol='EURJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurjpy = False
    # EURCHF
    if data['eur'].iloc[-1] < -best_time and data['chf'].iloc[-1] > best_time and flag_buy_eurchf:
        if not flag_sell_eurchf:
            func.close_trader('buy',order_request_sell_eurchf, ea_magic_number=ea_magic_number)
            order_request_buy_eurchf = func.open_trade(action='buy', symbol='EURCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurchf = True
            flag_buy_eurchf = False
        else:
            order_request_buy_eurchf = func.open_trade(action='buy', symbol='EURCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurchf = False
    elif data['eur'].iloc[-1] > best_time and data['chf'].iloc[-1] < -best_time and flag_sell_eurchf:
        if not flag_buy_eurchf:
            func.close_trader('sell',order_request_buy_eurchf, ea_magic_number=ea_magic_number)
            order_request_sell_eurchf = func.open_trade(action='sell', symbol='EURCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurchf = True
            flag_sell_eurchf = False
        else:
            order_request_sell_eurchf = func.open_trade(action='sell', symbol='EURCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurchf = False
    # EURNZD
    if data['eur'].iloc[-1] < -best_time and data['nzd'].iloc[-1] > best_time and flag_buy_eurnzd:
        if not flag_sell_eurnzd:
            func.close_trader('buy',order_request_sell_eurnzd, ea_magic_number=ea_magic_number)
            order_request_buy_eurnzd = func.open_trade(action='buy', symbol='EURNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurnzd = True
            flag_buy_eurnzd = False
        else:
            order_request_buy_eurnzd = func.open_trade(action='buy', symbol='EURNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurnzd = False
    elif data['eur'].iloc[-1] > best_time and data['nzd'].iloc[-1] < -best_time and flag_sell_eurnzd:
        if not flag_buy_eurnzd:
            func.close_trader('sell',order_request_buy_eurnzd, ea_magic_number=ea_magic_number)
            order_request_sell_eurnzd = func.open_trade(action='sell', symbol='EURNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurnzd = True
            flag_sell_eurnzd = False
        else:
            order_request_sell_eurnzd = func.open_trade(action='sell', symbol='EURNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurnzd = False
    # EURUAD
    if data['eur'].iloc[-1] < -best_time and data['aud'].iloc[-1] > best_time and flag_buy_euraud:
        if not flag_sell_euraud:
            func.close_trader('buy',order_request_sell_euraud, ea_magic_number=ea_magic_number)
            order_request_buy_euraud = func.open_trade(action='buy', symbol='EURAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_euraud = True
            flag_buy_euraud = False
        else:
            order_request_buy_euraud = func.open_trade(action='buy', symbol='EURAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_euraud = False
    elif data['eur'].iloc[-1] > best_time and data['aud'].iloc[-1] < -best_time and flag_sell_euraud:
        if not flag_buy_:
            func.close_trader('sell',order_request_buy_euraud, ea_magic_number=ea_magic_number)
            order_request_sell_euraud = func.open_trade(action='sell', symbol='EURAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_euraud = True
            flag_sell_euraud = False
        else:
            order_request_sell_euraud = func.open_trade(action='sell', symbol='EURAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_euraud = False
    # EURCAD
    if data['eur'].iloc[-1] < -best_time and data['cad'].iloc[-1] > best_time and flag_buy_eurcad:
        if not flag_sell_eurcad:
            func.close_trader('buy',order_request_sell_eurcad, ea_magic_number=ea_magic_number)
            order_request_buy_eurcad = func.open_trade(action='buy', symbol='EURCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurcad = True
            flag_buy_eurcad = False
        else:
            order_request_buy_eurcad = func.open_trade(action='buy', symbol='EURCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurcad = False
    elif data['eur'].iloc[-1] > best_time and data['cad'].iloc[-1] < -best_time and flag_sell_eurcad:
        if not flag_buy_eurcad:
            func.close_trader('sell',order_request_buy_eurcad, ea_magic_number=ea_magic_number)
            order_request_sell_eurcad = func.open_trade(action='sell', symbol='EURCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_eurcad = True
            flag_sell_eurcad = False
        else:
            order_request_sell_eurcad = func.open_trade(action='sell', symbol='EURCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_eurcad = False
            # USD
   # GBPUSD
    if data['gbp'].iloc[-1] < -best_time and data['usd'].iloc[-1] > best_time and flag_buy_gbpusd:
        if not flag_sell_gbpusd:
            func.close_trader('buy',order_request_sell_gbpusd, ea_magic_number=ea_magic_number)
            order_request_buy_gbpusd = func.open_trade(action='buy', symbol='GBPUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpusd = True
            flag_buy_gbpusd = False
        else:
            order_request_buy_gbpusd = func.open_trade(action='buy', symbol='GBPUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpusd = False
    elif data['gbp'].iloc[-1] > best_time and data['usd'].iloc[-1] < -best_time and flag_sell_gbpusd:
        if not flag_buy_gbpusd:
            func.close_trader('sell',order_request_buy_gbpusd, ea_magic_number=ea_magic_number)
            order_request_sell_gbpusd = func.open_trade(action='sell', symbol='GBPUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpusd = True
            flag_sell_gbpusd = False
        else:
            order_request_sell_gbpusd = func.open_trade(action='sell', symbol='GBPUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpusd = False
    # USDCHF
    if data['usd'].iloc[-1] < -best_time and data['chf'].iloc[-1] > best_time and flag_buy_usdchf:
        if not flag_sell_usdchf:
            func.close_trader('buy',order_request_sell_usdchf, ea_magic_number=ea_magic_number)
            order_request_buy_usdchf = func.open_trade(action='buy', symbol='USDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_usdchf = True
            flag_buy_usdchf = False
        else:
            order_request_buy_usdchf = func.open_trade(action='buy', symbol='USDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_usdchf = False
    elif data['usd'].iloc[-1] > best_time and data['chf'].iloc[-1] < -best_time and flag_sell_usdchf:
        if not flag_buy_usdchf:
            func.close_trader('sell',order_request_buy_usdchf, ea_magic_number=ea_magic_number)
            order_request_sell_usdchf = func.open_trade(action='sell', symbol='USDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_usdchf = True
            flag_sell_usdchf = False
        else:
            order_request_sell_usdchf = func.open_trade(action='sell', symbol='USDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_usdchf = False
    # USDJPY
    if data['usd'].iloc[-1] < -best_time and data['jpy'].iloc[-1] > best_time and flag_buy_usdjpy:
        if not flag_sell_usdjpy:
            func.close_trader('buy',order_request_sell_usdjpy, ea_magic_number=ea_magic_number)
            order_request_buy_usdjpy = func.open_trade(action='buy', symbol='USDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_usdjpy = True
            flag_buy_usdjpy = False
        else:
            order_request_buy_usdjpy = func.open_trade(action='buy', symbol='USDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_usdjpy = False
    elif data['usd'].iloc[-1] > best_time and data['jpy'].iloc[-1] < -best_time and flag_sell_usdjpy:
        if not flag_buy_usdjpy:
            func.close_trader('sell',order_request_buy_usdjpy, ea_magic_number=ea_magic_number)
            order_request_sell_usdjpy = func.open_trade(action='sell', symbol='USDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_usdjpy = True
            flag_sell_usdjpy = False
        else:
            order_request_sell_usdjpy = func.open_trade(action='sell', symbol='USDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_usdjpy = False
    # AUDUSD
    if data['aud'].iloc[-1] < -best_time and data['usd'].iloc[-1] > best_time and flag_buy_audusd:
        if not flag_sell_audusd:
            func.close_trader('buy',order_request_sell_audusd, ea_magic_number=ea_magic_number)
            order_request_buy_audusd = func.open_trade(action='buy', symbol='', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audusd = True
            flag_buy_audusd = False
        else:
            order_request_buy_audusd = func.open_trade(action='buy', symbol='AUDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audusd = False
    elif data['aud'].iloc[-1] > best_time and data['usd'].iloc[-1] < -best_time and flag_sell_audusd:
        if not flag_buy_audusd:
            func.close_trader('sell',order_request_buy_audusd, ea_magic_number=ea_magic_number)
            order_request_sell_audusd = func.open_trade(action='sell', symbol='AUDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audusd = True
            flag_sell_audusd = False
        else:
            order_request_sell_audusd = func.open_trade(action='sell', symbol='AUDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audusd = False
    # NZDUSD
    if data['nzd'].iloc[-1] < -best_time and data['usd'].iloc[-1] > best_time and flag_buy_nzdusd:
        if not flag_sell_nzdusd:
            func.close_trader('buy',order_request_sell_nzdusd, ea_magic_number=ea_magic_number)
            order_request_buy_nzdusd = func.open_trade(action='buy', symbol='NZDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdusd = True
            flag_buy_nzdusd = False
        else:
            order_request_buy_nzdusd = func.open_trade(action='buy', symbol='NZDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdusd = False
    elif data['nzd'].iloc[-1] > best_time and data['usd'].iloc[-1] < -best_time and flag_sell_:
        if not flag_buy_nzdusd:
            func.close_trader('sell',order_request_buy_nzdusd, ea_magic_number=ea_magic_number)
            order_request_sell_nzdusd = func.open_trade(action='sell', symbol='NZDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdusd = True
            flag_sell_nzdusd = False
        else:
            order_request_sell_nzdusd = func.open_trade(action='sell', symbol='NZDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdusd = False
    # USDCAD
    if data['usd'].iloc[-1] < -best_time and data['cad'].iloc[-1] > best_time and flag_buy_usdcad:
        if not flag_sell_usdcad:
            func.close_trader('buy',order_request_sell_usdcad, ea_magic_number=ea_magic_number)
            order_request_buy_usdcad = func.open_trade(action='buy', symbol='USDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_usdcad = True
            flag_buy_usdcad = False
        else:
            order_request_buy_usdcad = func.open_trade(action='buy', symbol='USDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_usdcad = False
    elif data['usd'].iloc[-1] > best_time and data['cad'].iloc[-1] < -best_time and flag_sell_:
        if not flag_buy_nzdusd:
            func.close_trader('sell',order_request_buy_nzdusd, ea_magic_number=ea_magic_number)
            order_request_sell_nzdusd = func.open_trade(action='sell', symbol='NZDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdusd = True
            flag_sell_nzdusd = False
        else:
            order_request_sell_nzdusd = func.open_trade(action='sell', symbol='NZDUSD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdusd = False
            # GBP
    # GBPAUD
    if data['gbp'].iloc[-1] < -best_time and data['aud'].iloc[-1] > best_time and flag_buy_gbpaud:
        if not flag_sell_gbpaud:
            func.close_trader('buy',order_request_sell_gbpaud, ea_magic_number=ea_magic_number)
            order_request_buy_gbpaud = func.open_trade(action='buy', symbol='GBPAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpaud = True
            flag_buy_gbpaud = False
        else:
            order_request_buy_gbpaud = func.open_trade(action='buy', symbol='GBPAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpaud = False
    elif data['gbp'].iloc[-1] > best_time and data['aud'].iloc[-1] < -best_time and flag_sell_gbpaud:
        if not flag_buy_gbpaud:
            func.close_trader('sell',order_request_buy_gbpaud, ea_magic_number=ea_magic_number)
            order_request_sell_gbpaud = func.open_trade(action='sell', symbol='GBPAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpaud = True
            flag_sell_gbpaud = False
        else:
            order_request_sell_gbpaud = func.open_trade(action='sell', symbol='GBPAUD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpaud = False
    # GBPCHF
    if data['gbp'].iloc[-1] < -best_time and data['chf'].iloc[-1] > best_time and flag_buy_gbpchf:
        if not flag_sell_gbpchf:
            func.close_trader('buy',order_request_sell_gbpchf, ea_magic_number=ea_magic_number)
            order_request_buy_gbpchf = func.open_trade(action='buy', symbol='GBPCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpchf = True
            flag_buy_gbpchf = False
        else:
            order_request_buy_gbpchf = func.open_trade(action='buy', symbol='GBPCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpchf = False
    elif data['gbp'].iloc[-1] > best_time and data['chf'].iloc[-1] < -best_time and flag_sell_:
        if not flag_buy_gbpchf:
            func.close_trader('sell',order_request_buy_gbpchf, ea_magic_number=ea_magic_number)
            order_request_sell_gbpchf = func.open_trade(action='sell', symbol='GBPCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpchf = True
            flag_sell_gbpchf = False
        else:
            order_request_sell_gbpchf = func.open_trade(action='sell', symbol='GBPCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpchf = False
    # GBPJPY
    if data['gbp'].iloc[-1] < -best_time and data['jpy'].iloc[-1] > best_time and flag_buy_gbpjpy:
        if not flag_sell_gbpjpy:
            func.close_trader('buy',order_request_sell_gbpjpy, ea_magic_number=ea_magic_number)
            order_request_buy_gbpjpy = func.open_trade(action='buy', symbol='GBPJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpjpy = True
            flag_buy_gbpjpy = False
        else:
            order_request_buy_gbpjpy = func.open_trade(action='buy', symbol='GBPJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpjpy = False
    elif data['gbp'].iloc[-1] > best_time and data['jpy'].iloc[-1] < -best_time and flag_sell_gbpjpy:
        if not flag_buy_gbpjpy:
            func.close_trader('sell',order_request_buy_gbpjpy, ea_magic_number=ea_magic_number)
            order_request_sell_gbpjpy = func.open_trade(action='sell', symbol='GBPJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpjpy = True
            flag_sell_gbpjpy = False
        else:
            order_request_sell_gbpjpy = func.open_trade(action='sell', symbol='GBPJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpjpy = False
    # GBPCAD
    if data['gbp'].iloc[-1] < -best_time and data['cad'].iloc[-1] > best_time and flag_buy_gbpcad:
        if not flag_sell_gbpcad:
            func.close_trader('buy',order_request_sell_gbpcad, ea_magic_number=ea_magic_number)
            order_request_buy_gbpcad = func.open_trade(action='buy', symbol='GBPCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpcad = True
            flag_buy_gbpcad = False
        else:
            order_request_buy_gbpcad = func.open_trade(action='buy', symbol='GBPCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpcad = False
    elif data['gbp'].iloc[-1] > best_time and data['cad'].iloc[-1] < -best_time and flag_sell_gbpcad:
        if not flag_buy_gbpcad:
            func.close_trader('sell',order_request_buy_gbpcad, ea_magic_number=ea_magic_number)
            order_request_sell_gbpcad = func.open_trade(action='sell', symbol='GBPCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpcad = True
            flag_sell_gbpcad = False
        else:
            order_request_sell_gbpcad = func.open_trade(action='sell', symbol='GBPCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpcad = False
    # GBPNZD
    if data['gbp'].iloc[-1] < -best_time and data['nzd'].iloc[-1] > best_time and flag_buy_gbpnzd:
        if not flag_sell_gbpnzd:
            func.close_trader('buy',order_request_sell_gbpnzd, ea_magic_number=ea_magic_number)
            order_request_buy_gbpnzd = func.open_trade(action='buy', symbol='GBPNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpnzd = True
            flag_buy_gbpnzd = False
        else:
            order_request_buy_gbpnzd = func.open_trade(action='buy', symbol='GBPNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpnzd = False
    elif data['gbp'].iloc[-1] > best_time and data['nzd'].iloc[-1] < -best_time and flag_sell_gbpnzd:
        if not flag_buy_gbpnzd:
            func.close_trader('sell',order_request_buy_gbpnzd, ea_magic_number=ea_magic_number)
            order_request_sell_gbpnzd = func.open_trade(action='sell', symbol='GBPNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_gbpnzd = True
            flag_sell_gbpnzd = False
        else:
            order_request_sell_gbpnzd = func.open_trade(action='sell', symbol='GBPNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_gbpnzd = False
            # JPY
    # AUDJPY
    if data['aud'].iloc[-1] < -best_time and data['jpy'].iloc[-1] > best_time and flag_buy_audjpy:
        if not flag_sell_audjpy:
            func.close_trader('buy',order_request_sell_audjpy, ea_magic_number=ea_magic_number)
            order_request_buy_audjpy = func.open_trade(action='buy', symbol='AUDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audjpy = True
            flag_buy_audjpy = False
        else:
            order_request_buy_audjpy = func.open_trade(action='buy', symbol='AUDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audjpy = False
    elif data['aud'].iloc[-1] > best_time and data['jpy'].iloc[-1] < -best_time and flag_sell_audjpy:
        if not flag_buy_audjpy:
            func.close_trader('sell', order_request_buy_audjpy, ea_magic_number=ea_magic_number)
            order_request_sell_audjpy = func.open_trade(action='sell', symbol='AUDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audjpy = True
            flag_sell_audjpy = False
        else:
            order_request_sell_audjpy = func.open_trade(action='sell', symbol='AUDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audjpy = False
    # CADJPY
    if data['cad'].iloc[-1] < -best_time and data['jpy'].iloc[-1] > best_time and flag_buy_cadjpy:
        if not flag_sell_cadjpy:
            func.close_trader('buy',order_request_sell_cadjpy, ea_magic_number=ea_magic_number)
            order_request_buy_cadjpy = func.open_trade(action='buy', symbol='CADJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_cadjpy = True
            flag_buy_cadjpy = False
        else:
            order_request_buy_cadjpy = func.open_trade(action='buy', symbol='CADJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_cadjpy = False
    elif data['cad'].iloc[-1] > best_time and data['jpy'].iloc[-1] < -best_time and flag_sell_cadjpy:
        if not flag_buy_cadjpy:
            func.close_trader('sell',order_request_buy_cadjpy, ea_magic_number=ea_magic_number)
            order_request_sell_cadjpy = func.open_trade(action='sell', symbol='CADJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_cadjpy = True
            flag_sell_cadjpy = False
        else:
            order_request_sell_cadjpy = func.open_trade(action='sell', symbol='CADJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_cadjpy = False
    # CHFJPY
    if data['chf'].iloc[-1] < -best_time and data['jpy'].iloc[-1] > best_time and flag_buy_chfjpy:
        if not flag_sell_chfjpy:
            func.close_trader('buy',order_request_sell_chfjpy, ea_magic_number=ea_magic_number)
            order_request_buy_chfjpy = func.open_trade(action='buy', symbol='CHFJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_chfjpy = True
            flag_buy_chfjpy = False
        else:
            order_request_buy_chfjpy = func.open_trade(action='buy', symbol='CHFJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_chfjpy = False
    elif data['chf'].iloc[-1] > best_time and data['jpy'].iloc[-1] < -best_time and flag_sell_chfjpy:
        if not flag_buy_chfjpy:
            func.close_trader('sell',order_request_buy_chfjpy, ea_magic_number=ea_magic_number)
            order_request_sell_chfjpy = func.open_trade(action='sell', symbol='CHFJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_chfjpy = True
            flag_sell_chfjpy = False
        else:
            order_request_sell_chfjpy = func.open_trade(action='sell', symbol='CHFJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_chfjpy = False
    # NZDJPY
    if data['nzd'].iloc[-1] < -best_time and data['jpy'].iloc[-1] > best_time and flag_buy_nzdjpy:
        if not flag_sell_nzdjpy:
            func.close_trader('buy',order_request_sell_nzdjpy, ea_magic_number=ea_magic_number)
            order_request_buy_nzdjpy = func.open_trade(action='buy', symbol='NZDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdjpy = True
            flag_buy_nzdjpy = False
        else:
            order_request_buy_nzdjpy = func.open_trade(action='buy', symbol='NZDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdjpy = False
    elif data['nzd'].iloc[-1] > best_time and data['jpy'].iloc[-1] < -best_time and flag_sell_nzdjpy:
        if not flag_buy_nzdjpy:
            func.close_trader('sell',order_request_buy_nzdjpy, ea_magic_number=ea_magic_number)
            order_request_sell_nzdjpy = func.open_trade(action='sell', symbol='NZDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdjpy = True
            flag_sell_nzdjpy = False
        else:
            order_request_sell_nzdjpy = func.open_trade(action='sell', symbol='NZDJPY', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdjpy = False
            # CHF
    # AUDCHF
    if data['aud'].iloc[-1] < -best_time and data['chf'].iloc[-1] > best_time and flag_buy_audchf:
        if not flag_sell_audchf:
            func.close_trader('buy',order_request_sell_audchf, ea_magic_number=ea_magic_number)
            order_request_buy_audchf = func.open_trade(action='buy', symbol='AUDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audchf = True
            flag_buy_audchf = False
        else:
            order_request_buy_audchf = func.open_trade(action='buy', symbol='AUDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audchf = False
    elif data['aud'].iloc[-1] > best_time and data['chf'].iloc[-1] < -best_time and flag_sell_audchf:
        if not flag_buy_audchf:
            func.close_trader('sell',order_request_buy_audchf, ea_magic_number=ea_magic_number)
            order_request_sell_audchf = func.open_trade(action='sell', symbol='AUDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audchf = True
            flag_sell_audchf = False
        else:
            order_request_sell_audchf = func.open_trade(action='sell', symbol='AUDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audchf = False
    # CADCHF
    if data['cad'].iloc[-1] < -best_time and data['chf'].iloc[-1] > best_time and flag_buy_cadchf:
        if not flag_sell_cadchf:
            func.close_trader('buy',order_request_sell_cadchf, ea_magic_number=ea_magic_number)
            order_request_buy_cadchf = func.open_trade(action='buy', symbol='CADCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_cadchf = True
            flag_buy_cadchf = False
        else:
            order_request_buy_cadchf = func.open_trade(action='buy', symbol='CADCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_cadchf = False
    elif data['cad'].iloc[-1] > best_time and data['chf'].iloc[-1] < -best_time and flag_sell_cadchf:
        if not flag_buy_cadchf:
            func.close_trader('sell',order_request_buy_cadchf, ea_magic_number=ea_magic_number)
            order_request_sell_cadchf = func.open_trade(action='sell', symbol='CADCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_cadchf = True
            flag_sell_cadchf = False
        else:
            order_request_sell_cadchf = func.open_trade(action='sell', symbol='CADCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_cadchf = False
    # NZDCHF
    if data['nzd'].iloc[-1] < -best_time and data['chf'].iloc[-1] > best_time and flag_buy_nzdchf:
        if not flag_sell_nzdchf:
            func.close_trader('buy',order_request_sell_nzdchf, ea_magic_number=ea_magic_number)
            order_request_buy_nzdchf = func.open_trade(action='buy', symbol='NZDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdchf = True
            flag_buy_nzdchf = False
        else:
            order_request_buy_nzdchf = func.open_trade(action='buy', symbol='NZDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdchf = False
    elif data['nzd'].iloc[-1] > best_time and data['chf'].iloc[-1] < -best_time and flag_sell_nzdchf:
        if not flag_buy_nzdchf:
            func.close_trader('sell',order_request_buy_nzdchf, ea_magic_number=ea_magic_number)
            order_request_sell_nzdchf = func.open_trade(action='sell', symbol='NZDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdchf = True
            flag_sell_nzdchf = False
        else:
            order_request_sell_nzdchf = func.open_trade(action='sell', symbol='NZDCHF', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdchf = False
            # NZD
    # AUDNZD
    if data['aud'].iloc[-1] < -best_time and data['nzd'].iloc[-1] > best_time and flag_buy_audnzd:
        if not flag_sell_audnzd:
            func.close_trader('buy',order_request_sell_audnzd, ea_magic_number=ea_magic_number)
            order_request_buy_audnzd = func.open_trade(action='buy', symbol='AUDNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audnzd = True
            flag_buy_audnzd = False
        else:
            order_request_buy_audnzd = func.open_trade(action='buy', symbol='AUDNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audnzd = False
    elif data['aud'].iloc[-1] > best_time and data['nzd'].iloc[-1] < -best_time and flag_sell_audnzd:
        if not flag_buy_audnzd:
            func.close_trader('sell',order_request_buy_audnzd, ea_magic_number=ea_magic_number)
            order_request_sell_audnzd = func.open_trade(action='sell', symbol='AUDNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audnzd = True
            flag_sell_audnzd = False
        else:
            order_request_sell_audnzd = func.open_trade(action='sell', symbol='AUDNZD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audnzd = False
    # NZDCAD
    if data['nzd'].iloc[-1] < -best_time and data['cad'].iloc[-1] > best_time and flag_buy_nzdcad:
        if not flag_sell_nzdcad:
            func.close_trader('buy',order_request_sell_nzdcad, ea_magic_number=ea_magic_number)
            order_request_buy_nzdcad = func.open_trade(action='buy', symbol='NZDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdcad = True
            flag_buy_nzdcad = False
        else:
            order_request_buy_nzdcad = func.open_trade(action='buy', symbol='NZDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdcad = False
    elif data['nzd'].iloc[-1] > best_time and data['cad'].iloc[-1] < -best_time and flag_sell_nzdcad:
        if not flag_buy_nzdcad:
            func.close_trader('sell',order_request_buy_nzdcad, ea_magic_number=ea_magic_number)
            order_request_sell_nzdcad = func.open_trade(action='sell', symbol='NZDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_nzdcad = True
            flag_sell_nzdcad = False
        else:
            order_request_sell_nzdcad = func.open_trade(action='sell', symbol='NZDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_nzdcad = False
            # AUD
    # AUDCAD
    if data['aud'].iloc[-1] < -best_time and data['cad'].iloc[-1] > best_time and flag_buy_audcad:
        if not flag_sell_audcad:
            func.close_trader('buy',order_request_sell_audcad, ea_magic_number=ea_magic_number)
            order_request_buy_audcad = func.open_trade(action='buy', symbol='AUDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audcad = True
            flag_buy_audcad = False
        else:
            order_request_buy_audcad = func.open_trade(action='buy', symbol='AUDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audcad = False
    elif data['aud'].iloc[-1] > best_time and data['cad'].iloc[-1] < -best_time and flag_sell_audcad:
        if not flag_buy_audcad:
            func.close_trader('sell',order_request_buy_audcad, ea_magic_number=ea_magic_number)
            order_request_sell_audcad = func.open_trade(action='sell', symbol='AUDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_buy_audcad = True
            flag_sell_audcad = False
        else:
            order_request_sell_audcad = func.open_trade(action='sell', symbol='AUDCAD', balance=margin_free, risk=risk, leverage=leverage, ea_magic_number=ea_magic_number)
            flag_sell_audcad = False

    sleep(0.1)

mt5.shutdown()
