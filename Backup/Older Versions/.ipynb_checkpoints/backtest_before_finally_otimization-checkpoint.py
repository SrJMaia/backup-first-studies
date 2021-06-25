import pandas as pd
from IPython.display import clear_output
import analysis_functions as af
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from numba import jit

SYMBOLS =  ['EURUSD','EURCHF','EURGBP','EURJPY','EURNZD','EURAUD','EURCAD',
            'GBPAUD','GBPCHF','GBPJPY','GBPCAD','GBPUSD','GBPNZD','USDCHF',
            'USDJPY','AUDUSD','NZDUSD','USDCAD','AUDJPY','CADJPY','CHFJPY',
            'NZDJPY','AUDCHF','CADCHF','NZDCHF','AUDNZD','NZDCAD','AUDCAD']

OPERACOES = np.array(
        [
            [
                1., # buy true #0
                1., # sell true #1
                0., # buy_price #2
                0., # sell_price #3
                0., # tp sell #4
                0., # sl sell #5
                0., # tp buy #6
                0., # sl buy #7
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
            [
                1., # buy true
                1., # sell true
                0., # buy_price
                0., # sell_price
                0., # tp sell
                0., # sl sell
                0., # tp buy
                0., # sl buy
            ],
        ], dtype=np.float64)

TRADE_HISTORY = [
        [],[],[],[],[],[],
        [],[],[],[],[],[],
        [],[],[],[],[],[],
        [],[],[],[],[],[],
        [],[],[],[]

]

STRINGS = np.array(
        [
            [1,0],
            [1,0],
            [1,0],
            [1,1],
            [1,0],
            [1,0],
            [1,0],
            [0,0],
            [0,0],
            [0,1],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,1],
            [0,0],
            [0,0],
            [0,0],
            [0,1],
            [0,1],
            [0,1],
            [0,1],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
        ], dtype=np.bool_
    )

def constantes(data):

    SERIES = np.array(
            [
                data[['EURUSD_Open','EURUSD_buy','EURUSD_sell','EURUSD_Open']].T,
                data[['EURCHF_Open','EURCHF_buy','EURCHF_sell','EURCHF_Open']].T,
                data[['EURGBP_Open','EURGBP_buy','EURGBP_sell','EURGBP_Open']].T,
                data[['EURJPY_Open','EURJPY_buy','EURJPY_sell','EURJPY_Open']].T,
                data[['EURNZD_Open','EURNZD_buy','EURNZD_sell','EURNZD_Open']].T,
                data[['EURAUD_Open','EURAUD_buy','EURAUD_sell','EURAUD_Open']].T,
                data[['EURCAD_Open','EURCAD_buy','EURCAD_sell','EURCAD_Open']].T,
                data[['GBPAUD_Open','GBPAUD_buy','GBPAUD_sell','EURGBP_Open']].T,
                data[['GBPCHF_Open','GBPCHF_buy','GBPCHF_sell','EURGBP_Open']].T,
                data[['GBPJPY_Open','GBPJPY_buy','GBPJPY_sell','EURGBP_Open']].T,
                data[['GBPCAD_Open','GBPCAD_buy','GBPCAD_sell','EURGBP_Open']].T,
                data[['GBPUSD_Open','GBPUSD_buy','GBPUSD_sell','EURGBP_Open']].T,
                data[['GBPNZD_Open','GBPNZD_buy','GBPNZD_sell','EURGBP_Open']].T,
                data[['USDCHF_Open','USDCHF_buy','USDCHF_sell','EURUSD_Open']].T,
                data[['USDJPY_Open','USDJPY_buy','USDJPY_sell','EURUSD_Open']].T,
                data[['AUDUSD_Open','AUDUSD_buy','AUDUSD_sell','EURAUD_Open']].T,
                data[['NZDUSD_Open','NZDUSD_buy','NZDUSD_sell','EURNZD_Open']].T,
                data[['USDCAD_Open','USDCAD_buy','USDCAD_sell','EURUSD_Open']].T,
                data[['AUDJPY_Open','AUDJPY_buy','AUDJPY_sell','EURAUD_Open']].T,
                data[['CADJPY_Open','CADJPY_buy','CADJPY_sell','EURCAD_Open']].T,
                data[['CHFJPY_Open','CHFJPY_buy','CHFJPY_sell','EURCHF_Open']].T,
                data[['NZDJPY_Open','NZDJPY_buy','NZDJPY_sell','EURNZD_Open']].T,
                data[['AUDCHF_Open','AUDCHF_buy','AUDCHF_sell','EURAUD_Open']].T,
                data[['CADCHF_Open','CADCHF_buy','CADCHF_sell','EURCAD_Open']].T,
                data[['NZDCHF_Open','NZDCHF_buy','NZDCHF_sell','EURNZD_Open']].T,
                data[['AUDNZD_Open','AUDNZD_buy','AUDNZD_sell','EURAUD_Open']].T,
                data[['NZDCAD_Open','NZDCAD_buy','NZDCAD_sell','EURNZD_Open']].T,
                data[['AUDCAD_Open','AUDCAD_buy','AUDCAD_sell','EURAUD_Open']].T,
            ], dtype=np.float64)

    return SERIES


@jit(nopython=True)
def otimizado(series, tksl=1, balance=1000):
    """
    Se single False e for um multi test
    Mudar o valor de tot, pois alem do tamanho das iterações
    tot será usado como TP e SL
    """

    check_eur_jpy = np.array(
            [
                [1,0],
                [1,0],
                [1,0],
                [1,1],
                [1,0],
                [1,0],
                [1,0],
                [0,0],
                [0,0],
                [0,1],
                [0,0],
                [0,0],
                [0,0],
                [0,0],
                [0,1],
                [0,0],
                [0,0],
                [0,0],
                [0,1],
                [0,1],
                [0,1],
                [0,1],
                [0,0],
                [0,0],
                [0,0],
                [0,0],
                [0,0],
                [0,0],
            ], dtype=np.bool_
        )
    operacoes = np.zeros((28,6),dtype=np.float32)
    buy_sell = np.ones((28,2),dtype=np.bool_)
    #history = TRADE_HISTORY

    buy_orders = []
    sell_orders = []

    balance_backtest = balance
    list_backtest = [balance_backtest]

    flag_jpy_buy, flag_jpy_sell = False, False
    flag_normal_buy, flag_normal_sell = False, False

    tk_normal, sl_normal, tk_jpy, sl_jpy = 0, 0, 0, 0

    # Talvez arrumar? Esta muito feio

    tk_normal = tksl / 10000
    sl_normal = tksl / 20000
    tk_jpy = tksl / 100
    sl_jpy = tksl / 200

    for i in range(series[0][0].size): # 63k

        buy_result = 0
        sell_result = 0

        for h in range(len(series)): # 28

            if series[h][1][i] and buy_sell[h][0]:
                operacoes[h][2] = series[h][0][i]
                buy_sell[h][0] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][6] = series[h][0][i] + tk_jpy
                    operacoes[h][7] = series[h][0][i] - sl_jpy
                else:
                    operacoes[h][6] = series[h][0][i] + tk_normal
                    operacoes[h][7] = series[h][0][i] - sl_normal
            if buy_sell[h][0] == False and series[h][0][i] >= operacoes[h][6]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][6],
                                                                   saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                buy_orders.append(buy_result)
                buy_sell[h][0] = True
            elif buy_sell[h][0] == False and series[h][0][i] <= operacoes[h][7]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][7],
                                                                   saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                buy_orders.append(buy_result)
                buy_sell[h][0] = True

            if series[h][2][i] and buy_sell[h][1]:
                operacoes[h][3] = series[h][0][i]
                buy_sell[h][1] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][4] = series[h][0][i] - tk_jpy
                    operacoes[h][5] = series[h][0][i] + sl_jpy
                else:
                    operacoes[h][4] = series[h][0][i] - tk_normal
                    operacoes[h][5] = series[h][0][i] + sl_normal

            if buy_sell[h][1] == False and series[h][0][i] <= operacoes[h][4]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][3],
                                                                    saldo_final=operacoes[h][4], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                sell_orders.append(sell_result)
                buy_sell[h][1] = True
            elif buy_sell[h][1] == False and series[h][0][i] >= operacoes[h][5]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[h][3],
                                                                    saldo_final=operacoes[h][5], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                sell_orders.append(sell_result)
                buy_sell[h][1] = True

    return list_backtest, sell_orders, buy_orders


@jit(nopython=True)
def best_f(diff_array):
    """
    diff_array: A diferença do capital .diff()
    do pandas, com o dropna()
    O maior valor é o optimal f
    Return: optimal f
    """
    max_loss = diff_array.min()
    results = []
    for j in np.arange(0.01,0.2,0.01):
        calc = []
        my_result = 1
        for i in diff_array:
            calc.append(1+j*(-i/max_loss))
        for k in calc:
            my_result *= k
        results.append(sqrt(my_result))
    x = np.array(results)
    return (np.where(x == x.max())[0][0]+1)/100


@jit(nopython=True)
def finance_calculation(balance, saldo_inicial, saldo_final, preco_eur, eur):

    initial_balance = 1000

    lot = initial_balance

    calc = balance - initial_balance

    #if balance > initial_balance:
        #lot = (balance + (calc * 0.025)) // 1000 * 1000

    comission = (lot//1000) * 0.1

    if eur:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = round(tot - comission,2)
        return (tot2 + balance), tot2
    else:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = round(tot / saldo_final / preco_eur - comission,2)
        return (tot2 + balance), tot2


def pip_calculation(pip_balance,preco_inicial, preco_final):
    pip = preco_inicial - preco_final
    return pip + pip_balance


def pct_backtest(series, tksl=1, balance=1000, single=True, tot=1, init_tp=5):
    """
    Se single False e for um multi test
    Mudar o valor de tot, pois alem do tamanho das iterações
    tot será usado como TP e SL
    """

    balance_bests_results = pd.DataFrame()
    best_tksl = deque()

    check_eur_jpy = STRINGS

    x = 0
    if single:
        x = np.arange(1,2)
    else:
        x = np.arange(init_tp, tot)

    for j in x:

        if not single:
            clear_output(wait=True)
            print(f'{j}/{tot-1}')

        operacoes = OPERACOES
        history = TRADE_HISTORY

        buy_orders = deque()
        sell_orders = deque()

        balance_backtest = balance
        list_backtest = deque([balance_backtest])

        flag_jpy_buy, flag_jpy_sell = False, False
        flag_normal_buy, flag_normal_sell = False, False

        tk_normal, sl_normal, tk_jpy, sl_jpy = 0, 0, 0, 0

        # Talvez arrumar? Esta muito feio
        if single:
            tk_normal = tksl / 10000
            sl_normal = tksl / 20000
            tk_jpy = tksl / 100
            sl_jpy = tksl / 200
        else:
            tk_normal = j / 10000
            sl_normal = j / 20000
            tk_jpy = j / 100
            sl_jpy = j / 200

        for i in range(len(series[0][0])): # 63k

            buy_result = 0
            sell_result = 0

            for h in range(len(series)): # 28

                if series[h][1][i] and buy_sell[h][0]:
                    operacoes[h][2] = series[h][0][i]
                    buy_sell[h][0] = False
                    if check_eur_jpy[h][1]:
                        operacoes[h][6] = series[h][0][i] + tk_jpy
                        operacoes[h][7] = series[h][0][i] - sl_jpy
                    else:
                        operacoes[h][6] = series[h][0][i] + tk_normal
                        operacoes[h][7] = series[h][0][i] - sl_normal
                if buy_sell[h][0] == False and series[h][0][i] >= operacoes[h][6]:
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][6],
                                                                       saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                       preco_eur=series[h][3][i])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(buy_result)
                    history[h].append(buy_result)
                    buy_sell[h][0] = True
                elif buy_sell[h][0] == False and series[h][0][i] <= operacoes[h][7]:
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][7],
                                                                       saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                       preco_eur=series[h][3][i])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(buy_result)
                    history[h].append(buy_result)
                    buy_sell[h][0] = True

                if series[h][2][i] and buy_sell[h][1]:
                    operacoes[h][3] = series[h][0][i]
                    buy_sell[h][1] = False
                    if check_eur_jpy[h][1]:
                        operacoes[h][4] = series[h][0][i] - tk_jpy
                        operacoes[h][5] = series[h][0][i] + sl_jpy
                    else:
                        operacoes[h][4] = series[h][0][i] - tk_normal
                        operacoes[h][5] = series[h][0][i] + sl_normal

                if buy_sell[h][1] == False and series[h][0][i] <= operacoes[h][4]:
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][3],
                                                                        saldo_final=operacoes[h][4], eur = check_eur_jpy[h][0],
                                                                        preco_eur=series[h][3][i])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(sell_result)
                    history[h].append(sell_result)
                    buy_sell[h][1] = True
                elif buy_sell[h][1] == False and series[h][0][i] >= operacoes[h][5]:
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[h][3],
                                                                        saldo_final=operacoes[h][5], eur = check_eur_jpy[h][0],
                                                                        preco_eur=series[h][3][i])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(sell_result)
                    history[h].append(sell_result)
                    buy_sell[h][1] = True

        if single:
            balance_bests_results['result'] = pd.Series(list_backtest)
            balance_bests_results['buy'] = pd.Series(buy_orders)
            balance_bests_results['sell'] = pd.Series(sell_orders)
            for h in range(len(history)):
                 balance_bests_results[SYMBOLS[h]] = pd.Series(history[h])
            return balance_bests_results
        else:
            if balance_backtest > balance:
                balance_bests_results[f'TPSL:{j}'] = pd.Series(list_backtest)
                balance_bests_results[j] = pd.Series(list_backtest)
                best_tksl.append(j)

    balance_bests_results['best_tksl'] = pd.Series(best_tksl)
    return balance_bests_results


def pct_backtest_without_tpsl(data, risco=0.01, balance=1000):

    balance_bests_results = pd.DataFrame()
    best_tksl = []

    buy_orders = []
    sell_orders = []

    balance_backtest = balance
    list_backtest = [balance_backtest]

    flag_jpy_buy, flag_jpy_sell = False, False
    flag_normal_buy, flag_normal_sell = False, False

    my_events = EVENTS

    for i in range(len(data)):

        clear_output(wait=True)
        print(f'{i}/{len(data)-1}')

        buy_result = 0
        sell_result = 0

        for h in my_events.values():

            if data[h['flag_buy']].iloc[i] and h['buy']:
                if not h['sell']:
                    h['buy_price'] = data[h['symbol']].iloc[i]
                    h['buy'] = False
                    h['sell'] = True
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,  risk=risco, saldo_inicial=h['sell_price'],
                                                                        saldo_final=data[h['symbol']].iloc[i], eur=True if h['first_currency'] == 'eur' else False,
                                                                        preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    sell_orders.append(sell_result)
                    h['trade_history'].append(sell_result)
                else:
                    h['buy_price'] = data[h['symbol']].iloc[i]
                    h['buy'] = False

            if data[h['flag_sell']].iloc[i] and h['sell']:
                if not h['buy']:
                    h['sell_price'] = data[h['symbol']].iloc[i]
                    h['sell'] = False
                    h['buy'] = True
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest,  risk=risco, saldo_inicial=data[h['symbol']].iloc[i],
                                                                       saldo_final=h['buy_price'], eur=True if h['first_currency'] == 'eur' else False,
                                                                       preco_eur=data[h['preco_euro']].iloc[i], jpy=h['second_currency'])
                    list_backtest.append(balance_backtest)
                    buy_orders.append(buy_result)
                    h['trade_history'].append(buy_result)
                else:
                    h['sell_price'] = data[h['symbol']].iloc[i]
                    h['sell'] = False


    balance_bests_results['result'] = pd.Series(list_backtest)
    balance_bests_results['buy'] = pd.Series(buy_orders)
    balance_bests_results['sell'] = pd.Series(sell_orders)
    for h in my_events:
        balance_bests_results[my_events[h]['symbol']] = pd.Series(my_events[h]['trade_history'])

    return balance_bests_results


def walk_forward_test(walk1, test1, walk2, test2, walk3, test3, walk4, test4, walk5, test5, final, tot_iterations, plot=False):

    test_walk1 = pct_backtest(walk1, single=False, tot=tot_iterations)

    walk1_test1_test = pd.DataFrame()
    for i in range(len(test_walk1.iloc[:,-1].dropna())):
        clear_output(wait=True)
        print(f'Teste 1: {i}/{len(test_walk1.iloc[:,-1].dropna())}')
        result_test1 = pct_backtest(test1, tksl=test_walk1['best_tksl'].iloc[i])
        walk1_test1_test[f"{test_walk1['best_tksl'].iloc[i]}"] = result_test1['result']

    test_walk2 = pct_backtest(walk2, single=False, tot=tot_iterations)

    walk2_test2_test = pd.DataFrame()
    for i in range(len(test_walk2.iloc[:,-1].dropna())):
        clear_output(wait=True)
        print(f'Teste 2: {i}/{len(test_walk2.iloc[:,-1].dropna())}')
        result_test2 = pct_backtest(test2, tksl=test_walk2['best_tksl'].iloc[i])
        walk2_test2_test[f"{test_walk2['best_tksl'].iloc[i]}"] = result_test2['result']

    test_walk3 = pct_backtest(walk3, single=False, tot=tot_iterations)

    walk3_test3_test = pd.DataFrame()
    for i in range(len(test_walk3.iloc[:,-1].dropna())):
        clear_output(wait=True)
        print(f'Teste 3: {i}/{len(test_walk3.iloc[:,-1].dropna())}')
        result_test3 = pct_backtest(test3, tksl=test_walk3['best_tksl'].iloc[i])
        walk3_test3_test[f"{test_walk3['best_tksl'].iloc[i]}"] = result_test3['result']

    test_walk4 = pct_backtest(walk4, single=False, tot=tot_iterations)

    walk4_test4_test = pd.DataFrame()
    for i in range(len(test_walk4.iloc[:,-1].dropna())):
        clear_output(wait=True)
        print(f'Teste 4: {i}/{len(test_walk4.iloc[:,-1].dropna())}')
        result_test4 = pct_backtest(test4, tksl=test_walk4['best_tksl'].iloc[i])
        walk4_test4_test[f"{test_walk4['best_tksl'].iloc[i]}"] = result_test4['result']

    test_walk5 = pct_backtest(walk5, single=False, tot=tot_iterations)

    walk5_test5_test = pd.DataFrame()
    for i in range(len(test_walk5.iloc[:,-1].dropna())):
        clear_output(wait=True)
        print(f'Teste 5: {i}/{len(test_walk5.iloc[:,-1].dropna())}')
        result_test5 = pct_backtest(test5, tksl=test_walk5['best_tksl'].iloc[i])
        walk5_test5_test[f"{test_walk5['best_tksl'].iloc[i]}"] = result_test5['result']

    x = af.compare(walk5_test5_test, walk4_test4_test, walk3_test3_test, walk2_test2_test, walk1_test1_test)
    test_final = pd.DataFrame()
    for i in range(len(x)):
        clear_output(wait=True)
        print(f'Final: {i}/{len(x)-1}')
        final_result = pct_backtest(test5, tksl=x[i])
        test_final[f"{x[i]}"] = final_result['result']

    if plot:
        try:
            test_walk1.iloc[:,:-1].plot()
            plt.title('Teste Walk 1', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            walk1_test1_test.plot()
            plt.title('Teste 1', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            test_walk2.iloc[:,:-1].plot()
            plt.title('Teste Walk 2', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            walk2_test2_test.plot()
            plt.title('Teste 2', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            test_walk3.iloc[:,:-1].plot()
            plt.title('Teste Walk 3', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            walk3_test3_test.plot()
            plt.title('Teste 3', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            test_walk4.iloc[:,:-1].plot()
            plt.title('Teste Walk 4', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            walk4_test4_test.plot()
            plt.title('Teste 4', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            test_walk5.iloc[:,:-1].plot()
            plt.title('Teste Walk 5', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            walk5_test5_test.plot()
            plt.title('Teste 5', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

        try:
            test_final.plot()
            plt.title('Final', fontsize=30)
            plt.grid()
        except TypeError:
            print('No data to plot.')

    return list(test_final.columns)
