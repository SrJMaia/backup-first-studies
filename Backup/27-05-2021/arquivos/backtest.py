import numpy as np
from numba import njit

@njit(fastmath=True)
def finance_calculation(balance, saldo_inicial, saldo_final, preco_eur, eur):

    initial_balance = 1000
    lot = 1000

    #if balance > (3*initial_balance):
    #    lot = (balance - initial_balance) // 1000 * 1000

    comission = (lot//1000) * 0.07
    overnight = (lot//1000) * 0.1
    # random entre -2 a 2 pips para simular slippage

    if eur:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = tot - comission
        return (tot2 + balance), tot2
    else:
        tot = (lot * (saldo_inicial - saldo_final)) / saldo_final
        tot2 = tot / saldo_final / preco_eur - comission
        return (tot2 + balance), tot2


@njit(parallel=True)
def otimizado_tpsl(series, multiply_tp, multiply_sl, balance=1000):
    """
    tpsl = TakeProfit e StopLoss int > 0
    multiply_tpsl = float > 0
                    Será o valor que irá dividir SL
                    Se 1 significa risco 1:1, se 2, 2:1 and so on
    ---
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

    balance_backtest = balance

    check_eur_jpy = np.array([
                        [1, 0],[1, 0],[1, 1],[1, 0],[1, 0],[1, 0],[1, 0],
                        [0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 1],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]
                        ], dtype=np.bool_)

    operacoes = np.zeros((28,6),dtype=np.float32)
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_sell_list_indi = np.zeros(3, dtype=np.int32)

    buy_orders = np.zeros((2_000_000), dtype=np.float32)
    sell_orders = np.zeros((2_000_000), dtype=np.float32)
    buy_orders[0] = balance_backtest
    sell_orders[0] = balance_backtest
    buy_sell_list_indi[0] += 1
    buy_sell_list_indi[1] += 1

    each_pair_index = np.zeros((28), dtype=np.int32)
    each_pair = np.zeros((28,100_000), dtype=np.float32)
    for i in range(28):
        each_pair[i][each_pair_index[i]] = balance_backtest
        each_pair_index[i] += 1

    list_backtest = np.zeros((2_000_000), dtype=np.float32)
    list_backtest[0] = balance_backtest
    buy_sell_list_indi[2] += 1

    #tk_normal = round(tpsl / 10000,5)
    #sl_normal = round(tpsl / 10000 / multiply_tpsl, 5)
    #tk_jpy = round(tpsl / 100)
    #sl_jpy = round(tpsl / 100 / multiply_tpsl,5)

    for i in range(series[0][0].size): # 63k

        buy_result = 0
        sell_result = 0

        for h in range(len(series)): # 28


            if series[h][1][i] and buy_sell[h][0]:
                operacoes[h][0] = series[h][0][i]
                buy_sell[h][0] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][4] = series[h][0][i] + round(multiply_tp * series[h][5][i],3) # TP
                    #operacoes[h][4] = series[h][0][i] + tk_jpy
                    operacoes[h][5] = series[h][0][i] - round(multiply_sl * series[h][5][i],3) # SL
                    #operacoes[h][5] = series[h][0][i] - sl_jpy
                else:
                    operacoes[h][4] = series[h][0][i] + round(multiply_tp * series[h][5][i],5) # TP
                    #operacoes[h][4] = series[h][0][i] + tk_normal
                    operacoes[h][5] = series[h][0][i] - round(multiply_sl * series[h][5][i],5) # SL
                    #operacoes[h][5] = series[h][0][i] - sl_normal

            if buy_sell[h][0] == False and series[h][0][i] <= operacoes[h][5]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                   saldo_inicial=operacoes[h][5],
                                                                   saldo_final=operacoes[h][0],
                                                                   eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest[buy_sell_list_indi[2]] = balance_backtest
                buy_orders[buy_sell_list_indi[0]] = buy_orders[buy_sell_list_indi[0]-1] + buy_result
                each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + buy_result
                each_pair_index[h] += 1
                buy_sell[h][0] = True
                buy_sell_list_indi[2] += 1
                buy_sell_list_indi[0] += 1
            elif buy_sell[h][0] == False and series[h][0][i] >= operacoes[h][4]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest,
                                                                   saldo_inicial=operacoes[h][4],
                                                                   saldo_final=operacoes[h][0],
                                                                   eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest[buy_sell_list_indi[2]] = balance_backtest
                buy_orders[buy_sell_list_indi[0]] = buy_orders[buy_sell_list_indi[0]-1] + buy_result
                each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + buy_result
                each_pair_index[h] += 1
                buy_sell[h][0] = True
                buy_sell_list_indi[2] += 1
                buy_sell_list_indi[0] += 1

            if series[h][2][i] and buy_sell[h][1]:
                operacoes[h][1] = series[h][0][i]
                buy_sell[h][1] = False
                if check_eur_jpy[h][1]:
                    operacoes[h][2] = series[h][0][i] - round(multiply_tp * series[h][5][i],3) # TP
                    #operacoes[h][2] = series[h][0][i] - tk_jpy
                    operacoes[h][3] = series[h][0][i] + round(multiply_sl * series[h][5][i],3) # SL
                    #operacoes[h][3] = series[h][0][i] + sl_jpy
                else:
                    operacoes[h][2] = series[h][0][i] - round(multiply_tp * series[h][5][i],5) # TP
                    #operacoes[h][2] = series[h][0][i] - tk_normal
                    operacoes[h][3] = series[h][0][i] + round(multiply_sl * series[h][5][i],5) # SL
                    #operacoes[h][3] = series[h][0][i] + sl_normal

            if buy_sell[h][1] == False and series[h][0][i] >= operacoes[h][3]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                    saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][3],
                                                                    eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[buy_sell_list_indi[2]] = balance_backtest
                sell_orders[buy_sell_list_indi[1]] = sell_orders[buy_sell_list_indi[1]-1] + sell_result
                each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + sell_result
                each_pair_index[h] += 1
                buy_sell[h][1] = True
                buy_sell_list_indi[2] += 1
                buy_sell_list_indi[1] += 1
            elif buy_sell[h][1] == False and series[h][0][i] <= operacoes[h][2]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,
                                                                    saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][2],
                                                                    eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[buy_sell_list_indi[2]] = balance_backtest
                sell_orders[buy_sell_list_indi[1]] = sell_orders[buy_sell_list_indi[1]-1] + sell_result
                each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + sell_result
                each_pair_index[h] += 1
                buy_sell[h][1] = True
                buy_sell_list_indi[2] += 1
                buy_sell_list_indi[1] += 1

    return list_backtest, sell_orders, buy_orders, each_pair


@njit(parallel=True)
def otimizado_no_tpsl(series, balance=1000):
    """
    buy_sell: 0 = Compra
              1 = Venda
    operacoes: 0 = Preço de Compra
               1 = Preço de Venda
    check_eur_jpy: 0 = eur
                   1 = jpy
    """

    balance_backtest = balance

    check_eur_jpy = np.array([
                        [1, 0],[1, 0],[1, 1],[1, 0],[1, 0],[1, 0],[1, 0],
                        [0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 1],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]
                        ], dtype=np.bool_)

    operacoes = np.zeros((28,6),dtype=np.float32)
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_sell_list_indi = np.zeros(3, dtype=np.int32)

    buy_orders = np.zeros((2_000_000), dtype=np.float32)
    sell_orders = np.zeros((2_000_000), dtype=np.float32)
    buy_orders[0] = balance_backtest
    sell_orders[0] = balance_backtest
    buy_sell_list_indi[0] += 1
    buy_sell_list_indi[1] += 1

    each_pair_index = np.zeros((28), dtype=np.int32)
    each_pair = np.zeros((28,100_000), dtype=np.float32)
    for i in range(28):
        each_pair[i][each_pair_index[i]] = balance_backtest
        each_pair_index[i] += 1

    list_backtest = np.zeros((2_000_000), dtype=np.float32)
    list_backtest[0] = balance_backtest
    buy_sell_list_indi[2] += 1

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
                    list_backtest[buy_sell_list_indi[2]] = balance_backtest
                    sell_orders[buy_sell_list_indi[1]] = sell_orders[buy_sell_list_indi[1]-1] + sell_result
                    each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + sell_result
                    each_pair_index[h] += 1
                    buy_sell_list_indi[1] += 1
                    buy_sell_list_indi[2] += 1
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
                    list_backtest[buy_sell_list_indi[2]] = balance_backtest
                    buy_orders[buy_sell_list_indi[0]] = buy_orders[buy_sell_list_indi[0]-1] + buy_result
                    each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + buy_result
                    each_pair_index[h] += 1
                    buy_sell_list_indi[0] += 1
                    buy_sell_list_indi[2] += 1
                else:
                    operacoes[h][1] = series[h][0][i]
                    buy_sell[h][1] = False

    return list_backtest, sell_orders, buy_orders, each_pair


@njit(parallel=True)
def big_backtest_otimizado_tpsl(series, m1, multiply_tp, multiply_sl, balance=1000):
    """
    tpsl = TakeProfit e StopLoss int > 0
    multiply_tpsl = float > 0
                    Será o valor que irá dividir SL
                    Se 1 significa risco 1:1, se 2, 2:1 and so on
    ---
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

    balance_backtest = balance

    check_eur_jpy = np.array([
                        [1, 0],[1, 0],[1, 1],[1, 0],[1, 0],[1, 0],[1, 0],
                        [0, 0],[0, 0],[0, 1],[0, 0],[0, 0],[0, 0],[0, 0],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 1],[0, 1],[0, 1],
                        [0, 1],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0],[0, 0]
                        ], dtype=np.bool_)

    operacoes = np.zeros((28,6),dtype=np.float32)
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_sell_list_indi = np.zeros(3, dtype=np.int32)

    buy_orders = np.zeros((2_000_000), dtype=np.float32)
    sell_orders = np.zeros((2_000_000), dtype=np.float32)
    buy_orders[0] = balance_backtest
    sell_orders[0] = balance_backtest
    buy_sell_list_indi[0] += 1
    buy_sell_list_indi[1] += 1

    each_pair_index = np.zeros((28), dtype=np.int32)
    each_pair = np.zeros((28,100_000), dtype=np.float32)
    for i in range(28):
        each_pair[i][each_pair_index[i]] = balance_backtest
        each_pair_index[i] += 1

    list_backtest = np.zeros((2_000_000), dtype=np.float32)
    list_backtest[0] = balance_backtest
    buy_sell_list_indi[2] += 1

    #tk_normal = round(tpsl / 10000,5)
    #sl_normal = round(tpsl / 10000 / multiply_tpsl, 5)
    #tk_jpy = round(tpsl / 100)
    #sl_jpy = round(tpsl / 100 / multiply_tpsl,5)

    for i in range(series[0][0].size): # 63k

        buy_result = 0
        sell_result = 0

        for h in range(len(series)): # 28

            for super in np.arange(m1[h][0][i].size): # Big backtest

                if series[h][1][i] and buy_sell[h][0]:
                    operacoes[h][0] = series[h][0][i]
                    buy_sell[h][0] = False
                    if check_eur_jpy[h][1]:
                        operacoes[h][4] = series[h][0][i] + round(multiply_tp * series[h][5][i],3) # TP
                        #operacoes[h][4] = series[h][0][i] + tk_jpy
                        operacoes[h][5] = series[h][0][i] - round(multiply_sl * series[h][5][i],3) # SL
                        #operacoes[h][5] = series[h][0][i] - sl_jpy
                    else:
                        operacoes[h][4] = series[h][0][i] + round(multiply_tp * series[h][5][i],5) # TP
                        #operacoes[h][4] = series[h][0][i] + tk_normal
                        operacoes[h][5] = series[h][0][i] - round(multiply_sl * series[h][5][i],5) # SL
                        #operacoes[h][5] = series[h][0][i] - sl_normal

                check_buy_sl = (m1[h][0][i][super] <= operacoes[h][5]) or (m1[h][1][i][super] <= operacoes[h][5]) or (m1[h][2][i][super] <= operacoes[h][5]) or (m1[h][3][i][super] <= operacoes[h][5])
                check_buy_tp = (m1[h][0][i][super] >= operacoes[h][4]) or (m1[h][1][i][super] >= operacoes[h][4]) or (m1[h][2][i][super] >= operacoes[h][4]) or (m1[h][3][i][super] >= operacoes[h][4])

                if series[h][2][i] and buy_sell[h][1]:
                    operacoes[h][1] = series[h][0][i]
                    buy_sell[h][1] = False
                    if check_eur_jpy[h][1]:
                        operacoes[h][2] = series[h][0][i] - round(multiply_tp * series[h][5][i],3) # TP
                        #operacoes[h][2] = series[h][0][i] - tk_jpy
                        operacoes[h][3] = series[h][0][i] + round(multiply_sl * series[h][5][i],3) # SL
                        #operacoes[h][3] = series[h][0][i] + sl_jpy
                    else:
                        operacoes[h][2] = series[h][0][i] - round(multiply_tp * series[h][5][i],5) # TP
                        #operacoes[h][2] = series[h][0][i] - tk_normal
                        operacoes[h][3] = series[h][0][i] + round(multiply_sl * series[h][5][i],5) # SL
                        #operacoes[h][3] = series[h][0][i] + sl_normal

                check_sell_sl = (m1[h][0][i][super] >= operacoes[h][3]) or (m1[h][1][i][super] >= operacoes[h][3]) or (m1[h][2][i][super] >= operacoes[h][3]) or (m1[h][3][i][super] >= operacoes[h][3])
                check_sell_buy = (m1[h][0][i][super] <= operacoes[h][2]) or (m1[h][1][i][super] <= operacoes[h][2]) or (m1[h][2][i][super] <= operacoes[h][2]) or (m1[h][3][i][super] <= operacoes[h][2])

                if buy_sell[h][0] == False and check_buy_sl:
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][5],
                                                                       saldo_final=operacoes[h][0], eur = check_eur_jpy[h][0],
                                                                       preco_eur=series[h][3][i])
                    list_backtest[buy_sell_list_indi[2]] = balance_backtest
                    buy_orders[buy_sell_list_indi[0]] = buy_orders[buy_sell_list_indi[0]-1] + buy_result
                    each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + buy_result
                    each_pair_index[h] += 1
                    buy_sell_list_indi[0] += 1
                    buy_sell_list_indi[2] += 1
                    buy_sell[h][0] = True
                    break
                elif buy_sell[h][0] == False and check_buy_tp:
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][4],
                                                                       saldo_final=operacoes[h][0], eur = check_eur_jpy[h][0],
                                                                       preco_eur=series[h][3][i])
                    list_backtest[buy_sell_list_indi[2]] = balance_backtest
                    buy_orders[buy_sell_list_indi[0]] = buy_orders[buy_sell_list_indi[0]-1] + buy_result
                    each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + buy_result
                    each_pair_index[h] += 1
                    buy_sell_list_indi[0] += 1
                    buy_sell_list_indi[2] += 1
                    buy_sell[h][0] = True
                    break

                if buy_sell[h][1] == False and check_sell_sl:
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[h][1],
                                                                        saldo_final=operacoes[h][3], eur = check_eur_jpy[h][0],
                                                                        preco_eur=series[h][3][i])
                    list_backtest[buy_sell_list_indi[2]] = balance_backtest
                    sell_orders[buy_sell_list_indi[1]] = sell_orders[buy_sell_list_indi[1]-1] + sell_result
                    each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + sell_result
                    each_pair_index[h] += 1
                    buy_sell_list_indi[1] += 1
                    buy_sell_list_indi[2] += 1
                    buy_sell[h][1] = True
                    break
                elif buy_sell[h][1] == False and check_sell_buy:
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][1],
                                                                        saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                        preco_eur=series[h][3][i])
                    list_backtest[buy_sell_list_indi[2]] = balance_backtest
                    sell_orders[buy_sell_list_indi[1]] = sell_orders[buy_sell_list_indi[1]-1] + sell_result
                    each_pair[h][each_pair_index[h]] = each_pair[h][each_pair_index[h]-1] + sell_result
                    each_pair_index[h] += 1
                    buy_sell_list_indi[1] += 1
                    buy_sell_list_indi[2] += 1
                    buy_sell[h][1] = True
                    break

    return list_backtest, sell_orders, buy_orders, each_pair
