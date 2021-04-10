import numpy as np
from numba import njit
from math import sqrt


@njit
def best_f(diff_array):
    """
    diff_array: A diferença do capital .diff()
    do pandas, com o dropna()
    O maior valor é o optimal f
    Return: optimal f
    """
    max_loss = diff_array.min()
    results = []
    for j in np.arange(0.00,1,0.01):
        calc = []
        my_result = 1
        for i in diff_array:
            calc.append(1+j*(-i/max_loss))
        for k in calc:
            my_result *= k
        results.append(sqrt(my_result))
    x = np.array(results)
    retburn (np.where(x == x.max())[0][0])/100, x


@njit
def finance_calculation(balance, saldo_inicial, saldo_final, preco_eur, eur):

    #initial_balance = 1000

    lot = 1000

    #calc = balance - initial_balance
    #if balance > initial_balance:
    #    lot = (balance + (calc * 0.99)) // 1000 * 1000

    comission = (lot//1000) * 0.07

    if eur:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = round(tot - comission,2)
        return (tot2 + balance), tot2
    else:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = round(tot / saldo_final / preco_eur - comission,2)
        return (tot2 + balance), tot2


@njit
def otimizado_tpsl(series, tpsl, balance=1000):
    """
    buy_sell: 0 = Compra
              1 = Venda
    operacoes: 0 = Preço de Compra
               1 = Preço de Venda
               2 = TP Venda
               3 = SL Venda
               4 = TP Compra
               5 = SL Compra
    check_eur_jpy: 0 = eur
                   1 = jpy
    """

    each_pair_index = np.zeros((28,1), dtype='int32')

    each_pair = np.zeros((28,50_000), dtype='float64')

    check_eur_jpy = np.array([
                        [1, 0],[1, 0],[1, 1],[1, 0],[1, 0],[1, 0],[1, 0],
                        [0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 1],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]
                        ], dtype=np.bool_)

    operacoes = np.zeros((28,6),dtype='float64')
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_ind, sell_ind, list_backtest_indi = 0, 0, 1

    buy_orders = np.zeros((500_000), dtype='float64')
    sell_orders = np.zeros((500_000), dtype='float64')

    balance_backtest = balance
    list_backtest = np.zeros((1_000_000), dtype='float64')
    list_backtest[0] = balance_backtest

    tk_normal = tpsl / 10000
    sl_normal = tpsl / 20000
    tk_jpy = tpsl / 100
    sl_jpy = tpsl / 200

    for i in range(series[0][0].size): # 63k

        buy_result = 0
        sell_result = 0

        for h in range(len(series)): # 28


            if series[h][1][i] and buy_sell[h][0]:
                operacoes[h][0] = series[h][0][i]
                buy_sell[h][0] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][4] = series[h][0][i] + tk_jpy
                    operacoes[h][5] = series[h][0][i] - sl_jpy
                else:
                    operacoes[h][4] = series[h][0][i] + tk_normal
                    operacoes[h][5] = series[h][0][i] - sl_normal

            if buy_sell[h][0] == False and series[h][0][i] <= operacoes[h][5]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                   saldo_inicial=operacoes[h][5],
                                                                   saldo_final=operacoes[h][0],
                                                                   eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                buy_orders[buy_ind] = buy_result
                each_pair[h][each_pair_index[h]] = buy_result
                each_pair_index[h] += 1
                buy_sell[h][0] = True
                list_backtest_indi += 1
                buy_ind += 1
            elif buy_sell[h][0] == False and series[h][0][i] >= operacoes[h][4]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                   saldo_inicial=operacoes[h][4],
                                                                   saldo_final=operacoes[h][0],
                                                                   eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                buy_orders[buy_ind] = buy_result
                each_pair[h][each_pair_index[h]] = buy_result
                each_pair_index[h] += 1
                buy_sell[h][0] = True
                list_backtest_indi += 1
                buy_ind += 1

            if series[h][2][i] and buy_sell[h][1]:
                operacoes[h][1] = series[h][0][i]
                buy_sell[h][1] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][2] = series[h][0][i] - tk_jpy
                    operacoes[h][3] = series[h][0][i] + sl_jpy
                else:
                    operacoes[h][2] = series[h][0][i] - tk_normal
                    operacoes[h][3] = series[h][0][i] + sl_normal

            if buy_sell[h][1] == False and series[h][0][i] >= operacoes[h][3]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                    saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][3],
                                                                    eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                sell_orders[sell_ind] = sell_result
                each_pair[h][each_pair_index[h]] = sell_result
                each_pair_index[h] += 1
                buy_sell[h][1] = True
                list_backtest_indi += 1
                sell_ind += 1
            elif buy_sell[h][1] == False and series[h][0][i] <= operacoes[h][2]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                    saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][2],
                                                                    eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                sell_orders[sell_ind] = sell_result
                each_pair[h][each_pair_index[h]] = sell_result
                each_pair_index[h] += 1
                buy_sell[h][1] = True
                list_backtest_indi += 1
                sell_ind += 1

    return list_backtest, sell_orders, buy_orders, each_pair


@njit
def otimizado_no_tpsl(series, balance=1000):
    """
    buy_sell: 0 = Compra
              1 = Venda
    operacoes: 0 = Preço de Compra
               1 = Preço de Venda
    check_eur_jpy: 0 = eur
                   1 = jpy
    """

    check_eur_jpy = np.array([
                        [1, 0],[1, 0],[1, 1],[1, 0],[1, 0],[1, 0],[1, 0],
                        [0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 1],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]
                        ], dtype=np.bool_)

    operacoes = np.zeros((28,2),dtype='float64')
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_ind, sell_ind, list_backtest_indi = 0, 0, 1

    buy_orders = np.zeros((500_000), dtype='float64')
    sell_orders = np.zeros((500_000), dtype='float64')

    balance_backtest = balance
    list_backtest = np.zeros((1_000_000), dtype='float64')
    list_backtest[0] = balance_backtest

    for i in range(series[0][0].size): # 63k

        buy_result = 0
        sell_result = 0

        for h in range(len(series)): #28

            if series[h][1][i] and buy_sell[h][0]:
                if not buy_sell[h][1]:
                    operacoes[h][0] = series[h][0][i]
                    buy_sell[h][0] = False
                    buy_sell[h][1] = True
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                        saldo_inicial=operacoes[h][1],
                                                                        saldo_final=series[h][0][i],
                                                                        eur=check_eur_jpy[h][0],
                                                                        preco_eur=series[h][3][i])
                    list_backtest[list_backtest_indi] = balance_backtest
                    sell_orders[sell_ind] = sell_result
                    sell_ind += 1
                    list_backtest_indi += 1
                else:
                    operacoes[h][0] = series[h][0][i]
                    buy_sell[h][0] = False

            if series[h][2][i] and buy_sell[h][1]:
                if not buy_sell[h][0]:
                    operacoes[h][1] = series[h][0][i]
                    buy_sell[h][1] = False
                    buy_sell[h][0] = True
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                       saldo_inicial=series[h][0][i],
                                                                       saldo_final=operacoes[h][0],
                                                                       eur=check_eur_jpy[h][0],
                                                                       preco_eur=series[h][3][i])
                    list_backtest[list_backtest_indi] = balance_backtest
                    buy_orders[buy_ind] = buy_result
                    buy_ind += 1
                    list_backtest_indi += 1
                else:
                    operacoes[h][1] = series[h][0][i]
                    buy_sell[h][1] = False

    return list_backtest, sell_orders, buy_orders


@njit
def otimizado_tpsl_ohl(series, tpsl, balance=1000):
    """
    buy_sell: 0 = Compra
              1 = Venda
    operacoes: 0 = Preço de Compra
               1 = Preço de Venda
               2 = TP Venda
               3 = SL Venda
               4 = TP Compra
               5 = SL Compra
    check_eur_jpy: 0 = eur
                   1 = jpy
    """

    check_eur_jpy = np.array([
                        [1, 0],[1, 0],[1, 1],[1, 0],[1, 0],[1, 0],[1, 0],
                        [0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 1],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]
                        ], dtype=np.bool_)

    operacoes = np.zeros((28,6),dtype='float64')
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_ind, sell_ind, list_backtest_indi = 0, 0, 1

    buy_orders = np.zeros((500_000), dtype='float64')
    sell_orders = np.zeros((500_000), dtype='float64')

    balance_backtest = balance
    list_backtest = np.zeros((1_000_000), dtype='float64')
    list_backtest[0] = balance_backtest

    tk_normal = tpsl / 10000
    sl_normal = tpsl / 20000
    tk_jpy = tpsl / 100
    sl_jpy = tpsl / 200

    for i in range(series[0][0].size): # 63k

        buy_result = 0
        sell_result = 0

        for h in range(len(series)): # 28

            if series[h][1][i] and buy_sell[h][0]:
                operacoes[h][0] = series[h][0][i]
                buy_sell[h][0] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][4] = series[h][0][i] + tk_jpy
                    operacoes[h][5] = series[h][0][i] - sl_jpy
                else:
                    operacoes[h][4] = series[h][0][i] + tk_normal
                    operacoes[h][5] = series[h][0][i] - sl_normal

            if buy_sell[h][0] == False and (series[h][0][i] >= operacoes[h][4] or series[h][4][i] >= operacoes[h][4]):
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][4],
                                                                   saldo_final=operacoes[h][0], eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                buy_orders[buy_ind] = buy_result
                buy_sell[h][0] = True
                list_backtest_indi += 1
                buy_ind += 1
            elif buy_sell[h][0] == False and (series[h][0][i] <= operacoes[h][5] or series[h][5][i] <= operacoes[h][5]):
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][5],
                                                                   saldo_final=operacoes[h][0], eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                buy_orders[buy_ind] = buy_result
                buy_sell[h][0] = True
                list_backtest_indi += 1
                buy_ind += 1

            if series[h][2][i] and buy_sell[h][1]:
                operacoes[h][1] = series[h][0][i]
                buy_sell[h][1] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][2] = series[h][0][i] - tk_jpy
                    operacoes[h][3] = series[h][0][i] + sl_jpy
                else:
                    operacoes[h][2] = series[h][0][i] - tk_normal
                    operacoes[h][3] = series[h][0][i] + sl_normal

            if buy_sell[h][1] == False and (series[h][0][i] <= operacoes[h][2] or series[h][5][i] <= operacoes[h][2]):
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                sell_orders[sell_ind] = sell_result
                buy_sell[h][1] = True
                list_backtest_indi += 1
                sell_ind += 1
            elif buy_sell[h][1] == False and (series[h][0][i] >= operacoes[h][3] or series[h][4][i] >= operacoes[h][3]):
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][3], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                sell_orders[sell_ind] = sell_result
                buy_sell[h][1] = True
                list_backtest_indi += 1
                sell_ind += 1

    return list_backtest, sell_orders, buy_orders


@njit
def single_backtest(series, tpsl, balance=1000):
    """
    Apenas EUR por enquanto
    """
    operacoes = np.array([1.,1.,0.,0.,0.,0.,0.,0.])

    buy_ind, sell_ind, list_backtest_indi = 0, 0, 1

    buy_orders = np.zeros((100_000), dtype='float64')
    sell_orders = np.zeros((100_000), dtype='float64')

    balance_backtest = balance
    list_backtest = np.zeros((200_000), dtype='float64')
    list_backtest[0] = balance_backtest

    tk_normal = tpsl / 10000
    sl_normal = tpsl / 20000

    for i in range(len(series[0])): # 63k

        buy_result = 0
        sell_result = 0

        if series[1][i] and operacoes[0]:
            operacoes[2] = series[0][i]
            operacoes[0] = False
            operacoes[6] = series[0][i] + tk_normal
            operacoes[7] = series[0][i] - sl_normal

        if operacoes[0] == False and series[0][i] >= operacoes[6]:
            balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[6],
                                                                saldo_final=operacoes[2], preco_eur=0, eur=True)
            list_backtest[list_backtest_indi] = balance_backtest
            buy_orders[buy_ind] = buy_result
            operacoes[0] = True
            list_backtest_indi += 1
            buy_ind += 1
        elif operacoes[0] == False and series[0][i] <= operacoes[7]:
            balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[7],
                                                                saldo_final=operacoes[2], preco_eur=0, eur=True)
            list_backtest[list_backtest_indi] = balance_backtest
            buy_orders[buy_ind] = buy_result
            operacoes[0] = True
            list_backtest_indi += 1
            buy_ind += 1

        if series[2][i] and operacoes[1]:
            operacoes[3] = series[0][i]
            operacoes[1] = False
            operacoes[4] = series[0][i] - tk_normal
            operacoes[5] = series[0][i] + sl_normal

        if operacoes[1] == False and series[0][i] <= operacoes[4]:
            balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[3],
                                                                saldo_final=operacoes[4], preco_eur=0, eur=True)
            list_backtest[list_backtest_indi] = balance_backtest
            sell_orders[sell_ind] = sell_result
            operacoes[1] = True
            list_backtest_indi += 1
            sell_ind += 1
        elif operacoes[1] == False and series[0][i] >= operacoes[5]:
            balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[3],
                                                                saldo_final=operacoes[5], preco_eur=0, eur=True)
            list_backtest[list_backtest_indi] = balance_backtest
            sell_orders[sell_ind] = sell_result
            operacoes[1] = True
            list_backtest_indi += 1
            sell_ind += 1

    return list_backtest, buy_orders, sell_orders
