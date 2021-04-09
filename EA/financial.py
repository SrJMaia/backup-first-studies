import MetaTrader5 as mt5
from mt5 import get_info

RISK = 0.01
JPY = ['EURJPY','USDJPY','GBPJPY','AUDJPY','CHFJPY','NZDJPY','CADJPY']

MY_EVENTS = {
    'EURUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURUSD','first_currency':'eur','second_currency':'usd'},
    'EURCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURCHF','first_currency':'eur','second_currency':'chf'},
    'EURGBP':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURGBP','first_currency':'eur','second_currency':'gbp'},
    'EURJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURJPY','first_currency':'eur','second_currency':'jpy'},
    'EURNZD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURNZD','first_currency':'eur','second_currency':'nzd'},
    'EURAUD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURAUD','first_currency':'eur','second_currency':'aud'},
    'EURCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURCAD','first_currency':'eur','second_currency':'cad'},

    'GBPAUD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPAUD','first_currency':'gbp','second_currency':'aud'},
    'GBPCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPCHF','first_currency':'gbp','second_currency':'chf'},
    'GBPJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPJPY','first_currency':'gbp','second_currency':'jpy'},
    'GBPCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPCAD','first_currency':'gbp','second_currency':'cad'},
    'GBPUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPUSD','first_currency':'gbp','second_currency':'usd'},
    'GBPNZD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPNZD','first_currency':'gbp','second_currency':'nzd'},

    'USDCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'USDCHF','first_currency':'usd','second_currency':'chf'},
    'USDJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'USDJPY','first_currency':'usd','second_currency':'jpy'},
    'AUDUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDUSD','first_currency':'aud','second_currency':'usd'},
    'NZDUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDUSD','first_currency':'nzd','second_currency':'usd'},
    'USDCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'USDCAD','first_currency':'usd','second_currency':'cad'},

    'AUDJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDJPY','first_currency':'aud','second_currency':'jpy'},
    'CADJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'CADJPY','first_currency':'cad','second_currency':'jpy'},
    'CHFJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'CHFJPY','first_currency':'chf','second_currency':'jpy'},
    'NZDJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDJPY','first_currency':'nzd','second_currency':'jpy'},

    'AUDCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDCHF','first_currency':'aud','second_currency':'chf'},
    'CADCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'CADCHF','first_currency':'cad','second_currency':'chf'},
    'NZDCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDCHF','first_currency':'nzd','second_currency':'chf'},

    'AUDNZD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDNZD','first_currency':'aud','second_currency':'nzd'},
    'NZDCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDCAD','first_currency':'nzd','second_currency':'cad'},

    'AUDCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDCAD','first_currency':'aud','second_currency':'cad'}
}

def account_information():
    account = mt5.account_info()._asdict()
    if account == None:
        print(f'Erro ao pegar dados da conta. Erro: {mt5.last_error()}')
        mt5.shutdown()
    else:
        return account['leverage'],account['margin_free']


def lot_calculation(balance,leverage,symbol):
    """
    Fazer o calculo multiplicando a quantidade de
    alavancagem que eu desejo
    Leverage = 2 por exemplo
    como no backtest
    """
    leverage *= 0.1
    lot = round(balance*RISK*leverage/100_000,2)
    if lot < 0.01:
        lot = 0.01
    elif symbol in ['NZDCAD','NZDCHF','NZDJPY'] and lot < 0.1:
        lot = 0.1
    return lot



def open_trade(action, tksl, symbol, ea_magic_number):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    symbol_info = get_info(symbol)

    tk, sl = 0, 0

    leverage, balance = account_information()

    if symbol in JPY:
        tk = tksl / 100
        sl = tksl / 200
    else:
        tk = tksl / 10000
        sl = tksl / 20000

    if action == 'buy':
        trade_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
        tk += price
        sl = price - sl
    elif action =='sell':
        trade_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
        tk = price - tk
        sl += price

    point = mt5.symbol_info(symbol).point

    order_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_calculation(balance,leverage,symbol),
        "type": trade_type,
        "price": price,
        "sl": sl,
        "tp": tk,
        "deviation": 10,
        "magic": ea_magic_number,
        "comment": "MAYBE LATER A COMMENT",
        "type_time": mt5.ORDER_TIME_GTC, # good till cancelled
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }
    # send a trading request
    result = mt5.order_send(order_request)

    if result[0] == 10009:
        print(f"{action.title()} | Symbol: {symbol} | Price: {order_request['price']} | Volume: {order_request['volume']}")
        return order_request
    elif result[0] == 10004 or result[0] == 10021:
        while result[0] == 10004:
            result = mt5.order_send(order_request)
            print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]} | New Price.")
        if result[0] == 10009:
            print(f"{action.title()} | Symbol: {symbol} | Price: {order_request['price']} | Volume: {order_request['volume']}")
        else:
            print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]}")
    else:
        print(f"Error Order {symbol}: {mt5.last_error()} | Code: {result[0]}")


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
        print(f'Error Closing {symbol}: {mt5.last_error()} | Code: {result[0]}')
    print(f"Closing as: {action.title()} | Symbol: {symbol} | Volume: {result[3]} | Price: {result[4]}")

    # Backup
    # if result[0] == 10009:
    #     print(f"Closing as: {action.title()} | Symbol: {symbol} | Volume: {result[3]} | Price: {result[4]}")
    # else:
    #     print(f'Error Closing {symbol}: {mt5.last_error()} | Code: {result[0]}')
