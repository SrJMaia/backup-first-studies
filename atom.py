@njit
def otimizado_tpsl(series, tpsl, balance=1000):

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
    operacoes = np.zeros((28,2),dtype=np.float64)
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_ind, sell_ind, list_backtest_indi = 0, 0, 1

    buy_orders = np.zeros((500_000), dtype=np.float64)
    sell_orders = np.zeros((500_000), dtype=np.float64)

    balance_backtest = balance
    list_backtest = np.zeros((1_000_000), dtype=np.float64)
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
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][5],
                                                                   saldo_final=operacoes[h][0], eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                buy_orders[buy_ind] = buy_result
                buy_sell[h][0] = True
                list_backtest_indi += 1
                buy_ind += 1
            elif buy_sell[h][0] == False and series[h][0][i] >= operacoes[h][4]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][4],
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

            if buy_sell[h][1] == False and series[h][0][i] >= operacoes[h][3]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][3], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                sell_orders[sell_ind] = sell_result
                buy_sell[h][1] = True
                list_backtest_indi += 1
                sell_ind += 1
            elif buy_sell[h][1] == False and series[h][0][i] <= operacoes[h][2]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest[list_backtest_indi] = balance_backtest
                sell_orders[sell_ind] = sell_result
                buy_sell[h][1] = True
                list_backtest_indi += 1
                sell_ind += 1

    return list_backtest, sell_orders, buy_orders
