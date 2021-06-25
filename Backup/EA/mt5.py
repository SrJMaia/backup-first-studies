import MetaTrader5 as mt5

def login_mt5(login,password,server):
    mt5.initialize()

    info = mt5.terminal_info()

    if not info[4]:
        print(f'AlgoTrading não ativado! Erro: {mt5.last_error()}')
        mt5.shutdown()

    if not mt5.initialize(login=login,password=password,server=server):
        print(f'MT5 não iniciado. Erro: {mt5.last_error()}')
        mt5.shutdown()


def get_info(symbol):
    '''https://www.mql5.com/en/docs/integration/python_metatrader5/mt5symbolinfo_py
    '''
    # get symbol properties
    info=mt5.symbol_info(symbol)
    return info
