import MetaTrader5 as mt5
from mt5 import get_info

RISK = 0.01

def account_information():
    account = mt5.account_info()._asdict()
    if account == None:
        print(f'Erro ao pegar dados da conta. Erro: {mt5.last_error()}')
        mt5.shutdown()
    else:
        return account['leverage'],account['margin_free']


def lot_calculation(balance,leverage):
    leverage *= 0.1
    lot = round(balance*RISK*leverage/100_000,2)
    if lot < 0.01:
        lot = 0.01
    return lot



def open_trade(action, symbol, ea_magic_number):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5ordersend_py
    '''
    # prepare the buy request structure
    symbol_info = get_info(symbol)

    leverage, balance = account_information()

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
        "volume": lot_calculation(balance,leverage),
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
