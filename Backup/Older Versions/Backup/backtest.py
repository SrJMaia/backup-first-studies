import pandas as pd
from IPython.display import clear_output
import analysis_functions as af
import matplotlib.pyplot as plt
import numpy as np
from numba import njit
from sklearn.linear_model import LinearRegression
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
    return (np.where(x == x.max())[0][0])/100, x


@njit
def finance_calculation(balance, saldo_inicial, saldo_final, preco_eur, eur):

    initial_balance = 1000

    lot = initial_balance

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


def walk_forward_test(walk1, test1, walk2, test2, walk3, test3, walk4, test4, walk5, test5, final, data_numpy, tot_iterations, plot=False, balance=1000):

    walk = np.array([walk1, walk2, walk3, walk4, walk5])
    test = np.array([test1, test2, test3, test4, test5])

    no_tpsl, _, _ = otimizado_no_tpsl(data_numpy, balance=1000)
    if plot:
        try:
            pd.Series(no_tpsl).plot()
            plt.title(f'No TPSL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    # -------------------------------------------------------------------------

    walk_columns = []

    for j in range(5):

        walk_pd = pd.DataFrame()
        test_pd = pd.DataFrame()

        for i in range(1, tot_iterations):
            walk_result, _, _ = otimizado_tpsl(walk[j], tpsl=i)
            if walk_result[-1] > balance:
                walk_pd[i] = pd.Series(walk_result)

        if plot:
            try:
                walk_pd.plot()
                plt.title(f'Teste Walk Open {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        for i in walk_pd.columns:
            test_result, _, _ = otimizado_tpsl(test[j], tpsl=i)
            if test_result[-1] > balance:
                test_pd[i] = pd.Series(test_result)

        if plot:
            try:
                test_pd.plot()
                plt.title(f'Teste Open {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        walk_columns.append(list(test_pd.columns))

    x = af.compare(walk_columns)

    test_final = pd.DataFrame()
    for i in x:
        final_result, _, _ = otimizado_tpsl(final, tpsl=i)
        test_final[i] = pd.Series(final_result)

    if plot:
        try:
            test_final.plot()
            plt.title(f'Teste Final Open', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    all_tpsl = pd.DataFrame()
    for i in range(1, tot_iterations):
        a, _, _ = otimizado_tpsl(data_numpy, tpsl=i)
        all_tpsl[i] = pd.Series(a)

    if plot:
        try:
            all_tpsl.plot()
            plt.title(f'All Open', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    bests_results_lr = []
    cut = 0.0
    for i in all_tpsl.columns:
        lr_test = pd.DataFrame()
        lr_test['x'] = pd.Series(range(len(all_tpsl[i].dropna())))
        lr_test['y'] = all_tpsl[i].dropna()
        x_v = lr_test[['x']]
        y_v = lr_test[['y']]
        model = LinearRegression()
        model.fit(x_v, y_v)
        result = model.score(x_v, y_v)
        if result > cut:
            bests_results_lr.append(i)
            cut = result

    if plot:
        try:
            all_tpsl[bests_results_lr].plot()
            plt.title(f'Linear Regression Open', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    # -------------------------------------------------------------------------

    walk_columns = []

    for j in range(5):

        walk_pd = pd.DataFrame()
        test_pd = pd.DataFrame()

        for i in range(1, tot_iterations):
            walk_result, _, _ = otimizado_tpsl_ohl(walk[j], tpsl=i)
            if walk_result[-1] > balance:
                walk_pd[i] = pd.Series(walk_result)

        if plot:
            try:
                walk_pd.plot()
                plt.title(f'Teste Walk OHL {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        for i in walk_pd.columns:
            test_result, _, _ = otimizado_tpsl_ohl(test[j], tpsl=i)
            if test_result[-1] > balance:
                test_pd[i] = pd.Series(test_result)

        if plot:
            try:
                test_pd.plot()
                plt.title(f'Teste OHL {j+1}', fontsize=30)
                plt.grid()
                plt.show()
            except TypeError:
                print('No data to plot.')

        walk_columns.append(list(test_pd.columns))

    x = af.compare(walk_columns)

    test_final = pd.DataFrame()
    for i in x:
        final_result, _, _ = otimizado_tpsl_ohl(final, tpsl=i)
        test_final[i] = pd.Series(final_result)

    if plot:
        try:
            test_final.plot()
            plt.title(f'Teste Final OHL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    all_tpsl = pd.DataFrame()
    for i in range(1, tot_iterations):
        a, _, _ = otimizado_tpsl_ohl(data_numpy, tpsl=i)
        all_tpsl[i] = pd.Series(a)

    if plot:
        try:
            all_tpsl.plot()
            plt.title(f'All OHL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')

    bests_results_lr = []
    cut = 0.0
    for i in all_tpsl.columns:
        lr_test = pd.DataFrame()
        lr_test['x'] = pd.Series(range(len(all_tpsl[i].dropna())))
        lr_test['y'] = all_tpsl[i].dropna()
        x_v = lr_test[['x']]
        y_v = lr_test[['y']]
        model = LinearRegression()
        model.fit(x_v, y_v)
        result = model.score(x_v, y_v)
        if result > cut:
            bests_results_lr.append(i)
            cut = result

    if plot:
        try:
            all_tpsl[bests_results_lr].plot()
            plt.title(f'Linear Regression OHL', fontsize=30)
            plt.grid()
            plt.show()
        except TypeError:
            print('No data to plot.')


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
    operacoes = np.zeros((28,6),dtype=np.float64)
    buy_sell = np.ones((28,2),dtype=np.bool_)
    #history = TRADE_HISTORY

    buy_orders = []
    sell_orders = []

    balance_backtest = balance
    list_backtest = [balance_backtest]

    # Talvez arrumar? Esta muito feio

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
                list_backtest.append(balance_backtest)
                buy_orders.append(buy_result)
                buy_sell[h][0] = True
            elif buy_sell[h][0] == False and series[h][0][i] >= operacoes[h][4]:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][4],
                                                                   saldo_final=operacoes[h][0], eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                buy_orders.append(buy_result)
                buy_sell[h][0] = True

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
                list_backtest.append(balance_backtest)
                sell_orders.append(sell_result)
                buy_sell[h][1] = True

            elif buy_sell[h][1] == False and series[h][0][i] <= operacoes[h][2]:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][2], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                sell_orders.append(sell_result)
                buy_sell[h][1] = True

    return list_backtest, sell_orders, buy_orders


@njit
def otimizado_no_tpsl(series, balance=1000):

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

    buy_orders = np.zeros((400_000), dtype=np.float64)
    sell_orders = np.zeros((400_000), dtype=np.float64)

    balance_backtest = balance
    list_backtest = np.zeros((800_000), dtype=np.float64)
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
                    balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][1],
                                                                        saldo_final=series[h][0][i], eur=check_eur_jpy[h][0],
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
                    balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=series[h][0][i],
                                                                       saldo_final=operacoes[h][0], eur=check_eur_jpy[h][0],
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
    # Alterado para checar primeiro sl e depois tp

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
    operacoes = np.zeros((28,6),dtype=np.float64)
    buy_sell = np.ones((28,2),dtype=np.bool_)

    buy_orders = []
    sell_orders = []

    balance_backtest = balance
    list_backtest = [balance_backtest]

    # Talvez arrumar? Esta muito feio

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
                list_backtest.append(balance_backtest)
                buy_orders.append(buy_result)
                buy_sell[h][0] = True
            elif buy_sell[h][0] == False and (series[h][0][i] <= operacoes[h][5] or series[h][5][i] <= operacoes[h][5]):
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[h][5],
                                                                   saldo_final=operacoes[h][0], eur = check_eur_jpy[h][0],
                                                                   preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                buy_orders.append(buy_result)
                buy_sell[h][0] = True

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
                list_backtest.append(balance_backtest)
                sell_orders.append(sell_result)
                buy_sell[h][1] = True
            elif buy_sell[h][1] == False and (series[h][0][i] >= operacoes[h][3] or series[h][4][i] >= operacoes[h][3]):
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[h][1],
                                                                    saldo_final=operacoes[h][3], eur = check_eur_jpy[h][0],
                                                                    preco_eur=series[h][3][i])
                list_backtest.append(balance_backtest)
                sell_orders.append(sell_result)
                buy_sell[h][1] = True

    return list_backtest, sell_orders, buy_orders


@njit
def single_backtest(series, tpsl, balance=1000):
    """
    Apenas EUR por enquanto
    """
    operacoes = np.array([1.,1.,0.,0.,0.,0.,0.,0.])

    buy_orders = []
    sell_orders = []

    balance_backtest = balance
    list_backtest = [balance_backtest]

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
            list_backtest.append(balance_backtest)
            buy_orders.append(buy_result)
            operacoes[0] = True
        elif operacoes[0] == False and series[0][i] <= operacoes[7]:
            balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[7],
                                                                saldo_final=operacoes[2], preco_eur=0, eur=True)
            list_backtest.append(balance_backtest)
            buy_orders.append(buy_result)
            operacoes[0] = True

        if series[2][i] and operacoes[1]:
            operacoes[3] = series[0][i]
            operacoes[1] = False
            operacoes[4] = series[0][i] - tk_normal
            operacoes[5] = series[0][i] + sl_normal

        if operacoes[1] == False and series[0][i] <= operacoes[4]:
            balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacoes[3],
                                                                saldo_final=operacoes[4], preco_eur=0, eur=True)
            list_backtest.append(balance_backtest)
            sell_orders.append(sell_result)
            operacoes[1] = True
        elif operacoes[1] == False and series[0][i] >= operacoes[5]:
            balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacoes[3],
                                                                saldo_final=operacoes[5], preco_eur=0, eur=True)
            list_backtest.append(balance_backtest)
            sell_orders.append(sell_result)
            operacoes[1] = True

    return list_backtest, buy_orders, sell_orders
