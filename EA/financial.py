import MetaTrader5 as mt5
from mt5 import get_info

RISK = 0.01
JPY = ['EURJPY','USDJPY','GBPJPY','AUDJPY','CHFJPY','NZDJPY','CADJPY']

MY_EVENTS = {
    'EURUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURUSD','buy_strategy':'EURUSD_buy','sell_strategy':'EURUSD_sell'},
    'EURCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURCHF','buy_strategy':'EURCHF_buy','sell_strategy':'EURCHF_sell'},
    'EURGBP':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURGBP','buy_strategy':'EURGBP_buy','sell_strategy':'EURGBP_sell'},
    'EURJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURJPY','buy_strategy':'EURJPY_buy','sell_strategy':'EURJPY_sell'},
    'EURNZD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURNZD','buy_strategy':'EURNZD_buy','sell_strategy':'EURNZD_sell'},
    'EURAUD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURAUD','buy_strategy':'EURAUD_buy','sell_strategy':'EURAUD_sell'},
    'EURCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'EURCAD','buy_strategy':'EURCAD_buy','sell_strategy':'EURCAD_sell'},

    'GBPAUD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPAUD','buy_strategy':'GBPAUD_buy','sell_strategy':'GBPAUD_sell'},
    'GBPCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPCHF','buy_strategy':'GBPCHF_buy','sell_strategy':'GBPCHF_sell'},
    'GBPJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPJPY','buy_strategy':'GBPJPY_buy','sell_strategy':'GBPJPY_sell'},
    'GBPCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPCAD','buy_strategy':'GBPCAD_buy','sell_strategy':'GBPCAD_sell'},
    'GBPUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPUSD','buy_strategy':'GBPUSD_buy','sell_strategy':'GBPUSD_sell'},
    'GBPNZD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'GBPNZD','buy_strategy':'GBPNZD_buy','sell_strategy':'GBPNZD_sell'},

    'USDCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'USDCHF','buy_strategy':'USDCHF_buy','sell_strategy':'USDCHF_sell'},
    'USDJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'USDJPY','buy_strategy':'USDJPY_buy','sell_strategy':'USDJPY_sell'},
    'AUDUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDUSD','buy_strategy':'AUDUSD_buy','sell_strategy':'AUDUSD_sell'},
    'NZDUSD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDUSD','buy_strategy':'NZDUSD_buy','sell_strategy':'NZDUSD_sell'},
    'USDCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'USDCAD','buy_strategy':'USDCAD_buy','sell_strategy':'USDCAD_sell'},

    'AUDJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDJPY','buy_strategy':'AUDJPY_buy','sell_strategy':'AUDJPY_sell'},
    'CADJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'CADJPY','buy_strategy':'CADJPY_buy','sell_strategy':'CADJPY_sell'},
    'CHFJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'CHFJPY','buy_strategy':'CHFJPY_buy','sell_strategy':'CHFJPY_sell'},
    'NZDJPY':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDJPY','buy_strategy':'NZDJPY_buy','sell_strategy':'NZDJPY_sell'},

    'AUDCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDCHF','buy_strategy':'AUDCHF_buy','sell_strategy':'AUDCHF_sell'},
    'CADCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'CADCHF','buy_strategy':'CADCHF_buy','sell_strategy':'CADCHF_sell'},
    'NZDCHF':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDCHF','buy_strategy':'NZDCHF_buy','sell_strategy':'NZDCHF_sell'},

    'AUDNZD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDNZD','buy_strategy':'AUDNZD_buy','sell_strategy':'AUDNZD_sell'},
    'NZDCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'NZDCAD','buy_strategy':'NZDCAD_buy','sell_strategy':'NZDCAD_sell'},

    'AUDCAD':{'buy':True,'sell':True,'sell_request':0,'buy_request':0,'symbol':'AUDCAD','buy_strategy':'AUDCAD_buy','sell_strategy':'AUDCAD_sell'}
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



def open_trade(action, tksl, symbol, ea_magic_number, multiply=2):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    symbol_info = get_info(symbol)

    tk, sl = 0, 0

    leverage, balance = account_information()

    if symbol in JPY:
        tk = tksl / 100
        sl = tksl / (100 * multiply)
    else:
        tk = tksl / 10000
        sl = tksl / (10000 * multiply)

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
