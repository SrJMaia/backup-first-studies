import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import datetime as dt

def diff_data(list_symbol,start,end):
    df2 = pd.DataFrame()
    for i in range(len(list_symbol)):
        df=pd.DataFrame(mt5.copy_rates_from_pos(list_symbol[i], mt5.TIMEFRAME_H1 , start, end))
        df2[list_symbol[i]] = df['close'].pct_change()
        del df
    df2['sum'] = df2.sum(axis=1)
    df2['sma'] = round(df2['sum'].rolling(5).sum()*10000,0)
    return df2['sma']


def account_information():
    account = mt5.account_info()._asdict()
    if account == None:
        print(f'Erro ao pegar dados da conta. Erro: {mt5.last_error()}')
        mt5.shutdown()
    else:
        return account['leverage'],account['margin_free'],account['balance'],account['profit']


def login_mt5(login,password,server):
    mt5.initialize()

    if not mt5.initialize(login=40305620,password='x8dcteyv',server='MetaQuotes-Demo'):
        print(f'MT5 não iniciado. Erro: {mt5.last_error()}')
        mt5.shutdown()


def lot_calculation(balance,risk,leverage):
    leverage *= 0.1
    lot = round(balance*risk*leverage/100_000,2)
    if lot < 0.01:
        lot = 0.01
    return lot


def get_info(symbol):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
    '''
    # get symbol properties
    info=mt5.symbol_info(symbol)
    return info


def open_trade(action, symbol, balance, risk, leverage, ea_magic_number):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    symbol_info = get_info(symbol)

    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    point = mt5.symbol_info(symbol).point

    order_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_calculation(balance,risk,leverage),
        "type": trade_type,
        "price": price,
        "deviation": 0,
        "magic": ea_magic_number,
        "comment": "MAYBE LATER A COMMENT",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(order_request)

    if result[0] == 10009:
        print(f"{action.title()} | Symbol: {symbol} | Price: {order_request['price']} | Volume: {order_request['volume']}")
    else:
        print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]}")

    return order_request


def close_trade(action, order_request):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # create a close request
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
        "deviation": 0,
        "magic": order_request['magic'],
        "comment": f"Closing position: {order_request['symbol']}",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a close request
    result=mt5.order_send(close_request)
    if result[0] == 10009:
        print(f"Closing as: {action.title()} | Symbol: {symbol} | Volume: {result[3]} | Price: {result[4]}")
    else:
        print(f'Error Closing {symbol}: {mt5.last_error()} | Code: {result[0]}')
