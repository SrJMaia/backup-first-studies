"""
Crio uma coluna nova com o timeframe que sera testado e os respectivos preços
coluna OHLC sera para testar o TPSL
um unico loop onde, quando nao for nan e flag abrir operacao == True, abre operacao
else, apenas passa pelos preços OHLC
"""

@njit(parallel=True)
def single_backtest(array, multiply_tp, multiply_sl, eur = True, balance = 1000):
    """
    Caso for operar moedas nao eur, mudar o sistema do array
    array = [0] Open
            [1] High
            [2] Low
            [3] Close
            [4] Preços do TimeFrame
            [5] TPSL
            [6] Sell Flag
            [7] Buy Flag
    tpsl = TakeProfit e StopLoss int > 0
    multiply_tpsl = float > 0
                    Será o valor que irá dividir SL
                    Se 1 significa risco 1:1, se 2, 2:1 and so on
    ---
    buy_sell: 0 = Compra
              1 = Venda
    operacao_info: 0 = Preço de Compra
                   1 = Preço de Venda
                   2 = TP Venda
                   3 = SL Venda
                   4 = TP Compra
                   5 = SL Compra
    """

    balance_backtest = balance

    operacao_info = np.zeros((6),dtype=np.float32)
    buy_sell = np.ones((2),dtype=np.bool_)

    buy_sell_tot_trades_indi = np.zeros(3, dtype=np.int32)

    buy_orders = np.zeros((array[0].size), dtype=np.float32)
    sell_orders = np.zeros((array[0].size), dtype=np.float32)
    buy_orders[0] = balance_backtest
    sell_orders[0] = balance_backtest
    buy_sell_tot_trades_indi[0] += 1
    buy_sell_tot_trades_indi[1] += 1

    tot_trades = np.zeros((array[0].size), dtype=np.float32)
    tot_trades[0] = balance_backtest
    buy_sell_tot_trades_indi[2] += 1

    #tk_normal = round(tpsl / 10000,5)
    #sl_normal = round(tpsl / 10000 / multiply_tpsl, 5)
    #tk_jpy = round(tpsl / 100)
    #sl_jpy = round(tpsl / 100 / multiply_tpsl,5)

    for i in np.arange(array[0].size): # Array tamanho

        if array[7][i] and buy_sell[0] and array[4][i] != np.nan: #Compra
            operacao_info[0] = array[4][i]
            buy_sell[0] = False
            if eur:
                operacao_info[4] = array[4][i] + round(multiply_tp * array[5][i],3) # TP
                #operacao_info[4] = array[0][i] + tk_jpy
                operacao_info[5] = array[4][i] - round(multiply_sl * array[5][i],3) # SL
                #operacao_info[5] = array[0][i] - sl_jpy
            else:
                operacao_info[4] = array[4][i] + round(multiply_tp * array[5][i],5) # TP
                #operacao_info[4] = array[0][i] + tk_normal
                operacao_info[5] = array[4][i] - round(multiply_sl * array[5][i],5) # SL
                #operacao_info[5] = array[0][i] - sl_normal
        elif array[6][i] and buy_sell[1] and array[4][i] != np.nan:
            operacao_info[1] = array[4][i]
            buy_sell[1] = False
            if eur:
                operacao_info[2] = array[4][i] - round(multiply_tp * array[5][i],3) # TP
                #operacao_info[2] = array[0][i] - tk_jpy
                operacao_info[3] = array[4][i] + round(multiply_sl * array[5][i],3) # SL
                #operacao_info[3] = array[0][i] + sl_jpy
            else:
                operacao_info[2] = array[4][i] - round(multiply_tp * array[5][i],5) # TP
                #operacao_info[2] = array[0][i] - tk_normal
                operacao_info[3] = array[4][i] + round(multiply_sl * array[5][i],5) # SL
                #operacao_info[3] = array[0][i] + sl_normal

        check_sell_sl = (array[0][i] >= operacao_info[3]) or (array[1][i] >= operacao_info[3]) or (array[2][i] >= operacao_info[3]) or (array[3][i] >= operacao_info[3])
        check_sell_buy = (array[0][i] <= operacao_info[2]) or (array[1][i] <= operacao_info[2]) or (array[2][i] <= operacao_info[2]) or (array[3][i] <= operacao_info[2])
        check_buy_sl = (array[0][i] <= operacao_info[5]) or (array[1][i] <= operacao_info[5]) or (array[2][i] <= operacao_info[5]) or (array[3][i] <= operacao_info[5])
        check_buy_tp = (array[0][i] >= operacao_info[4]) or (array[1][i] >= operacao_info[4]) or (array[2][i] >= operacao_info[4]) or (array[3][i] >= operacao_info[4])

        if array[4][i] != np.nan:
            if buy_sell[0] == False and check_buy_sl:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacao_info[5],
                                                                   saldo_final=operacao_info[0], eur = eur,
                                                                   preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                buy_orders[buy_sell_tot_trades_indi[0]] = buy_orders[buy_sell_tot_trades_indi[0]-1] + buy_result
                buy_sell_tot_trades_indi[0] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[0] = True
                break
            elif buy_sell[0] == False and check_buy_tp:
                balance_backtest, buy_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacao_info[4],
                                                                   saldo_final=operacao_info[0], eur = eur,
                                                                   preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                buy_orders[buy_sell_tot_trades_indi[0]] = buy_orders[buy_sell_tot_trades_indi[0]-1] + buy_result
                buy_sell_tot_trades_indi[0] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[0] = True
                break

            if buy_sell[1] == False and check_sell_sl:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest,saldo_inicial=operacao_info[1],
                                                                    saldo_final=operacao_info[3], eur = eur,
                                                                    preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                sell_orders[buy_sell_tot_trades_indi[1]] = sell_orders[buy_sell_tot_trades_indi[1]-1] + sell_result
                buy_sell_tot_trades_indi[1] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[1] = True
                break
            elif buy_sell[1] == False and check_sell_buy:
                balance_backtest, sell_result = finance_calculation(balance=balance_backtest, saldo_inicial=operacao_info[1],
                                                                    saldo_final=operacao_info[2], eur = eur,
                                                                    preco_eur=1)
                tot_trades[buy_sell_tot_trades_indi[2]] = balance_backtest
                sell_orders[buy_sell_tot_trades_indi[1]] = sell_orders[buy_sell_tot_trades_indi[1]-1] + sell_result
                buy_sell_tot_trades_indi[1] += 1
                buy_sell_tot_trades_indi[2] += 1
                buy_sell[1] = True
                break

    return tot_trades, sell_orders, buy_orders
